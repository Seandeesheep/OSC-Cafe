# 13/06/22

# modules
from tkinter import *
from PIL import Image, ImageTk
import json


# supporting functions
def getImage(frame, bg, filepath, resize):
    """returns a working image label"""
    IMG = Image.open(filepath)
    image = ImageTk.PhotoImage(IMG.resize(resize))
    img_lbl = Label(frame, image=image, bg=bg)
    img_lbl.image = image
    return img_lbl


# supporting classes
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


# data encapsulation classes
class MenuItem:
    """an object class that stores/represents the information of a menu item"""
    def __init__(self, title, image, price):
        self.title = title
        self.image = image
        self.price = price


class Menu:
    """a data class that compiles the information of each menu item"""
    def __init__(self):
        # initialising menu file
        file = open("menu.json")
        self.DATA = json.load(file)

        # categorised menus
        self.FAV = [self.call("Beef Burger"), self.call("Mac 'n' Cheese"), self.call("Wedges"), self.call("Latte")]
        self.MAIN = [self.call("Beef Burger"), self.call("Mac 'n' Cheese"), self.call("Hotdog"), self.call("Chicken Katsu")]
        self.SIDES = [self.call("Wedges"), self.call("Nuggets"), self.call("Garden Salad"), self.call("Cookie")]
        self.DRINK = [self.call("Coke"), self.call("Lipton"), self.call("Bundaberg"), self.call("Latte")]

    def call(self, item):
        return MenuItem(self.DATA[item]["title"], self.DATA[item]["image"], self.DATA[item]["price"])

    def get(self):
        return dict(self.DATA).copy()

    # categorised menu returning methods
    def fav_get(self):
        return self.FAV.copy()

    def main_get(self):
        return self.MAIN.copy()

    def sides_get(self):
        return self.SIDES.copy()

    def drink_get(self):
        return self.DRINK.copy()


class Order:
    """encapsulates a customers order into a single object"""

    def __init__(self, items):
        self.items = items
        self.name = ""


class OrderData:
    """encapsulates all the customers order"""
    def __init__(self):
        self.orders = []


# supporting GUI class
class QuantityButton:
    """creates a scroll frame containing buttons that can flip through pages"""
    def __init__(self, master, typeface, size, width, func1, func2, var, bg):
        # initialising variables
        self.var = var
        self.func2 = func2
        if func1 == 'self.add':
            self.func1 = self.add
        else:
            func1 = self._null
        if func2 is None:
            self.func2 = self._null

        # initialising widgets
        self.main = Frame(master, height=size, bg=bg)
        self.l_btn = Button(self.main, text='<', font=typeface, height=size, width=size, bg='light gray',
                            command=lambda: [self.func1(-1), self.func2()], state=DISABLED)
        self.n_lbl = Label(self.main, textvariable=var, font=typeface, height=size, width=width, bg='light gray')
        self.r_btn = Button(self.main, text='>', font=typeface, height=size, width=size, bg='light gray',
                            command=lambda: [self.func1(1), self.func2()])

        # state check
        if var.get() >= 1:
            self.l_btn.configure(state=ACTIVE)

        # gridding onto frame
        self.l_btn.grid(row=0, column=0, padx=5, sticky=W)
        self.n_lbl.grid(row=0, column=1, padx=5)
        self.r_btn.grid(row=0, column=2, padx=5, sticky=E)

    def get_main(self):
        """returns the main widget"""
        return self.main

    def add(self, num):
        """command binding for the buttons in QuantityButton method; adds/subtract a value from the given variable"""
        self.var.set(self.var.get() + num)
        if self.var.get() < 1:
            self.l_btn.configure(state=DISABLED)
        elif self.var.get() == 1:
            self.l_btn.configure(state=ACTIVE)

    def _null(self):
        """an empty function that can be used when there are no command binding"""
        pass


