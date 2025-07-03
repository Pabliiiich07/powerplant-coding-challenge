from dataclasses import dataclass
from typing import List, Dict, Any
import json
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.INFO)
logging.info("Starting classes...")

@dataclass
class PricePerFuel:
    gas_euro_per_mwh: float
    kerosine_euro_per_mwh: float
    co2_euro_per_ton: float
    wind_percentage: float

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PricePerFuel':
        return PricePerFuel(
            gas_euro_per_mwh=data.get("gas(euro/MWh)", 0),
            kerosine_euro_per_mwh=data.get("kerosine(euro/MWh)", 0),
            co2_euro_per_ton=data.get("co2(euro/ton)", 0),
            wind_percentage=data.get("wind(%)", 0)
        )

@dataclass
class PowerPlant:
    name: str
    type: str
    efficiency: float
    optimal_pmin: float
    optimal_pmax: float
    real_pmin: float
    real_pmax: float
    mwh_price: float
    production_needed: float

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PowerPlant':
        return PowerPlant(
            name=data["name"],
            type=data["type"],
            efficiency=data["efficiency"],
            optimal_pmin=data["pmin"],
            optimal_pmax=data["pmax"],
            real_pmin=0.0,
            real_pmax=0.0,
            mwh_price=0.0,
            production_needed=0.0
        )

    def __str__(self):
        return f"Power plant {self.name}: Production range [{self.real_pmin} - {self.real_pmax}], production needed: {self.production_needed} (mwh price: {self.mwh_price})"

    def compute_real_stats(self, price_per_fuel: PricePerFuel):
        self.calculate_real_production(price_per_fuel)
        self.compute_mwh_price(price_per_fuel)

    def compute_mwh_price(self, price_per_fuel: PricePerFuel):
        if self.type == "gasfired":
            self.mwh_price = float(price_per_fuel.gas_euro_per_mwh / self.efficiency)
        elif self.type == "turbojet":
            self.mwh_price = float(price_per_fuel.kerosine_euro_per_mwh / self.efficiency)
        elif self.type == "windturbine":
            self.mwh_price = 0.0
        else:
            logging.error(f"Unknown power plant type: {self.type}")
            raise ValueError(f"Unknown power plant type: {self.type}")

    def calculate_real_production(self, price_per_fuel: PricePerFuel):
        if self.type == "windturbine":
            self.real_pmin = float(self.optimal_pmin * price_per_fuel.wind_percentage / 100 * self.efficiency)
            self.real_pmax = float(self.optimal_pmax * price_per_fuel.wind_percentage / 100 * self.efficiency)
        elif self.type == "gasfired" or self.type == "turbojet":
            self.real_pmin = float(self.optimal_pmin) 
            self.real_pmax = float(self.optimal_pmax)             
        else:
            logging.error(f"Unknown power plant type: {self.type}")
            raise ValueError(f"Unknown power plant type: {self.type}")
    
@dataclass
class Payload:
    load: float
    price_per_fuel: PricePerFuel
    powerplants: List[PowerPlant]
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Payload':
        load = data["load"]
        price_per_fuel = PricePerFuel.from_dict(data["fuels"])
        powerplants = [PowerPlant.from_dict(pp) for pp in data["powerplants"]]

        for pp in powerplants:
            logging.info(f"Power plant loaded: {pp}")
            pp.compute_real_stats(price_per_fuel)

        return Payload(
            load=load,
            price_per_fuel=price_per_fuel,
            powerplants=powerplants
        )

def load_payload(file_path: str) -> Payload:
    with open(file_path, "r") as f:
        data = json.load(f)
    return Payload.from_dict(data)

if __name__ == "__main__":
    payload = load_payload("example_payloads/payload3.json")
    for pp in payload.powerplants:
        print(pp)