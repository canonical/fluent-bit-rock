#
# Copyright 2024 Canonical, Ltd.
#
import logging

import pytest
from k8s_test_harness import harness
from k8s_test_harness.util import env_util, k8s_util
# from k8s_test_harness.util import constants, env_util, k8s_util


# pytest_plugins = ["k8s_test_harness.plugin"]

LOG = logging.getLogger(__name__)


# @pytest.mark.parametrize("image_version", ("2.1.6", "1.9.5"))
@pytest.mark.parametrize("image_version", ["2.1.6"])
def test_integration_fluent_bit(
    function_instance: harness.Instance, image_version: str
):
    fluent_bit_rock = env_util.get_build_meta_info_for_rock_version(
        "fluent-bit", image_version, "amd64"
    )

    images = [k8s_util.HelmImage(fluent_bit_rock.image)]

    helm_command = k8s_util.get_helm_install_command(
        "fluent-bit",
        "fluent-bit",
        namespace="fluent-bit",
        repository="https://fluent.github.io/helm-charts",
        chart_version="0.34.2",  # chart version with 2.1.6 app
        images=images,
    )

    function_instance.exec(helm_command)

    k8s_util.wait_for_daemonset(function_instance, "fluent-bit", "fluent-bit")
