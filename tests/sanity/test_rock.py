import os
import subprocess


def test_sanity():
    image_variable = "ROCK_FLUENT_BIT"
    entrypoint = "/fluent-bit/bin/fluent-bit"
    image = os.getenv(image_variable)
    assert image is not None, f"${image_variable} is not set"

    docker_run = subprocess.run(
        ["docker", "run", "--rm", "--entrypoint", entrypoint, image, "--version"],
        capture_output=True,
        check=True,
        text=True,
    )
    assert "Fluent Bit v2.1.6" in docker_run.stdout
