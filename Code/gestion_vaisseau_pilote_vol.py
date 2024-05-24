import random
import tkinter

class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Customer(Human):
    id = 1   
    def __init__(self, name, age, mail):
        super().__init__(name, age)
        self.id = Customer.id
        self.mail = mail
        self.bookings = [] #Historique des réservations
        self.destination = None
        Customer.id += 1 #On incrémente à chaque fois qu'on crée un passager
    
    """Peut-être créer un système de recherche par nom et voir si ce que tappe l'user est dans la liste des planetes dispo"""
    def choose_destination(self):
        for planet in Planet.destination_possible:
            print(planet.name)
   
    def buy_ticket(self):
        return (f"{self.name} has bought a Ticket")
    
class Pilot(Human):
    def __init__(self, name, age, license, spaceship=None):
        super().__init__(name, age)
        self.license = license
        self.spaceship = spaceship

class Ticket:
    def __init__(self, destination, price):
        self.destination = destination
        self.price = price 

class Destination: #A quoi sert cette classe ? 
    destinations = ["Mars", "Venus", "Mercure","Jupiter", "Pluton"]
    def __init__(self, name): # Ne pas mettre distance depuis la terre (la mettre dans class planet), mais plutot la distance voyage pour calculer la durée
        self.name = name
        self.price = self.distanceEarth * 5.5
    
    def calculate_price(self): #Pas besoin de calculer .. peut être dans init. On pourrait calculer en fonction de la période (ex : vacances scolaires)
        price = self.distanceEarth * 5.5
        return price
    
class Flight: #Cette classe doit contenir (Vaisseau, ListePassagers, LieuDépart, Destination, calculer la durée en fonction distance et vitesse vaisseau)
    flight_id = 1
    
    def __init__(self):
        self.id = Flight.flight_id
        self.passengers = []
        self.pilots = []
        Flight.flight_id += 1

    #Placer les pilotes et passagers dans le vol car spécifique au vol et pas au vaisseau
    def add_spaceship(self, spaceship, centre): #Demande au centre de controle de vérifier si le vaisseau est disponible
        if centre.is_spaceship_available(spaceship):
            self.spaceship = spaceship
            centre.assign_spaceship_to_flight(spaceship, self)
            print(f"Spaceship [{spaceship.name}] has been added to flight ID {self.id}.")
        else:
            print(f"Spaceship {spaceship.name} is already assigned to another flight.")

    def add_pilot(self, pilot, centre):
        if len(self.pilots) < self.spaceship.required_pilots:  # Vérifie si le nombre de pilotes ne dépasse pas le maximum requis pour piloter le vaisseau
            approved, message = centre.approve_pilot(pilot, self.spaceship)  # Le centre approuve ou non en fonction du permis du pilote et de sa disponibilité
            if approved:
                self.pilots.append(pilot)
                centre.busy_pilots[pilot] = self  # Marquer le pilote comme occupé pour ce vol
                print(f"Pilot {pilot.name} added successfully to flight ID {self.id}")
                return True
            else:
                print(f"Cannot add pilot to flight ID {self.id} : {message}")  # Affiche le message spécifique de refus
                return False
        else:
            print("Cannot add more pilots: maximum pilot capacity reached")
            return False

    
                   
    def add_passenger(self, passenger):
        if len(self.pilots) == self.spaceship.required_pilots: #Vérifier d'abord la présence des pilotes             
            if len(self.passengers) < self.spaceship.max_capacity - self.spaceship.required_pilots: #Vérifier la capacité max en comptant les pilotes
                self.passengers.append(passenger)
                print(f"Passenger [id : {Customer.id}] added successfully")
                return True
            else:
                print(f"Cannot ad passenger [id : {Customer.id}]. Spaceship max capacity reached")
                return False
        else:
            print("Cannot add passengers : Insufficient pilots on board")
            return False
        
    def get_passenger(self):
        for passenger in self.passengers:
            print(passenger.name)

    def get_pilot(self):
        for pilot in self.pilots:
            print(pilot.name)
   
