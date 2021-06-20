import http.client

conn = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")

api_key = '7338400324341a6e0cb891835c254b28'

headers = {
    'x-rapidapi-key': "1030a0e474msh06ceece1b7430fdp19d373jsnf993c2bb0fbe",
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com"
    }

conn.request("GET", "/seasons/", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))