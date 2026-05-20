import traceback


def test_docs(example_names, examples):
    code = examples[example_names]
    namespace = {"fuso": __import__("fuso")}
    try:
        compiled = compile(code, f"<doc example: {example_names}>", "exec")
        exec(compiled, namespace, namespace)
    except AssertionError as e:
        print(
            "\n".join(
                [
                    f"[DocTest FAIL] Example: {example_names}",
                    "--- Code ---",
                    code,
                    "--- AssertionError ---",
                    str(e),
                    "--- Traceback ---",
                    traceback.format_exc(),
                ]
            )
        )
        raise
    except Exception as e:
        print(
            "\n".join(
                [
                    f"[DocTest ERROR] Example: {example_names}",
                    "--- Code ---",
                    code,
                    "--- Exception ---",
                    str(e),
                    "--- Traceback ---",
                    traceback.format_exc(),
                ]
            )
        )
        raise
