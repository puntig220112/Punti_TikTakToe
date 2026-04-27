import requests

r1 = requests.put('http://127.0.0.1:8000/games/1/move/1?char=X')
print(1, r1.status_code, r1.text)

r2 = requests.put('http://127.0.0.1:8000/games/1/move/2?char=X')
print(2, r2.status_code, r2.text)
