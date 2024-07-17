from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING
from zipfile import ZipFile

import pandas as pd

if TYPE_CHECKING:
    from pandas import DataFrame


@dataclass
class ExportedData:
    submissions: DataFrame
    votes: DataFrame
    competitors: DataFrame
    rounds: DataFrame


def load_from_zip(path: str | Path) -> ExportedData:
    with ZipFile(Path(path)) as zf:
        with (
            zf.open('submissions.csv') as submissions,
            zf.open('votes.csv') as votes,
            zf.open('competitors.csv') as competitors,
            zf.open('rounds.csv') as rounds,
        ):
            return ExportedData(
                pd.read_csv(submissions),
                pd.read_csv(votes),
                pd.read_csv(competitors),
                pd.read_csv(rounds),
            )
