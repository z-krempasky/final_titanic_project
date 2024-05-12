import tkinter as tk
import tensorflow as tf
import numpy as np
import sys

def loadModel():
    # Load Crew Model
    try:
        crew_model = tf.keras.models.load_model("./models/crew_dataset.keras")
        print("Crew Model loaded successfully.")
    except Exception as e:
        print("Error loading crew model:", e)
        sys.exit(1)

    # Load Passenger Model
    try:
        passenger_model = tf.keras.models.load_model("./models/passenger_dataset.keras")
        print("Passenger Model loaded successfully.")
    except Exception as e:
        print("Error loading passenger model:", e)
        sys.exit(1)

    # Return Models
    return passenger_model, crew_model

def executeModel(p_model, c_model, gender, age, passenger_crew, class_type, children, parents, siblings, crew_pos):
    # Format Inputs
    # Gender
    if (gender == 'Male'):
        gender = 0
    else:
        gender = 1
    
    # Class Type
    if (class_type == "First Class"):
        class_type = 1
    elif (class_type == "Second Class"):
        class_type = 2
    else: #Third Class
        class_type = 3

    # Crew Type
    if (crew_pos == "Deck Hand"):
        crew_pos = 0
    elif (crew_pos == "Engineering Crew"):
        crew_pos = 1
    elif (crew_pos == "Restaurant Staff"):
        crew_pos = 2
    else: #Vict...
        crew_pos = 3

    # Combine/Convert Parents/Children
    parents = int(parents) + int(children)

    # Convert Siblings/Spouses
    siblings = int(siblings)

    # Convert Age
    age = float(age)

    # Passenger Model
    if (passenger_crew == "Passenger"):
        # Assemble Data
        data = np.array([[class_type, gender, age, siblings, parents, 25, 0]])
        # Make Predictions
        try:
            prediction = p_model.predict(data, verbose=0)
            print("**********Prediction:", prediction)
        except Exception as e:
            print("Error making predictions:", e)
            sys.exit(1)

    else: # Crew Model
        # Assemble Data
        data = np.array([[gender, age, crew_pos, 0]])
        # Make Predictions
        try:
            prediction = c_model.predict(data)
            print("**********Prediction:", prediction)
        except Exception as e:
            print("Error making predictions:", e)
            sys.exit(1)

    return round(prediction[0][0])

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

