from os import system
import pickle
#from ordersActions import loadOrders, addOrder, printOrder, deleteOrder, editOrder



class Shipping():
    def __init__(self, Type, Price):
        self.Type = Type
        self.Price = Price

class Customer():
    def __init__(self, Name, Address, ID):
        self.Address = Address
        self.Name = Name
        self.ID = ID



# Třída reprezentující Objednávku
class Order():
    States = {1: "Přijata", 2: "Vyhotovena", 3:"Na cestě", 4: "Doručena", 5: "Zrušena"} 
    PaymentMethods = {1: "ComGate - Platba kartou", 2: "Comgate - Převod na Účet", 3:"Hotově při převzetí"} 
    def __init__(self, Date, ID, isPaid, PaymentMethod, Shipping, Customer, Cupon, State, Books):
        self.Date = Date
        self.ID = ID
        self.isPaid = isPaid
        self.PaymentMethod = PaymentMethod
        self.Cupon = Cupon
        self.Books = Books
        self.TotalPrice = self.getPrice()
        self.State = State
        self.Shipping = Shipping
        self.Customer = Customer

    def getState(self):
        try:
            return self.States[int(self.State)]
        except:
            return "Nedefinováno"

    def getPaymentMethod(self):
        try:
            return self.PaymentMethods[int(self.PaymentMethod)]
        except:
            return "Nedefinováno"

    def __str__(self):
        return f'Objednávka č. {self.ID}'

    # Projde ceny knížek a sečte je do proměnné TotalPrice
    def getPrice(self):
        try:
            p = 0
            if self.Books:
                if self.Cupon == "" or self.Cupon == "0":
                    for b in self.Books:
                        p += b.Price * b.Count
                else:
                    
                    for b in self.Books:
                        p += (b.Price * b.Count) - ((b.Price * b.Count)/100)* float(self.Cupon)
            
            return p

        except: 
            return 0
        
    # Vypíše Parametry Objednávky
    def PrintParameters(self):
        print("\n\nObjednávka č.", self.ID)
        print("Datum: ", self.Date.strftime("%Y-%m-%d"))
        print("Zaplacená: ", self.isPaid)
        print("Platební metoda: ", self.getPaymentMethod())
        print("Kupón (Procento): ", self.Cupon)
        print("Cena celkem: ", self.TotalPrice, " Kč")
        print("Stav Objednávky: ", self.getState())
        print("Počet knih: ", len(self.Books))
        print()
        for i in range(len(self.Books)):
            print("\n----------------------------------------\n")

            print(i + 1, ". Kniha:\n")
            self.Books[i].PrintParameters()
            print()

    def PrintParametersLite(self):
        print("\n\nObjednávka č.", self.ID, "| Z Data: ", self.Date.strftime("%Y-%m-%d"))
        print("Zaplacená: ", self.isPaid,"| Platební metodou: ", self.getPaymentMethod())
        print("Cena celkem: ", self.TotalPrice, " Kč | Použit kupón v hodnotě: ", self.Cupon, "%")
        print("Stav Objednávky: ", self.getState())
        print("Knihy: ")
        print()
        for i in range(len(self.Books)):

            print(i + 1, f". Kniha: {self.Books[i]}")
        
        print("\n=====================================================\n")
def loadOrders():
    print('Nahrávám Objednávky...')
   # try:
    with open('orders.pkl', "rb") as f:
        try: orders = pickle.load(f)
        except: orders = []
    print('Objednávky nahrány úspěšně...')
    print("\n------------------------------------\n")

    return orders

        

        

   # except:
   #     print("Nahrání se nepovedlo")


def createID():
    #Now = datetime.datetime.now()
    #ID = str(Now.day) + "_" + str(Now.month) + "_" + str(Now.year) + "_" + str(Now.second) + "_" + str(random.randint(10000, 99999))
    if ORDERS == []: return 1
    else: return ORDERS[-1].ID + 1

