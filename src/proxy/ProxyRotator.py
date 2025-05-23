import requests
import random

# Lista de proxies
proxies = [
    "http://51.158.68.68:8811",
    "http://185.199.228.244:7492",
    "http://195.154.255.194:80",
    "http://82.165.97.35:80",
    "http://103.105.49.53:80",
    "http://185.199.231.45:8383",
    "http://45.167.125.97:9992",
    "http://212.83.143.210:80",
    "http://185.199.229.156:7492",
    "http://45.167.125.61:9992",
    "http://185.199.229.156:8383",
    "http://178.128.21.246:3128",
    "http://190.61.88.147:8080",
    "http://167.172.238.168:8080",
    "http://64.225.8.110:9981",
    "http://94.237.120.210:8080",
    "http://134.209.29.120:8080",
    "http://167.172.238.168:8080",
    "http://64.225.8.110:9981",
    "http://168.138.211.5:8080"
]


def test_proxy(p1):
    try:
        response = requests.get('https://httpbin.org/ip', proxies={"http": p1, "https": p1}, timeout=5)
        if response.status_code == 200:
            print(f"✅ Proxy funciona: {p1} — IP detectada: {response.json()['origin']}")
            return True
    except:
        return False
    print(f"❌ Proxy falló: {p1}")
    return False


def get_good():
    
  pr = random.choice(proxies)
  res = test_proxy(pr)
  while res is False:
      pr = random.choice(proxies)
      res = test_proxy(pr)
  
  print(f"Proxy {pr} operativo")
  return pr
