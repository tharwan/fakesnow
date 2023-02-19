from unittest.mock import MagicMock

import pytest
import snowflake.connector
import snowflake.connector.pandas_tools
from snowflake.connector import connect
from snowflake.connector.pandas_tools import write_pandas

import fakesnow


def test_patch_snowflake_connector_connect(_fake_snow: None) -> None:
    assert isinstance(snowflake.connector.connect, MagicMock), "snowflake.connector.connect is not mocked"


def test_patch_snowflake_connector_pandas_tools_write_pandas(_fake_snow: None) -> None:
    assert isinstance(
        snowflake.connector.pandas_tools.write_pandas, MagicMock
    ), "snowflake.connector.pandas_tools.write_pandas is not mocked"


def test_patch_this_modules_connect() -> None:
    with fakesnow.patch(f"{__name__}.connect"):
        assert isinstance(connect, MagicMock), "connect is not mocked"


def test_patch_this_modules_write_pandas() -> None:
    with fakesnow.patch(f"{__name__}.write_pandas"):
        assert isinstance(write_pandas, MagicMock), "write_pandas is not mocked"


def test_cannot_patch_twice(_fake_snow: None) -> None:
    # _fake_snow is the first patch

    with pytest.raises(AssertionError) as excinfo:
        # second patch will fail
        with fakesnow.patch():
            pass

    assert "Snowflake connector is already patched" in str(excinfo.value)