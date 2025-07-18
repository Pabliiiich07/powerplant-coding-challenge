# PowerPlant Coding Challenge

## Author

Pablo Sancho Saiz

This repository is a personal project for educational purposes and it is not intended to be used for any commercial use.

## Quick Start with Docker
```bash
# Build the Docker image
docker build -t powerplant-api .

# Run the container
docker run -d --name powerplant-api -p 8888:8888 powerplant-api
```

## Local Development (without Docker)

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Pabliiiich07/powerplant-coding-challenge.git
cd powerplant-coding-challenge
```

2. **Install dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Run the application**
```bash
# For API usage
uvicorn code.main:app --reload --port 8888

# For local execution
python code/main.py
```

---

## API Usage

### Endpoint
- **URL**: `http://localhost:8888/productionplan`
- **Method**: POST
- **Content-Type**: application/json

### Test the API

```bash
# Test with example payload
curl -X POST http://localhost:8888/productionplan \
  -H "Content-Type: application/json" \
  -d @example_payloads/payload1.json
```

### API Documentation
- **Swagger UI**: http://localhost:8888/docs
- **ReDoc**: http://localhost:8888/redoc

## Input JSON Example

```json
{
  "load": 200,
  "fuels": {
    "gas(euro/MWh)": 13.4,
    "kerosine(euro/MWh)": 50.8,
    "co2(euro/ton)": 20,
    "wind(%)": 60
  },
  "powerplants": [
    {
      "name": "windturbine1",
      "type": "windturbine",
      "efficiency": 1,
      "pmin": 0,
      "pmax": 150
    },
    {
      "name": "gasfired1",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    {
      "name": "turbojet1",
      "type": "turbojet",
      "efficiency": 0.3,
      "pmin": 0,
      "pmax": 16
    }
  ]
}
```

## Output JSON Example

```json
[
    {
        "name": "windturbine1",
        "p": 90
    },
    {
        "name": "gasfired1",
        "p": 110
    },
    {
        "name": "turbojet1",
        "p": 0
    }
]
```

## Project Structure

```
powerplant-coding-challenge/
├── code/
│   ├── __init__.py
│   ├── classes.py          # Data models and business logic
│   └── main.py            # FastAPI application
├── example_payloads/
│   ├── payload1.json      # Example input payloads
│   ├── payload2.json
│   ├── payload3.json
│   └── response3.json     # Example output
├── output/                # Generated output files
├── Dockerfile            # Docker configuration
├── requirements.txt      # Python dependencies
├── deploy.sh            # Deployment script
└── README.md            # This file
```

## Future upgrades
For a future production deployment, it will be necessary to complete the development of the CO2 consumption feature and to carry out thorough testing across all steps of the program. I have implemented some basic tests, but given the estimated 4-hour time limit, my priority was to deliver a functional program.

## Problem Description

This is a coding challenge for calculating optimal power plant production plans. The goal is to determine how much power each power plant should produce to meet a given load while minimizing costs.

### Key Features

- **Merit Order**: Power plants are activated based on cost efficiency
- **Load Balancing**: Total production must exactly match the demand
- **Constraints**: Each power plant has minimum and maximum production limits
- **Fuel Costs**: Different fuel types (gas, kerosine) have different costs
- **Wind Integration**: Wind turbines have zero fuel cost but variable output

### Power Plant Types

1. **Gas-fired**: Uses gas fuel, moderate efficiency (~50%)
2. **Turbojet**: Uses kerosine fuel, lower efficiency (~30%)
3. **Wind turbine**: Zero fuel cost, output depends on wind percentage

## Acceptance Criteria

✅ **API exposed on port 8888**  
✅ **README.md with build and launch instructions**  
✅ **Dockerfile for easy deployment**  
✅ **Proper error handling and validation**  
✅ **Example payloads and responses**

## License

This project is for educational purposes only.

## Problem description

Below you can find the description of a coding challenge that we ask people to perform when applying for a job in our team.

The goal of this coding challenge is to provide the applicant some insight into the business we're in and as such provide the applicant an indication about the challenges she/he will be confronted with. Next, during the first interview we will use the applicant's implementation as a seed to discuss all kinds of interesting software engineering topics.  

Time is scarce, we know. Therefore we recommend you not to spend more than 4 hours on this challenge. We know it is not possible to deliver a finished implementation of the challenge in only four hours so, please, try to detail in a few lines how you'll improve it, what it is missing due to lack of time. Even though your submission will not be complete, it will provide us plenty of information and topics to discuss later on during the talks.

This coding-challenge is part of a formal process and is used in collaboration with the recruiting companies we work with.  Submitting a pull-request will not automatically trigger the recruitement process.
## Who are we 

