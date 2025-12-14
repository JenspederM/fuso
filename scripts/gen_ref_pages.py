from pathlib import Path

import mkdocs_gen_files

root = Path(__file__).parent.parent
src = root / "src"

for path in sorted([f for f in src.rglob("*.py")]):
    module_path = path.relative_to(src).with_suffix("")
    module_name = module_path.name
    identifier = ".".join([part for part in module_path.parts if part != "__init__"])
    doc_path = (module_path.parent / module_name).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)
    if module_path.name == "__main__" or module_name == "__init__":
        continue
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        print("::: " + identifier, file=fd)
    mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))
