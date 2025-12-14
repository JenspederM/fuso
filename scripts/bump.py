import subprocess
import sys
import tomllib


def bump_version(args):
    subprocess.run(["uv", "version", "--bump", *args], check=True)


def get_version():
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
    return pyproject["project"]["version"]


def create_tag(version):
    tag_command = ["git", "tag", f"v{version}"]
    subprocess.run(tag_command, check=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    current_version = get_version()
    bump_version(args)
    new_version = get_version()
    if "--dry-run" not in args:
        create_tag(new_version)
        print(f"Tag v{new_version} created successfully.")  # noqa: T201
