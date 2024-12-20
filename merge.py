import os
import json
import pandas as pd
from glob import glob
from PIL import Image
import xlsxwriter

from PIL import Image

def normalize_image(image_path, width=200, height=200):
    # Attempt to open and re-save the image as PNG
    with Image.open(image_path) as img:
        # Convert image to a standard mode (e.g., "RGB")
        img = img.convert("RGB")
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        new_path = image_path.rsplit('.', 1)[0] + "_converted.png"
        img.save(new_path, format="PNG")
    return new_path

input_excel_path = "data/Unresponsive AI researchers list.xlsx"
info_dir = "info"
image_base_dir = "images"
output_excel_path = "final_output.xlsx"

def convert_webp_to_png(image_path):
    if image_path.lower().endswith('.webp'):
        png_path = image_path.rsplit(".", 1)[0] + ".png"
        with Image.open(image_path) as img:
            img.save(png_path, "PNG")
        os.remove(image_path)  # remove original webp file
        return png_path
    return image_path

# Read only the first_name and last_name
df = pd.read_excel(input_excel_path, usecols=["First name", "Last name"])

data_rows = []
for _, row in df.iterrows():
    first_name = row["First name"]
    last_name = row["Last name"]

    json_filename = f"{first_name}-{last_name}.json"
    json_path = os.path.join(info_dir, json_filename)
    if not os.path.exists(json_path):
        continue

    with open(json_path, 'r', encoding='utf-8') as f:
        person_info = json.load(f)

    # Find and possibly convert the image
    image_dir = os.path.join(image_base_dir, f"{first_name}-{last_name}")
    image_path = None
    if os.path.isdir(image_dir):
        image_files = glob(os.path.join(image_dir, "*"))
        if image_files:
            candidate = image_files[0]
            candidate = convert_webp_to_png(candidate)
            # Check if it's now supported (png or jpg)
            ext = os.path.splitext(candidate)[1].lower()
            if ext in [".png", ".jpg", ".jpeg"]:
                image_path = candidate

    person_info["image"] = image_path
    data_rows.append(person_info)

final_df = pd.DataFrame(data_rows)

# Write using xlsxwriter directly
workbook = xlsxwriter.Workbook(output_excel_path)
worksheet = workbook.add_worksheet()

# Write headers
for col_num, col_name in enumerate(final_df.columns):
    worksheet.write(0, col_num, col_name)

# Write data and insert images
for row_num, row_data in enumerate(final_df.itertuples(index=False), start=1):
    for col_num, value in enumerate(row_data):
        if final_df.columns[col_num] == 'image' and value and os.path.isfile(value):
            new_image_path = normalize_image(value)
            worksheet.insert_image(row_num, col_num, new_image_path)
        else:
            cell_value = value
            if isinstance(cell_value, list):
                cell_value = ", ".join([str(v) for v in cell_value])
            worksheet.write(row_num, col_num, cell_value if cell_value is not None else "")

workbook.close()

print("Done! Check the final_output.xlsx file.")
