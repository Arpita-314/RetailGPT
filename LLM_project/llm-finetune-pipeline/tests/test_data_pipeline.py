"""Unit tests for data pipeline (placeholders).
Run with pytest.
"""


def test_clean_text_exists():
    from data_pipeline.etl import clean_text
    assert callable(clean_text)
