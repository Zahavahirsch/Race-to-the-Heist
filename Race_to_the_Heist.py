#Game building begins here:
from tkinter import *
import random
import string



# Define the locations of the items
locations = {
    "Fire Place": (609, 717, 354, 452),
    "Footstep Painting": (624, 683, 195, 257),
    "Computer": (102, 228, 354, 423),
    "E": (588, 602, 284, 310),
    "Letters": (344, 385, 495, 529),
    "Dictionary": (3, 79, 498, 533),
    "Bottle": (340, 350, 361, 393),
    "Coins": (443, 470, 415, 431),
    "Magnifying Glass": (415, 458, 468, 482),
    "Phone": (51, 124, 451, 488),
    "Safe": (200, 245, 469, 577),
    "Calendar": (356, 390, 331, 358),
    "Door": (453, 560, 227, 425),
    "Chest": (784, 895, 409, 594)}



#CIPHER FUNCTIONS
#function to split input into 3 "equal" parts
def split_alphabet(alphabet):
    # Split the alphabet into 3 parts of equal length
    part_length = len(alphabet) // 3
    part1 = alphabet[:part_length+1]
    part2 = alphabet[part_length+1:2*part_length+1]
    part3 = alphabet[2*part_length+1:]

    # Return the parts
    return (alphabet, ''.join(part1), ''.join(part2), ''.join(part3))

#function to find unique letters in input
def unique(list1):
    unique_list = [] # initialize a null list
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            if x.isalpha():
                unique_list.append(x)
    return unique_list

#function to cipehr the input
def cipher(sentence):
    # Create a mapping of each letter to a random letter
    mapping = dict(zip(Real, random.sample(Real, len(Real))))
    
    # Cipher the sentence by replacing each letter with the corresponding mapped letter
    ciphered_sentence = ''.join([mapping.get(char.upper(), char) for char in sentence])
    return ciphered_sentence, mapping


#CHOOSE LANDMARK
#Extract landmark names from text file and choose landmark
with open('Landmark_names', 'r') as f:
    landmark_names = f.readlines()
    f.close()
landmark_names = [item.strip()for item in landmark_names]
#print(landmark_names[0])
num_landmarks = len(landmark_names)

#open the text file  
with open('Landmark_info.txt', 'r') as f: 
  #read the text file into a list of lines 
    lines = f.readlines() 
    f.close()
    
#loop through the lines in the text file and apply values to dict
landmark = {} #create an empty dictionary 
#[0] gives 1st coordiante, [1] gives 2nd coordinate, [2] gives NESW directions, [3] gives clue
for line in lines: 
    #split the line on ':' 
    key, value = line.split(':') 
    #strip the whitespace 
    key = key.strip() 
    value = value.strip() 
    #add the key, value pair to the dictionary 
    landmark[key] = value 
    landmark[key] = landmark[key].split(';')

#Choose a landmark at random and provide the clue:
val2 = random.randrange(0,num_landmarks)
chosen_landmark = landmark_names[val2]
landmark_clue = landmark[chosen_landmark][3]

#CIPHER THE LANDMARK CLUE
#find unique letters in landmark clue and only cipher those
unique_letters_landmark = unique(landmark_clue.upper())
# Shuffle the letters randomly
random.shuffle(unique_letters_landmark)
# Get real letters split into 3 parts
Real, Real1, Real2, Real3 = split_alphabet(unique_letters_landmark)
Real = list(Real)

#cipher the clue
ciphered_landmark, mapping = cipher(landmark_clue)

#Extract the cipher in correct order
Code = ""
for letter, cipher in mapping.items():
    Code += cipher
    
#Separate into similar groupings as Real
Code = list(Code)
Code, Code1, Code2, Code3 = split_alphabet(Code)
    


#Create text for chest no hints:
file1 = open('Riddles_chest_order.txt', 'r') #read mode
file2 = open('Riddles_chest.txt', 'w') #write mode
for line in file1:
    file2.write(line)
file2.write(ciphered_landmark)
file1.close()
file2.close()
with open('riddles_chest.txt', 'r') as f: 
  #read the text file into a list of lines 
    chest_text = f.read() 
    f.close()

