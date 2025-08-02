import superlinked.framework as sl
from loguru import logger

from superlinked_app import index, query
from superlinked_app.config import settings

product_source: sl.RestSource = sl.RestSource(index.product)

product_data_loader_parse = sl.DataFrameParser(
    index.product, mapping={index.product.id: "asin"}
)
product_data_loader_config = sl.DataLoaderConfig(str(settings))
