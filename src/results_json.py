import os
import json
from serise_json import Series

# Read configuration (assumes configMod.json exists with appropriate settings)
import json
with open("configMod.json", "r") as f:
    config = json.load(f)
print("Config type:", type(config))
print("Config content:", config)
pyFile, QEfile = config["pyFile"], config["QEfile"]

# Create necessary directories if they don't exist
dirs = ("Icicle", "shortCourse1", "shortCourse2", "shortCourse3", "shortCourse4",
        "fastnet", "portland", "rockall", "houghton", "caulcott", "Watts", "blackaby", "wednesday", "Autumn")
for d in dirs:
    if d not in os.listdir():
        os.mkdir(d)

# Example: generating JSON for the "Icicle" series
series = Series(pyFile, "2025_QE_JAN.txt", {"Icicle"}, "Icicle")
# Optionally, you can apply filters such as:
# series.filterByBoatType("M") or series.filterByBoatType("C")

# Generate the JSON data structure
json_data = series.generateJSONResults()

# Write the JSON data to a file
with open("Icicle_seriesResults.json", "w") as out:
    json.dump(json_data, out, indent=4)

print("JSON output generated: Icicle_seriesResults.json")
