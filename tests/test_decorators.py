from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture

from src.decorators import log


def test_log_console_success(capsys: CaptureFixture[str]) -> None:
    @log()
    def greet(name: str) -> str:
        return f"Hello, {name}"

    greet("Alice")

    captured = capsys.readouterr().out
    assert "greet started" in captured
    assert "greet ok" in captured


def test_log_console_error(capsys: CaptureFixture[str]) -> None:
    @log()
    def fail() -> float:
        return 1 / 0

    with pytest.raises(ZeroDivisionError):
        fail()

    captured = capsys.readouterr().out
    assert "fail started" in captured
    assert "fail error: ZeroDivisionError. Inputs: (), {}" in captured


def test_log_file_success(tmp_path: Path) -> None:
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def multiply(a: int, b: int) -> int:
        return a * b

    multiply(3, 5)

    content = log_file.read_text(encoding="utf-8")
    assert "multiply started" in content
    assert "multiply ok" in content


def test_log_file_error(tmp_path: Path) -> None:
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def bad_func(x: int) -> int:
        raise ValueError(f"Error with value {x}")

    with pytest.raises(ValueError):
        bad_func(10)

    content = log_file.read_text(encoding="utf-8")
    assert "bad_func started" in content
    assert "bad_func error: ValueError. Inputs: (10,), {}" in content
