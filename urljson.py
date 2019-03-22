import urllib

conditions = {"id": 83500, "type/name": "Printer", "name": "TEST API PRINTER"} 
query = {"pageSize": 1000, "conditions": conditions}
params = urllib.urlencode(query)
final_url = str(APIurl) + "&" + str(params)
#response = requests.get(url=final_url)
