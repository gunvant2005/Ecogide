"""Emission factors in kg CO2e per unit (IPCC / EPA approximations for education)."""

TRANSPORT = {
    "car_petrol": 0.21,
    "car_electric": 0.05,
    "bus": 0.10,
    "train": 0.04,
    "bike": 0.0,
    "walk": 0.0,
    "flight_short": 0.25,
    "flight_long": 0.15,
}

FOOD = {
    "beef": 6.5,
    "pork": 3.0,
    "chicken": 2.5,
    "fish": 2.0,
    "vegetarian": 1.0,
    "vegan": 0.7,
}

ENERGY = {
    "electricity_kwh": 0.42,
    "natural_gas_kwh": 0.20,
    "heating_oil_liter": 2.68,
}

SHOPPING = {
    "clothing_item": 10.0,
    "electronics_item": 50.0,
    "groceries_bag": 2.5,
}

# Weekly benchmark for an average urban professional (kg CO2e)
WEEKLY_BENCHMARK = 120.0

CATEGORY_LABELS = {
    "transport": "Transport",
    "food": "Food",
    "energy": "Home Energy",
    "shopping": "Shopping",
}
