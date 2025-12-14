import subprocess
import sys
import tomllib


def bump_version(args):
    subprocess.run(["uv", "version", "--bump", *args], check=True)


def get_version():
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
    return pyproject["project"]["version"]


def create_tag(old_version, new_version):
    commit_command = [
        "git",
        "commit",
        "-am",
        f"bump: {old_version} → {new_version}",
    ]
    subprocess.run(commit_command, check=True)
    tag_command = [
        "git",
        "tag",
        "-a",
        f"v{new_version}",
        "-m",
        f"Version {new_version}",
    ]
    subprocess.run(tag_command, check=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    old_version = get_version()
    bump_version(args)
    new_version = get_version()
    if "--dry-run" not in args:
        create_tag(old_version, new_version)
        print(f"Tag v{new_version} created successfully.")  # noqa: T201
