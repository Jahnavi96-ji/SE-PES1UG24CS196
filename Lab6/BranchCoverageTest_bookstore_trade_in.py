import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration


def b(fmt="paperback", books=None, approved=True, credit=False):
    return {
        "intake_approved": approved,
        "format": fmt,
        "books": [] if books is None else books,
        "payout_in_credit": credit,
    }


def bk(condition="good", missing_pages=0, counterfeit=False):
    return {
        "condition": condition,
        "missing_pages": missing_pages,
        "counterfeit": counterfeit,
    }


@pytest.mark.parametrize(
    "batches,bonus,expected",
    [
        ([b("textbook", [bk("mint")])], 0,
         {"total_payout": 50.0, "status": "COMPLETED"}),
        ([b("hardcover", [bk("poor")])], 0,
         {"total_payout": 6.0, "status": "COMPLETED"}),
        ([b("paperback", [bk("ordinary")])], 0,
         {"total_payout": 8.0, "status": "COMPLETED"}),
        ([b("invalid", [bk()])], 0,
         {"total_payout": 0.0, "status": "ZERO_CREDIT"}),
        ([b("paperback", [bk()], approved=False)], 0,
         {"total_payout": 0.0, "status": "ZERO_CREDIT"}),
        ([b("paperback", [bk(missing_pages=1)])], 0,
         {"total_payout": 0.0, "status": "ZERO_CREDIT"}),
        ([b("paperback", [bk(counterfeit=True)])], 0,
         {"total_payout": 0.0, "status": "ZERO_CREDIT"}),
        ([b("textbook", [bk(), bk(counterfeit=True), bk()])], 0,
         {"total_payout": 0.0, "status": "ZERO_CREDIT"}),
        ([b("paperback", [bk()], credit=True)], 2,
         {"total_payout": 10.0, "status": "COMPLETED"}),
        ([b("paperback", [bk(missing_pages=1) for _ in range(5)])], 0,
         {"total_payout": 0.0, "status": "AUDIT_REJECTED"}),
        ([b("paperback", [])], 0,
         {"total_payout": 0.0, "status": "ZERO_CREDIT"}),
    ],
)
def test_buyback_decision_branches(batches, bonus, expected):
    assert process_book_buybacks(batches, bonus) == expected


@pytest.mark.parametrize(
    "matrix,expected",
    [
        ([], "NO_DATA"),
        ([[1, 2, 3]], "CALIBRATED"),
        ([[6, 2, 7]], "CALIBRATED"),
        ([[6, 7]], "RECALIBRATE"),
        ([[], [1, 6, 6]], "RECALIBRATE"),
    ],
)
def test_scanner_decision_branches(matrix, expected):
    assert inspect_scanner_calibration(matrix) == expected


@pytest.mark.parametrize(
    "batches,bonus",
    [
        ("not a list", 0),
        ([], -0.1),
    ],
)
def test_invalid_arguments(batches, bonus):
    with pytest.raises(ValueError):
        process_book_buybacks(batches, bonus)


def test_empty_batches_no_loop_path():
    assert process_book_buybacks([], 0) == {
        "total_payout": 0.0, "status": "ZERO_CREDIT"
    }