#create text for chest with hints
file1 = open('Riddles_chest_hints_order.txt', 'r') #read mode
file2 = open('Riddles_chest_hints.txt', 'w') #write mode
for line in file1:
    file2.write(line)
file2.write(ciphered_landmark)
file1.close()
file2.close()
with open('riddles_chest_hints.txt', 'r') as f: 
  #read the text file into a list of lines 
    chest_hints_text = f.read() 
    f.close()



chest_key = False #chest_key stays false until the Safe code is cracked and the key is found

#function to handle the clicks of each individual item 
def handle_click(event):
    global chest_key
    # Loop through the locations and check if the click was within any of the item's coordinates
    for item, loc in locations.items():
        if loc[0] < event.x < loc[1] and loc[2] < event.y < loc[3]:
            #Create the popups with clues when items are clicked:
            clue_window = Toplevel(root)
            clue_window.geometry("325x200")
            clue_window.title(item)
    
            #Function to organize the popup label
            def clue_org(item, label_text):
                # Center the popup on the main window
                x = root.winfo_rootx() + root.winfo_width()//2 - clue_window.winfo_width()//2
                y = root.winfo_rooty() + root.winfo_height()//2 - clue_window.winfo_height()//2
                clue_window.geometry("+{}+{}".format(x, y))
            
                label = Label(clue_window, text=label_text, compound="top")
                label.pack(padx=10, pady=10)
            
            #function to Check if the inputted answer is correct
            def check_answer(item, popup_text, answer, wrong_text, correct_text): 
                global chest_key
                # Define a function to create and display the label
                def display_label(text):
                    # Remove any existing label in the window
                    for widget in clue_window.winfo_children():
                        widget.destroy()
                    # Create a new label with the given text and display it in the window
                    label = Label(clue_window, text=text, compound="top")
                    label.pack(padx=10, pady=10)
                    
                # Define a submit function
                def submit():
                    global chest_key
                    user_answer = input_answer.get() # Get the user's answer
                    if all(c.isalpha() or c.isspace() for c in user_answer): #Check that letters or spaces
                        user_answer = user_answer.lower()
                    # Check if the answer is correct
                    if answer not in user_answer:
                        text = wrong_text
                        label = Label(clue_window, text=text, compound="top")
                        label.pack(padx=10, pady=10)              
                    elif answer in user_answer:
                        text = correct_text
                        label = Label(clue_window, text=text, compound="top")
                        label.pack(padx=10, pady=10)
                        display_label(text)
                        if item == 'Safe': 
                            global chest_key
                            chest_key = True #Now the chest can be opened
                        elif item == "Door":
                            def quit_game():
                                root.destroy()
                            quit_button = Button(clue_window, text="Quit Game", command=quit_game)
                            quit_button.pack(pady=5)
                            
                
                label_text = popup_text
                clue_org(item, label_text)
        
                # Add an entry box for the player to input their answer
                input_answer = StringVar()
                entry = Entry(clue_window, textvariable=input_answer)
                entry.pack()
            
                # Add a submit button to save the answer   
                Button(clue_window, text="Submit", command=submit).pack()
               
    

            # FIND CLICKED ON OBJECT
            if item == "Fire Place":
                if chest_key ==True:
                    label_text = "There's some chalk writing by the FIRE!\nIt reads:\n\n"+Real1
                    clue_org(item, label_text)
                else:
                    label_text = "The FIRE is still going."
                    clue_org(item, label_text)
            elif item == "Coins":
                if chest_key == True:
                    label_text = "There's something etched under these COINS!\nIt reads:\n\n"+Real2
                    clue_org(item, label_text)
                else:
                    label_text = "Weird place to keep a pile of COINS."
                    clue_org(item, label_text)
            elif item == "Bottle":
                if chest_key == True:
                    label_text = "There's a rolled up note in this BOTTLE!\nIt reads:\n\n"+Real3
                    clue_org(item, label_text) 
                else:
                    label_text = "An old glass BOTTLE.\n\nLooks like there's some trash inside."
                    clue_org(item, label_text)
                   
            elif item == "Dictionary":
                check_answer(item,
                             "What word do you want to look up in the DICTIONARY?",
                             "today",
                             "There's nothing useful here.",
                             "There are numbers written in the margin!\nThey read:\n\n"+Code1)
            elif item == "Footstep Painting":
                if chest_key == True:
                    label_text = "There's some text written on the back of this painting of FOOTSTEPS!\nIt reads:\n\n"+Code2
                    clue_org(item, label_text)
                else:
                    label_text = "A painting of FOOTSSTEPS. \n\nInteresting..."
                    clue_org(item, label_text)
            elif item == "E":
                if chest_key == True:
                    label_text = "There is a ripped note under the E!\nIt reads:\n\n"+Code3
                    clue_org(item, label_text) 
                else:
                    label_text = "I wonder what E stands for."
                    clue_org(item, label_text)
     
            elif item == "Magnifying Glass":
                check_answer(item,
                             "What would you like to Magnify?",
                             "letters", 
                             "There was nothing to see.",
                             "Magnifying the letters reveals something:\n\nTo Decipher:\n1=5\n4=3\n2=6")
                
            elif item == "Letters":
                label_text = "There's something written, but it's too small to read."
                clue_org(item, label_text)
                
            elif item == "Computer":
                label_text = "There's a message open on the computer:\n\n\nAll info safely locked away\nCheck moon landing\nUnscramble then phone"
                clue_org(item, label_text)
                
            elif item == "Phone":
                # Load the phone image and display it in the popup
                clue_window.geometry("600x500")
                phone_image = PhotoImage(file="house phone.png").subsample(2,2)
                phone_label = Label(clue_window, image=phone_image)
                phone_label.image = phone_image # Keep a reference to the image to avoid garbage collection
                phone_label.pack()
                
            elif item == "Safe":
                chest_key = check_answer(item, 
                             "You need a passcode to open the safe:\n\n_ _ _ _",
                             "7587", 
                             "That passcode is incorrect", 
                             "Great job! You opened the safe!\n\n\nInside you found a key.")
                
                
            elif item == "Calendar":
                check_answer(item, 
                             "What date do you want to check?\n(mm/dd)",
                             "07/20", 
                             "No entry for this date",
                             "This date has an entry!\n\n1U79054\n57070L6\n9519735\n3P754S0\n\nWhat could this mean?")
            elif item == "Chest":
                if chest_key == True:
                    clue_window.geometry("600x400")
                    label_text = "You found a notebook!\nInside reads:\n\n\n"+chest_text
                    clue_org(item, label_text)
                    
                else:
                    label_text = "This chest is locked.\n\nYou need a key."
                    clue_org(item, label_text)
                
            
            elif item == "Door":
                    check_answer(item, 
                                "Where is the next heist going to be?",
                                 chosen_landmark,
                                "you call into headquarters,\nthat location is incorrect.",
                                "Great job!\nYou cracked the code!\n\nThere's not time to waste!\nTime to head to The "+chosen_landmark.capitalize()+"!")

                    
