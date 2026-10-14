from pathlib import Path

import pandas as pd
import pytest

from data_utils import DataValidationError, load_products

COLUMNS = ["Category", "Name", "Price", "Stars", "Subcategory", "Best Seller"]


def write_csv(tmp_path: Path, rows: list[dict[str, object]]) -> Path:
    path = tmp_path / "products.csv"
    pd.DataFrame(rows, columns=COLUMNS).to_csv(path, index=False)
    return path


def test_load_products_normalises_types_without_fabricating_values(tmp_path: Path) -> None:
    path = write_csv(
        tmp_path,
        [
            {
                "Category": " Face ",
                "Name": "Example blush",
                "Price": "$1,299.50",
                "Stars": "4.5",
                "Subcategory": "Blush",
                "Best Seller": "yes",
            },
            {
                "Category": "Eyes",
                "Name": "No price",
                "Price": "not available",
                "Stars": "6",
                "Subcategory": "Mascara",
                "Best Seller": "unknown",
            },
        ],
    )

    frame = load_products(path)

    assert frame.loc[0, "Category"] == "Face"
    assert frame.loc[0, "Price"] == 1299.50
    assert frame.loc[0, "Best Seller"] == 1
    assert pd.isna(frame.loc[1, "Price"])
    assert pd.isna(frame.loc[1, "Stars"])
    assert pd.isna(frame.loc[1, "Best Seller"])


def test_missing_data_fails_with_actionable_message(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Run the scraper first"):
        load_products(tmp_path / "missing.csv")


def test_missing_column_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "products.csv"
    pd.DataFrame({"Name": ["Only a name"]}).to_csv(path, index=False)

    with pytest.raises(DataValidationError, match="required column"):
        load_products(path)
