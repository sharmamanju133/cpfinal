




#import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import os

# Constants for emission factors (kg CO2 per unit)
EMISSION_FACTORS = {
    'electricity': 0.7,  # per kWh
    'car': 0.21,         # per km
    'flights': 0.09,     # per km
    'waste': 1.2         # per kg
}

# Directory for storing reports
REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def calculate_emissions(data):
    """Calculates carbon emissions based on input data."""
    emissions = {}
    total_emissions = 0
    for category, value in data.items():
        emission = value * EMISSION_FACTORS.get(category, 0)
        emissions[category] = emission
        total_emissions += emission
    emissions['total'] = total_emissions
    return emissions

def generate_pdf_report(data, emissions, suggestions, filename):
    """Generates a PDF report with the given data and emissions."""
    file_path = os.path.join(REPORT_DIR, filename)
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(50, 750, "Carbon Footprint Report")
    c.drawString(50, 730, f"Electricity Usage: {data.get('electricity', 0)} kWh")
    c.drawString(50, 710, f"Car Travel: {data.get('car', 0)} km")
    c.drawString(50, 690, f"Flights: {data.get('flights', 0)} km")
    c.drawString(50, 670, f"Waste: {data.get('waste', 0)} kg")

    c.drawString(50, 650, "Emissions Summary (kg CO2):")
    c.drawString(50, 630, f"- Electricity: {emissions.get('electricity', 0):.2f}")
    c.drawString(50, 610, f"- Car Travel: {emissions.get('car', 0):.2f}")
    c.drawString(50, 590, f"- Flights: {emissions.get('flights', 0):.2f}")
    c.drawString(50, 570, f"- Waste: {emissions.get('waste', 0):.2f}")
    c.drawString(50, 550, f"Total Emissions: {emissions.get('total', 0):.2f} kg CO2")

    c.drawString(50, 530, "Suggestions:")
    for i, suggestion in enumerate(suggestions, start=1):
        c.drawString(50, 510 - (i * 20), f"- {suggestion}")

    c.save()
    print(f"Report saved to {file_path}")


def generate_emissions_chart(emissions, filename):
    """Generates a pie chart of emissions."""
    categories = list(emissions.keys())
    values = [emissions[cat] for cat in categories if cat != 'total']

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=categories[:-1], autopct='%1.1f%%', startangle=140)
    plt.title("Emissions Breakdown")
    chart_path = os.path.join(REPORT_DIR, filename)
    plt.savefig(chart_path)
    plt.close()
    print(f"Chart saved to {chart_path}")

def main():
    print("Welcome to the Carbon Footprint Monitoring Tool")

    try:
        data = {
            'electricity': float(input("Enter electricity usage (kWh): ")),
            'car': float(input("Enter car travel distance (km): ")),
            'flights': float(input("Enter flights distance (km): ")),
            'waste': float(input("Enter waste generated (kg): "))
        }

        # Validate inputs
        if any(value < 0 for value in data.values()):
            raise ValueError("All input values must be non-negative.")

        emissions = calculate_emissions(data)
        suggestions = [
            "Switch to renewable energy sources.",
            "Carpool or use public transport.",
            "Avoid unnecessary flights.",
            "Increase recycling efforts."
        ]

        generate_pdf_report(data, emissions, suggestions, "carbon_footprint_report.pdf")
        generate_emissions_chart(emissions, "carbon_footprint_chart.png")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()