def createOrder():
    isPaid = input("Byla objednávka zaplacena? Y/N: ") in ["y", "Y"]
    PaymentMethod = input("Platební metoda (1: ComGate - Platba kartou, 2: Comgate - Převod na Účet, 3: Hotově při převzetí): ")
    Cupon = input("Kupón: (Procento): ")
    State = input("Zadej stav objednávky (1: Přijata, 2: Vyhotovena, 3: Na cestě, 4: Doručena, 5: Zrušena: ")
    NumBooks = int(input("Kolik bude knih? "))
    Books = []

    for i in range(NumBooks):
        print('\n\n', i + 1, ". Kniha:")
        ID = createID()
        Name = input("\nJméno knihy: ")
        Author = input("Jméno Autora: ")
        ISBN = input("ISBN knihy: ")
        Price = float(input("Cena za 1 knihu: "))
        Count = int(input("Počet knih: "))

        B = Book(Name, Author, ISBN, Price, Count, None)
        Books.append(B)

    system("cls")
    return Order(datetime.datetime.now(), ID, isPaid, PaymentMethod, Cupon, State, Books)


# Přidá novou objednávku
def addOrder():
    print('Přidat Objednávku')
    print("\n------------------------------------\n")
    
    NewOrder = createOrder()
    NewOrder.PrintParameters()

    for book in NewOrder.Books:
        book.Order = NewOrder
        
    ORDERS.append(NewOrder)

    print("\n---------------------------------------------------\n")
    print(f"\nNová OBJEDNÁVKA č. {NewOrder.ID} za {NewOrder.TotalPrice},- úspěšně vytvořena\n")
    print("\n---------------------------------------------------\n")

    input()
    saveOrders()


# Vrátí objednávku podle ID
def getOrder(OrderID):
    for o in ORDERS:
        if int(o.ID) == int(OrderID): return o
    return None

def printOrderHeading(order):
    print("\n\n| | | | | | | | | | | | | | | | | | | | | | | | | | |\n\n")
    """
    print("                          \n=")
    print("                        =====")
    print("                      =========")
    print("                    =============")
    print("                  =================")
    print("                =====================")
    print("              =========================")
    print("            =============================")
    print("          =================================")
    print("        =====================================")
    print("      =========================================")
    print("    =============================================")
    print("  =================================================")
    print("=====================================================")
    """
    print("=====================================================")
    print(f"                   {order}")
    print("=====================================================")

# Vypíše buď všechny nebo pouze jednu objednávku
def printOrder(OrderID=""):
    system("cls")
    print('Vypsat Objednávky')
    print("\n-----------------------------------------------\n\n")

    if OrderID == "": 
        if len(ORDERS) > 0:
            for o in ORDERS:
                
                printOrderHeading(o)
                o.PrintParametersLite()


        else: print("Neneašli jsme žádné objednávky - vytvoř nějaké")

    else:
        Order = getOrder(OrderID)
        if Order:
            printOrderHeading(Order)
            Order.PrintParameters()
        else: print("Neplatné číslo objednávky")

    input()

    system("cls")

# přesune objednávku z ORDERS do DELETED_ORDERS
def deleteOrder():
    print('Odstranit Objednávku')
    print("\n------------------------------------\n")

    ID = input('Zadej ID Objednávky, kterou chceš vymazat: ')
    o = getOrder(ID)
    if o != None:
        if input(f'Opravdu chceš vymazat položku: {o} (Y/N): ') in ["Y", "y"]:
            ORDERS.remove(o)
            DELETED_ORDERS.append(o)
            print(f"Objednávka {o} BYLA smazána")
        else: print(f"Objednávka {o} NEBYLA smazána")
    

