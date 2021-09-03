import numpy as np

# chr(10)-->'\n' newlinefeed;
# chr(9)-->'   'tab;
# chr(32)-->' ' space;
# chr(13)-->'\r' carriage return, but it does not work stable since its used to debug the '~' problem. YOU KNOW THAT }0~
# it must be added at last. YOU KNOW WHY
CYPHER_CODE = chr(10) + chr(9) + chr(32) + '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' + chr(13)



def in_cyphercode(letter):
    ''' Checks if letter is in CYPHER_CODE'''
    if letter not in CYPHER_CODE:
        return False
    return True


def break_string_into_three(word):
    '''Breaks a string into three pieces (in this case. can be modified)
    Returns the broken pieces in a list'''

    import math

    break_string = []
    break_length = math.floor(len(word) / 3)  # determines length of each word

    # let's assume the total length of the string is 117 (ie: just an example to understand), then
    first_cut_length = break_length  # first_cut_length will be 39
    second_cut_length = break_length * 2  # second_cut_length will be 78

    start_word = word[:first_cut_length]  # start_word will be letters of word from start to 39
    middle_word = word[first_cut_length: second_cut_length]  # middle_word will be letters of word from 39 to 78
    last_word = word[second_cut_length:]  # last_word will be letters of word from 78 to end

    break_string.append(start_word)
    break_string.append(middle_word)
    break_string.append(last_word)

    return break_string


def get_random_nums_as_list(limit, count=3):
    '''Gets random numbers below the given limit  and count of 3 (count can be increased)'''
    import secrets

    r_nums = []
    for n in range(count):
        r_nums.append(secrets.randbelow(limit))

    return r_nums


def cypher(byte_array, split_lim):
    """Recieves bytes as ndarray
       Returns cyphered bytes as ndarray"""

    # do not try to change the code without completely understanding the algorithm
    vidsize = byte_array.size

    trailing_byte_count = vidsize%split_lim
    trailing_byte = None
    if trailing_byte_count > 0:
        trailing_byte = byte_array[-(trailing_byte_count):]
        byte_array = byte_array[:-(trailing_byte_count)]

    split_array = np.split(byte_array, split_lim)
    byte_array = None

    if trailing_byte is None:
        # return np.concatenate((split_array[3], split_array[2], split_array[1], split_array[0]))
        return np.concatenate(tuple(split_array[i] for i in range(split_lim-1, -1, -1)))

    else:
        # classic = np.concatenate((split_array[3], split_array[2], split_array[1], split_array[0], trailing_byte))
        return np.concatenate((np.concatenate(tuple(split_array[i] for i in range(split_lim-1, -1, -1))), trailing_byte))

def encrypt_byte_list(byte_array):
    """Recieves bytes as ndarray
    Returns encrypted bytes as ndarray"""

    #4 layers of encryption + flip
    byte_array = cypher(byte_array, 4)
    byte_array = cypher(byte_array, 8)
    byte_array = cypher(byte_array, 12)
    byte_array = cypher(byte_array, 16)
    return np.flip(byte_array)

def decrypt_byte_list(byte_array):
    """Recieves bytes as ndarray
       Returns decrypted bytes as ndarray"""

    #6 layers of decryption + flip
    byte_array = np.flip(byte_array)
    byte_array = cypher(byte_array, 16)
    byte_array = cypher(byte_array, 12)
    byte_array = cypher(byte_array, 8)
    return cypher(byte_array, 4)

def encrypt_text(data_to_encrypt):
    ''' Encrypts the given string (only ASCII). Returns encrypted string along with a code_word which is used for decryption'''

    cypher_code = CYPHER_CODE
    cypherlimit = cypher_code.index(cypher_code[-1])  # 97 in this case

    word_list_ = break_string_into_three(data_to_encrypt)  # same break_string_into_three ALGORITHM is applied in decryption
    shift_list_ = get_random_nums_as_list(cypherlimit, count=3)  # element of shift list is used/applied for element of word list respectively
    # same process/steps is followed in decryption!

    # Encrypting string text. MAIN PROCESS----------------------------------------------------------------
    encrypted_string = ''
    for index, word in enumerate(word_list_):  # shift1 for first_word, shift2 for middle_word, shift3 for last_word;
        shift_number = shift_list_[index]  # shift1 for first_word, shift2 for middle_word, shift3 for last_word;
        for letter in word:
            # ########WARINIG! DO NOT CHANGE THE ALGORITHM/LOGIC###############################
            index_number = cypher_code.index(letter)
            index_plus_shift = index_number + shift_number

            if index_plus_shift <= cypherlimit:  # if index value(index_plus_shift)exists in cyphercode
                encrypted_string += cypher_code[index_plus_shift]
            else:
                # if encryption searches for value greater than cypherlimit, then it re-evaluates from start(ie: like modulo) since there is no value after cypherlimit.
                # So bigger shift_code basically gets lowered below 95(cypherlimit). modulo always returns value(remainder) lower than the cypherlimit
                modulo = index_plus_shift % cypherlimit
                encrypted_string += cypher_code[modulo]

    interpreted_data = {'data': encrypted_string, 'code': shift_list_}
    # Returning encrypted data & encrypted shift list (encrypted shift list is the code_word for decryption)
    return interpreted_data


def decrypt_text(data_to_decrypt, shift_list_):
    ''' Decrypts the given string (only ASCII) using the code_word that is given while encryption.
    Returns decrypted string'''

    cypher_code = CYPHER_CODE
    cypherlimit = cypher_code.index(cypher_code[-1])  # 97 in this case

    word_list_ = break_string_into_three(data_to_decrypt)  # same break_string_into_three ALGORITHM is followed in encryption

    # Decrypting string text. MAIN PROCESS----------------------------------------------------------------
    decrypted_string = ''
    for index, word in enumerate(word_list_):  # shift1 for first_word, shift2 for middle_word, shift3 for last_word;
        shift_number = shift_list_[index]  # shift1 for first_word, shift2 for middle_word, shift3 for last_word;

        for letter in word:
            # ########WARINIG! DO NOT CHANGE THE ALGORITHM/LOGIC###############################
            # if letter not in cypher code, replaces letter with '?'
            if not in_cyphercode(letter):
                decrypted_string += '?'
                continue
            index_number = cypher_code.index(letter)
            index_minus_shift = index_number - shift_number

            if index_minus_shift >= 0:  # if positive;
                if index_minus_shift == 1:  # if decrypted letter points to tab (1 is the index of tab in CYPHER_CODE)
                    # adding tab space manually to make the string more readable.
                    decrypted_string += '        '
                else:
                    decrypted_string += cypher_code[index_minus_shift]
            else:  # if negative;
                modulo = abs(index_minus_shift) % cypherlimit
                if cypherlimit - modulo == 1:  # if decrypted letter points to tab (1 is the index of tab in CYPHER_CODE)
                    # adding tab space manually to make the string more readable.
                    decrypted_string += '        '
                else:
                    decrypted_string += cypher_code[cypherlimit - modulo]
    return decrypted_string


# ---------------------------------------------------------------------------------------------------
