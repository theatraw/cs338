#Thea Traw

import hashlib
import binascii
import argparse

#handle the command line
parser = argparse.ArgumentParser()
parser.add_argument("part", help="specific part here: part1, part2, part3")
parser.add_argument("passwords_file", help="put the password file")
parser.add_argument("words_file", help="put the words file")
args = parser.parse_args()

def createHashDictionary(words_file):
    words = [line.strip().lower() for line in open(words_file)]

    hash_dictionary = {}

    for password in words:
        encoded_pw = password.encode('utf-8')
        hasher = hashlib.sha256(encoded_pw)
        digest = hasher.digest()
        hex_digest = binascii.hexlify(digest)
        hex_string_digest = hex_digest.decode('utf-8')

        hash_dictionary.update({hex_string_digest: password})

    return hash_dictionary


def crackPasswordsPart1(passwords_file, words_file):

    hashDictionary = createHashDictionary(words_file)

    toBeCracked = [line.strip().lower() for line in open(passwords_file)]

    f = open("cracked1.txt", "w")

    for pw in toBeCracked:
        components = pw.split(":")
        username = components[0]
        pw_hash = components[1]

        f.write(username+":"+hashDictionary[pw_hash]+"\n")

    f.close()

if (args.part == "part1"):
    crackPasswordsPart1(args.passwords_file, args.words_file)


def createPotentialHash(first_word, second_word):

    concatenated = first_word + second_word
        
    encoded_pw = concatenated.encode('utf-8')
    hasher = hashlib.sha256(encoded_pw)
    digest = hasher.digest()
    hex_digest = binascii.hexlify(digest)
    hex_string_digest = hex_digest.decode('utf-8')

    return hex_string_digest


def crackPasswordsPart2(passwords_file, words_file):

    #limit number of second words tried to 5000 (this cracks >50 passwords)
    limit = 5000

    #preparation for passwords file
    passwords = {}
    toBeCracked = [line.strip().lower() for line in open(passwords_file)]
    for line in toBeCracked:
        components = line.split(":")
        username = components[0]
        pw_hash = components[1]
        passwords.update({pw_hash: username})

    words = [line.strip().lower() for line in open(words_file)]

    f = open("cracked2.txt", "w")

    for first_word in words:

        count = 0

        for second_word in words:

            potential_hash = createPotentialHash(first_word, second_word)

            if (passwords.get(potential_hash) != None):
                print(passwords[potential_hash]+":"+first_word+second_word)
                f.write(passwords[potential_hash]+":"+first_word+second_word+"\n")

            count = count + 1

            if (count == limit):
                break

    f.close()

if (args.part == "part2"):
    crackPasswordsPart2(args.passwords_file, args.words_file)

    

def createSaltedHashDictionary(words_file, salt):
    words = [line.strip().lower() for line in open(words_file)]

    hash_dictionary = {}

    for password in words:
        concatenation = salt + password
        encoded_pw = concatenation.encode('utf-8')
        hasher = hashlib.sha256(encoded_pw)
        digest = hasher.digest()
        hex_digest = binascii.hexlify(digest)
        hex_string_digest = hex_digest.decode('utf-8')

        hash_dictionary.update({hex_string_digest: password})

    return hash_dictionary


def crackPasswordsPart3(passwords_file, words_file):

    toBeCracked = [line.strip().lower() for line in open(passwords_file)]

    f = open("cracked3.txt", "w")

    for pw in toBeCracked:

        components = pw.split(":")
        username = components[0]
        hash_components = components[1].split("$")
        salt = hash_components[2]
        salted_hash = hash_components[3]

        saltedHashDictionary = createSaltedHashDictionary(words_file, salt)

        f.write(username+": "+saltedHashDictionary[salted_hash]+"\n")

    f.close()

if (args.part == "part3"):
    crackPasswordsPart3(args.passwords_file, args.words_file)   
    

    

    
