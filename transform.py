df.drop(columns = ['__id', 'dba_name', 'aka_name', 'license_', 'latitude', 'longitude', 'location', 'location_address','location_city', 'location_state', 'location_zip', 'address', ], inplace=True)
df = df[df['state'] == 'IL']
df.drop(columns = ['state', 'city'], inplace =True)
df.drop_duplicates(inplace=True)

def strip_and_lower(df, column_name):
  df['coulum_name'].str.lower().str.strip()

def convert_datetime_column(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name]).dt.date
    return df
  
### CLEANS VIOLATION ###
def extract_violation_numbers(text):
    if pd.isna(text):
        return []
    # Find all number-dot patterns like 18., 32., etc.
    return re.findall(r'\b(\d+)\.', text)

def clean_facility_type(df, column='facility_type'):
    category_map = [
        ('grocery', 'Grocery'),
        ('convenien', 'Convenience Store'),
        ('liquor', 'Liquor'),
        ('restaurant', 'Restaurant'),
        ('coffee', 'Coffee Shop'),
        ('school', 'School'),
        ('daycare', 'Child Services'),
        ('children', 'Child Services'),
        ('hospital', 'Hospital'),
        ('bakery', 'Bakery'),
        ('catering', 'Catering'),
        ('church', 'Church'),
        ('mobile', 'Mobile Vendor'),
        ('bar', 'Bar'),
        ('pantry', 'Food Pantry'),
        ('deli', 'Deli'),
        ('juice', 'Juice/Smoothie'),
        ('herbal', 'Herbal/Nutrition'),
        ('tea', 'Tea Shop'),
        ('ice cream', 'Ice Cream'),
        ('popcorn', 'Snack Shop'),
        ('cafe', 'Cafe'),
        ('tavern', 'Bar'),
        ('college', 'College/University'),
        ('university', 'College/University'),
        ('venue', 'Venue'),
        ('vendor','Vendor'),
        ('mobil', 'Vendor'),
        ('event', 'Event Space'),
        ('banquet', 'Banquet Hall'),
        ('gas', 'Gas Station'),
        ('fuel', 'Gas Station'),
        ('store', 'Store'),
        ('retail','Retail'),
        ('theatre', 'Theater'),
        ('theater', 'Theater'),
        ('supportive living', 'Assisted Living'),
        ('senior', 'Assisted Living'),
        ('nursing home', 'Assisted Living'),
        ('long-term care facility', 'Assisted Living'),
        ('day care', 'Child Services'),
        ('years old', 'Child Services'),
        ('rstaurant', 'Restaurant'),
        ('candy', 'Candy'),
        ('icecream', 'Ice Cream'),
        ('roof', 'Rooftop'),
        ('health', 'Health'),
        ('fitness', 'Fitness'),
        ('kitchen', 'Kitchen'),
        ('diner', 'Diner'),
        ('commisary','Commissary'),
        ('truck', 'Truck'),
        ('class', 'Class'),
        ('golf', 'Golf Course'),
        ('rehab', 'Rehab Center'),
        ('care', 'Care Facility'),
        ('shop', 'Shop'),
        ('produce', 'Produce'),
        ('gallery', 'Gallery'),
        ('child', "Children's Services"),
        ('1023', "Children's Services"),
        ('kiosk', 'Kiosk'),
        ('nutrition', 'Nutrition'),
        ('distri', 'Distributor'),
        ('dine', 'Restaurant'),
        ('shcool', 'School'),
        ('profit', 'Non-Profit')
    ]

    # Fill missing with 'Unknown'
    df[column] = df[column].fillna("Unknown").astype(str)

    # Apply mapping
    for keyword, new_category in category_map:
        mask = df[column].str.contains(keyword, case=False, na=False)
        df.loc[mask, column] = new_category

    # Lowercase the column
    df[column] = df[column].str.lower()

    return df