def getOutro(name, gender, cabin, age, siblings, children, status, passenger_crew, crew_pos):
    if status==0 and gender=="Male":
        endString="On the fateful night of April 14, 1912, aboard the RMS Titanic, tragedy struck in the frigid waters of the North Atlantic. Among the countless heartbreaking stories, one recounts the demise of a young man named"+name+". "+name+", a "+cabin+" passenger on the ill-fated vessel, found himself amidst chaos and panic as the ship collided with an iceberg. Despite valiant efforts by crew members to launch lifeboats, there simply weren't enough for all aboard."+name+", like many others, faced the grim reality of the limited supply of life-saving flotation devices. In the chaos that ensued, he struggled against the surging crowds, desperately seeking a means of escape. Tragically, "+name+" succumbed to the freezing waters before he could secure a place in a lifeboat, becoming one of the many victims of the Titanic disaster whose stories echo through history with profound sorrow."
    elif status==0 and gender=="Male" and cabin=="First Class" and children>0:
        endstring="Among the opulent corridors and lavish salons of the RMS Titanic, the demise of a wealthy magnate named " +name+ " unfolded in the early hours of April 15, 1912. As a "+cabin+"-class passenger, "+name+" enjoyed the luxuries afforded by his wealth, but even his privilege couldn't shield him from the cruel hand of fate. When the ship struck the iceberg, chaos ensued, and "+name+" found himself amidst a frenzy of panicked passengers scrambling for safety. Despite his affluence, the scarcity of lifeboats proved a harsh reality. Determined to secure a place for himself and his loved ones, "+name+" bravely attempted to navigate the chaos. However, in the frantic scramble, fate dealt its cruel blow, and "+name+", unable to find a place on a lifeboat, succumbed to the icy waters of the Atlantic. His untimely demise serves as a poignant reminder that in the face of nature's wrath, wealth offers no immunity, and tragedy spares no one."
    elif status==0 and gender=="Female" and passenger_crew=="Crew" and crew_pos=="Deck Hand":
        endstring="Amidst the bustling decks and diligent work of the crew aboard the RMS Titanic, the tragic fate of a dedicated steward named "+name+" unfolded on the fateful night of April 14, 1912. As an integral part of the ship's service staff, "+name+" took pride in her duties, ensuring the comfort and safety of the passengers in her care. When the unthinkable occurred and the Titanic struck an iceberg, "+name+" professionalism and composure were put to the ultimate test. Amidst the chaos and panic that ensued, "+name+" tirelessly assisted passengers, guiding them to safety and offering reassurance in the face of impending disaster. Despite her selfless efforts, the limited availability of lifeboats proved insurmountable. In a heart-wrenching moment, "+name+" made the ultimate sacrifice, relinquishing her chance of survival to ensure the safety of others. Her unwavering dedication and bravery in the face of adversity stand as a testament to the heroism of the crew who faced unimaginable challenges that fateful night."
    elif status==0 and gender=="Male" and children>0 and cabin !="First Class":
        endString="On the ill-fated voyage of the RMS Titanic, the heartbreaking tale of a devoted father named "+name+" unfolded amidst the chaos of April 14, 1912. As a passenger in "+cabin+" class, "+name+" cherished the journey with his beloved daughter, Sarah, holding onto dreams of a brighter future awaiting them in America. When the ship struck an iceberg, panic seized the decks, and "+name+"'s instincts shifted to protecting his precious child. Amidst the clamor for lifeboats, "+name+"'s unwavering focus remained on securing a place for Sarah, sacrificing his own safety without hesitation. With stoic resolve, he clung to hope, comforting Sarah with promises of rescue even as the icy waters crept closer. In a heart-wrenching moment of farewell, "+name+" ensured Sarah's place in a lifeboat, whispering words of love and encouragement before bidding her farewell. His final act of paternal love, etched in the annals of history, serves as a poignant reminder of the enduring strength and sacrifice of a father's love."
    elif status==1 and gender=="Female" and children==1:
        endString="In the annals of the RMS Titanic's tragic voyage, the poignant story of a resilient woman named "+name+" emerges, her life entwined with the harrowing events of April 14, 1912. As a passenger in "+cabin+" class, "+name+" embarked on the journey with aspirations of a new beginning in the New World. Yet, when the ship collided with an iceberg, her dreams were shattered amidst the chaos that ensued. With courage and determination, "+name+" navigated the pandemonium, her maternal instincts propelling her to safeguard her young daughter, Amelia. Amidst the scramble for lifeboats, "+name+"'s unwavering resolve to protect her child remained steadfast. In a tender display of maternal sacrifice, she ensured Amelia's safety, whispering words of comfort and love before bidding her farewell. Eleanor's unwavering strength in the face of adversity, and her ultimate sacrifice, embody the resilience and love of a mother living amidst the unforgiving waves of fate."
    elif status==1 and gender=="Male" and age<=10:
        endString="In the shadow of the RMS Titanic's tragic voyage, the tender tale of a young boy named "+name+" unfolds amidst the tumult of April 14, 1912. As a wide-eyed passenger in "+cabin+" class, Thomas embarked on the oceanic journey with a sense of wonder and anticipation, eager for the adventures that awaited in America. Yet, when the colossal ship collided with an iceberg, his innocence collided with the harsh reality of disaster. Amidst the frenzy that consumed the decks, "+name+" clung to his father's hand, his small frame enveloped by the chaos. With a child's resilience, he sought solace amidst the pandemonium, finding comfort in the embrace of his father's unwavering love. As lifeboats dwindled and desperation mounted, "+name+"'s father, with a heavy heart, lifted him into the safety of a departing vessel, his own fate sealed with a tender kiss and whispered promises of reunion. In the face of adversity, "+name+"'s innocent spirit and the enduring bond between father and son shine as beacons of hope amidst the darkness of tragedy."
    elif status==0 and siblings==1 and gender=="Female":
        endString="In the tragic narrative of the RMS Titanic's fateful voyage, the poignant bond between siblings, "+name+" and David, emerges as a testament to love and sacrifice amidst the turmoil of April 14, 1912. As passengers in "+cabin+" class, they embarked on the grand adventure with hearts full of excitement and anticipation. Yet, when the majestic vessel collided with an iceberg, their world was plunged into chaos and uncertainty. Amidst the frantic scramble for survival, "+name+"'s protective instinct surged forth, her arms encircling her younger brother, David, shielding him from the pandemonium that engulfed the decks. With courage born of sibling devotion, "+name+" guided David through the turmoil, offering words of reassurance and comfort as they faced the chilling waters together. As lifeboats dwindled and desperation loomed, "+name+" made the ultimate sacrifice, securing David's place on a departing vessel with a tearful embrace and whispered promises of safety. In the face of adversity, the enduring bond between "+name+" and David shines as a beacon of love amidst the darkness of tragedy, their intertwined fate a poignant reminder of the strength found in sibling solidarity."
    elif status ==0 and siblings==1 and gender=="Male":
        endString="In the tragic narrative of the RMS Titanic's fateful voyage, the poignant bond between siblings, Emma and "+name+", emerges as a testament to love and sacrifice amidst the turmoil of April 14, 1912. As passengers in "+cabin+" class, they embarked on the grand adventure with hearts full of excitement and anticipation. Yet, when the majestic vessel collided with an iceberg, their world was plunged into chaos and uncertainty. Amidst the frantic scramble for survival, Emma's protective instinct surged forth, her arms encircling her younger brother, "+name+", shielding him from the pandemonium that engulfed the decks. With courage born of sibling devotion, Emma guided "+name+" through the turmoil, offering words of reassurance and comfort as they faced the chilling waters together. As lifeboats dwindled and desperation loomed, Emma made the ultimate sacrifice, securing "+name+"'s place on a departing vessel with a tearful embrace and whispered promises of safety. In the face of adversity, the enduring bond between Emma and "+name+" shines as a beacon of love amidst the darkness of tragedy, their intertwined fate a poignant reminder of the strength found in sibling solidarity."
    elif status==0 and gender=="Male" and children==2:
        endString="Amidst the grandeur of the RMS Titanic's ill-fated voyage, the poignant story of a family unfolds, weaving a tapestry of love, sacrifice, and tragedy amidst the chaos of April 14, 1912. As passengers in "+cabin+" class, the family embarked on the journey with hearts full of hope and dreams for a brighter future in America. Yet, when the colossal ship struck an iceberg, their world was torn asunder by the cruel hand of fate. Amidst the turmoil that engulfed the decks, patriarch "+name+" stood as a beacon of strength, his unwavering resolve guiding his wife, Margaret, and their two children, Emily and James, through the tumultuous waters of despair. With courage born of familial love, the Hendersons clung to each other amidst the chaos, finding solace in their united bond amidst the uncertainty that loomed. As lifeboats dwindled and desperation mounted, John made the ultimate sacrifice, ensuring the safety of his beloved family before bidding them farewell with a tearful embrace and whispered promises of reunion. In the face of adversity, the enduring love and sacrifice of the family shine as a testament to the resilience of the human spirit amidst the darkest of nights, their intertwined fate etched forever in the annals of history."
    elif status==0 and gender=="Male" and crew_pos=="Engineering Crew":
        endString="In the somber chronicles of the RMS Titanic's tragic voyage, the unsung heroes of the crew, including Chief Engineer "+name+" and his dedicated team, faced a harrowing ordeal amidst the chaos of April 14, 1912. As custodians of the ship's mechanical heart, they labored tirelessly below deck, their expertise and dedication ensuring the vessel's smooth operation. Yet, when fate dealt its cruel blow and the Titanic collided with an iceberg, the crew found themselves thrust into a battle against nature's relentless fury. Amidst the deafening cacophony of collapsing bulkheads and rushing water, Chief Engineer "+name+" and his valiant comrades fought a desperate struggle to stem the tide of disaster. With selfless resolve, they toiled against impossible odds, sacrificing their own safety in a valiant attempt to safeguard the lives of those aboard. In their final moments, as the icy waters of the Atlantic claimed the mighty ship, the crew of the Titanic stood as silent sentinels of duty and honor, their unwavering sacrifice a poignant testament to the indomitable spirit of human resilience in the face of unimaginable tragedy."
    elif status==1 and gender=="Female" and children==2:
        endString="In the wake of an unexpected tragedy, "+name+" found herself grappling with the profound loss of her husband, Daniel, while nurturing their two young children, Emily and Liam. Though grief cast a shadow over their once vibrant home, "+name+"'s steadfast love and unwavering determination became the cornerstone of their resilience. With tender strength, she navigated the challenges of single parenthood, enveloping Emily and Liam in a cocoon of warmth and security. Together, they forged a bond strengthened by shared memories and the enduring legacy of Daniel's love. Though his absence left an ache in their hearts, "+name+"'s unwavering devotion ensured that their family remained united, their spirits buoyed by the unwavering belief that love transcends even the deepest of sorrows."
    elif status==0 and gender=="Male" and crew_pos=="Restaurant Staff":
        endString="Onboard the opulent Titanic, the culinary team of the renowned À La Carte Restaurant epitomized excellence and sophistication. Led by Chef "+name+", whose culinary creations were revered by passengers across all classes, and supported by servers like Marie and Jacques, the restaurant provided a sanctuary of culinary delight amidst the grandeur of the ship. However, tragedy struck on the night of April 14, 1912, when the Titanic collided with an iceberg. Despite their valiant efforts to maintain composure and assist passengers, Chef "+name+", Marie, Jacques, and several other members of the restaurant crew met their untimely demise as the ship descended into the icy depths of the Atlantic. Their loss cast a pall over the culinary world, their talents extinguished in the darkness of the ocean, leaving behind a legacy of culinary excellence and service that would forever be remembered."
    elif status==0 and crew_pos=="Deck Hand":
        endString="As the lifeblood of the Titanic's operations, the deck crew worked tirelessly under the guidance of Chief Officer "+name+", ensuring the safety and smooth operation of the vessel. From maintaining the ship's navigation to overseeing the loading of lifeboats, their dedication was unwavering. However, when disaster struck on the fateful night of April 14, 1912, and the Titanic collided with an iceberg, the deck crew found themselves facing an unprecedented crisis. Despite their heroic efforts to lower lifeboats and maintain order, many members of the deck crew, including himself, perished in the frigid waters of the Atlantic. Their selfless sacrifices and unwavering commitment to duty serve as a poignant reminder of the human toll of the Titanic tragedy."
    elif status==1 and crew_pos=="Deck Hand":
        endString="Amidst the chaos and tragedy of the Titanic's sinking, there emerged moments of heroism and survival, epitomized by the courageous actions of First Officer "+name+". As one of the highest-ranking officers onboard, "+name+" worked tirelessly to ensure the safety of passengers and crew. When the order came to abandon ship, they helped load lifeboats, ensuring women and children boarded first. As the ship plunged into darkness, “name” found themself clinging to the overturned collapsible lifeboat, battling the icy waters of the Atlantic. Miraculously, they were rescued hours later, one of the few crew members to survive the disaster. Lightoller's indomitable spirit and unwavering determination to survive serve as a testament to the resilience of the human spirit in the face of unimaginable adversity."
    elif status==1 and gender=="Female" and children==0:
        endString="Amidst the chaos and tragedy of the Titanic's sinking, there emerged stories of individual bravery and survival, including that of "+name+" a single woman traveling aboard the ill-fated vessel. Despite the overwhelming panic and confusion that ensued after the collision with the iceberg, "+name+" remained calm and resourceful. With quick thinking, she secured a spot in one of the last lifeboats, ensuring her own survival amidst the chaos. As the Titanic slipped beneath the waves, "+name+" watched in disbelief from the safety of the lifeboat, grappling with the enormity of the disaster that had unfolded before his eyes. Alone amidst the vast expanse of the Atlantic, "+name+"'s journey to safety became a testament to the resilience of the human spirit in the face of unimaginable tragedy."
    elif status==1:
        endString="Amidst the chaos and despair of the Titanic's sinking, "+name+", a young immigrant traveling in steerage, found clinging to a piece of debris amidst the frigid waters of the North Atlantic. Despite the overwhelming odds stacked against them, "+name+"'s will to survive burned fiercely within them. With each wave that crashed over them, they summoned the strength to keep her head above water, their determination unyielding against the chilling currents. In a stroke of luck, a passing lifeboat spotted them flailing form and pulled them to safety, offering a glimmer of hope amidst the darkness. "+name+"'s miraculous survival stands as a testament to the resilience of the human spirit in the face of unimaginable adversity."
    else:
        endString="Amidst the frantic chaos of the Titanic's sinking, the fate of young "+name+" remains a haunting reminder of the tragedy's human toll. As "+cabin+"-class passengers fought against the surging crowds, "+name+" found themself separated from their family, their desperate cries drowned out by the cacophony of panic. With no lifeline in sight, they braved the freezing waters alone, their strength faltering against the relentless current. In a heart-wrenching moment, "+name+" succumbed to the icy embrace of the Atlantic, their dreams of a new life extinguished beneath the waves. Their tragic demise stands as a somber testament to the indiscriminate cruelty of fate on that fateful night of April 14, 1912."

    return endString

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

    # Get Intro Text
    intro = getIntro(name, gender, age, passenger_crew, cabin, children, parents, siblings, crew_pos)
    print(intro)

    # Predict Survival
    p_model, c_model = loadModel()
    survived = executeModel(p_model, c_model, gender, age, passenger_crew, cabin, children, parents, siblings, crew_pos)

    # Get Outro Text
    outro=getOutro(name, gender, cabin, age, siblings, children, survived, passenger_crew, crew_pos)
    print(outro)

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
