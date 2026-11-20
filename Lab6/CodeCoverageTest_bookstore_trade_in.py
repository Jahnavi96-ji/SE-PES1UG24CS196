import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration


def batch(format_type="paperback", books=None, approved=True, credit=False):
    return {
        "intake_approved": approved,
        "format": format_type,
        "payout_in_credit": credit,
        "books": [] if books is None else books,
    }


def book(condition="good", missing_pages=0, counterfeit=False):
    return {
        "condition": condition,
        "missing_pages": missing_pages,
        "counterfeit": counterfeit,
    }


def test_invalid_input_types_and_bonus():
    with pytest.raises(ValueError):
        process_book_buybacks("not a list", 5.0)
    with pytest.raises(ValueError):
        process_book_buybacks([], -1.0)


def test_all_supported_formats_and_conditions():
    batches = [
        batch("textbook", [book("mint")]),
        batch("hardcover", [book("poor")]),
        batch("paperback", [book("good")]),
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result == {"total_payout": 40.0 * 1.25 + 15.0 * 0.40 + 8.0,
                      "status": "COMPLETED"}


def test_unapproved_and_unknown_format_batches_are_skipped_or_rejected():
    result = process_book_buybacks([
        batch("paperback", [book()], approved=False),
        batch("ebook", [book()]),
    ], 0.0)
    assert result == {"total_payout": 0.0, "status": "ZERO_CREDIT"}


def test_missing_pages_and_counterfeit_paperback_are_rejected():
    result = process_book_buybacks([
        batch("paperback", [
            book(missing_pages=2),
            book(counterfeit=True),
            book(),
        ])
    ], 0.0)
    assert result == {"total_payout": 8.0, "status": "COMPLETED"}


def test_counterfeit_textbook_cancels_batch_credit():
    result = process_book_buybacks([
        batch("textbook", [book(), book(counterfeit=True), book()])
    ], 0.0)
    assert result == {"total_payout": 0.0, "status": "ZERO_CREDIT"}


def test_store_credit_bonus_is_added():
    result = process_book_buybacks([
        batch("hardcover", [book()], credit=True)
    ], 5.0)
    assert result == {"total_payout": 20.0, "status": "COMPLETED"}


def test_more_than_four_rejections_triggers_audit():
    result = process_book_buybacks([
        batch("paperback", [book(missing_pages=1) for _ in range(5)])
    ], 0.0)
    assert result == {"total_payout": 0.0, "status": "AUDIT_REJECTED"}


def test_empty_book_list_with_credit_bonus_completes():
    result = process_book_buybacks([batch("paperback", [], credit=True)], 3.0)
    assert result == {"total_payout": 3.0, "status": "COMPLETED"}


def test_empty_batches_returns_zero_credit():
    assert process_book_buybacks([], 0.0) == {
        "total_payout": 0.0, "status": "ZERO_CREDIT"
    }


def test_scanner_empty_data():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_calibrated_after_low_or_single_high_reading():
    assert inspect_scanner_calibration([[1, 2, 6, 3], [0, 5]]) == "CALIBRATED"


def test_scanner_recalibrates_after_two_consecutive_high_readings():
    assert inspect_scanner_calibration([[1, 6, 7]]) == "RECALIBRATE"
