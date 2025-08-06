# src/prompt_builder.py

import json
import os

INPUT_FILE = os.path.join("input", "data.json")

def load_input_data():
    with open(INPUT_FILE, "r") as f:
        return json.load(f)

def build_demand_forecast_prompt(data):
    return f"""
You are an AI supply chain analyst.
Analyze the following historical order volumes across different quarters and customer segments.
Also, consider the seasonal notes. Provide a clear forecast.

Orders history: {data['orders_history']}
Segments: {data['segments']}
Seasonal notes: {data['seasonal_notes']}
"""

def build_supplier_prompt(messages):
    return f"""
You are an AI assistant for supplier management.
Summarize the supplier updates below, highlighting delays, risks, and on-track shipments.

Supplier messages:
{chr(10).join(messages)}
"""

def build_logistics_prompt(updates):
    return f"""
You are an AI logistics risk advisor.
Analyze the logistics updates below.
Summarize disruptions, delays, and improvements.

Logistics updates:
{chr(10).join(updates)}
"""

def build_inventory_prompt(inventory_data, safety_policy):
    return f"""
You are an AI inventory planner.
Analyze the inventory data and recommend optimal stock actions.
Consider average weekly consumption and the safety stock policy.

Inventory data:
{inventory_data}
Safety stock policy: {safety_policy}
"""

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
