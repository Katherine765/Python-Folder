alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def encrypt (message):
    message=list(message) 
    ciphered=''
    
    for char in message:
        if char in alphabet:
            char_val=alphabet.index(char)
            if char in ['X','Y','Z']:
                new_char_val = char_val-23
            else:                    
                new_char_val = char_val+3 
            new_char=alphabet[new_char_val]  
            ciphered += new_char
        else:
            ciphered += char
    return ciphered

def decrypt (message):
    deciphered=''
    for char in message:
        if char in alphabet:
            new_char=alphabet[alphabet.index(char)-3]
            deciphered += new_char           
        else:
            deciphered += char
    return deciphered

'''
while True:
    if input('Encrypt or decrypt?  ') == 'encrypt':
        message=input('What do you want to encrypt?  ').upper()
        print(encrypt(message))
    else:
        message=input('What do you want to decrypt?  ').upper()
        print(decrypt(message))
    print()
'''