url = 'https://data.cityofchicago.org/api/odata/v4/4ijn-s7e5'
response = requests.get(url)

data = pd.read_json(response.text)
data.head()

all_data = []
top = 1000
skip = 0

while True:
    paged_url = f'https://data.cityofchicago.org/api/odata/v4/4ijn-s7e5?$top={top}&$skip={skip}'
    response = requests.get(paged_url)
    page_data = response.json().get('value', [])
    
    if not page_data:
        break

    all_data.extend(page_data)
    skip += top

# Convert to DataFrame
df = pd.DataFrame(all_data)
