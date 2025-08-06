# src/html_generated.py

import json
import os

OUTPUT_JSON_FILE = os.path.join("output", "ai_report.json")
OUTPUT_HTML_FILE = os.path.join("output", "ti_sci_report.html")


# -----------------------------
# 1) Save raw responses to JSON
# -----------------------------
def save_responses_to_json(responses: dict):
    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_JSON_FILE, "w") as f:
        json.dump({"TI_SCI_Report": responses}, f, indent=4)
    print(f"[INFO] Raw responses saved to {OUTPUT_JSON_FILE}")


# -----------------------------
# 2) Convert final JSON to HTML
# -----------------------------
def generate_html_from_json(input_file=OUTPUT_JSON_FILE):
    if not os.path.exists(input_file):
        print(f"[ERROR] JSON file not found: {input_file}")
        return

    with open(input_file, "r") as f:
        data = json.load(f)

    report = data.get("TI_SCI_Report", {})

    html_content = """
    <html>
    <head>
        <title>TI SCI Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            h1 { color: #003366; text-align: center;}
            h2 { color: #005599; margin-top: 30px; }
            .section { background: #fff; padding: 15px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0px 2px 6px rgba(0,0,0,0.1); }
            ul { margin: 0; padding-left: 20px; }
            li { margin-bottom: 5px; }
            .highlight { font-weight: bold; color: #cc0000; }
        </style>
    </head>
    <body>
        <h1>TI SCI - Texas Instruments Supply Chain IntelliSense</h1>
    """

    # -------------------
    # Demand Forecast
    # -------------------
    demand = report.get("demand_forecast", {}).get("Time_Series_Analysis", {})
    html_content += '<div class="section">'
    html_content += "<h2>📊 Demand Forecast → “How much will customers need?”</h2>"
    html_content += f"<p><b>Forecast Summary:</b> {demand.get('forecast_summary','')}</p>"
    if "risk_factors" in demand:
        html_content += "<p><b>Risk Factors:</b></p><ul>"
        for rf in demand["risk_factors"]:
            html_content += f"<li>{rf}</li>"
        html_content += "</ul>"
    html_content += f"<p><b>Recommendation:</b> {demand.get('recommendation','')}</p>"
    html_content += "</div>"

    # -------------------
    # Supplier Summary
    # -------------------
    supplier = report.get("supplier_summary", {}).get("Supplier_Summary", {})
    html_content += '<div class="section">'
    html_content += "<h2>🏭 Supplier Summary → “Can our suppliers deliver what’s needed?”</h2>"

    if "delayed_suppliers" in supplier:
        html_content += "<p><b>Delayed Suppliers:</b></p><ul>"
        for d in supplier["delayed_suppliers"]:
            html_content += f"<li>{d['name']} - {d['issue']} ({d['impact']})</li>"
        html_content += "</ul>"

    if "on_track_suppliers" in supplier:
        html_content += "<p><b>On-Track Suppliers:</b></p><ul>"
        for o in supplier["on_track_suppliers"]:
            html_content += f"<li>{o['name']} - {o['status']}</li>"
        html_content += "</ul>"

    html_content += f"<p><b>Overall Assessment:</b> {supplier.get('overall_assessment','')}</p>"
    html_content += "</div>"

    # -------------------
    # Logistics Alerts
    # -------------------
    logistics = report.get("logistics_alerts", {}).get("Logistics_Alerts", {})
    html_content += '<div class="section">'
    html_content += "<h2>🚛 Logistics Alerts → “Can the goods move through the chain on time?”</h2>"

    if "critical_disruptions" in logistics:
        html_content += "<p><b>Critical Disruptions:</b></p><ul>"
        for c in logistics["critical_disruptions"]:
            html_content += f"<li class='highlight'>{c}</li>"
        html_content += "</ul>"

    if "positive_updates" in logistics:
        html_content += "<p><b>Positive Updates:</b></p><ul>"
        for p in logistics["positive_updates"]:
            html_content += f"<li>{p}</li>"
        html_content += "</ul>"

    html_content += f"<p><b>Recommendation:</b> {logistics.get('recommendation','')}</p>"
    html_content += "</div>"

    # -------------------
    # Inventory Optimization
    # -------------------
    inventory = report.get("inventory_optimization", {}).get("Inventory_Optimization", {})
    html_content += '<div class="section">'
    html_content += "<h2>📦 Inventory Optimization → “What stock actions do we take right now?”</h2>"

    if "understocked_products" in inventory:
        html_content += "<p><b>Understocked Products:</b></p><ul>"
        for u in inventory["understocked_products"]:
            html_content += f"<li>{u['name']} - Stock: {u['current_stock']}, Weekly Consumption: {u['avg_weekly_consumption']}, Reorder: {u['recommended_reorder']} ({u['action']})</li>"
        html_content += "</ul>"

    if "overstocked_products" in inventory:
        html_content += "<p><b>Overstocked Products:</b></p><ul>"
        for o in inventory["overstocked_products"]:
            html_content += f"<li>{o['name']} - Stock: {o['current_stock']}, Weekly Consumption: {o['avg_weekly_consumption']}, Excess: {o['excess_units']} ({o['action']})</li>"
        html_content += "</ul>"

    html_content += f"<p><b>Overall Inventory Health:</b> {inventory.get('overall_inventory_health','')}</p>"
    html_content += "</div>"

    # -------------------
    # Close HTML
    # -------------------
    html_content += """
    </body>
    </html>
    """

    with open(OUTPUT_HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[INFO] HTML report saved to {OUTPUT_HTML_FILE}")


generate_html_from_json(input_file=OUTPUT_JSON_FILE)