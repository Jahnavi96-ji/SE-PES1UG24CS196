
from hypothesis import given, strategies as st

from processor import (
    verify_isbn10_format,
    calculate_depreciation_factor,
    lookup_condition_multiplier
)


@given(st.text() | st.none())
def test_verify_isbn10_format_no_crash(s):
    try:
        verify_isbn10_format(s)
    except Exception as e:
        assert False, f"ISBN function crashed with {s!r}: {e}"


@given(st.text() | st.none())
def test_calculate_depreciation_factor_safe(s):
    try:
        calculate_depreciation_factor(s)
    except Exception as e:
        assert False, f"Depreciation function crashed with {s!r}: {e}"


@given(st.text() | st.none())
def test_lookup_condition_multiplier_safe(s):
    try:
        lookup_condition_multiplier(s)
    except Exception as e:
        assert False, f"Condition function crashed with {s!r}: {e}"

def test_valid_isbn():
    assert verify_isbn10_format("0-306-40615-2") == \
        "Group 306: Starts 0, Checksum 2"


def test_valid_depreciation():
    assert calculate_depreciation_factor("3/10") == 0.7


def test_valid_condition():
    assert lookup_condition_multiplier("MINT") == 1.25