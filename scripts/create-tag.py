import subprocess
import tomllib


def get_version():
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
    return pyproject["project"]["version"]


if __name__ == "__main__":
    version = get_version()
    print(f"Creating tag for version: {version}")  # noqa: T201
    git_tag_command = ["git", "tag", f"v{version}"]
    print("Running command:", " ".join(git_tag_command))  # noqa: T201
    subprocess.run(git_tag_command, check=True)
    print(f"Tag v{version} created successfully.")  # noqa: T201
