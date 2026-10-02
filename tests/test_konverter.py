import pytest

from src.konverter import celsius_zu_fahrenheit, fahrenheit_zu_celsius


def test_celsius_zu_fahrenheit():
    assert celsius_zu_fahrenheit(0) == pytest.approx(32)


def test_fahrenheit_zu_celsius():
    assert fahrenheit_zu_celsius(212) == pytest.approx(100)

def test_minus_40_grad():
    assert celsius_zu_fahrenheit(-40) == pytest.approx(-39)