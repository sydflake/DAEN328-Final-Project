import pandas as pd
import re
from rapidfuzz import fuzz, process

# ---------- Valid Inspection Types ----------
BASE_INSPECTION_TYPES = [
    'canvass', 'consultation', 'complaint', 'license',
    'suspect food poisoning', 'task-force inspection'
]
VALID_INSPECTION_TYPES = BASE_INSPECTION_TYPES + [f"{t} re-inspection" for t in BASE_INSPECTION_TYPES]

# ---------- Individual Cleaning Functions ----------
def strip_and_lower(df, column_name):
    df[column_name] = df[column_name].astype(str).str.lower().str.strip()
    return df

def convert_datetime_column(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce').dt.date
    return df

def fuzzy_match_inspection_type(value, valid_choices=VALID_INSPECTION_TYPES, threshold=85):
    if pd.isna(value):
        return 'other'
    match, score, _ = process.extractOne(value, valid_choices, scorer=fuzz.token_sort_ratio)
    return match if score >= threshold else 'other'

def clean_inspection_type_column(df, column='inspection_type'):
    df['cleaned_inspection_type'] = df[column].apply(lambda x: x if x in VALID_INSPECTION_TYPES else fuzzy_match_inspection_type(x))
    return df

def clean_facility_type(df, column='facility_type'):
    category_map = [
        ('grocery', 'Grocery'), ('convenien', 'Convenience Store'), ('liquor', 'Liquor'),
        ('restaurant', 'Restaurant'), ('coffee', 'Coffee Shop'), ('school', 'School'),
        ('daycare', 'Child Services'), ('children', 'Child Services'), ('hospital', 'Hospital'),
        ('bakery', 'Bakery'), ('catering', 'Catering'), ('church', 'Church'), ('mobile', 'Mobile Vendor'),
        ('bar', 'Bar'), ('pantry', 'Food Pantry'), ('deli', 'Deli'), ('juice', 'Juice/Smoothie'),
        ('herbal', 'Herbal/Nutrition'), ('tea', 'Tea Shop'), ('ice cream', 'Ice Cream'),
        ('popcorn', 'Snack Shop'), ('cafe', 'Cafe'), ('tavern', 'Bar'), ('college', 'College/University'),
        ('university', 'College/University'), ('venue', 'Venue'), ('vendor', 'Vendor'), ('mobil', 'Vendor'),
        ('event', 'Event Space'), ('banquet', 'Banquet Hall'), ('gas', 'Gas Station'),
        ('fuel', 'Gas Station'), ('store', 'Store'), ('retail', 'Retail'), ('theatre', 'Theater'),
        ('theater', 'Theater'), ('supportive living', 'Assisted Living'), ('senior', 'Assisted Living'),
        ('nursing home', 'Assisted Living'), ('long-term care facility', 'Assisted Living'),
        ('day care', 'Child Services'), ('years old', 'Child Services'), ('rstaurant', 'Restaurant'),
        ('candy', 'Candy'), ('icecream', 'Ice Cream'), ('roof', 'Rooftop'), ('health', 'Health'),
        ('fitness', 'Fitness'), ('kitchen', 'Kitchen'), ('diner', 'Diner'), ('commisary', 'Commissary'),
        ('truck', 'Truck'), ('class', 'Class'), ('golf', 'Golf Course'), ('rehab', 'Rehab Center'),
        ('care', 'Care Facility'), ('shop', 'Shop'), ('produce', 'Produce'), ('gallery', 'Gallery'),
        ('child', "Children's Services"), ('1023', "Children's Services"), ('kiosk', 'Kiosk'),
        ('nutrition', 'Nutrition'), ('distri', 'Distributor'), ('dine', 'Restaurant'),
        ('shcool', 'School'), ('profit', 'Non-Profit')
    ]
    df[column] = df[column].fillna("Unknown").astype(str)
    for keyword, new_category in category_map:
        mask = df[column].str.contains(keyword, case=False, na=False)
        df.loc[mask, column] = new_category
    df[column] = df[column].str.lower()
    return df

# ---------- Master Clean Function ----------
def clean_data(df):
    # Drop unnecessary columns
    df = df.drop(columns=[
        '__id', 'aka_name', 'license_', 'latitude', 'longitude', 'location',
        'location_address', 'location_city', 'location_state', 'location_zip',
        'address'
    ], errors='ignore')

    # Filter for Illinois and drop irrelevant location columns
    df = df[df['state'] == 'IL']
    df = df.drop(columns=['state', 'city'], errors='ignore')

    # Handle missing data
    df = df.dropna(subset=['zip'])
    df = df.drop_duplicates()

    # Clean specific columns
    strip_and_lower(df, 'dba_name')
    convert_datetime_column(df, 'inspection_date')
    clean_inspection_type_column(df, 'inspection_type')
    clean_facility_type(df, 'facility_type')

    return df
