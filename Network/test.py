import hash

wifi = {
    "wifiname":"homenetwork",
    "password": "12345678",
}

token = hash.encrypt_data(wifi)
print(token)