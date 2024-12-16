import json
import os 

def forge_query(df):
    """
    Form a query using the faculty information
    """
    query = []
    for row in df.iterrows():
        row = row[1]
        first_name = row['First name']
        last_name = row['Last name']
        school = row['School']
        title = row['Title']
        department = row['Department/Unit']
        email = row['Email address']
        # Form the query
        single_query = f"{first_name} {last_name} emory"
        name = f"{first_name}-{last_name}"
        query.append((name, single_query))
    
    return query

def save_json(data, name, file_path='info'):
    """
    Save a JSON object to a local file.

    Parameters:
        data (dict or list): The JSON data to save.
        file_path (str): The path to the file where the JSON data will be saved.

    Returns:
        None
    """
    path = os.path.join(f"{file_path}", f"{name}.json")
    try:
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"JSON data successfully saved")
    except Exception as e:
        print(f"An error occurred while saving JSON to file: {e}")
