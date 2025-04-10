from fastapi import FastAPI
from pydantic_models.chat_body import ChatBody
from services.search_service import SearchService
from services.sorting_sources import SortingSourcesService

app = FastAPI()

search_service = SearchService()
sorting_sources_service = SortingSourcesService()

# chat (post request to get query from user)
@app.post("/chat")
def chat_endpoint(body: ChatBody):
    # search the web and find appropriate sources
    search_results = search_service.web_search(body.query)
    # sort the sources
    sorted_results = sorting_sources_service.sort_sources(body.query, search_results)
    # generate responses using LLMs
    return body.query