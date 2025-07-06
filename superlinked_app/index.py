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

vertex_client = genai.Client()
handler = VertexGeminiHandler(client=vertex_client)
title_space = sl.TextSimilaritySpace(
    text=product.title,
    model_handler=handler
)