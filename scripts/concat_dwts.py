"""Combine all per-season DWTS parquet files into a single tidy dataset."""

from pathlib import Path

import polars as pl

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
OUT_PATH = DATA_DIR / "dwts_all_seasons.parquet"


def concat_seasons(data_dir: Path = RAW_DIR) -> pl.DataFrame:
    season_files = sorted(
        data_dir.glob("season-*.parquet"),
        key=lambda p: int(p.stem.split("-")[1]),
    )
    if not season_files:
        raise FileNotFoundError(f"No season-*.parquet files found in {data_dir}")

    frames = [pl.read_parquet(f) for f in season_files]
    combined = pl.concat(frames, how="diagonal_relaxed")
    return combined


if __name__ == "__main__":
    combined = concat_seasons()
    combined.write_parquet(OUT_PATH)
    print(f"combined {combined.get_column('season').n_unique()} seasons")
    print(f"wrote {combined.height} rows to {OUT_PATH}")
    print(combined)
