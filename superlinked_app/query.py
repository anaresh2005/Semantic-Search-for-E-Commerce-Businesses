from superlinked import framework as sl

from superlinked_app import constants, index
from superlinked_app.config import settings

assert (
    settings.OPENAI_API_KEY
), "OPENAI_API_KEY must be set in environment variables to use natural language queries."
