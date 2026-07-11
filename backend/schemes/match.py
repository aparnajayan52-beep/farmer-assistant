"""
match.py — Module 2: Government Scheme Recommender
 
Reads data/schemes.csv and returns schemes matching a farmer's
state, crop, land size, and income category.
 
Note: "All India" schemes always match regardless of the farmer's state,
and "All Crops" schemes always match regardless of the farmer's crop.
"""
 
import os
import csv
 
SCHEMES_CSV_PATH = os.path.join("..", "data", "schemes.csv")
 
 
def load_schemes():
    """Reads schemes.csv into a list of dictionaries."""
    schemes = []
    if not os.path.exists(SCHEMES_CSV_PATH):
        print(f"WARNING: {SCHEMES_CSV_PATH} not found.")
        return schemes
 
    with open(SCHEMES_CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            schemes.append(row)
    return schemes
 
 
def get_eligible_schemes(state, crop, land_size_category="Any", income_category="All Farmers"):
    """
    Filters schemes based on farmer inputs.
    A scheme matches if:
      - its state is "All India" OR matches the farmer's state
      - its crop_type is "All Crops" OR matches the farmer's crop (case-insensitive)
      - its income_category is "All Farmers" OR matches the farmer's income category
    """
    schemes = load_schemes()
    matches = []
 
    for scheme in schemes:
        state_match = (
            scheme["state"] == "All India" or scheme["state"].lower() == state.lower()
        )
        crop_match = (
            scheme["crop_type"] == "All Crops" or scheme["crop_type"].lower() == crop.lower()
        )
        income_match = (
            scheme["income_category"] == "All Farmers"
            or scheme["income_category"].lower() == income_category.lower()
        )
 
        if state_match and crop_match and income_match:
            # Split the semicolon-separated documents list into a proper array
            scheme["documents_required"] = scheme["documents_required"].split(";")
            matches.append(scheme)
 
    return matches
 
 
if __name__ == "__main__":
    # Quick manual test
    results = get_eligible_schemes(
        state="Kerala",
        crop="Paddy",
        income_category="Small and Marginal Farmers"
    )
    print(f"Found {len(results)} matching schemes:\n")
    for s in results:
        print(f"- {s['scheme_name']}: {s['benefits']}")