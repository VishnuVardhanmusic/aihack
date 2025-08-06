# src/prompt_builder.py

import json
import os

INPUT_FILE = os.path.join("input", "data.json")

def load_input_data():
    with open(INPUT_FILE, "r") as f:
        return json.load(f)

# ------------------------------
# Demand Forecast Prompt
# ------------------------------
def build_demand_forecast_prompt(data):
    return f"""
You are an AI supply chain analyst.
Analyze the historical order volumes, segments, seasonal notes, and macro factors.
Provide a forecast for the next 2 quarters with risks and recommendations.

Return the output STRICTLY in JSON with this format:

{{
  "Time_Series_Analysis": {{
    "forecast_summary": "<string>",
    "risk_factors": ["<string>", "<string>"],
    "recommendation": "<string>"
  }}
}}

Data Provided:
Orders history: {data['orders_history']}
Segments: {data['segments']}
Seasonal notes: {data['seasonal_notes']}
Macro factors: {data['macro_factors']}
"""

# ------------------------------
# Supplier Summary Prompt
# ------------------------------
def build_supplier_prompt(messages):
    return f"""
You are an AI assistant for supplier management.
Summarize the suppliers' messages, classify them into delayed or on-track,
and provide an overall assessment.

Return the output STRICTLY in JSON with this format:

{{
  "Supplier_Summary": {{
    "delayed_suppliers": [
      {{
        "name": "<string>",
        "issue": "<string>",
        "impact": "<string>"
      }}
    ],
    "on_track_suppliers": [
      {{
        "name": "<string>",
        "status": "<string>"
      }}
    ],
    "overall_assessment": "<string>"
  }}
}}

Supplier messages: {messages}
"""

# ------------------------------
# Logistics Alerts Prompt
# ------------------------------
def build_logistics_prompt(updates):
    return f"""
You are an AI logistics risk advisor.
Analyze active shipments, external conditions, and strategic notes.
Summarize disruptions, improvements, and recommendations.

Return the output STRICTLY in JSON with this format:

{{
  "Logistics_Alerts": {{
    "critical_disruptions": ["<string>", "<string>"],
    "positive_updates": ["<string>", "<string>"],
    "recommendation": "<string>"
  }}
}}

Logistics updates: {updates}
"""

# ------------------------------
# Inventory Optimization Prompt
# ------------------------------
def build_inventory_prompt(inventory_data, safety_policy):
    return f"""
You are an AI inventory planner.
Analyze product stock, average consumption, and lead times.
Recommend urgent reorder quantities and actions for understocked items,
and adjustment actions for overstocked items.

Return the output STRICTLY in JSON with this format:

{{
  "Inventory_Optimization": {{
    "understocked_products": [
      {{
        "name": "<string>",
        "current_stock": <int>,
        "avg_weekly_consumption": <int>,
        "recommended_reorder": <int>,
        "action": "<string>"
      }}
    ],
    "overstocked_products": [
      {{
        "name": "<string>",
        "current_stock": <int>,
        "avg_weekly_consumption": <int>,
        "excess_units": <int>,
        "action": "<string>"
      }}
    ],
    "overall_inventory_health": "<string>"
  }}
}}

Inventory data: {inventory_data}
Safety stock policy: {safety_policy}
"""

# ------------------------------
# Build All Prompts
# ------------------------------
def build_all_prompts():
    data = load_input_data()
    prompts = {
        "demand_forecast": build_demand_forecast_prompt(data["demand_forecasting"]),
        "supplier_summary": build_supplier_prompt(data["supplier_messages"]),
        "logistics_alerts": build_logistics_prompt(data["logistics_updates"]),
        "inventory_optimization": build_inventory_prompt(
            data["inventory_data"], data["safety_stock_policy"]
        )
    }
    return prompts