#CREATE INTRO STORY POPUP
def show_intro_popup():
    
    # create a popup window
    intro_popup = Toplevel(root)
    intro_popup.title("Race to the Heist")
    intro_popup.geometry("500x300")
    
    # Make the popup appear in front of the image
    intro_popup.attributes('-topmost', True)
    
    # Center the popup on the main window
    x = root.winfo_rootx() + root.winfo_width()//2 - intro_popup.winfo_width()//2
    y = root.winfo_rooty() + root.winfo_height()//2 - intro_popup.winfo_height()//2
    intro_popup.geometry("+{}+{}".format(x, y))
            
    # add a label to the popup
    label = Label(intro_popup, text="You're a world renowned thief\nYour identity is a secret\n\nEveryone refers to you as:\n\nName", compound='top')
    label.pack(padx=10, pady=10)
    
    # Add an entry box for the player to input their answer
    input_name = StringVar()
    name_entry = Entry(intro_popup, textvariable=input_name)
    name_entry.pack()
    
    label = Label(intro_popup, text="Pronouns\n(she, he, they)", compound='top')
    label.pack(padx=10, pady=10)
    
    input_pronoun = StringVar()
    pronoun_entry = Entry(intro_popup, textvariable=input_pronoun)
    pronoun_entry.pack()
    
    def name_submit():
        name_answer = input_name.get()
        pronoun_answer = input_pronoun.get()
        
        pronoun_dict = {'she':('her', 'her'), 'he':('him','his'), 'they':('them', 'their')}
        
        def display_label(text):
            # Remove any existing label in the window
            for widget in intro_popup.winfo_children():
                widget.destroy()
            # Create a new label with the given text and display it in the window
            intro_popup.geometry("550x500")
            label = Label(intro_popup, text=text, compound="top")
            label.pack(padx=10, pady=10)

        with open('Intro_story.txt', 'r') as f: 
          #read the text file into a list of lines 
            story_text = f.read() 
            f.close()
        
        #Replace input name in displayed text
        story_text = story_text.replace('NAME', name_answer.capitalize())
        #replace input pronouns in displayed text
        story_text = story_text.replace('THEY', pronoun_answer.lower())
        story_text = story_text.replace('THEM', pronoun_dict[pronoun_answer.lower()][0])
        story_text = story_text.replace('THEIR', pronoun_dict[pronoun_answer.lower()][1])
        
        #display story
        label = Label(intro_popup, text=story_text, compound="top")
        label.pack(padx=10, pady=10)
        display_label(story_text)
        
        # add a button to start the game
        start_button = Button(intro_popup, text="Start Game", command=intro_popup.destroy)
        start_button.pack(padx=10, pady=5)
        
    # Add a submit button to save the answer   
    Button(intro_popup, text="Submit Name", command=name_submit).pack()

    
    
