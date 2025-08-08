from superlinked import framework as sl
from superlinked_app import constants
from google import genai
from superlinked_app.embedding import GeminiHandler
from superlinked_app.config import settings


assert (
    settings.GEMINI_API_KEY
), "GEMINI_API_KEY must be set in environment variables to use the Gemini encoding model."

# Initialize the Vertex AI client and the model handler for text embeddings
vertex_client = genai.Client(api_key=settings.GEMINI_API_KEY.get_secret_value())
handler = GeminiHandler(client=vertex_client)


# Define the schema for a product using Superlinked's schema definition
class ProductSchema(sl.Schema):
    id: sl.IdField
    type: sl.String
    category: sl.StringList
    title: sl.String
    description: sl.String
    review_ratings: sl.Float
    review_count: sl.Integer
    price: sl.Float


product = ProductSchema()

# Define the category space for products using Superlinked's category space definition
category_space = sl.CategoricalSimilaritySpace(
    category_input=product.category,
    categories=constants.CATEGORIES,
    uncategorized_as_category=True,
    negative_filter=-1,
)


# Define the text similarity spaces for title and description using Superlinked's text similarity space definition
title_space = sl.TextSimilaritySpace(text=product.title, model_handler=handler)

description_space = sl.TextSimilaritySpace(
    text=product.description, model_handler=handler
)

review_ratings_space = sl.NumberSpace(
    number=product.review_ratings, min_value=-1.0, max_value=5.0, mode=sl.Mode.MAXIMUM
)

price_space = sl.NumberSpace(
    number=product.price, min_value=0.0, max_value=1000.0, mode=sl.Mode.MINIMUM
)

product_index = sl.Index(
    spaces=[
        category_space,
        title_space,
        description_space,
        review_ratings_space,
        price_space,
    ],
    fields=[product.type, product.category, product.review_ratings, product.price],
)
