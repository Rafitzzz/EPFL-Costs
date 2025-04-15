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
                 "Rue du Petit-St-Jean 5, 1003 Lausanne"
    ],

    "Type": ['Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment',
             'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Apartment', 'Duplex'],

    "Price (CHF/month)": [2560, 2276, 2060, 2750, 2790, 2860, 3350, 3150, 3370, 2570, 2390, 2090, 2630, 3005, 2490, 1790, 3150, 2745, 2600, 3355],

    "Size (m²)": [124, 85, 78, 100, 102, 100, 120, 121, 110, 76, 81, 80, 105, 122, 81, 103, 114, 109, 77, 98],

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
        ['Kitchen', 'Living Room', '2 Bedrooms', 'Office', '2 Bathroom', '1 Toilet', 'Cellar']
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
        "https://www.homegate.ch/louer/4002051405" 
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
                     ['In Heart of Lausanne']
    ]
}

## Mostrar la tabla en formato pandas para visualización
housing_df = pd.DataFrame(housing_dict)
print(housing_df)