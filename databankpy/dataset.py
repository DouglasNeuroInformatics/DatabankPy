from __future__ import annotations

import csv
import sys

from typing import cast, overload, Literal, TypedDict

import requests

from databankpy import BASE_URL
from databankpy.auth import get_access_token

DatasetColumnType = Literal["FLOAT", "INTEGER", "STRING"]

DatasetLicense = Literal["PUBLIC_DOMAIN", "OTHER"]

DatasetColumnData = list[int | float | str]

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
        self._columns = {
            k: cast(DatasetColumn, {**v, "data": []})
            for k, v in info["columns"].items()
        }

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

    def load_csv(self, filepath: str) -> None:
        """Load the data from a csv file"""
        with open(filepath, "r", newline="") as f:
            reader = csv.reader(f, delimiter=",", strict=True)
            column_names = next(reader)
            for col in self.columns.keys():
                if col not in column_names:
                    raise RuntimeError(f"Column '{col}' not found in file: {filepath}")
            for row in reader:
                for i in range(len(row)):
                    self.columns[column_names[i]]["data"].append(row[i])

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
