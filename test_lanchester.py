from lanchester import main
import pytest

def get_default_args():
    default_args = {
            "a": "1",
            "b": "1",
            "A": "1",
            "B": "1"
        }
    return default_args

def test_empty():
    args = {
    }

    with pytest.raises(SystemExit):
        main(args)

def test_underspecified():
    args = {
        "a": 1,
        "b": 1,
        "A": 1
    }

    with pytest.raises(SystemExit):
        main(args)

def test_abAB_zero_minus():
    for value in ["-1", "0"]:
        for key in ["a", "b", "A", "B"]:
            args = get_default_args()
            args[key] = value

            args_str = ["--a", args["a"], "--b", args["b"], "--A", args["A"], "--B", args["B"]]
            with pytest.raises(SystemExit):
                main(args_str)

def test_type_bluesky():
    args = get_default_args()
    args_str = ["--a", args["a"], "--b", args["b"], "--A", args["A"], "--B", args["B"], "--type", "linear"]
    main(args_str)

def test_type_error():
    args = {
            "a": "1",
            "b": "1",
            "A": "1",
            "B": "1"
        }

    args_str = ["--a", args["a"], "--b", args["b"], "--A", args["A"], "--B", args["B"], "--type", "dgwggew"]
    with pytest.raises(SystemExit):
        main(args_str)

def test_n():
    args = get_default_args()
    args_str = ["--a", args["a"], "--b", args["b"], "--A", args["A"], "--B", args["B"], "--n", "0"]
    with pytest.raises(SystemExit):
        main(args_str)

    args_str = ["--a", args["a"], "--b", args["b"], "--A", args["A"], "--B", args["B"], "--n", "-1"]
    with pytest.raises(SystemExit):
        main(args_str)

def test_end_t():
    args = get_default_args()
    args_str = ["--a", args["a"], "--b", args["b"], "--A", args["A"], "--B", args["B"], "--end_t", "0"]
    with pytest.raises(SystemExit):
        main(args_str)

    args_str = ["--a", args["a"], "--b", args["b"], "--A", args["A"], "--B", args["B"], "--end_t", "-1"]
    with pytest.raises(SystemExit):
        main(args_str)

def test_1(capsys):
    args_str = ["--a", "1", "--b", "1", "--A", "5", "--B", "3", "--end_t", "100", "--dt", "0.001"]
    main(args_str)

    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    last_line = lines[-2]
    (t, A, B) = [float(token) for token in last_line.split()]

    assert len(lines) == 1389
    assert t == pytest.approx(0.69300)
    assert A == pytest.approx(4.00, rel=1e-3)
    assert B == pytest.approx(0.0, abs=1e-3)

def test_draw(capsys):
    args_str = ["--a", "4", "--b", "1", "--A", "1", "--B", "2", "--end_t", "7", "--dt", "0.1"]
    main(args_str)

    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    last_line = lines[-2]
    (t, A, B) = [float(token) for token in last_line.split()]

    assert len(lines) == 143
    assert t == pytest.approx(7.0)
    assert A == pytest.approx(0.0)
    assert B == pytest.approx(0.0)

def test_linear(capsys):
    args_str = ["--a", "2", "--b", "1", "--A", "1", "--B", "1", "--end_t", "1", "--dt", "0.01", "--type", "linear"]
    main(args_str)

    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    last_line = lines[-2]
    (t, A, B) = [float(token) for token in last_line.split()]

    assert len(lines) == 101
    assert t == pytest.approx(0.49)
    assert A == pytest.approx(0.51)
    assert B == pytest.approx(0.02)

def test_1_markov(capsys):
    args_str = ["--a", "1", "--b", "1", "--A", "5", "--B", "3", "--end_t", "10", "--n", "10000", "--type", "markov_quadratic", "--seed", "1"]
    main(args_str)

    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    target_line = lines[1]
    print(target_line)
    win_percent = float(target_line[11:15]) / 100

    assert len(lines) == 6
    assert 0.875 <= win_percent <= 0.895

def test_markov_linear(capsys):
    args_str = ["--a", "2", "--b", "1", "--A", "1", "--B", "1", "--end_t", "1000", "--n", "100000", "--type", "markov_linear"]
    main(args_str)

    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    target_line = lines[1]
    print(target_line)
    win_percent = float(target_line[11:15]) / 100

    assert len(lines) == 6
    assert 0.66 <= win_percent <= 0.67