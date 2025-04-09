import pandas as pd

## Configurar formato de output en consola
# Mostrar más columnas y más ancho para que no te las trunque
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 50)  # Máximo ancho por celda

## Diccionario con la info de housing
housing_dict = {
    "Location": ["Lausanne, Avenue de Valmont 20",
                 "Lausanne, d'Echallens 8",
                 "Lausanne, Avenue de la Chablière 35bis"],
    "Type": ['Apartment', 'Apartment', 'Apartment'],
    "Price (CHF/month)": [2560, 2276, 2060],
    "Size (m²)": [124, 85, 78],
    "Accommodations": [
        ['Kitchen', '3 Bedrooms', '2 WC', '1 Bathroom', '2 Balcony'],
        ['Living Room', '2 Bedrooms', 'Kitchen', '1 Bathroom', '1 Storeroom'],
        ['Living Room', '3 Bedrooms', 'Kitchen', '1 Bathroom', '1 Balcony']
    ],
    "Link": [
        "https://www.immoscout24.ch/louer/4002031641",
        "https://www.immoscout24.ch/louer/4001980189",
        "https://www.immoscout24.ch/louer/4001976823"
    ],
    "Observations": [[],
                     [],
                     ['5-y fixed-term lease', 'Extract from the Office of Prosecutions', 'Rental application (www.realestate.Apleona Real Estate.com)']]
}

## Mostrar la tabla en formato pandas para visualización
housing_df = pd.DataFrame(housing_dict)
print(housing_df.head())