#CREATE NOTEBOOK POPUP
def show_notebook():
    # create a notebook popup window
    notebook_popup = Toplevel(root)
    notebook_popup.title("Notebook")
    notebook_popup.geometry("400x400")
    
    # create a text widget for the notebook
    notebook_text = Text(notebook_popup)
    notebook_text.delete('1.0', END)  # Clear the text widget
    notebook_text.pack(fill="both", expand=True)
    
    # load saved notes if available
    try:
        with open("notebook.txt", "r") as f:
            notebook_text.insert("1.0", f.read())
    except FileNotFoundError:
        pass
    
    # save notes when window is closed
    def save_notes():
        with open("notebook.txt", "w") as f:
            f.write(notebook_text.get("1.0", "end"))
        notebook_popup.destroy()
    notebook_popup.protocol("WM_DELETE_WINDOW", save_notes)


def show_directions_popup():
    # create a popup window
    directions_popup = Toplevel(root)
    directions_popup.title("Race to the Heist")
    directions_popup.geometry("500x300")
    
    # Make the popup appear in front of the image
    directions_popup.attributes('-topmost', True)
    
    # Center the popup on the main window
    x = root.winfo_rootx() + root.winfo_width()//2 - directions_popup.winfo_width()//2
    y = root.winfo_rooty() + root.winfo_height()//2 - directions_popup.winfo_height()//2
    directions_popup.geometry("+{}+{}".format(x, y))
    
    #extract text from file:
    with open('Directions.txt', 'r') as f: 
          #read the text file into a list of lines 
            directions_text = f.read() 
            f.close()
            
    # add a label to the popup
    label = Label(directions_popup, text=directions_text, compound='top')
    label.pack(padx=10, pady=10)    

    
#MAIN GAME
# Define the main window
root = Tk()
root.title("Nightingale Study")
#root.attributes('-fullscreen', True)

#clear the notebook:
with open("notebook.txt", "w") as f:
    f.write("")
# create a button to show the notebook popup
notebook_button = Button(root, text="Notebook", command=show_notebook)
notebook_button.pack(padx=10, pady=10)

# Load the image
img = PhotoImage(file="Study room_additions.png")

# Add the image to a canvas
canvas = Canvas(root, width=img.width(), height=img.height())
canvas.image = img
canvas.pack()
canvas.create_image(0, 0, anchor=NW, image=img)

# Bind the canvas to the click event
canvas.bind("<Button-1>", handle_click)

#Intro story popup
show_intro_popup()

#Directions popup
show_directions_popup()

# Start the main loop
root.mainloop()
