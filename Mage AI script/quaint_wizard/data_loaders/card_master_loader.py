from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_cardmaster_data(*args, **kwargs):
    query = 'SELECT * FROM cardmaster'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        return loader.load(query)

@test
def test_load_cardmaster_data(output, *args) -> None:
    assert isinstance(output, pd.DataFrame), 'The output is not a DataFrame'
    assert not output.empty, 'The DataFrame is empty'
