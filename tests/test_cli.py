from genomeforge.cli import main

 
def test_cli_correct_gc(capsys):
    exit_code = main(["AGCT"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "50.00%\n"
    assert captured.err == ""

def test_cli_invalid_sequence(capsys):
    exit_code = main(["AGXT"])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "invalid" in captured.err

def test_cli_error_if_empty(capsys):
    exit_code = main([""])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert captured.err == "Sequence can't be empty!\n"