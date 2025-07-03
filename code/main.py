import code.classes as classes
import json
from typing import List
from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%d-%m-%Y %H:%M:%S', 
    level=logging.INFO,
    force=True
)
logging.info("Starting application...")

app = FastAPI()

# Example payload for documentation
example_payload = {
    "load": 480,
    "fuels": {
        "gas(euro/MWh)": 13.4,
        "kerosine(euro/MWh)": 50.8,
        "co2(euro/ton)": 20,
        "wind(%)": 60
    },
    "powerplants": [
        {
            "name": "gasfiredbig1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "windpark1",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 150
        }
    ]
}

def validate_simple_payload(payload: classes.Payload) -> bool:
    logging.info(f"Validating payload: {payload}")
    
    # Check if load is valid
    if payload.load <= 0:
        raise HTTPException(status_code=400, detail="Load must be greater than 0")
    
    if len(payload.powerplants) == 0:
        raise HTTPException(status_code=400, detail="At least one power plant is required")
    
    # Check if total available power can meet the load
    total_max_capacity = sum(pp.real_pmax for pp in payload.powerplants)
    logging.info(f"Total max capacity: {total_max_capacity}")
    logging.info(f"Load: {payload.load}")
    if total_max_capacity < payload.load:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient capacity. Required: {payload.load}, Available: {total_max_capacity}"
        )
    return True

def compute_optimal_production(payload: classes.Payload, local_execution: bool = False, output_file_path: str = "output/response.json"):
    production_objective = payload.load
    total_production_cost = 0
    logging.info(f"Production objective: {production_objective}")

    powerplants_efficient_ordered_list = sorted(payload.powerplants, key=lambda pp: pp.mwh_price)

    logging.info("Power plants ordered by efficiency:")
    for pp in powerplants_efficient_ordered_list:
        if production_objective <= 0.0:
            break
        if production_objective > pp.real_pmax:
            pp.production_needed = pp.real_pmax
            production_objective -= pp.real_pmax
        else:
            pp.production_needed = production_objective
            production_objective = 0.0
        total_production_cost += pp.production_needed * pp.mwh_price
        logging.info(pp)

    logging.info(f"Total production cost: {total_production_cost}")
    if local_execution:
        export_local_production_json(powerplants_efficient_ordered_list, output_file_path)
    else:
        return powerplants_efficient_ordered_list

def export_local_production_json(powerplants: List[classes.PowerPlant], output_file_path: str):
    production_list = []
    for pp in powerplants:
        production_list.append({"name": pp.name, "p": pp.production_needed})
    
    with open(output_file_path, "w") as f:
        json.dump(production_list, f, indent=4)

def export_api_production_json(powerplants: List[classes.PowerPlant]):
    production_list = []
    for pp in powerplants:
        production_list.append({"name": pp.name, "p": pp.production_needed})
    
    return production_list

@app.post("/productionplan")
def productionplan(payload: dict = Body(..., example=example_payload)):
    """
    Calculate optimal production plan for power plants
    
    Args:
        payload (dict): JSON payload containing:
            - load: Total load to be produced
            - fuels: Dictionary of fuel prices
            - powerplants: List of power plants with their specifications
    
    Returns:
        JSONResponse: List of power plants with their production values
    """
    payload_obj = classes.Payload.from_dict(payload)
    validate_simple_payload(payload_obj)
    
    powerplants_efficient_ordered_list = compute_optimal_production(payload_obj, local_execution=False)
    if powerplants_efficient_ordered_list is None:
        raise HTTPException(status_code=400, detail="Failed to compute optimal production")
    return JSONResponse(content=export_api_production_json(powerplants_efficient_ordered_list))

def local_execution():
    logging.info("Starting local execution...")
    input_file_path = input("Enter input file path: ")
    output_file_path = input("Enter output file path: ")
    compute_optimal_production(classes.load_payload(input_file_path), True, output_file_path)

if __name__ == "__main__":
    local_execution()
    