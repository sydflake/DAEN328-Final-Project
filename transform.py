df.drop(columns = ['__id', 'dba_name', 'aka_name', 'license_', 'latitude', 'longitude', 'location', 'location_address','location_city', 'location_state', 'location_zip', 'address', ], inplace=True)
df = df[df['state'] == 'IL']
df.drop(columns = ['state', 'city'], inplace =True)
df.drop_duplicates(inplace=True)

def strip_and_lower(df, column_name):
  df['coulum_name'].str.lower().str.strip()

def convert_datetime_column(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name]).dt.date
    return df