class Spaceship:
    def __init__(self, name, max_capacity, speed, required_license, required_pilots): 
        self.name = name
        self.max_capacity = max_capacity
        self.speed = speed
        self.required_license = required_license #Type de license requise pour piloter le vaisseau
        self.required_pilots = required_pilots #Nbre pilote nécessaire pour piloter le vaisseau

    def takeoff(self):  #Décollage
        pass # Imaginer que le vaisseau doit obtenir l'accord du centre contrôle qui gère tous les paramètres liés au vol (météo, obstacles etc, gère les techniciens)
        #Technicien vérifie l'intégrité du vaisseau, remplissage réservoir
    def landing(self): #Atterrissage
        pass

    def accelerate(self): #Accélérer
        pass

    def decelerate(self): #Ralentir
        pass

    def dodge_obstacle(self): #Eviter obstacle
        #Ajouter des trucs (genre en fonction de la distance de l'obstacle, ralentir ou tourner etc)
        print(f"{self.name} débute la manoeuvre d'évitement")

class Planet:
    destination_possible = []
    def __init__(self, name, distance_from_earth,height,orbit,rotation_speed,day_night_cycle):
        self.name = name 
        self.distance_from_earth = distance_from_earth
        self.height = height #rayon, déduire la moitié de la distance à parcourir (1 unité = 1000km de rayon)
        self.orbit = orbit #utilité ?
        self.rotation_speed = rotation_speed #utile ?
        self.day_night_cycle = day_night_cycle #pour indiquer si l'atterissage se fait de jour ou de nuit
        Planet.destination_possible.append(self)
    
    
    @staticmethod #Méthode statique -> pas besoin de créer une instance de classe pour pouvoir l'utiliser. On veut pouvoir accéder à la liste des destinations possibles sans créer un objet
    def list_planets():
        for planet in Planet.destination_possible:
            print(planet.name)

class ControlRoom: #Centre de contrôle
    def __init__(self):
        self.flights = []
        self.spaceship_assignments = {}  # Dictionnaire pour suivre les affectations vol/vaisseau
        self.busy_pilots = {}
        
    def add_flight(self, flight):
        self.flights.append(flight)
        print(f"Ajout du vol ID {flight.id}")

    def assign_spaceship_to_flight(self, spaceship, flight): # Utilisé dans la méthode add_spaceship de la classe Flight
        self.spaceship_assignments[spaceship] = flight #Dictionnaire, la clé est vaisseau, valeur vol
         
    def is_spaceship_available(self, spaceship): # Utilisé dans la classe Flight (Vérifie si Vaisseau est dispo) 
        return spaceship not in self.spaceship_assignments #Pour cela, regarde si présent dans le dico 
        
    def display_flights_in_progress(self):
        print("Voici les vols en cours : ")
        for flight in self.flights:
            print(f"Vol n°{flight.id}")
   
    def approve_pilot(self, pilot, spaceship): # Vérifie si le pilote détient le permis et s'il n'est pas déjà pris pour un vol
        if pilot.license != spaceship.required_license:
            return False, f"Le pilote {pilot.name} n'a pas le permis requis pour piloter le vaisseau {spaceship.name}" #Renvoie un tuple (booleen, chaine de caractères)
        if pilot in self.busy_pilots:
            occupied_flight = self.busy_pilots[pilot]
            return False, f"Le pilote {pilot.name} est déjà occupé sur le vol ID {occupied_flight.id}"
        
        return True, "Le pilote est approuvé pour le vol"
    
    def assign_pilot(self, pilot, flight):
        self.busy_pilots[pilot] = flight
    
    def approve_passenger(self, passenger, flight): #Vérifier ticket par exemple 
        pass
    """Voir code en dessous pour add passenger dans la classe flight"""

    def check_weather(self): #Ou check les conditions en général avant le décollage
        pass

    def detect_obstacle(self, flight): #Doit se référer au vol 
        obstacle_distance = random.randint(100,300) #Génère une distance aléatoire entre 100 et 300
        if random.randint(0,10) > 2: #Génère random 0 et 10, et si plus grand que 2 = obstacle détecté
            print(f"Obstacle détecté à {obstacle_distance} km")
            flight.spaceship.dodge_obstacle()
        else:
            print("Aucun obstacle, la voie est libre")
    
    

    
           
