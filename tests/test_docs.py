import traceback


def test_docs(example_names, examples):
    code = examples[example_names]
    namespace = {"fuso": __import__("fuso")}
    try:
        compiled = compile(code, f"<doc example: {example_names}>", "exec")
        exec(compiled, namespace, namespace)
    except AssertionError as e:
        print(
            f"\n[DocTest FAIL] Example: {example_names}\n--- Code ---\n{code}\n--- AssertionError ---\n{e}\n--- Traceback ---\n{traceback.format_exc()}"
        )
        raise
    except Exception as e:
        print(
            f"\n[DocTest ERROR] Example: {example_names}\n--- Code ---\n{code}\n--- Exception ---\n{e}\n--- Traceback ---\n{traceback.format_exc()}"
        )
        raise
