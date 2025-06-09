import json
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# pip install uvicorn
# uvicorn main:app --reload

from sp_queryservice import sp_ext_service_get_completed_rides, sp_ext_service_get_flagged_rides

app = FastAPI(title="SuperPumped API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at the root URL
@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

# Pydantic model for POST request body
class ProcessRequest(BaseModel):
    input_text: str
    multiplier: int = 1

# GET Flagged Rides: Return rides that are flagged for support review
@app.get("/api/flagged_rides")
async def get_flagged_rides():
    #curl -X GET "http://localhost:8000/api/flagged_rides"
    try:
        print("Role US Support - Flagged Rides")
        print("================================")
        flagged_rides = sp_ext_service_get_flagged_rides("support")
        print(json.dumps(flagged_rides, indent=2))
        #return json.dumps(flagged_rides, indent=2)
        return flagged_rides
        
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    
# GET Flagged Rides: Return rides that are flagged for support review
@app.get("/api/flagged_rides_in")
async def get_flagged_rides_in():
    #curl -X GET "http://localhost:8000/api/flagged_rides"
    try:
        print("Role IN Support - Flagged Rides")
        print("================================")
        flagged_rides = sp_ext_service_get_flagged_rides("in-support")
        print(json.dumps(flagged_rides, indent=2))
        #return json.dumps(flagged_rides, indent=2)
        return flagged_rides
        
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

#flagged_driver_passenger_details
# curl -X GET "http://localhost:8000/api/flagged_driver_passenger_details"
@app.get("/api/flagged_driver_passenger_details")
async def get_flagged_driver_passenger_details():
    try:
        print("Role US Support - Flagged Driver and Passenger Details")
        print("================================")
        flagged_details =""#= sp_ext_service_get_flagged_rides("support")
        #print(json.dumps(flagged_details, indent=2))
        return json.dumps(flagged_details, indent=2)
        
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

#flagged_driver_passenger_details
# curl -X GET "http://localhost:8000/api/flagged_driver_passenger_details_in"
@app.get("/api/flagged_driver_passenger_details_in")
async def get_flagged_driver_passenger_details_in():
    try:
        print("Role IN Support - Flagged Driver and Passenger Details")
        print("================================")
        flagged_details =""#= sp_ext_service_get_flagged_rides("in-support")
        #print(json.dumps(flagged_details, indent=2))
        return json.dumps(flagged_details, indent=2)
        
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    
# superpumped analyst API for completed rides
# curl -X GET "http://localhost:8000/api/completed_rides"
@app.get("/api/completed_rides")
async def get_completed_rides():
    try:
        print("Role US Analyst - Completed Rides")
        print("================================")
        completed_rides = sp_ext_service_get_completed_rides("analyst")
        print(json.dumps(completed_rides, indent=2))
        #return json.dumps(completed_rides, indent=2)
        return completed_rides
        
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

# superpumped analyst API for completed rides
# curl -X GET "http://localhost:8000/api/completed_rides_in"
@app.get("/api/completed_rides_in")
async def get_completed_rides_in():
    try:
        print("Role IN Analyst - Completed Rides")
        print("================================")
        completed_rides = sp_ext_service_get_completed_rides("in-analyst")
        print(json.dumps(completed_rides, indent=2))
        #return json.dumps(completed_rides, indent=2)
        return completed_rides
        
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

# GET endpoint: Returns a greeting with multiple query parameters
@app.get("/api/greet")
async def greet(name: str = "World", times: int = 1):
    """
    Example: /api/greet?name=Alice&times=3
    Returns a greeting repeated 'times' times.
    """
    return {"message": f"Hello, {name}!" * times}

# GET endpoint: Process query parameters
@app.get("/api/process")
async def process_data(input: str = "test", case: str = "upper"):
    """
    Example: /api/process?input=example&case=lower
    Processes input string based on case parameter (upper/lower).
    """
    result = input.upper() if case.lower() == "upper" else input.lower()
    return {"result": f"Processed: {result}"}

# POST endpoint: Process JSON payload
@app.post("/api/process")
async def process_data_post(request: ProcessRequest):
    """
    Example payload: {"input_text": "example", "multiplier": 2}
    Returns the input text transformed and repeated 'multiplier' times.
    """
    result = f"Processed: {request.input_text.upper() * request.multiplier}"
    return {"result": result}

#curl -X POST "http://localhost:8000/api/process" -H "Content-Type: application/json" -d '{"input_text": "test", "multiplier": 2}'

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)