import os
import logging
import json
import azure.functions as func
from azure.functions import HttpRequest, HttpResponse
import openai

apis = func.Blueprint()
# Initialize OpenAI API Key
openai.api_key = os.getenv("AZURE_OPENAI_ENDPOINT")
DEFAULT_CHAT_STORAGE_SETTING = "AzureWebJobsStorage"
DEFAULT_CHAT_COLLECTION_NAME = "ChatState"

@apis.function_name(name="CreateAssistant")
@apis.route(route="assistants/{assistantId}", methods=["PUT"], auth_level=func.AuthLevel.FUNCTION)
@apis.assistant_create_output(arg_name="requests")
async def create_assistant(req: func.HttpRequest, requests: func.Out[str]) -> func.HttpResponse:
    assistantId = req.route_params.get("assistantId")
    # Log the assistantId
    logging.info(f"assistantId: {assistantId}")
    instructions = """
            Don't make assumptions about what values to plug into functions.
            Ask for clarification if a user request is ambiguous.
            """
    create_request = {
        "id": assistantId,
        "instructions": instructions,
        "chatStorageConnectionSetting": DEFAULT_CHAT_STORAGE_SETTING,
        "collectionName": DEFAULT_CHAT_COLLECTION_NAME
    }
    requests.set(json.dumps(create_request))
    response_json = {"assistantId": assistantId, "instructions": instructions}
    return func.HttpResponse(json.dumps(response_json), status_code=202, mimetype="application/json")


@apis.function_name(name="PostUserQuery")
@apis.route(route="assistants/{assistantId}", methods=["POST"])
@apis.assistant_post_input(
    arg_name="state",
    id="{assistantId}",
    user_message="{message}",
    model="%CHAT_MODEL_DEPLOYMENT_NAME%",
    chat_storage_connection_setting=DEFAULT_CHAT_STORAGE_SETTING, collection_name=DEFAULT_CHAT_COLLECTION_NAME)
def post_user_response(req: func.HttpRequest, state: str) -> func.HttpResponse:
    logging.info("PostUserQuery trigger called.")
    
      # Parse the JSON string into a dictionary
    data = json.loads(state)

    # Extract the content of the recentMessage
    recent_message_content = data['recentMessages'][0]['content']
    return func.HttpResponse(recent_message_content, status_code=200, mimetype="text/plain")


