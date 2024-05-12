import tkinter as tk

def update_ui(selection):
    if selection == "Passenger":
        cabin_menu.grid(row=4, column=1, sticky="w")
        siblings_entry.grid(row=5, column=1)
        children_entry.grid(row=6, column=1)
        parents_entry.grid(row=7, column=1)
    else:
        cabin_menu.grid_remove()
        siblings_entry.grid_remove()
        children_entry.grid_remove()
        parents_entry.grid_remove()

def submit_persona():
    name = name_entry.get()
    gender = gender_var.get()
    age = age_entry.get()
    passenger_crew = passenger_crew_var.get()
    cabin = cabin_var.get()
    siblings = siblings_entry.get()
    children = children_entry.get()
    parents = parents_entry.get()

    # Example usage
    # Do something with the persona data (e.g., print it)
    print("Name:", name)
    print("Gender:", gender)
    print("Age:", age)
    print("Passenger vs. Crew:", passenger_crew)
    print("Cabin:", cabin)
    print("Number of Siblings Aboard:", siblings)
    print("Number of Children Aboard:", children)
    print("Number of Parents Aboard:", parents)

# Create main window
root = tk.Tk()
root.title("Titanic Survival Simulator")

# Labels
tk.Label(root, text="Name:").grid(row=0, column=0, sticky="w")
tk.Label(root, text="Gender:").grid(row=1, column=0, sticky="w")
tk.Label(root, text="Age:").grid(row=2, column=0, sticky="w")
tk.Label(root, text="Passenger vs. Crew:").grid(row=3, column=0, sticky="w")
tk.Label(root, text="Cabin:").grid(row=4, column=0, sticky="w")
tk.Label(root, text="Number of Siblings Aboard:").grid(row=5, column=0, sticky="w")
tk.Label(root, text="Number of Children Aboard:").grid(row=6, column=0, sticky="w")
tk.Label(root, text="Number of Parents Aboard:").grid(row=7, column=0, sticky="w")

# Entry fields
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

gender_var = tk.StringVar()
gender_var.set("Male")  # Default value
gender_menu = tk.OptionMenu(root, gender_var, "Male", "Female")
gender_menu.grid(row=1, column=1, sticky="w")

age_entry = tk.Entry(root)
age_entry.grid(row=2, column=1)

passenger_crew_var = tk.StringVar()
passenger_crew_var.set("Passenger")  # Default value
passenger_crew_menu = tk.OptionMenu(root, passenger_crew_var, "Passenger", "Restaurant Staff", "Engineering Crew", "Deck Hand", "Victualling", command=update_ui)
passenger_crew_menu.grid(row=3, column=1, sticky="w")

cabin_var = tk.StringVar()
cabin_var.set("First Class")  # Default value
cabin_menu = tk.OptionMenu(root, cabin_var, "First Class", "Second Class", "Third Class")
siblings_entry = tk.Entry(root)
children_entry = tk.Entry(root)
parents_entry = tk.Entry(root)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_persona)
submit_button.grid(row=8, columnspan=2)

root.mainloop()