We are the Iberia IS team for the Short-term Power within [GEMS](https://gems.engie.com/).

[GEMS](https://gems.engie.com/), which stands for 'Global Energy Management & Sales', is the energy management arm of [ENGIE](https://www.engie.com/), one of the largest global energy players, 
with access to local markets all over the world.  

SPaaS is a team consisting of around 100 people with experience in energy markets, IT and modeling. In smaller teams consisting of a mix of people with different experiences, we are active on the [day-ahead](https://en.wikipedia.org/wiki/European_Power_Exchange#Day-ahead_markets) market, [intraday markets](https://en.wikipedia.org/wiki/European_Power_Exchange#Intraday_markets) and [collaborate with the TSO to balance the grid continuously](https://en.wikipedia.org/wiki/Transmission_system_operator#Electricity_market_operations).

## The challenge

### In short
Calculate how much power each of a multitude of different [powerplants](https://en.wikipedia.org/wiki/Power_station) need to produce (a.k.a. the production-plan) when the [load](https://en.wikipedia.org/wiki/Load_profile) is given and taking into account the cost of the underlying energy sources (gas,  kerosine) and the Pmin and Pmax of each powerplant.

### More in detail

The load is the continuous demand of power. The total load at each moment in time is forecasted. For instance for Belgium you can see the load forecasted by the grid operator [here](https://www.elia.be/en/grid-data/load-and-load-forecasts).

At any moment in time, all available powerplants need to generate the power to exactly match the load.  The cost of generating power can be different for every powerplant and is dependent on external factors: The cost of producing power using a [turbojet](https://en.wikipedia.org/wiki/Gas_turbine#Industrial_gas_turbines_for_power_generation), that runs on kerosine, is higher compared to the cost of generating power using a gas-fired powerplant because of gas being cheaper compared to kerosine and because of the [thermal efficiency](https://en.wikipedia.org/wiki/Thermal_efficiency) of a gas-fired powerplant being around 50% (2 units of gas will generate 1 unit of electricity) while that of a turbojet is only around 30%.  The cost of generating power using windmills however is zero. Thus deciding which powerplants to activate is dependent on the [merit-order](https://en.wikipedia.org/wiki/Merit_order).

When deciding which powerplants in the merit-order to activate (a.k.a. [unit-commitment problem](https://en.wikipedia.org/wiki/Unit_commitment_problem_in_electrical_power_production)) the maximum amount of power each powerplant can produce (Pmax) obviously needs to be taken into account.  Additionally gas-fired powerplants generate a certain minimum amount of power when switched on, called the Pmin. 


### Performing the challenge

Build a REST API exposing an endpoint `/productionplan` that accepts a POST of which the body contains a payload as you can find in the `example_payloads` directory and that returns a json with the same structure as in `example_response.json` and that manages and logs run-time errors.

For calculating the unit-commitment, we prefer you not to rely on an existing (linear-programming) solver but instead write an algorithm yourself.

Implementations can be submitted in either C# (on .Net 5 or higher) or Python (3.8 or higher) as these are (currently) the main languages we use in SPaaS. Along with the implementation should be a README that describes how to compile (if applicable) and launch the application.

- C# implementations should contain a project file to compile the application. 
- Python implementations should contain a `requirements.txt` or a `pyproject.toml` (for use with poetry) to install all needed dependencies.

#### Payload

The payload contains 3 types of data:
 - load: The load is the amount of energy (MWh) that need to be generated during one hour.
 - fuels: based on the cost of the fuels of each powerplant, the merit-order can be determined which is the starting point for deciding which powerplants should be switched on and how much power they will deliver.  Wind-turbine are either switched-on, and in that case generate a certain amount of energy depending on the % of wind, or can be switched off. 
   - gas(euro/MWh): the price of gas per MWh. Thus if gas is at 6 euro/MWh and if the efficiency of the powerplant is 50% (i.e. 2 units of gas will generate one unit of electricity), the cost of generating 1 MWh is 12 euro.
   - kerosine(euro/Mwh): the price of kerosine per MWh.
   - co2(euro/ton): the price of emission allowances (optionally to be taken into account).
   - wind(%): percentage of wind. Example: if there is on average 25% wind during an hour, a wind-turbine with a Pmax of 4 MW will generate 1MWh of energy.
 - powerplants: describes the powerplants at disposal to generate the demanded load. For each powerplant is specified:
   - name:
   - type: gasfired, turbojet or windturbine.
   - efficiency: the efficiency at which they convert a MWh of fuel into a MWh of electrical energy. Wind-turbines do not consume 'fuel' and thus are considered to generate power at zero price.
   - pmax: the maximum amount of power the powerplant can generate.
   - pmin: the minimum amount of power the powerplant generates when switched on. 

#### response

The response should be a json as in `example_payloads/response3.json`, which is the expected answer for `example_payloads/payload3.json`, specifying for each powerplant how much power each powerplant should deliver. The power produced by each powerplant has to be a multiple of 0.1 Mw and the sum of the power produced by all the powerplants together should equal the load.

### Want more challenge?

Having fun with this challenge and want to make it more realistic. Optionally, do one of the extra's below:

#### Docker

Provide a Dockerfile along with the implementation to allow deploying your solution quickly.

#### CO2

Taken into account that a gas-fired powerplant also emits CO2, the cost of running the powerplant should also take into account the cost of the [emission allowances](https://en.wikipedia.org/wiki/Carbon_emission_trading).  For this challenge, you may take into account that each MWh generated creates 0.3 ton of CO2. 

## Acceptance criteria

For a submission to be reviewed as part of an application for a position in the team, the project needs to:
  - contain a README.md explaining how to build and launch the API
  - expose the API on port `8888`

Failing to comply with any of these criteria will automatically disqualify the submission.

## More info

For more info on energy management, check out:

 - [Global Energy Management Solutions](https://www.youtube.com/watch?v=SAop0RSGdHM)
 - [COO hydroelectric power station](https://www.youtube.com/watch?v=edamsBppnlg)
 - [Management of supply](https://www.youtube.com/watch?v=eh6IIQeeX3c) - video made during winter 2018-2019

## FAQ

##### Can an existing solver be used to calculate the unit-commitment
Implementations should not rely on an external solver and thus contain an algorithm written from scratch (clarified in the text as of version v1.1.0)

