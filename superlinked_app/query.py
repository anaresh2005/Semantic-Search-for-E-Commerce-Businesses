from superlinked import framework as sl

from superlinked_app import constants, index
from superlinked_app.config import settings

assert (
    settings.OPENAI_API_KEY
), "OPENAI_API_KEY must be set in environment variables to use natural language queries."


openai_config = sl.OpenAIClientConfig(
    api_key=settings.OPENAI_API_KEY.get_secret_value(), model=settings.OPENAI_MODEL_ID
)

category_similar_param = sl.Param(
    name="query_category",
    description="The text in the user's query that refers to the category of the product.",
    options=constants.CATEGORIES,
)

price_param = sl.Param(
    name="query_price",
    description="The text in the user's query that refers to the price of the product.",
)

review_rating_param = sl.Param(
    name="query_review_rating",
    description="The text in the user's query that refers to the review rating of the product.",
)

descr_similar_param = sl.Param(
    name="query_description",
    description="The text in the user's query that refers to the description of the product.",
)

title_similar_param = sl.Param(
    name="query_title",
    description="The text in the user's query that refers to the title of the product.",
)


base_query = (
    sl.Query(
        index=index.product_index,
        weights={
            index.title_space: sl.Param("title_weight"),
            index.description_space: sl.Param("description_weight"),
            index.review_ratings_space: sl.Param("review_ratings_weight"),
            index.price_space: sl.Param("price_weight"),
        },
    )
    .find(index.product)
    .limit(sl.Param("limit"))
    .with_natural_query(sl.Param("natural_query"), openai_config)
    .filter(
        index.product.type
        == sl.Param(
            "filter_by_type",
            description="Filter products by type",
            option=constants.TYPE,
        ),
    )
)

filter_query = (
    base_query.similar(
        index.description_space,
        descr_similar_param,
        sl.Param("description_similar_clause_weight"),
    )
    .filter(
        index.product.category == category_similar_param,
    )
    .filter(
        index.product.review_ratings >= review_rating_param,
    )
    .filter(
        index.product.price <= price_param,
    )
)

semantic_query = (
    base_query.similar(
        index.description_space,
        descr_similar_param,
        sl.Param("description_similar_clause_weight"),
    )
    .similar(
        index.title_space,
        title_similar_param,
        sl.Param("title_similar_clause_weight"),
    )
    .filter(
        index.product.category == category_similar_param,
    )
)

similar_items_query = semantic_query.with_vector(index.product, sl.Param("product_id"))
