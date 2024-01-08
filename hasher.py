import hashlib

while True:
    hasher = input("Введите пароль: ")

    if hasher.lower() == 'exit':
        break

    hashed_password = hashlib.sha256(hasher.encode()).hexdigest()
    print("Хеш пароля:", hashed_password)

