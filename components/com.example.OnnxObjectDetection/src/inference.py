import onnxruntime
import cv2
import numpy as np

class ONNXInference:
    ort_session = None
    input_names = None
    output_names = None
    input_shape = None
    conf_thresold = None
    model = None

    def __init__(self, model_path, confidence_threshold):
        self.model = model_path
        EP_list = ['CPUExecutionProvider']
        self.ort_session = onnxruntime.InferenceSession(self.model, providers=EP_list)
        model_inputs = self.ort_session.get_inputs()
        self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]
        self.input_shape = model_inputs[0].shape
        model_output = self.ort_session.get_outputs()
        self.output_names = [model_output[i].name for i in range(len(model_output))]
        self.conf_thresold = confidence_threshold

    def xywh2xyxy(self, x):
        # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
        y = np.copy(x)
        y[..., 0] = x[..., 0] - x[..., 2] / 2
        y[..., 1] = x[..., 1] - x[..., 3] / 2
        y[..., 2] = x[..., 0] + x[..., 2] / 2
        y[..., 3] = x[..., 1] + x[..., 3] / 2
        return y

    def compute_iou(self, box, boxes):
        box = self.xywh2xyxy(box)
        boxes = self.xywh2xyxy(boxes)
        # Compute xmin, ymin, xmax, ymax for both boxes
        xmin = np.maximum(box[0], boxes[:, 0])
        ymin = np.maximum(box[1], boxes[:, 1])
        xmax = np.minimum(box[2], boxes[:, 2])
        ymax = np.minimum(box[3], boxes[:, 3])

        # Compute intersection area
        intersection_area = np.maximum(0, xmax - xmin) * np.maximum(0, ymax - ymin)

        # Compute union area
        box_area = (box[2] - box[0]) * (box[3] - box[1])
        boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
        union_area = box_area + boxes_area - intersection_area

        # Compute IoU
        iou = intersection_area / union_area

        return iou

    def nms(self, boxes, scores, iou_threshold):
        # Sort by score
        sorted_indices = np.argsort(scores)[::-1]

        keep_boxes = []
        while sorted_indices.size > 0:
            # Pick the last box
            box_id = sorted_indices[0]
            keep_boxes.append(box_id)

            # Compute IoU of the picked box with the rest
            ious = self.compute_iou(boxes[box_id, :], boxes[sorted_indices[1:], :])

            # Remove boxes with IoU over the threshold
            keep_indices = np.where(ious < iou_threshold)[0]

            # print(keep_indices.shape, sorted_indices.shape)
            sorted_indices = sorted_indices[keep_indices + 1]

        return keep_boxes

    def preprocess(self, image_path):
        image = cv2.imread(image_path)
        image_height, image_width = image.shape[:2]

        input_height, input_width = self.input_shape[2:]
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(image_rgb, (input_width, input_height))

        # Scale input pixel value to 0 to 1
        input_image = resized / 255.0
        input_image = input_image.transpose(2,0,1)
        input_tensor = input_image[np.newaxis, :, :, :].astype(np.float32)
        return input_tensor, input_height, input_width, image_height, image_width

    def process(self, image_path):
        input_tensor, input_height, input_width, image_height, image_width = self.preprocess(image_path)
        outputs = self.ort_session.run(self.output_names, {self.input_names[0]: input_tensor})[0]
        boxes, scores, class_ids = self.postprocess(outputs, input_height, input_width, image_height, image_width)

        boxes  = np.array(boxes).tolist()
        scores = np.array(scores).tolist()
        class_ids = np.array(class_ids).tolist()

        return {"boxes": boxes, "scores": scores, "class_ids": class_ids}
    
    def postprocess(self, outputs, input_height, input_width, image_height, image_width):
        predictions = np.squeeze(outputs).T

        # Filter out object confidence scores below threshold
        scores = np.max(predictions[:, 4:], axis=1)
        predictions = predictions[scores > self.conf_thresold, :]
        scores = scores[scores > self.conf_thresold]

        class_ids = np.argmax(predictions[:, 4:], axis=1)
        
        # Get bounding boxes for each object
        boxes = predictions[:, :4]

        #rescale box
        input_shape = np.array([input_width, input_height, input_width, input_height])
        boxes = np.divide(boxes, input_shape, dtype=np.float32)
        boxes *= np.array([image_width, image_height, image_width, image_height])
        boxes = boxes.astype(np.int32)

        indices = self.nms(boxes, scores, 0.3)
        return boxes[indices], scores[indices], class_ids[indices]