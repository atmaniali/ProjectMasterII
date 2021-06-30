import requests

data = requests.get('https://api.corona-dz.live/country/all').json
print(data)

# dates = []
# deathes = []
# for i in data:
#     print(i.deaths)    
print("hello")