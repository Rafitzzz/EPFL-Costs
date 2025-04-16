import pandas as pd

## Configurar formato de output en consola
# Mostrar más columnas y más ancho para que no te las trunque
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 100)  # Máximo ancho por celda

## Diccionario con la info de housing
housing_dict = {
    "Location": ["Lausanne, Avenue de Valmont 20",
                 "Lausanne, d'Echallens 8",
                 "Lausanne, Avenue de la Chablière 35bis", 
                 "Route du Pavement 34, 1018 Lausanne", 
                 "Rue Couchirard 4, 1004 Lausanne", 
                 "Avenue Virgile-Rossel 9, 1012 Lausanne", 
                 "Violette District 4, 1018 Lausanne", 
                 "Avenue des Toises 8, 1005 Lausanne", 
                 "Chemin de Renens 52d, 1004 Lausanne", 
                 "Route de Berne 1, 1010 Lausanne", 
                 "Louve Street 1, 1003 Lausanne", 
                 "Chemin du Martinet 28, 1007 Lausanne", 
                 "Chemin des Sauges 9, 1018 Lausanne", 
                 "Avenue Davel 18, 1004 Lausanne", 
                 "Chemin du Martinet 22, 1007 Lausanne", 
                 "Avenue du Grey 76, 1018 Lausanne", 
                 "Wolf Park 5A/B & Route des Plaines-du-Loup 39A/B, 1018 Lausanne", 
                 "des Boveresses 84, 1010 Lausanne", 
                 "Rue Marterey 1-3, 1003 Lausanne", 
                 "Rue du Petit-St-Jean 5, 1003 Lausanne",
                 "Lausanne Base, Boulevard de Grancy 51 1006 Lausanne, Switzerland",
                 "Rue du Valentin 62, 1004 Lausanne, Switzerland"
    ],

    "Type": ['Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment',
             'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Duplex',  "Apartment", "Apartment"],

    "Price (CHF/month)": [2560, 2276, 2060, 2750, 2790, 2860, 3350, 3150, 3370, 2570, 2390, 2090, 2630, 3005, 2490, 1790, 3150, 2745, 2600, 3355, 4200, 5600],

    "Size (m²)": [124, 85, 78, 100, 102, 100, 120, 121, 110, 76, 81, 80, 105, 122, 81, 103, 114, 109, 77, 98, 70, 80],

    "Accommodations": [
        ['Kitchen', '3 Bedrooms', '2 WC', '1 Bathroom', '2 Balcony'],
        ['Living Room', '2 Bedrooms', 'Kitchen', '1 Bathroom', '1 Storeroom'],
        ['Living Room', '3 Bedrooms', 'Kitchen', '1 Bathroom', '1 Balcony'], 
        ['Kitchen', 'Bathroom'], 
        ['Kitchen', 'Living Room', '2 Bedrooms', '1 Bedroom/Office', '2 Bathroom', '1 Balcony'], 
        ['Kitchen', '3 Bedrooms', '2 Bathroom', 'Dining Room', '1 Balcony', '1 Cellar', 'Washing Machene'], 
        ['Kitchen', 'Living Room', '3 Bedrooms', '2 Bathroom', '2 Balcony', '1 Cellar'], 
        ['Kitchen', 'Living Room', '3 Bedrooms', '2 Bathroom'], 
        ['Kitchen', 'Living Room', '3 Bedrooms', '2 Bathroom', 'Laundry Room'], 
        ['Kitchen', '3 Bedrooms', '1 Bathroom', '2 Toilets', '1 Living Room'], 
        ['Kitchen', 'Living Room', '3 Bedrooms', '1 Bathroom'], 
        ['Kitchen', '1 Bathroom', '1 Living Room', '2 Bedroom', '1 Balcony'], 
        ['Kitchen', 'Living Room', '1 Balcony', '3 Bedrooms', '2 Bathroom', 'Cellar'], 
        ['Kitchen', 'Living Room', '3 Bedrooms', '2 Bathroom', '2 Balcony', 'Cellar'], 
        ['Kitchen', '4.5 Rooms', '1 Toilet', '1 Balcony'], 
        ['Kitchen', 'Living Room', '3 Bedrooms', '1 Bathroom', '1 Toilet', '1 Balcony'], 
        ['Kitchen', 'Living Room', '3 Bedrooms', '1 Bathroom', '1 Toilet', '1 Balcony'], 
        ['Kitchen', 'Living Room', '3 Bedrooms', '2 Bathroom', '2 Balcony', 'Cellar'], 
        ['Kitchen', 'Living Room', '3 Bedrooms', 'Storage/Wash room', '1 Bathroom'], 
        ['Kitchen', 'Living Room', '2 Bedrooms', 'Office', '2 Bathroom', '1 Toilet', 'Cellar'],
        ['Kitchen', 'Living Room', '1 Bedrooms', '2 Bathroom', '1 Toilet'],
        ['Kitchen', 'Living Room', '2 Bedrooms', '2 Bathroom', '1 Toilet', 'Parking']
    ],

    "Link": [
        "https://www.immoscout24.ch/louer/4002031641",
        "https://www.immoscout24.ch/louer/4001980189",
        "https://www.immoscout24.ch/louer/4001976823", 
        "https://www.homegate.ch/louer/4002069859", 
        "https://www.homegate.ch/louer/4002071391", 
        "https://www.homegate.ch/louer/4002072748", 
        "https://www.homegate.ch/louer/4002083242", 
        "https://www.homegate.ch/louer/4002031647", 
        "https://www.homegate.ch/louer/4002020012", 
        "https://www.homegate.ch/louer/4002062505", 
        "https://www.homegate.ch/louer/4002039824", 
        "https://www.homegate.ch/louer/4002050069",
        "https://www.homegate.ch/louer/4002031904", 
        "https://www.homegate.ch/louer/4002007245", 
        "https://www.homegate.ch/louer/4001902460", 
        "https://www.homegate.ch/louer/4002100359", 
        "https://www.homegate.ch/louer/4001880732", 
        "https://www.homegate.ch/louer/4001876861", 
        "https://www.homegate.ch/louer/4002074870", 
        "https://www.homegate.ch/louer/4002051405",
        "https://www.baseaparthotels.com/en/lausanne-2/",
        "https://www.oklogements.ch/en/appartements-et-studios/lausanne/3"
    ],

    "Observations": [['N/A'],
                     ['N/A'],
                     ['5-y fixed-term lease', 'Extract from the Office of Prosecutions', 'Rental application (www.realestate.Apleona Real Estate.com)'], 
                     ['Historic Building'], 
                     ['Shared Laundry Room'], 
                     ['Smoking Allowed', 'Parking Space'], 
                     ['Modern'], 
                     ['No Balcony'], 
                     ['Annexes: Charges CHF 150.-/month; 1 indoor space at CHF 175.-/month; Rent including VAT CHF 3,695.-/month'], 
                     ['Shared Laundry Room'], 
                     ['Apply through website'], 
                     ['Not many photos'], 
                     ['N/A'], 
                     ['5-y fixed-term lease'], 
                     ['Not many photos'], 
                     ['N/A'], 
                     ['Pre-installation for washmachine/dry'], 
                     ['Rental application required'], 
                     ['Rental application required'], 
                     ['In Heart of Lausanne'],
                     ['BASE XL: Un baño, pero al final son 2 cuartos y estan equipados. Wifi, Dishwasher, Nesspreso, Oven, A/C, y se ven nuevos | Podemos conectar 2 de 24 m2 y sale mas baras', 'Tel : +41 21 552 30 60 Email : hello@baselausanne.com'],
                     ['80 m² 3.5 roomsfrom 5600 month Place de parc', 'Book Now: https://www.oklogements.ch/en/demande?rooms=3-3.5&location=Lausanne%20-%20Rue%20du%20Valentin%2062c']
    ]
}

