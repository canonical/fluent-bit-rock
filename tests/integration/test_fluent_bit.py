#
# Copyright 2024 Canonical, Ltd.
#
import logging
import os

from test_util import harness, util

LOG = logging.getLogger(__name__)


def test_integration_fluent_bit(session_instance: harness.Instance):
    image_name_env_variable = "ROCK_FLUENT_BIT"

    image_uri = os.getenv(image_name_env_variable)
    assert image_uri is not None, f"{image_name_env_variable} is not set"
    image_split = image_uri.split(":")

    helm_command = [
        "k8s",
        "helm",
        "install",
        "fluent-bit",
        "--repo",
        "https://fluent.github.io/helm-charts",
        "fluent-bit",
        "--namespace",
        "fluent-bit",
        "--create-namespace",
        "--version",
        "0.34.2",  # chart version with 2.1.6 app
        "--set",
        "installCRDs=true",
        "--set",
        f"image.repository={image_split[0]}",
        "--set",
        f"image.tag={image_split[1]}",
        "--set",
        "securityContext.runAsUser=584792",
    ]

    session_instance.exec(helm_command)

    util.stubbornly(retries=5, delay_s=5).on(session_instance).exec(
        [
            "k8s",
            "kubectl",
            "rollout",
            "status",
            "daemonset",
            "fluent-bit",
            "--namespace",
            "fluent-bit",
            "--timeout",
            "180s",
        ]
    )
