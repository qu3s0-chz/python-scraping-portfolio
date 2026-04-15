name = "Jesse"
city = "Ocala"
print(f"My name is {name} and I live in {city}")

businesses = ["Joe's HVAC", "Tampa Roofing Co", "Sunshine Plumbing"]
for business in businesses:
    print(business)

lead = {
    "name": "Joe's HVAC",
    "phone": "555-0101",
    "city": "Tampa"
}
print(lead["name"])
print(lead["phone"])

leads = [
    {"name": "Joe's HVAC", "phone": "555-0101", "city": "Tampa"},
    {"name": "Sunshine Plumbing", "phone": "555-0202", "city": "Orlando"},
]

for lead in leads:
    print(f"{lead['name']} - {lead['phone']} - {lead['city']}")

    import csv

leads = [
    {"name": "Joe's HVAC", "phone": "555-0101", "city": "Tampa"},
    {"name": "Sunshine Plumbing", "phone": "555-0202", "city": "Orlando"},
]

with open("leads.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "phone", "city"])
    writer.writeheader()
    writer.writerows(leads)

print("CSV saved!")