import requests
url = "https://ifconfig.co/ip"

data = requests.get(url)
print(data.text)