# Umožní Upravit Objednávku
def editOrder():
    print('Upravit Objednávku')
    print("\n------------------------------------\n")

    orderID = input('Zadej ID objednávky, kterou chceš upravit: ')
    order = getOrder(orderID)
    if order != None:
        system("cls")
        print('\nPokud nechceš měnit nech prázdné pole\n')

        #--------------------------------------------------------------

        isPaid = input("Byla objednávka zaplacena? Y/N: ")
        if isPaid == "":
            pass
        elif isPaid in ["Y", "y"]:
            order.isPaid = True
        else: 
            order.isPaid = False

        #--------------------------------------------------------------


        PaymentMethod = input("Platební metoda (1: ComGate - Platba kartou, 2: Comgate - Převod na Účet, 3: Hotově při převzetí): ")
        if PaymentMethod == "":
            pass
        elif str(PaymentMethod) in ["1", "2", "3", "4"]: 
            order.PaymentMethod = PaymentMethod
        else:
            order.PaymentMethod = "0"

        #--------------------------------------------------------------

        Cupon = input("Kupón: (Procento): ")
        if Cupon == "":
            pass
        else: 
            try: order.Cupon = float(Cupon)
            except: order.Cupon = 0
            order.TotalPrice = float(order.getPrice())
        
        #--------------------------------------------------------------

        State = input("Zadej stav objednávky (1: Přijata, 2: Vyhotovena, 3: Na cestě, 4: Doručena, 5: Zrušena: ")
        if State == "":
            pass
        else: 
            order.State = State

        #--------------------------------------------------------------
        
        NumBooks = input("Kolik bude knih? ")
        if NumBooks != "":

            Books = []

            for i in range(NumBooks):
                print('\n\n', i + 1, ". Kniha:")
                Name = input("\nJméno knihy: ")
                Author = input("Jméno Autora: ")
                ISBN = input("ISBN knihy: ")
                Price = float(input("Cena za 1 knihu: "))
                Count = int(input("Počet knih: "))

                B = Book(Name, Author, ISBN, Price, Count, None)
                Books.append(B)

            order.Books = Books

        print('\nEditace Objednávky proběhla úspěšně.\n')


    else: 
        system("cls")
        print('Neplatné ID')

    input()

    system("cls")


# List Objednávek
DELETED_ORDERS = []

# Třída reprezentující Knihu
class Book():
    def __init__(self, Name, Author, ISBN, Price, Count, Order):
        self.Name = Name
        self.Author = Author
        self.ISBN = ISBN
        self.Price = Price
        self.Count = Count
        self.Order = Order

    def __str__(self):
        return f"{self.Name} - {self.Author} | Cena/Kus: {self.Price},- | Počet Kusů: {self.Count}"

    def PrintParameters(self):
        print("Jméno knihy: ", self.Name)
        print("Jméno Autora: ", self.Author)
        print("ISBN knihy: ", self.ISBN)
        print("Cena za 1 knihu ", self.Price, " Kč")
        print("Počet knih: ", self.Count)
        print("Cena za všechny tyto knihy: ", self.Price * self.Count, " Kč")

        if self.Order:
            print("Patří k objenávce č.", self.Order.ID)

        


# Uvítací zprávy
def Welcome():
    print('\nVítejte ve objednávkovém systému Knížky pro rozvoj :-)\n')
    print('=============================================================\n')
    print('Přidat objednávku = 1')
    print('Vypsat objednávky = 2')
    print('Zrušit objednávku = 3')
    print('Upravit objednávku = 4')
    print('Ukončit program = 5')




        

   # except:
   #     print("Nahrání se nepovedlo")

def saveCustomers():
    system("cls")
    print("Ukládám Zákazníky...")
    with open('customers.pkl', 'wb') as f:
        pickle.dump(CUSTOMERS, f)



    print("Zákazníci uloženy...")
    print("\n------------------------------------\n")

    system("cls")

def loadCustomers():
    print('Nahrávám Zákazníky...')
   # try:
    with open('customers.pkl', "rb") as f:
        try: customers = pickle.load(f)
        except: customers = []
    print('Zákazníci nahráni úspěšně...')
    print("\n------------------------------------\n")

    return customers

ORDERS = loadOrders()
CUSTOMERS = loadCustomers()

# Tělo programu - Hlavní logika
def main():
    
    while True:
        print(ORDERS)

        Welcome()
        x = input('\nCo chceš udělat: ')

        system("cls")

        try:
            if x == "1": addOrder() 
            elif x == "2":
                OrderID = input("Číslo Objednávky (Prázné = Všechny): ")
                printOrder(OrderID)
            elif x == "3": deleteOrder()
            elif x == "4": editOrder()
            elif x == "5": break
            else: 
                print('Neplatný příkaz')
                print("\n------------------------------------------\n")

        
        except:
           print("Někde se vyskytla chyba.")


   
main()
print("\n\nDěkujeme za použití :-) Knížky pro rozvoj s.r.o. | 2021 | https://knizkyprorozvoj.com")
input()
