from pathlib import Path

import pytest


def _generate_doc_tests():
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

            examples[example_name] = "\n".join(examples[example_name])
            example_name = None
        elif example_name:
            if line.startswith("import "):
                imports.add(line.split(".")[0].strip())
            elif line.startswith("from "):
                imports.add(line.split()[1].split(".")[0].strip())
            examples[example_name].append(line)
    return examples


def pytest_generate_tests(metafunc: pytest.Metafunc):
    examples = _generate_doc_tests()
    if "example_names" in metafunc.fixturenames and "examples" in metafunc.fixturenames:
        metafunc.parametrize("example_names", list(examples.keys()))
        metafunc.parametrize("examples", [examples])
