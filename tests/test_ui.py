import builtins
import io
import sys
import time

import pytest

from Forrest_of_Doom import ui


def test_get_valid_input(monkeypatch):
    inputs = iter(["bad", "Yes"])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))
    choice = ui.get_valid_input('Enter yes/no: ', ['yes', 'no'])
    assert choice == 'yes'


def test_slow_print_fast_mode(monkeypatch, capsys):
    # Ensure fast mode prints without delay and does not block
    monkeypatch.setattr('builtins.input', lambda prompt='': '')
    ui.slow_print('Hello', fast=True, pause=False)
    captured = capsys.readouterr()
    assert 'Hello' in captured.out


def test_slow_print_no_delay(monkeypatch, capsys):
    # Patch time.sleep to ensure test is fast
    monkeypatch.setattr(time, 'sleep', lambda s: None)
    monkeypatch.setattr('builtins.input', lambda prompt='': '')
    ui.slow_print('World', delay=0.001, pause=False)
    captured = capsys.readouterr()
    assert 'World' in captured.out
