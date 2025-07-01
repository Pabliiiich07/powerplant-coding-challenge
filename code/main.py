import code.classes as classes
import json
from typing import List
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.INFO)
logging.info("Starting application...")

app = FastAPI()

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
def productionplan(payload: classes.PayloadModel):
    payload_obj = classes.Payload.from_dict(payload)
    compute_optimal_production(payload_obj)
    result = export_api_production_json(payload_obj.powerplants)
    return JSONResponse(content=result)

def local_execution():
    input_file_path = "example_payloads/payload3.json"
    output_file_path = "output/response.json"
    compute_optimal_production(classes.load_payload(input_file_path), True, output_file_path)

if __name__ == "__main__":
    local_execution()
    