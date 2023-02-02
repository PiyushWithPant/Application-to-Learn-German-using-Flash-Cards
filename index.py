from tkinter import *

import pandas

import random


card = {}
wordDictionary = {}
known = 0
unknown = 0

try:
    data = pandas.read_csv("wordsToLearn.csv")
    
except FileNotFoundError:
    originalData = pandas.read_csv("German200Words.csv")
    wordDictionary = originalData.to_dict(orient="records")
    
else:
    wordDictionary = data.to_dict(orient="records") # This will make it a list which will have the Dictionary


# the dictionary - the columns (german and english) have become the two keys and each of them stores a dictionary 
# that have all the words in their respective language. Each word is value associated with key as numbers

# print(wordDictionary["German"][0])

# but we need it to be like this {'german':'word', 'english':'word'}, that's why we used ORIENT
# print(wordDictionary)




BACKGROUND_COLOR = "#B1DDC6"

win = Tk()

win.title("Practice 200 most common German words")

win.config(padx=30, pady=30,bg=BACKGROUND_COLOR)



# To auto rotate cards

def flipCard():
    global card
    canvas.itemconfig(cardTitle ,text="English", fill="green")
    canvas.itemconfig(cardWord ,text=card["English"], fill="green")
    canvas.itemconfig(cardBackground ,image=imgBack)


timer = win.after(4000, func=flipCard)  # 4000 ms = 4 second



# Creating the canvas to put the card in
canvas = Canvas(height=540, width=850, bg=BACKGROUND_COLOR, highlightthickness=0)

# adding image to canvas
imgFront = PhotoImage(file="images/card_front.png")
imgBack = PhotoImage(file="images/card_back.png")
cardBackground = canvas.create_image(440,280,image=imgFront)
canvas.grid(row=0,column=0, columnspan=4)

# adding text
cardTitle = canvas.create_text(440,200,text="language", font=("Arial", 20, "italic"))
cardWord = canvas.create_text(440,300,text="WORD", font=("Arial", 40, "bold"))

cardDataRight = canvas.create_text(720, 500, text=known, font=("Arial",15, "bold"), fill="green")
cardDataWrong = canvas.create_text(140, 500, text=unknown, font=("Arial",15, "bold"), fill="red")


# Button

def nextCard():
    global card, timer
    win.after_cancel(timer)
    card = random.choice(wordDictionary)
    canvas.itemconfig(cardTitle, text="German", fill="dark green")
    canvas.itemconfig(cardWord, text= card["German"], fill="dark green")
    canvas.itemconfig(cardBackground ,image=imgFront)
    timer = win.after(3000, func=flipCard)  # 4000 ms = 4 second

def iDontKnow():
    global unknown
    unknown +=1
    canvas.itemconfig(cardDataWrong, text= unknown)
    pass
    nextCard()

def iKnowIt():
    global known
    known+=1
    canvas.itemconfig(cardDataRight, text= known)
    
    wordDictionary.remove(card)
    new = pandas.DataFrame(wordDictionary)
    new.to_csv("wordsToLearn.csv",index=False)
    nextCard()


    
    


wrongImg = PhotoImage(file="images/wrong.png")
wrongButton = Button(image=wrongImg, highlightthickness=0, command=iDontKnow)
wrongButton.grid(row=1,column=0)

rightImg = PhotoImage(file="images/right.png")
rightButton = Button(image=rightImg, highlightthickness=0, command=iKnowIt)
rightButton.grid(row=1,column=3)



nextCard()


win.mainloop()