class CategoryButton:
    """creates a category button for the menu screen of the main GUI class"""
    def __init__(self, master, item, title, typeface, command):
        # initialising variables
        self.category = item.title

        # initialising widgets
        self.main = Frame(master, bg='white', borderwidth=2, relief=GROOVE)
        image = getImage(self.main, 'white', item.image, (70, 70))
        name = Label(self.main, text=title, font=typeface, bg='white')

        # gridding widgets
        image.grid(row=0, padx=10, pady=3)
        name.grid(row=1, padx=3, pady=3)

        # event binding
        self.main.bind("<Button-1>", command)
        image.bind("<Button-1>", command)
        name.bind("<Button-1>", command)

    def get_main(self):
        """returns the widget"""
        return self.main

    def get_category(self):
        """returns the category name"""
        return self.category


class OrderItemCard:
    """creates cards of ordered items"""
    def __init__(self, master, font1, font2, item):
        # initialising menu data/variables
        self.DATA = Menu().get()
        self.n = IntVar()
        self.n.set(item[1])

        # initialising widgets
        self.main = Frame(master, bg='pink')
        image = getImage(self.main, 'white', self.DATA[item[0]]['image'], (80, 80))
        title = Label(self.main, text=item[0], bg='white', font=font1)
        price = Label(self.main, text=f"${self.DATA[item[0]]['price']}", bg='white', font=font1)
        card_spacer = Label(self.main, bg='red')
        quantity_btn = QuantityButton(self.main, typeface=font2, size=1, width=1, func1='self.add', func2=self.change, var=self.n, bg='white')

        # widget gridding
        image.grid(row=0, column=0, rowspan=2, padx=15, sticky=W)
        title.grid(row=0, column=1, sticky=W)
        price.grid(row=1, column=1, sticky=W)
        quantity_btn.get_main().grid(row=0, column=3, rowspan=2, padx=15, sticky=E)
        card_spacer.grid(row=3, column=0, columnspan=4, padx=255)

    def get_main(self):
        """returns the main frame widget"""
        return self.main

    def change(self):
        """changes the price and the button widget if the quantity is less than 1"""
        pass

