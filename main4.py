# 11/06/22

# modules
from tkinter import *
from PIL import Image, ImageTk
import os


# functions
def getImage(frame, bg, filepath, resize):
    """returns a working image label"""
    IMG = Image.open(filepath)
    image = ImageTk.PhotoImage(IMG.resize(resize))
    img_lbl = Label(frame, image=image, bg=bg)
    img_lbl.image = image
    return img_lbl


class QuantityButton:
    """creates a scroll frame containing buttons that can flip through pages"""
    def __init__(self, master, typeface, size, width, func, var):
        # initialising widgets
        self.main = Frame(master, height=size, bg='white')
        l_btn = Button(self.main, text='<', font=typeface, height=size, width=size, bg='light gray', command=lambda: func(-1, var))
        n_lbl = Label(self.main, textvariable=var, font=typeface, height=size, width=width, bg='light gray')
        r_btn = Button(self.main, text='>', font=typeface, height=size, width=size, bg='light gray', command=lambda: func(1, var))

        # gridding onto frame
        l_btn.grid(row=0, column=0, padx=5, sticky=W)
        n_lbl.grid(row=0, column=1, padx=5)
        r_btn.grid(row=0, column=2, padx=5, sticky=E)

    def get_main(self):
        return self.main


def add(num, var):
    """command binding for the buttons in QuantityButton method; adds/subtract a value from the given variable"""
    var.set(var.get()+num)


# supporting class
class Num:
    """this class is used for row and column gridding of the widgets"""

    def __init__(self):
        self.rn = -1
        self.cn = -1

    def rcall(self):
        """call the row number"""
        self.rn += 1
        return self.rn

    def ccall(self):
        """call the column number"""
        self.cn += 1
        return self.cn

    def rreset(self):
        """reset row number"""
        self.rn = -1

    def creset(self):
        """reset column number"""
        self.cn = -1

    def reset(self):
        """reset everything"""
        self.rreset()
        self.creset()


