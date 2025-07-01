from dataclasses import dataclass
from typing import List, Dict, Any

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
    pmin: float
    pmax: float

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PowerPlant':
        return PowerPlant(
            name=data["name"],
            type=data["type"],
            efficiency=data["efficiency"],
            pmin=data["pmin"],
            pmax=data["pmax"]
        )


@dataclass
class Payload:
    load: float
    price_per_fuel: PricePerFuel
    powerplants: List[PowerPlant]
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Payload':
        return Payload(
            load=data["load"],
            price_per_fuel=PricePerFuel.from_dict(data["fuels"]),
            powerplants=[PowerPlant.from_dict(pp) for pp in data["powerplants"]]
        )

if __name__ == "__main__":
    import json
    with open("example_payloads/payload3.json", "r") as f:
        data = json.load(f)
    payload = Payload.from_dict(data)
    print(payload.price_per_fuel)