from __future__ import annotations

import csv
import sys

from typing import cast, overload, Any, Literal, TypedDict

import numpy as np
import numpy.typing as npt
import requests

from databankpy import BASE_URL
from databankpy.auth import get_access_token

DatasetColumnType = Literal["FLOAT", "INTEGER", "STRING"]

DatasetLicense = Literal["PUBLIC_DOMAIN", "OTHER"]

DatasetColumnData = (
    npt.NDArray[np.int32] | npt.NDArray[np.float64] | npt.NDArray[np.str_]
)

DTYPE_MAP: dict[DatasetColumnType, npt.DTypeLike] = {
    "FLOAT": np.float64,
    "INTEGER": np.int32,
    "STRING": np.str_,
}


class DatasetColumnDefinition(TypedDict):
    description: str
    nullable: bool
    type: DatasetColumnType


class DatasetColumn(DatasetColumnDefinition):
    data: DatasetColumnData


class DatasetInfo(TypedDict):
    name: str
    description: str
    license: DatasetLicense
    columns: dict[str, DatasetColumnDefinition]


class Dataset:
    _name: str
    _description: str
    _license: DatasetLicense
    _columns: dict[str, DatasetColumn]

    def __init__(self, info: DatasetInfo) -> None:
        self._name = info["name"]
        self._description = info["description"]
        self._license = info["license"]
        self._columns = {}

        for key, value in info["columns"].items():
            self._columns[key] = cast(DatasetColumn, value)
            self._columns[key]["data"] = np.ndarray(0, dtype=DTYPE_MAP[value["type"]])

    def __len__(self) -> int:
        return len(self.columns[next(iter(self.columns))]["data"])

    @property
    def name(self) -> str:
        """The name of the dataset"""
        return self._name

    @property
    def description(self) -> str:
        """A brief description of the dataset"""
        return self._description

    @property
    def license(self) -> DatasetLicense:
        """The license for use of the dataset"""
        return self._license

    @property
    def columns(self) -> dict[str, DatasetColumn]:
        """A dictionary mapping column names to metadata and an array of values"""
        return self._columns

    @property
    def column_names(self) -> npt.NDArray[np.str_]:
        return np.array(list(self.columns.keys()), dtype=np.str_)

    def append_csv(self, filepath: str) -> None:
        """Load the rows from a CSV file and append them to the dataset"""
        with open(filepath, "r", newline="") as f:
            reader = csv.reader(f, delimiter=",", strict=True)

            csv_columns: dict[str, list[str]] = {k: [] for k in next(reader)}
            for col in self.column_names:
                if col not in csv_columns:
                    raise RuntimeError(f"Column '{col}' not found in file: {filepath}")

            for row in reader:
                for i, col in enumerate(csv_columns.keys()):
                    csv_columns[col].append(row[i])

            for key, value in csv_columns.items():
                self.columns[key]["data"] = np.append(
                    self.columns[key]["data"],
                    np.array(value, dtype=DTYPE_MAP[self.columns[key]["type"]]),
                )

    @overload
    def upload(self, access_token: str) -> None:
        """Upload this dataset to the databank using an access token"""
        ...

    @overload
    def upload(self, email: str, password: str) -> None:
        """Upload this dataset to the databank using your login credentials"""
        ...

    def upload(self, *args: str, **kwargs: str) -> None:
        """
        Upload this dataset instance to the databank. This method may be called with
        either an access token or your login credentials.
        """
        if len(args) == 2:
            access_token = get_access_token(*args)
        elif kwargs.get("email") or kwargs.get("password"):
            email, password = (
                kwargs.get("email") or args[0],
                kwargs.get("password") or args[1],
            )
            access_token = get_access_token(email, password)
        else:
            access_token = kwargs.get("access_token") or args[0]

        response = requests.post(
            f"{BASE_URL}/v1/datasets",
            json={
                "name": self.name,
                "description": self.description,
                "license": self.license,
                "columns": self.columns,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if response.ok:
            print("Success!")
        else:
            print(
                f"ERROR: Request failed with status code {response.status_code}",
                file=sys.stderr,
            )