"""Création des instances"""

#Création du centre de contrôle 
centre = ControlRoom()

#Création des planètes
p1 = Planet("Mars", 100, 3)
p2 = Planet("Mercure", 200, 2)
p3 = Planet("Jupiter", 300, 69)
p4 = Planet("Venus", 400, 6)
p5 = Planet("Uranus", 500, 25)

#Création des pilotes
pilot = Pilot("Albert",44,1)
pilot2 = Pilot("Roger", 56,3)

#Création des passagers (classe parent Client ? Que pourrait faire un passager >< client ?)
passager1 = Customer("Anthony Leclercq", 23, "anthony@mail.com")
passager2 = Customer("Arthur", 19, "arthur@mail.com")

#Création des vaisseaux
vaisseau = Spaceship("Qwerty II", 2, 200, 1, 2)
vaisseau_2 = Spaceship("Azerty X",2, 100, 3, 1)

#Création des vols
flight1 = Flight()
flight2 = Flight()

#Création du planificateur de vol


"""Test des méthodes"""


centre.add_flight(flight1)
centre.add_flight(flight2)

flight1.add_spaceship(vaisseau, centre)
flight2.add_spaceship(vaisseau, centre)  # Cette tentative devrait échouer car spaceship1 est déjà pris
flight2.add_spaceship(vaisseau_2,centre)


    
centre.approve_pilot(pilot, vaisseau)
flight1.add_pilot(pilot, centre)
flight1.add_pilot(pilot, centre)

centre.approve_pilot(pilot2, vaisseau_2)
flight2.add_pilot(pilot2, centre)

"""D'abord vérifier la présence d'un vol, puis d'un vaisseau et puis seulement ajouter les pilotes et passagers"""



"""
class ControlRoom:
    def approve_passenger(self, passenger, spaceship):
        # Vérification de conditions spécifiques, par exemple santé
        return True  # Simplifié pour l'exemple

def add_passenger(self, passenger, control_center):
    if len(self.pilots) == self.spaceship.required_pilots:
        if len(self.passengers) < self.spaceship.max_capacity - self.spaceship.required_pilots:
            if control_center.approve_passenger(passenger, self.spaceship):
                self.passengers.append(passenger)
                print(f"Passenger [id: {passenger.id}] added successfully")
                return True
            else:
                print("Passenger not approved by control center")
                return False
        else:
            print("Cannot add passenger: spaceship max capacity reached")
            return False
    else:
        print("Cannot add passengers: insufficient pilots on board")
        return False
"""

#Proposition de méthode pour ajouter les pilotes au fichier data.json
"""def save_pilot_to_json(pilot): 
    try:
        # Read existing data
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # If file not found, create a new list
        data = []

    # Add the new pilot
    data.append({
        "name": pilot.name,
        "age": pilot.age,
        "license": pilot.license,
        "spaceship": pilot.spaceship
    })

    # Save the updated data
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

def add_pilot():
    name = name_entry.get()
    age = age_entry.get()
    license = license_entry.get()
    spaceship = spaceship_entry.get()

    if not name or not age or not license:
        messagebox.showwarning("Input Error", "Name, age, and license are required fields.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showwarning("Input Error", "Age must be a number.")
        return

    new_pilot = Pilot(name, age, license, spaceship)
    save_pilot_to_json(new_pilot)
    messagebox.showinfo("Success", "Pilot added successfully.")

    # Clear the entry fields
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    license_entry.delete(0, tk.END)
    spaceship_entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Spacecraft Pilot Manager")

# Create and place the labels and entry widgets
tk.Label(root, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Age:").grid(row=1, column=0)
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1)

tk.Label(root, text="License:").grid(row=2, column=0)
license_entry = tk.Entry(root)
license_entry.grid(row=2, column=1)

tk.Label(root, text="Spaceship:").grid(row=3, column=0)
spaceship_entry = tk.Entry(root)
spaceship_entry.grid(row=3, column=1)

# Create and place the add button
add_button = tk.Button(root, text="Add Pilot", command=add_pilot)
add_button.grid(row=4, columnspan=2)

# Start the main loop
root.mainloop()

"""
