def test_docs(example_names, examples):
    exec(examples[example_names], {"fuso": __import__("fuso")}, {})
