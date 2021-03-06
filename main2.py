# 08/06/22

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

        # initialising menu data
        self.ALL_MENU = Menu()
        self.FAV_ITEMS = self.ALL_MENU.fav_get()
        self.current_menu_cards = []

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

    @staticmethod
    def forget_screen(widgets):
        """forgets all the widgets on the window given the list of widgets"""
        for wid in widgets:
            wid.grid_forget()

    def start(self, event):
        """resets/configures the windows widget and starts a new screen according to the current screen"""
        if self.screen == 'home':
            self.forget_screen(self.home_wid)
            self.screen = 'menu_fav'
            self.menu_screen()

    def card(self, img, title, price):
        """creates menu item cards"""
        card_frame = Frame(self.menu_f2)
        image = get_image(card_frame, 'white', img, (120, 120))
        title_label = Label(card_frame, text=title, bg='white', font=self.TINY_FONT)
        price_label = Label(card_frame, text=price, bg='white', font=self.TINY_FONT)
        image.grid(row=0)
        title_label.grid(row=1, sticky=W)
        price_label.grid(row=2, sticky=W)
        return card_frame

    def card_menu(self, menu):
        """creates a list of item cards"""
        cards = []
        for item in menu:
            cards.append(self.card(item.image, item.title, item.price))


    def home_screen(self):
        """grids all the home screen widgets"""
        self.screen = 'home'
        n = Num()
        for wid in self.home_wid[0:2]:
            wid.bind('<Button-1>', self.start)
            wid.grid(row=n.call(), ipadx=66, sticky=NSEW)
        n.reset()
        for wid in self.home_wid[2:]:
            wid.bind('<Button-1>', self.start)
            wid.grid(row=0, column=n.call(), ipadx=20)

    def menu_screen(self):
        """creates a menu screen"""
        n = Num()
        # initialising main frames and layout
        self.menu_wid.append(self.menu_f1)
        self.menu_f1.grid(row=0, column=n.call())
        self.menu_line.grid(row=0, column=n.call())
        self.menu_f2.grid(row=0, column=n.call())

        # create menu grids
        self.menu_title.grid(row=0, column=0, columnspan=2)


class Menu:
    """a data class that compiles the information of each menu item"""
    def __init__(self):
        # all menu items
        BEEF_BURGER = MenuItem("Beef Burger", "assets/home_img.png", "14.99")
        MACNCHEESE = MenuItem("Mac 'n' Cheese", "assets/macncheese.png", "5.99")
        WEDGES = MenuItem("Wedges", "assets/wedges.png", "4.99")
        LATTE = MenuItem("Latte", "assets/latte.png", "3.99")

        # categorised menus
        self.fav_menu = [BEEF_BURGER, MACNCHEESE, WEDGES, LATTE]

    # categorised menu returning methods
    def fav_get(self):
        return self.fav_menu.copy()


class MenuItem:
    """an object class that stores/represents the information of a menu item"""
    def __init__(self, title, image, price):
        self.title = title
        self.image = image
        self.price = price



# mainloop
root = Tk()
CustomerGUI(root)
root.title("OSC Cafe")
root.resizable(False, False)
root.mainloop()
