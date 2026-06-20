export const CATEGORY_OPTIONS = {
  transport: {
    label: "Transport",
    unit: "km",
    subTypes: [
      { value: "car_petrol", label: "Car (petrol)" },
      { value: "car_electric", label: "Car (electric)" },
      { value: "bus", label: "Bus" },
      { value: "train", label: "Train" },
      { value: "bike", label: "Bike" },
      { value: "walk", label: "Walk" },
      { value: "flight_short", label: "Flight (short haul)" },
      { value: "flight_long", label: "Flight (long haul)" },
    ],
  },
  food: {
    label: "Food",
    unit: "meal",
    subTypes: [
      { value: "beef", label: "Beef meal" },
      { value: "pork", label: "Pork meal" },
      { value: "chicken", label: "Chicken meal" },
      { value: "fish", label: "Fish meal" },
      { value: "vegetarian", label: "Vegetarian meal" },
      { value: "vegan", label: "Vegan meal" },
    ],
  },
  energy: {
    label: "Home Energy",
    unit: "kWh",
    subTypes: [
      { value: "electricity_kwh", label: "Electricity" },
      { value: "natural_gas_kwh", label: "Natural gas" },
      { value: "heating_oil_liter", label: "Heating oil (liters)" },
    ],
  },
  shopping: {
    label: "Shopping",
    unit: "item",
    subTypes: [
      { value: "clothing_item", label: "Clothing item" },
      { value: "electronics_item", label: "Electronics item" },
      { value: "groceries_bag", label: "Groceries bag" },
    ],
  },
} as const;

export const TRANSPORT_OPTIONS = [
  { value: "car_petrol", label: "Car (petrol)" },
  { value: "car_electric", label: "Car (electric)" },
  { value: "bus", label: "Bus" },
  { value: "train", label: "Train" },
  { value: "bike", label: "Bike" },
];

export const DIET_OPTIONS = [
  { value: "beef", label: "Regular red meat" },
  { value: "chicken", label: "Mixed / poultry" },
  { value: "vegetarian", label: "Vegetarian" },
  { value: "vegan", label: "Vegan" },
];

export const CATEGORY_COLORS: Record<string, string> = {
  transport: "#2d6a4f",
  food: "#40916c",
  energy: "#52b788",
  shopping: "#74c69d",
};

export const CATEGORY_LABELS: Record<string, string> = {
  transport: "Transport",
  food: "Food",
  energy: "Home Energy",
  shopping: "Shopping",
};

export function formatMarkdown(text: string): string {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n/g, "<br />");
}
