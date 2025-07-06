from superlinked import framework as sl
from superlinked_app import constants
from google import genai
from embedding import VertexGeminiHandler

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
category_space = sl.CategorySpace(
    category_input=product.category,
    categories=constants.CATEGORIES,
    uncategorized_as_category=True,
    negative_filter=-1
)

# Initialize the Vertex AI client and the model handler for text embeddings
vertex_client = genai.Client()
handler = VertexGeminiHandler(client=vertex_client)

# Define the text similarity spaces for title and description using Superlinked's text similarity space definition
title_space = sl.TextSimilaritySpace(
    text=product.title,
    model_handler=handler
)

dscription_space = sl.TextSimilaritySpace(
    text=product.description,
    model_handler=handler
)

review_ratings_space = sl.NumberSpace(
    number = product.review_ratings,
    min_value = -1.0,
    max_value = 5.0,
    mode=sl.Mode.MAXIMUM
)

price_space = sl.NumberSpace(
    number=product.price,
    min_value=0.0,
    max_value=1000.0,
    mode=sl.Mode.MINIMUM
)

product_index = sl.Index(
    spaces=[
        category_space,
        title_space,
        dscription_space,
        review_ratings_space,
        price_space
    ]
)
