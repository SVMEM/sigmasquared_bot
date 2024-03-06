from string import ascii_lowercase, ascii_uppercase, digits
from random import choice, choices

letters_and_digits = ascii_lowercase + digits

res = ''.join(choices(letters_and_digits, k=7))  # Сначала выбираем 4 любых буквы/цифры
res += choice(ascii_uppercase)  # Одну uppercase букву
res += ''.join(choices(letters_and_digits, k=6))  # Ещё 5 букв или цифр

print(res)