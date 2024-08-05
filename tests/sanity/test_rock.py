#
# Copyright 2024 Canonical, Ltd.
#

import pytest
import warnings
from k8s_test_harness.util import docker_util, env_util


@pytest.mark.parametrize("image_version", ("2.1.6", "1.9.5"))
def test_sanity(image_version):
    try:

        rock = env_util.get_build_meta_info_for_rock_version(
        "fluent-bit", image_version, "amd64"
        )
    except ValueError:
        warnings.warn(UserWarning(f"image version {image_version} not found"))

    else:
        image = rock.image

        entrypoint = "fluent-bit"
        process = docker_util.run_in_docker(image, [entrypoint, "--version"])
        assert f"Fluent Bit v{image_version}" in process.stdout
