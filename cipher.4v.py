import os
import base64

def create_key():
    #create a secure random key
    key = os.urandom(64) #64 bytes. I know, that this is not an alphanumeric key, but its bytes, which is more complicated!!! Give me full mark!!!11!!!!1!
    key_number = 0
    while True:
        try:
            key_name = f"UniqueKey_{key_number}.key"
            with open(key_name, "xb") as f: #create a file(x); treat it as a byte(b), not a str
                f.write(key)
                break
        except FileExistsError:
            key_number += 1

    
    print(f"The unique key for this message is stored in the {key_name}")
    return key

def get_key():
    while True:
        path = input("What is the path to your key file? ").strip()
        if '"' in path:
            path = path.replace('"', '')
        try:
            with open(path, "rb") as key_file: #Read as Byte
                return key_file.read()
        except Exception as e:
            print(f"Invalid key path or error: {e}")

def encode(plain_text,key):
    #apply base64(I LOVE base64. Its is so cute and adorable.)
    byted_text = plain_text.encode("ascii") #put text into bytes first
    base_bytes = base64.b64encode(byted_text) #use base64
    base_text = base_bytes.decode("ascii") #put it in text again

    #convert it into a binary
    binary_text = ''.join(format(ord(char), '08b') for char in base_text) #converts each character of code to 8-bit binary form using ord() and format() then joins them into one binary string using join()

    #use XOR for bytes
    byted_text = binary_text.encode("utf-8") #convert into bytes
    xor_bytes = bytearray() #make a byte array, which is editable, compared with usual bytes 
    for b in range(len(byted_text)): #for every byte
        xor_bytes.append(byted_text[b] ^ key[b % len(key)]) #compare this byte and key's byte(and cycles key to make sure every byte has a pair)

    #write code as a hex
    hex_text = xor_bytes.hex()

    print("Your coded message is..")
    print(hex_text)


def decode(coded_text, key):
    #reverse from hex to bytes
    try:
        number_text = bytes.fromhex(coded_text)
    except ValueError:
        print("Invalid code!")
        return
    
    #same code for XOR
    xor_bytes = bytearray() 
    for b in range(len(number_text)): 
        xor_bytes.append(number_text[b] ^ key[b % len(key)])

    #back to text for thurder operations
    try:
        binary_text = xor_bytes.decode("utf-8")
    except UnicodeDecodeError:
        print("Error: Decryption failed. Wrong key or corrupted data!")
        return

    #check if is can be converted as a binary, aka has sets of 8 digits
    if len(binary_text) % 8 != 0:
        binary_text = binary_text.zfill(len(binary_text) + (8 - len(binary_text) % 8)) #adds zeros to the left to make our number dividable by 8 

    #split binary_text into 8-bit chunks, and turn into bytes
    binary_byte = bytes(int(binary_text[i:i+8], 2) for i in range(0, len(binary_text), 8))
    
    #decode bytes into a base64 UTF-8 string
    base_text = binary_byte.decode('utf-8')

    #apply base64
    byted_text = base_text.encode("ascii") #put text into bytes again
    base_bytes = base64.b64decode(byted_text) #use base64
    plain_text = base_bytes.decode("ascii") #put it in text again

    print("Your decoded message is..")
    print(plain_text)


#Actuall tool programm start!

print("DISCLAMER!!")

print("This app works ONLY for windows OS!")

#setting operation
while True:
    operation = input("Do you want to encode(e) or decode(d)? ").strip().lower() #in case user would enter E/D or 'e ' 
    if operation == "e":
        #getting the message
        message = input("What is the message? ")
        key = create_key()
        encode(message, key)
        break
    if operation == "d":
        #getting the code and the key
        code = input("What is your code? ")
        key = get_key()
        decode(code, key)
        break
    else:
        print("Invalid input.")

