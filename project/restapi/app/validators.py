from rest_framework import serializers


def validate_password(data):
    """If password has no letters or no numbers"""
    password = tuple(data)
    password_length = len(password)
    permitted_numbers = tuple('1234567890')
    permitted_letters = tuple('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
    permitted_symbols = (*permitted_numbers, *permitted_letters)
    how_much_non_numbers = 0
    how_much_non_letters = 0

    for letter in password:
        if letter not in permitted_symbols:
            raise serializers.ValidationError('Password must contain letters and numbers')

    for symbol in password:
        if symbol not in permitted_numbers:
            how_much_non_numbers += 1

    for symbol in password:
        if symbol not in permitted_letters:
            how_much_non_letters += 1

    if how_much_non_numbers == password_length or how_much_non_letters == password_length:
        raise serializers.ValidationError('Password must contain letters and numbers')
