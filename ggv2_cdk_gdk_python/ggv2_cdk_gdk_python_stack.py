# Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
# Licensed under the Amazon Software License  http://aws.amazon.com/asl/

import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk.aws_codecommit import Repository
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep, CodeBuildOptions
from constructs import Construct
from aws_cdk import aws_iam as iam
import os

from ggv2_cdk_gdk_python.ggv2_cdk_gdk_python_app_stage import (
    Ggv2CdkGdkPythonAppStage,
)

class Ggv2CdkGdkPythonStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        params = {
            "accountNumber": self.node.try_get_context("account"),
            "region": self.node.try_get_context("region"),
            "repository_arn": self.node.try_get_context("codecommit_repository_arn"),
            "project_prefix": self.node.try_get_context("project_prefix"),
            "branch": self.node.try_get_context("default_branch_name")
        }

        repository = Repository.from_repository_arn(
            self,
            "CodeCommitRepository",
            repository_arn=params.get("repository_arn"),
        )

        pipeline = CodePipeline(
            self,
            "Pipeline",
            pipeline_name="GGv2CDKPipeline",
            docker_enabled_for_synth=True,
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.code_commit(
                    branch=params.get("branch"), repository=repository
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "python3 -m pip install -r requirements.txt",
                    "cdk synth --verbose"
                ],
            ),
            code_build_defaults=CodeBuildOptions(
                role_policy=[
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        resources=["*"],
                        actions=[
                            "ec2:*",
                            "greengrass:*",
                            "iot:*",
                            "logs:*",
                            "codebuild:*",
                            "s3:*"
                        ],
                    )
                ]
            ),
        )
  
        pipeline.add_stage(
            Ggv2CdkGdkPythonAppStage(
                self,
                "GGv2AppStage",
                env=cdk.Environment(
                    account=self.node.try_get_context("account"),
                    region=self.node.try_get_context("region"),
                ),
            )
        )



