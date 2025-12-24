# This code is used to generate the input data for .toml file for RustBCA simulation
# It should only be executed if you have .csv files in the folder Prepare_IEDF_array
# It should only be executed if you want to define the ion energied from custom IEDF distribution
# E = [{choices = [...], weights = [...]}]
# The console output will contain the arrays that need to be pasted in "choices" and "weights"

import numpy as np
import csv
import os

def extract_columns_from_csv(file_path, column):
    col1_data = []
    col2_data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            
            # Clean data by removing comment lines
            data_lines = []
            for line in file:
                # Remove leading/trailing whitespace and check for comment symbol '%'
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith('%'):
                    data_lines.append(stripped_line)
            
            # Process the cleaned data using the csv reader
            # We use a simple comma delimiter as is standard for CSV.
            reader = csv.reader(data_lines, delimiter=',')
            
            for row in reader:
                # Ensure the row has at least two columns and that the first two 
                # elements are not empty.
                if len(row) >= 2 and row[0].strip() and row[1].strip():
                    try:
                        # Convert the string data to floating-point numbers
                        val1 = float(row[0].strip())
                        val2 = float(row[1].strip())
                        
                        col1_data.append(val1)
                        col2_data.append(val2)
                        
                    except ValueError:
                        # Handle case where a data field cannot be converted to a number
                        print(f"Skipping row due to non-numeric data: {row}")
                        
        # 3. Convert the lists to numpy arrays
        # Note: numpy must be imported in the environment running this script.
        try:
            import numpy as np
            column1 = np.array(col1_data)
            quantity_array=np.array(col2_data)
            sum = np.sum(quantity_array)
            weight_array=quantity_array/sum
            energy_quantity=0
            for energy,quantity in  zip(column1, quantity_array):
                energy_quantity+=energy*quantity
            average_value=energy_quantity/np.sum(quantity_array)

            if column == 0:
                return column1
            if column == 1:
                return weight_array
            else:
                return average_value

        except ImportError:
            print("\nERROR: numpy is required for array creation but is not installed.")
            return col1_data
            
    except FileNotFoundError:
        print(f"\nERROR: File not found at path: {file_path}")
        return None, None
    except Exception as e:
        print(f"\nAn unexpected error occurred during file processing: {e}")
        return None, None

folder = os.getcwd()
for filename in os.listdir(folder):
      if filename.endswith(".csv"):
        file_path = os.path.join(folder, filename)
        print("Processing:", filename)
        rad_arr=extract_columns_from_csv(file_path,0)
        choices = extract_columns_from_csv(file_path,0).tolist()
        weights = extract_columns_from_csv(file_path,1).tolist()
        quantities = extract_columns_from_csv(file_path,2)
        print("PASTE THESE ARRAYS INTO .TOML")
        print("--------------choices---------------")
        print(choices)
        print("--------------weights---------------")
        print(weights)
        print("--------------AVERAGE ION ENERGY---------------")
        print(quantities)