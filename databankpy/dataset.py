from __future__ import annotations

import csv
import json
import sys

from typing import cast, overload, Literal, TypedDict

import numpy as np
import numpy.typing as npt
import requests

from databankpy import BASE_URL
from databankpy.auth import get_access_token
from databankpy.utils import NumpyEncoder, find_index

DatasetColumnType = Literal["FLOAT", "INTEGER", "STRING"]

DatasetLicense = Literal["PUBLIC_DOMAIN", "OTHER"]

DatasetColumnData = (
    npt.NDArray[np.int32] | npt.NDArray[np.float64] | npt.NDArray[np.object_]
)

DTYPE_MAP: dict[DatasetColumnType, npt.DTypeLike] = {
    "FLOAT": np.float64,
    "INTEGER": np.int32,
    "STRING": np.object_,
}

class DatasetColumnDefinition(TypedDict):
    name: str
    description: str
    nullable: bool
    type: DatasetColumnType


class DatasetColumn(DatasetColumnDefinition):
    data: DatasetColumnData


class DatasetInfo(TypedDict):
    name: str
    description: str
    license: DatasetLicense
    columns: list[DatasetColumnDefinition]


class Dataset:
    _name: str
    _description: str
    _license: DatasetLicense
    _columns: list[DatasetColumn]

    def __init__(self, info: DatasetInfo) -> None:
        self._name = info["name"]
        self._description = info["description"]
        self._license = info["license"]
        self._columns = []

        for col in info["columns"]:
            item = col | {'data' : np.ndarray(0, dtype=DTYPE_MAP[col["type"]])}
            self._columns.append(cast(DatasetColumn, item))
    
    def __array__(self) -> npt.NDArray[np.void]:
        shape = (len(self), 1)
        dtype = [(col['name'], DTYPE_MAP[col["type"]]) for col in self.columns]
        arr = np.empty(shape, dtype=dtype)
        for col in self.columns:
            arr[col["name"]] = col["data"].reshape((-1, 1))
        return arr.flatten()

    def __len__(self) -> int:
        return len(self.columns[0]["data"])

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
    def columns(self) -> list[DatasetColumn]:
        """A dictionary mapping column names to metadata and an array of values"""
        return self._columns

    @property
    def column_names(self) -> npt.NDArray[np.str_]:
        return np.array([col["name"] for col in self.columns], dtype=np.str_)
    
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
            
            for colname, data in csv_columns.items():
                index = find_index(self.columns, lambda col : col["name"] == colname)
                assert index is not None
                self.columns[index]['data'] = np.append(
                    self.columns[index]["data"],
                    np.array(data, dtype=DTYPE_MAP[self.columns[index]["type"]]),
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
            data=json.dumps(
                {
                    "name": self.name,
                    "description": self.description,
                    "license": self.license,
                    "columns": self.columns,
                },
                cls=NumpyEncoder,
            ),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )

        if response.ok:
            print("Success!")
        else:
            print(
                f"ERROR: Request failed with status code {response.status_code}",
                file=sys.stderr,
            )