# main GUI class
class CustomerGUI:
    """this class runs the interface for customers to allow them to view, process, and purchase their order.
    the processed order will be transferred and stored in a separate file"""

    def __init__(self, parent):
        # initialising fonts and images
        BIG_FONT = ("Lato", 90, "bold")
        self.MED_FONT = ("Lato", 65, "bold")
        self.MED_FONT1 = ("Lato", 36)
        self.SMALL_FONT = ("Lato", 26, "bold")
        self.SMALL_FONT1 = ("Lato", 24)
        self.SMALL_FONT2 = ("Lato", 15)
        self.SMALL_FONT3 = ("Lato", 18)
        self.SMALL_FONT4 = ("Lato", 14)
        self.TINY_FONT = ("Lato", 10)

        # initialising menu data
        self.ALL_MENU = Menu()
        self.current_menu_cards = []
        self.menu_cards = []

        # initialising order data class
        self.data = OrderData()
        self.current_order = []

        # initialising main variables
        self.screen = ""
        self.current_screen = ""

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
        self.menu_f1 = Label(self.top_f, height=52, width=15, bg='white')
        self.menu_f2 = Label(self.top_f, height=52, width=68, bg='white')
        self.menu_line = getImage(self.top_f, 'white', 'assets/line.png', (24, 782))
        self.menu_title = Label(self.menu_f2, font=self.MED_FONT, bg='white', fg="orange", padx=18)

        # initialising menu buttons
        self.red_btn_f = Frame(self.bot_f, bg='IndianRed3', padx=3, pady=3)
        self.red_btn = Button(self.red_btn_f, text='Cancel', font=self.SMALL_FONT1, bg='black',
                              fg='white', borderwidth=0, command=self.cancel_menu_popup)
        self.red_btn.grid(ipadx=25)

        self.green_btn_f = Frame(self.bot_f, bg='PaleGreen2', padx=3, pady=3)
        self.green_btn = Button(self.green_btn_f, text='Checkout', font=self.SMALL_FONT1, bg='black', fg='white',
                                borderwidth=0, command=self.checkout_screen, state=DISABLED)
        self.green_btn.grid(ipadx=5)

        self.menu_wid.append(self.menu_f1)
        self.menu_wid.append(self.menu_f2)
        self.menu_wid.append(self.menu_line)
        self.menu_wid.append(self.menu_title)
        self.menu_wid.append(self.red_btn_f)
        self.menu_wid.append(self.green_btn_f)

        # initialising menu category widgets
        self.cat_wid = []
        self.cat_wid.append(CategoryButton(self.menu_f1, item=self.ALL_MENU.fav_get()[0], title='Favourites', typeface=self.TINY_FONT,
                                           command=lambda event, screen="menu_fav": self.change_menu(event, screen)))
        self.cat_wid.append(CategoryButton(self.menu_f1, item=self.ALL_MENU.main_get()[2], title='Main', typeface=self.TINY_FONT,
                                           command=lambda event, screen="menu_main": self.change_menu(event, screen)))
        self.cat_wid.append(CategoryButton(self.menu_f1, item=self.ALL_MENU.sides_get()[2], title='Sides', typeface=self.TINY_FONT,
                                           command=lambda event, screen="menu_sides": self.change_menu(event, screen)))
        self.cat_wid.append(CategoryButton(self.menu_f1, item=self.ALL_MENU.drink_get()[0], title='Drinks', typeface=self.TINY_FONT,
                                           command=lambda event, screen="menu_drink": self.change_menu(event, screen)))

        # initialising checkout widgets/variables
        self.chkt_n = IntVar()

        self.chkt_wid = []
        self.chkt_wid.append(Label(self.top_f, font=self.MED_FONT, text='Your Order', bg='black', fg='white'))

        chkt_subtitle_f = Frame(self.top_f, bg='black')
        chkt_sub1_lbl = Label(chkt_subtitle_f, bg='white', text="Order Item List", font=self.TINY_FONT, borderwidth=2, relief=GROOVE)
        chkt_sub2_lbl = Label(chkt_subtitle_f, bg='white', text='Quantity', font=self.TINY_FONT, borderwidth=2, relief=GROOVE)
        chkt_sub1_lbl.grid(row=0, column=0, ipadx=100, padx=60)
        chkt_sub2_lbl.grid(row=0, column=1, ipadx=25, padx=60)

        self.chkt_wid.append(chkt_subtitle_f)
        self.chkt_wid.append(QuantityButton(self.top_f, typeface=self.SMALL_FONT2, size=1, width=1, func1='self.add', func2=None, var=self.chkt_n, bg='black').get_main())
        self.chkt_wid.append(getImage(self.top_f, 'black', 'assets/line2.png', (620, 10)))
        self.chkt_price = Label(self.top_f, bg='white', text="Total Price: $", font=self.SMALL_FONT)

        self.chkt_wid.append(self.chkt_price)

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
        """resets/configures the windows widget and starts a new screen according to the self.screen variable"""
        if self.screen == 'home':
            self.forget_screen(self.home_wid)
            self.screen = 'menu_fav'
            self.current_screen = 'menu_fav'
            self.menu_screen()

        if self.screen == 'return_home':
            self.forget_screen(self.menu_wid)
            self.screen = 'home'
            self.home_screen()

    def item_card(self, item):
        """creates menu item cards"""
        # initialising widgets
        main = Frame(self.menu_f2, bg='white', borderwidth=2, relief=GROOVE)
        image = getImage(main, 'white', item.image, (160, 160))
        title_label = Label(main, text=item.title, bg='white', font=self.TINY_FONT)
        price_label = Label(main, text=f"${item.price}", bg='white', font=self.TINY_FONT)

        # binding widgets
        main.bind("<Button-1>", lambda event, i=item: self.order_popup(event, i))
        image.bind("<Button-1>", lambda event, i=item: self.order_popup(event, i))
        title_label.bind("<Button-1>", lambda event, i=item: self.order_popup(event, i))
        price_label.bind("<Button-1>", lambda event, i=item: self.order_popup(event, i))

        # gridding onto card frame
        image.grid(row=0, column=0, pady=5, padx=5)
        title_label.grid(row=1, column=0, pady=3, padx=5, sticky=W)
        price_label.grid(row=2, column=0, pady=3, padx=5, sticky=W)

        return main

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
        self.menu_f1.grid(row=0, column=0)
        self.menu_line.grid(row=0, column=1)
        self.menu_f2.grid(row=0, column=2)
        self.menu_title.grid(row=n.rcall(), column=n.ccall(), columnspan=2)

        self.red_btn_f.grid(row=0, column=0, padx=67, pady=13)
        self.green_btn_f.grid(row=0, column=1, padx=67, pady=13)

        # reconfiguring widgets
        if self.screen == 'menu_fav':
            self.menu_title.configure(text="Favourites")
            self.card_menu(self.ALL_MENU.fav_get())

        # gridding card widgets
        for card in self.menu_cards:
            if n.rn < 2:
                card.grid(row=n.rcall(), column=0, pady=25, padx=30)
            else:
                card.grid(row=n.rcall() - 2, column=1, pady=25, padx=30)
            self.current_menu_cards.append(card)
        n.reset()
        for cat_btn in self.cat_wid:
            cat_btn.get_main().grid(row=n.rcall(), column=0, padx=5, pady=25)

    def change_menu(self, event, screen):
        """changes the menu screen"""
        self.screen = screen
        if self.screen != self.current_screen:
            self.forget_screen(self.current_menu_cards)
            self.current_menu_cards = []
            self.menu_cards = []
            if self.screen == 'menu_fav':
                self.current_screen = 'menu_fav'
                self.menu_title.configure(text='Favourites')
                self.card_menu(self.ALL_MENU.fav_get())
            elif self.screen == 'menu_main':
                self.current_screen = 'menu_main'
                self.menu_title.configure(text='Main')
                self.card_menu(self.ALL_MENU.main_get())
            elif self.screen == 'menu_sides':
                self.current_screen = 'menu_sides'
                self.menu_title.configure(text='Sides')
                self.card_menu(self.ALL_MENU.sides_get())
            elif self.screen == 'menu_drink':
                self.current_screen = 'menu_drink'
                self.menu_title.configure(text='Drink')
                self.card_menu(self.ALL_MENU.drink_get())

            # gridding card widgets
            n = Num()
            n.rn += 1
            n.cn += 1
            for card in self.menu_cards:
                if n.rn < 2:
                    card.grid(row=n.rcall(), column=0, pady=25, padx=31)
                else:
                    card.grid(row=n.rcall() - 2, column=1, pady=25, padx=31)
                self.current_menu_cards.append(card)

    def checkout_state(self):
        """changes when there are items ordered"""
        if len(self.current_order) > 0:
            self.green_btn.configure(state=ACTIVE)
        else:
            self.green_btn.configure(state=DISABLED)

    def checkout_screen(self):
        """displays the checkout screen"""
        # widget configuring
        self.forget_screen(self.menu_wid)

        # initialising organised order cards
        cards = self.create_order()
        self.top_f.configure(bg='black')

        # widget gridding
        n = Num()
        for wid in self.chkt_wid[0:2]:
            wid.grid(row=n.rcall())
        for wid in cards[0:4]:
            wid.grid(row=n.rcall(), pady=10)
        for wid in self.chkt_wid[2:]:
            wid.grid(row=n.rcall(), pady=10)

        total_price = 0
        for item in self.organise_order():
            total_price += item[1]*self.ALL_MENU.get()[item[0]]['price']
        self.chkt_price.configure(text=f"Total Price: ${total_price}")

    def organise_order(self):
        """organises the current order list"""
        organised_order = []
        items = []
        for item in self.current_order:
            if item[0] in items:
                for i in organised_order:
                    if item[0] == i[0]:
                        organised_order[organised_order.index(i)][1] += item[1]
            else:
                organised_order.append(item)
                items.append(item[0])
        return organised_order

    def create_order(self):
        """creates a list of OrderItemCard's"""
        cards = []
        for order in self.organise_order():
            cards.append(OrderItemCard(self.top_f, font1=self.SMALL_FONT4, font2=self.TINY_FONT, item=order).get_main())
        return cards

    # methods for toplevel displays
    def order_popup(self, event, item):
        """creates a popup window for adjusting quantity and confirm order from the item card selected"""

        # initialising functions for buttons
        def order_toplevel_destroy(cancel):
            """destroys the popup toplevel and stores the quantity information depending on the parameter"""
            if cancel:
                order_wn.destroy()
            else:
                self.current_order.append([item.title, n.get()])
                self.checkout_state()
                order_wn.destroy()

        def add_btn_state():
            """changes the state of the add button"""
            if n.get() < 1:
                add_btn.configure(state=DISABLED)
            elif n.get() == 1:
                add_btn.configure(state=ACTIVE)

        # window geometry variables
        x = root.winfo_rootx() + int(round(self.WIDTH / 4))
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
        main = Frame(order_wn, width=200, height=100, bg='white', borderwidth=5, relief=GROOVE)
        f1 = Frame(main, bg='white')
        f2 = Frame(main, bg='white')

        title = Label(f1, text=item.title, font=self.SMALL_FONT, bg='white')
        quantity_lbl = Label(f1, text="Quantity", font=self.SMALL_FONT3, bg='white', borderwidth=1, relief=GROOVE,
                             padx=25, pady=5)
        quantity_btn = QuantityButton(f1, typeface=self.SMALL_FONT2, size=1, width=10, func1='self.add',
                                      func2=add_btn_state, var=n, bg='white')
        cancel_btn = Button(f2, text='Cancel', font=self.SMALL_FONT3, bg='red', fg='white', borderwidth=1,
                            relief=GROOVE, command=lambda: order_toplevel_destroy(True))
        add_btn = Button(f2, text='Add', font=self.SMALL_FONT3, bg='green', fg='white', borderwidth=1, relief=GROOVE,
                         command=lambda: order_toplevel_destroy(False), state=DISABLED)

        # gridding widgets
        main.grid(sticky=NSEW)
        f1.grid(row=0)
        f2.grid(row=1)
        title.grid(row=0, column=0, padx=10, pady=15, sticky=NSEW)
        quantity_lbl.grid(row=1, column=0, padx=10, pady=15, sticky=NSEW)
        quantity_btn.get_main().grid(row=2, column=0, pady=10)
        cancel_btn.grid(row=0, column=0, pady=10, padx=10, ipadx=45)
        add_btn.grid(row=0, column=1, pady=10, padx=10, ipadx=55)

        # run
        order_wn.grab_set()

    def cancel_menu_popup(self):
        """displays a popup that shows whether if the user wants to cancel their order"""

        # initialising functions for buttons
        def cancel_menu():
            """returns to the home screen and deletes all current menu data"""
            self.current_order = []
            self.screen = 'return_home'
            self.start(None)
            cancel_wn.destroy()

        def return_menu():
            """returns to the menu"""
            cancel_wn.destroy()

        # window geometry variables
        x = root.winfo_rootx() + int(round(self.WIDTH / 4))
        y = root.winfo_rooty() + int(round(self.HEIGHT / 3))

        # initialising window
        cancel_wn = Toplevel(root)
        cancel_wn.title("Order Window")
        cancel_wn.resizable(False, False)
        cancel_wn.geometry(f"+{x}+{y}")
        cancel_wn.overrideredirect(True)

        # initialising widgets
        main = Frame(cancel_wn, width=200, height=100, bg='white', borderwidth=5, relief=GROOVE)
        f1 = Frame(main, bg='white')
        f2 = Frame(main, bg='white')

        title = Label(f1, font=self.MED_FONT1, text="Cancel\nOrder?", bg='white')
        no_btn = Button(f2, font=self.SMALL_FONT3, text="No", bg='red', fg='white', borderwidth=0, command=return_menu)
        yes_btn = Button(f2, font=self.SMALL_FONT3, text="Yes", bg='green', fg='white', borderwidth=0,
                         command=cancel_menu)

        # widget gridding
        main.grid()
        f1.grid(row=0)
        f2.grid(row=1)

        title.grid(padx=20, pady=25)
        no_btn.grid(row=0, column=0, ipadx=60, padx=15, pady=25)
        yes_btn.grid(row=0, column=1, ipadx=55, padx=15, pady=25)

        # run
        cancel_wn.grab_set()



# mainloop and main window adjustments
root = Tk()
CustomerGUI(root)
root.title("OSC Cafe")
root.resizable(False, False)
root.mainloop()
