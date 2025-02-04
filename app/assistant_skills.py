import os
import logging
import json
import azure.functions as func
import pytz
from datetime import datetime, timezone
skills = func.Blueprint()

@skills.function_name("GetWeatherForecast")
@skills.assistant_skill_trigger(arg_name="location", function_description="Provides the weather forecast")
def get_weather(location:str) -> str:
    logging.info('Python HTTP trigger function processed a get_weather request.')

    response_message = f"The current weather in {location} is 72 degrees and sunny."
    logging.info(f"Getting weather for location: {location}")
    
    return json.dumps(response_message)

@skills.function_name("GetCurrentTime")
@skills.assistant_skill_trigger(arg_name="location", function_description="Provides the current time")
def get_time(location:str) -> str:
    logging.info('Python HTTP trigger function processed a get_time request.')
     # Get the current time in PST
    pst_timezone = pytz.timezone('US/Pacific')
    current_time_utc = datetime.now(pst_timezone).isoformat()
   # current_time_utc = datetime.now(timezone.dst).isoformat()
    logging.info(f"Getting time in {location} is {current_time_utc}")
    response_message = f"The current time in {location} is  {current_time_utc} "
  
    return json.dumps(response_message)

