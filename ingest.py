import sqlite3
from pathlib import Path

import pandas as pd
from datasets import load_dataset


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^0-9a-zA-Z]+", "_", regex=True)
        .str.strip("_")
    )

    # Fix duplicate columns if any
    cols = []
    for col in df.columns:
        if col in cols:
            counter = 2
            new_col = f"{col}_{counter}"
            while new_col in cols:
                counter += 1
                new_col = f"{col}_{counter}"
            cols.append(new_col)
        else:
            cols.append(col)
    df.columns = cols
    return df


def save_dataset_to_db(dataset_name: str, table_name: str, db_path: Path) -> None:
    print(f"Loading dataset: {dataset_name}")
    dataset = load_dataset(dataset_name, split="train")
    df = dataset.to_pandas()
    df = normalize_columns(df)

    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    print(f"Saved {len(df)} rows to {db_path} table {table_name}")
    print("Columns:", ", ".join(df.columns.tolist()))


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    db_dir = base_dir / "dbs"

    save_dataset_to_db(
        "Mahadih534/Institutional-Information-of-Bangladesh",
        "institutions",
        db_dir / "institutions.db",
    )
    save_dataset_to_db(
        "Mahadih534/all-bangladeshi-hospitals",
        "hospitals",
        db_dir / "hospitals.db",
    )
    save_dataset_to_db(
        "Mahadih534/Bangladeshi-Restaurant-Data",
        "restaurants",
        db_dir / "restaurants.db",
    )

    print("Ingestion complete.")


if __name__ == "__main__":
    main()
