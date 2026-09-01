from pathlib import Path

import pytest


def _generate_examples():
    p = Path(__file__).parent.parent / "docs" / "user-guide.md"
    lines = p.read_text().splitlines()
    examples = {}
    example_name = None
    imports = set()
    for line in lines:
        if line.startswith("```python"):
            example_name = line[len("```python ") :].strip()
            examples[example_name] = []
        elif line.startswith("```") and examples:
            if imports != {"fuso"}:
                raise ValueError(
                    f"Example '{example_name}' imports unexpected modules: {imports}"
                )

            if not isinstance(example_name, str):
                raise ValueError(f"Example name is not a string: {example_name}")
            examples[example_name] = "\n".join(examples[example_name])
            example_name = None
        elif example_name:
            if line.startswith("import "):
                imports.add(line.split(".")[0].strip())
            elif line.startswith("from "):
                imports.add(line.split()[1].split(".")[0].strip())
            examples[example_name].append(line)
    return examples


EXAMPLES = _generate_examples()


@pytest.mark.parametrize("name", list(EXAMPLES.keys()))
def test_docs(name, tmp_path):
    # Arrange
    code = EXAMPLES[name]
    test_path = tmp_path / f"{name}.py"
    test_path.parent.mkdir(parents=True, exist_ok=True)
    test_func = [f"def test_{name}():"] + [f"    {line}" for line in code.splitlines()]
    test_path.write_text("\n".join(test_func))

    # Act
    exit_code = pytest.main(
        [
            test_path.absolute().as_posix(),
            "-vv",
        ]
    )

    # Assert
    assert exit_code == 0, f"Documentation tests failed with exit code {exit_code}"
