from rustbca import *
import os
model = "ferum_nitriding_"

root = os.getcwd()
list = os.listdir(root)
trajectory_input = input("Build trajectory plot (Y/n): ").strip().lower()
user_input = input("Delete .output files (Y/n): ").strip().lower()

if trajectory_input == "y":
    print("--------Building trajectory plot----------")
    do_trajectory_plot(model)
    
if user_input == 'y':
    root = os.getcwd()
    list = os.listdir(root)
    for file in list:
         if file.endswith(".output"):
             os.remove(file)
            
else:
    print("Invalid input. Please enter 'Y' for Yes or 'n' for No.")
