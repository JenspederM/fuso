from fuso import main


def test_main():
    result = main()
    assert result == "Welcome to Fuso!"
