import jwt

key = "secret"
encoded = jwt.encode({"username":"zamn","admin":True}, key, algorithm="HS256")

print(encoded)
