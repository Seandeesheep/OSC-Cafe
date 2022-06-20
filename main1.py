# 07/06/22

# modules
from tkinter import *
from PIL import Image, ImageTk
import os


# functions
def get_image(frame, bg, filepath, resize):
    """returns a working image label"""
    IMG = Image.open(filepath)
    image = ImageTk.PhotoImage(IMG.resize(resize))
    img_lbl = Label(frame, image=image, bg=bg)
    img_lbl.image = image
    return img_lbl


# supporting class
class Num:
    """this class is used for row and column gridding of the widgets"""
    def __init__(self):
        self.n = -1

    def call(self):
        self.n += 1
        return self.n

    def reset(self):
        self.n = -1


# main GUI class
class CustomerGUI:
    """this class runs the interface for customers to allow them to view, process, and purchase their order.
    the processed order will be transferred and stored in a separate file"""
    def __init__(self, parent):
        # initialising fonts and images
        BIG_FONT = ("Lato", 95, "bold")
        MED_FONT = ("Lato", 70, "bold")
        SMALL_FONT = ("Lato", 26, "bold")
        self.TINY_FONT = ("Lato", 14)

        # initialising data


        # initialing main variables
        self.screen = ""

        # initialising main frame
        main = Frame(parent, height=875, width=620, bg='purple')

        # initialising sub frames
        self.top_f = Frame(main, height=778, width=620, bg='white')
        self.bot_f = Frame(main, height=97, width=620, bg='black')

        # initialising home screen widgets
        self.home_wid = []
        self.home_wid.append(Label(self.top_f, text="Order\nHere", font=BIG_FONT, bg="white"))
        self.home_wid.append(get_image(self.top_f, 'white', 'assets/home_img.png', (485, 485)))
        self.home_wid.append(get_image(self.bot_f, 'black', 'assets/logo.png', (97, 97)))
        self.home_wid.append(Label(self.bot_f, text="Press Anywhere To Start", font=SMALL_FONT, padx=13, bg="black", fg="white"))

        # initialising menu screen widgets
        self.menu_wid = []
        self.menu_f1 = Label(self.top_f, height=52, width=15, bg='purple')
        self.menu_f2 = Label(self.top_f, height=52, width=68, bg='pink')
        self.menu_line = get_image(self.top_f, 'white', 'assets/line.png', (24, 782))
        self.menu_title = Label(self.menu_f2, text="Favourites", font=MED_FONT, bg='white', fg="orange")


        # frame gridding
        main.grid()
        self.top_f.grid(row=0)
        self.bot_f.grid(row=1)

        # screen initialisation
        self.home_screen()

    def start(self, event):
        """resets/configures the windows widget and starts a new screen according to the current screen"""
        if self.screen == 'home':
            self.forget_screen(self.home_wid)
            self.screen = 'menu_fav'
            self.menu_screen()

    def forget_screen(self, widgets):
        """forgets all the widgets on the window given the list of widgets"""
        for wid in widgets:
            wid.grid_forget()

    def home_screen(self):
        """grids all the home screen widgets"""
        self.screen = 'home'
        n = Num()
        for wid in self.home_wid[0:2]:
            wid.bind('<Button-1>', self.start)
            wid.grid(row=n.call(), ipadx=65, sticky=NSEW)
        n.reset()
        for wid in self.home_wid[2:]:
            wid.bind('<Button-1>', self.start)
            wid.grid(row=0, column=n.call(), ipadx=20)

    def card(self, img, title, price):
        """creates menu item cards"""
        card_frame = Frame(self.menu_f2)
        image = get_image(card_frame, 'white', img, (120, 120))
        title_label = Label(card_frame, text=title, bg='white', font=self.TINY_FONT)
        price_label = Label(card_frame, text=price, bg='white', font=self.TINY_FONT)
        image.grid(row=0)
        title_label.grid(row=1, sticky=W)
        price_label.grid(row=2, sticky=W)


    def menu_screen(self):
        n = Num()
        self.menu_wid.append(self.menu_f1)
        self.menu_f1.grid(row=0, column=n.call())
        self.menu_line.grid(row=0, column=n.call())
        self.menu_f2.grid(row=0, column=n.call())
        self.menu_title.grid(row=0, column=0, columnspan=2)


# mainloop
root = Tk()
CustomerGUI(root)
root.title("OSC Cafe")
root.resizable(0,0)
root.mainloop()
