from dagster import load_assets_from_package_module, repository

# from etl import assets
from etl.jobs import import_kindle_clippings


@repository
def etl():
    return [import_kindle_clippings]
    # return [load_assets_from_package_module(assets)]
