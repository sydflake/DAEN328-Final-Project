df.drop(columns = ['__id', 'aka_name', 'license_', 'latitude', 'longitude', 'location', 'location_address','location_city', 'location_state', 'location_zip', 'address', ], inplace=True)
df = df[df['state'] == 'IL']
df.drop(columns = ['state', 'city'], inplace =True)
