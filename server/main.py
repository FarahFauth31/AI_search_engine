from fastapi import FastAPI, WebSocket
from pydantic_models.chat_body import ChatBody
from services.search_service import SearchService
from services.sorting_sources import SortingSourcesService
from services.llm_service import LLMService
import traceback
import asyncio

app = FastAPI()

search_service = SearchService()
sorting_sources_service = SortingSourcesService()
llm_service = LLMService()

# chat websocket
@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await asyncio.sleep(0.1)
        data = await websocket.receive_json()
        query = data.get("query")
        if not query:
            raise ValueError("Query is null.")
        search_results = search_service.web_search(query)
        sorted_results = sorting_sources_service.sort_sources(query, search_results)
        await asyncio.sleep(0.1)
        await websocket.send_json({
            "type": "search_result",
            "data": sorted_results
        })
        for chunk in llm_service.generate_streamed_llm_response(query, sorted_results):
            await asyncio.sleep(0.1)
            await websocket.send_json({
                "type": "content",
                "data": chunk
            })
    except:
        print("Unexpected error occurred while streaming.")
        traceback.print_exc()
    finally:
        await websocket.close()

# chat (post request to get query from user)
@app.post("/chat")
def chat_endpoint(body: ChatBody):
    # search the web and find appropriate sources
    search_results = search_service.web_search(body.query)
    # sort the sources
    sorted_results = sorting_sources_service.sort_sources(body.query, search_results)
    # generate responses using LLMs
    llm_response = llm_service.generate_llm_response(body.query, sorted_results)
    return llm_response