# main GUI class
class CustomerGUI:
    """this class runs the interface for customers to allow them to view, process, and purchase their order.
    the processed order will be transferred and stored in a separate file"""

    def __init__(self, parent):
        # initialising fonts and images
        BIG_FONT = ("Lato", 95, "bold")
        self.MED_FONT = ("Lato", 65, "bold")
        self.SMALL_FONT = ("Lato", 26, "bold")
        self.SMALL_FONT1 = ("Lato", 24)
        self.SMALL_FONT2 = ("Lato", 15)
        self.TINY_FONT = ("Lato", 10)

        # initialising menu data
        self.ALL_MENU = Menu()
        self.current_menu_cards = []
        self.menu_cards = []

        # initialing main variables
        self.screen = ""

        # initialising main frame
        self.WIDTH = 620
        self.HEIGHT = 875
        main = Frame(parent, height=self.HEIGHT, width=self.WIDTH, bg='purple')

        # initialising sub frames
        self.top_f = Frame(main, height=778, width=620, bg='white')
        self.bot_f = Frame(main, height=97, width=620, bg='black')

        # initialising home screen widgets
        self.home_wid = []
        self.home_wid.append(Label(self.top_f, text="Order\nHere", font=BIG_FONT, bg="white"))
        self.home_wid.append(getImage(self.top_f, 'white', 'assets/home_img.png', (485, 485)))
        self.home_wid.append(getImage(self.bot_f, 'black', 'assets/logo.png', (97, 97)))
        self.home_wid.append(
            Label(self.bot_f, text="Press Anywhere To Start", font=self.SMALL_FONT, padx=13, bg="black", fg="white"))

        # initialising menu screen widgets
        self.menu_wid = []
        self.menu_f1 = Label(self.top_f, height=52, width=15, bg='purple')
        self.menu_f2 = Label(self.top_f, height=52, width=68, bg='pink')
        self.menu_line = getImage(self.top_f, 'white', 'assets/line.png', (24, 782))
        self.menu_title = Label(self.menu_f2, font=self.MED_FONT, bg='white', fg="orange", padx=18)

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

    def item_card(self, item):
        """creates menu item cards"""
        # initialising widgets
        card_frame = Frame(self.menu_f2, bg='white', borderwidth=2, relief=GROOVE)
        image = getImage(card_frame, 'white', item.image, (160, 160))
        title_label = Label(card_frame, text=item.title, bg='white', font=self.TINY_FONT)
        price_label = Label(card_frame, text=f"${item.price}", bg='white', font=self.TINY_FONT)

        # binding widgets
        card_frame.bind("<Button-1>", lambda event, i=item: self.order_popup(event, i))
        image.bind("<Button-1>", lambda event, i=item: self.order_popup(event, i))
        title_label.bind("<Button-1>", lambda event, i=item: self.order_popup(event, i))
        price_label.bind("<Button-1>", lambda event, i=item: self.order_popup(event, i))

        # gridding onto card frame
        image.grid(row=0, column=0, pady=5, padx=5)
        title_label.grid(row=1, column=0, pady=3, padx=5, sticky=W)
        price_label.grid(row=2, column=0, pady=3, padx=5, sticky=W)

        return card_frame

    def card_menu(self, menu):
        """creates a list of item cards"""
        self.menu_cards = []
        for item in menu:
            self.menu_cards.append(self.item_card(item))

    def home_screen(self):
        """grids all the home screen widgets"""
        self.screen = 'home'
        n = Num()
        for wid in self.home_wid[0:2]:
            wid.bind('<Button-1>', self.start)
            wid.grid(row=n.rcall(), ipadx=66, sticky=NSEW)
        n.reset()
        for wid in self.home_wid[2:]:
            wid.bind('<Button-1>', self.start)
            wid.grid(row=0, column=n.ccall(), ipadx=20)

    def menu_screen(self):
        """creates a menu screen"""
        n = Num()
        # initialising main frames and layout
        self.menu_wid.append(self.menu_f1)
        self.menu_f1.grid(row=0, column=0)
        self.menu_line.grid(row=0, column=1)
        self.menu_f2.grid(row=0, column=2)
        self.menu_title.grid(row=n.rcall(), column=n.ccall(), columnspan=2)

        # reconfiguring widgets
        if self.screen == 'menu_fav':
            self.menu_title.configure(text="Favourites")
            self.card_menu(self.ALL_MENU.fav_get())

        # gridding card widgets
        for card in self.menu_cards:
            if n.rn < 2:
                card.grid(row=n.rcall(), column=0, pady=25)
            else:
                card.grid(row=n.rcall() - 2, column=1, pady=25)

    def order_popup(self, event, item):
        """creates a popup window for adjusting quantity and confirm order from the item card selected"""
        # window geometry variables
        x = root.winfo_rootx() + int(round(self.WIDTH / 3))
        y = root.winfo_rooty() + int(round(self.HEIGHT / 3))

        # initialising window
        order_wn = Toplevel(root)
        order_wn.title("Order Window")
        order_wn.resizable(False, False)
        order_wn.geometry(f"+{x}+{y}")
        order_wn.overrideredirect(True)

        # quantity variable
        n = IntVar()
        n.set(0)

        # initialising widgets
        main = Frame(order_wn, width=200, height=100, bg='white')
        f1 = Frame(main, bg='white')

        title = Label(f1, text=item.title, font=self.SMALL_FONT, bg='white')
        quantity_lbl = Label(f1, text="Quantity", font=self.SMALL_FONT1, bg='white', borderwidth=1, relief=GROOVE, padx=25, pady=5)
        quantity_btn = QuantityButton(master=f1, typeface=self.SMALL_FONT2, size=1, width=10, func=add, var=n)

        # gridding widgets
        main.grid(sticky=NSEW)
        f1.grid(row=0)
        title.grid(row=0, column=0, padx=10, pady=15, sticky=NSEW)
        quantity_lbl.grid(row=1, column=0, padx=10, pady=15, sticky=NSEW)
        quantity_btn.get_main().grid(row=2, column=0)

        # run
        order_wn.grab_set()

    def _null(self):
        pass


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