# Define the expense patterns for 24-month view
def get_monthly_expense_patterns():
    """
    Returns a dictionary defining how expenses are distributed across 24 months
    """
    return {
        # COLLEGE expenses
        "tuition": {
            "total_chf": 2920.00,
            "monthly_values": [1460, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1460, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        },
        "registration_fee": {
            "total_chf": 276.00,
            "monthly_values": [138, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 138, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        },
        "health_insurance": {
            "total_chf": 14400.00,
            "monthly_values": [600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]
        },
        # SETTLEMENT expenses
        "supplies": {
            "total_chf": 3000.00,
            "monthly_values": [1500, 0, 0, 1500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        },
        "housing_deposit": {
            "total_chf": 0.00,  # This will be calculated dynamically based on housing selection
            "monthly_values": [0] * 24  # Will be updated dynamically
        },
        # LIVING expenses
        "rent": {
            "total_chf": 0.00,  # This will be calculated dynamically based on housing selection
            "monthly_values": [0] * 24  # Will be updated dynamically
        },
        "maintenance": {
            "total_chf": 2400.00,
            "monthly_values": [100] * 24
        },
        "water": {
            "total_chf": 1200.00,
            "monthly_values": [50] * 24
        },
        "electricity": {
            "total_chf": 2400.00,
            "monthly_values": [100] * 24
        },
        "wifi": {
            "total_chf": 2400.00,
            "monthly_values": [100] * 24
        },
        # PERSONAL expenses
        "groceries": {
            "total_chf": 24000.00,
            "monthly_values": [1000] * 24
        },
        "transportation": {
            "total_chf": 3600.00,
            "monthly_values": [150] * 24
        },
        "mobile": {
            "total_chf": 2400.00,
            "monthly_values": [100] * 24
        },
        "social": {
            "total_chf": 4800.00,
            "monthly_values": [200] * 24
        },
        "trips": {
            "total_chf": 7200.00,
            "monthly_values": [300] * 24
        },
        # Seasonal expenses - vary throughout the year
        "winter_clothing": {
            "total_chf": 1600.00,
            "monthly_values": [0, 0, 0, 0, 0, 0, 0, 0, 0, 800, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 800, 0, 0]
        },
        "holidays": {
            "total_chf": 3000.00,
            "monthly_values": [0, 500, 0, 0, 0, 1000, 0, 0, 0, 0, 500, 0, 0, 500, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0]
        }
    }

# Convert to DataFrame
housing_df = pd.DataFrame(housing_dict)

if __name__ == "__main__":
    print(housing_df)