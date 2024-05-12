import tkinter as tk

def getIntro(name, gender, age, position, cabin, children, parents, sibling, crew_pos):
    parentString = "0"
    sibString = "0"
    outString = "0"
    kidString = "0"
    positionString = "0"

    StartString = " Welcome to the Titanic! Your name is " + name + " and you are a " + age + " year old " + gender + ", excited for the journey ahead. \n" \
                  " As you walk toward the wonderful ship you can't help but gaze at the massive ship that you will soon board. \n" \
                  " You feel overjoyed being able to go on such a ship for its maiden voyage"

    if int(parents) == 1:
        parentString = " with one of you parents"
    elif int(parents) == 2:
        parentString = " with your parents"
    else:
        parentString = ""

    if int(sibling) > 0 and int(parents) > 0:
        sibString = " and your siblings"
    elif int(sibling) > 0:
        sibString = " with your siblings"
    else:
        sibString = ""

    if int(children) == 1 and int(parents) > 0 or int(children) == 1 and int(sibling) > 0:
        kidString = " and your child."
    elif int(children) == 1:
        kidString = " with your child."
    elif int(children) > 1 and int(parents) > 0 or int(children) > 1 and int(sibling) > 0:
        kidString = " and children."
    elif int(children) > 1:
        kidString = " with your children."
    else:
        kidString = ""

    if int(parents) > 1 and int(sibling) == 0 and int(children) == 0:
        parentString += "."

    if int(parents) == 0 and int(sibling) == 0 and int(children) == 0:
        StartString += "."

    if int(sibling) > 1 and int(children) == 0:
        sibString += "."

    if position == "Passenger":
        positionString = "\n \nAs a passenger of the Titanic, you look forward to a relaxing journey with no issues whatsoever." \
                         "\nRight when you are done thinking, you reach the line to board the ship." \
                         "\nAfter a very long wait, you finally set you feet on the Titanic." \
                         "\nYou decide to go to your " + cabin  + " cabin to rest for the time being. " \
                         "\nAs you enter your cabin you drop your things and go straight to your bed, exhausted." \
                         "\nYou decide to take a nap. After all, nothing bad can happen on this monster of a ship." \
                         "\nAs you drift to sleep, you dream of ice cold cocktails and a nice dip in the sea."

    if position == "Crew":
        positionString = "\n \nAs a member of the "+ crew_pos +  " crew on the Titanic, you are a little worried about this journey." \
                         "\nBut as you reach the boarding site for crew members, you realize that your worries are unfounded." \
                         "\nAfter all, this beast of a ship is practically unsinkable. The only issue would be the passengers if they got too rowdy." \
                         "\nYou walk toward the boarding ramp, getting in line to board the vessel." \
                         "\nAfter a short wait you set foot on ship and head to the crew quarters where you will be staying for the time being." \
                         "\nWhen you reach there you set your stuff down and mentally prepare for the sudden influx of passengers that will soon board." \
                         "\nYou are thankful that passengers do not board until tomorrow, and have the evening to prepare." \
                         "\nYou decide to go to bed early, to properly prepare for the coming voyage." \
                         "\nAs you drift to sleep, you dream of ice cold cocktails and a nice dip in the sea."

    outString = StartString + parentString + sibString + kidString + positionString

    return outString

def update_ui(selection):
    if selection == "Passenger":
        cabin_menu.grid(row=5, column=1, sticky="w")
        siblings_entry.grid(row=6, column=1)
        children_entry.grid(row=7, column=1)
        parents_entry.grid(row=8, column=1)
        crew_pos_menu.grid_remove()
    elif selection == "Crew":
        cabin_menu.grid_remove()
        siblings_entry.grid_remove()
        children_entry.grid_remove()
        parents_entry.grid_remove()
        crew_pos_menu.grid(row=5, column=1, sticky="w")
    else:
        cabin_menu.grid_remove()
        siblings_entry.grid_remove()
        children_entry.grid_remove()
        parents_entry.grid_remove()
        crew_pos_menu.grid_remove()

def submit_persona():
    name = name_entry.get()
    gender = gender_var.get()
    age = age_entry.get()
    passenger_crew = passenger_crew_var.get()
    crew_pos = crew_pos_var.get()
    cabin = cabin_var.get()
    siblings = siblings_entry.get()
    children = children_entry.get()
    parents = parents_entry.get()

    intro = getIntro(name, gender, age, passenger_crew, cabin, children, parents, siblings, crew_pos)
    print(intro)

# Create main window
root = tk.Tk()
root.title("Titanic Survival Simulator")

# Labels
tk.Label(root, text="Name:").grid(row=0, column=0, sticky="w")
tk.Label(root, text="Gender:").grid(row=1, column=0, sticky="w")
tk.Label(root, text="Age:").grid(row=2, column=0, sticky="w")
tk.Label(root, text="Passenger vs. Crew:").grid(row=3, column=0, sticky="w")
tk.Label(root, text="Crew Position:").grid(row=4, column=0, sticky="w")
tk.Label(root, text="Cabin:").grid(row=5, column=0, sticky="w")
tk.Label(root, text="Number of Siblings Aboard:").grid(row=6, column=0, sticky="w")
tk.Label(root, text="Number of Children Aboard:").grid(row=7, column=0, sticky="w")
tk.Label(root, text="Number of Parents Aboard:").grid(row=8, column=0, sticky="w")

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
passenger_crew_menu = tk.OptionMenu(root, passenger_crew_var, "Passenger", "Crew", command=update_ui)
passenger_crew_menu.grid(row=3, column=1, sticky="w")

crew_pos_var = tk.StringVar()
crew_pos_var.set("Restaurant Staff")
crew_pos_menu = tk.OptionMenu(root, crew_pos_var, "Restaurant Staff", "Engineering Crew", "Deck Hand", "Victualling")
crew_pos_menu.grid(row=4, column=1, sticky="w")

cabin_var = tk.StringVar()
cabin_var.set("First Class")  # Default value
cabin_menu = tk.OptionMenu(root, cabin_var, "First Class", "Second Class", "Third Class")
cabin_menu.grid(row=5, column=1, sticky="w")

siblings_entry = tk.Entry(root)
siblings_entry.grid(row=6, column=1)

children_entry = tk.Entry(root)
children_entry.grid(row=7, column=1)

parents_entry = tk.Entry(root)
parents_entry.grid(row=8, column=1)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_persona)
submit_button.grid(row=9, columnspan=2)

root.mainloop()
