ERROR_MESSAGE_1 = '''Encryption Failed!\n\nUNSUPPORTED CHARACTERS FOUND!
        Supported characters: "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"
        TEXT WITH UNSUPPORTED CHARACTERS CAN\'T BE ENCRYPTED.'''

ERROR_MESSAGE_2 = ('''Decryption Failed!\n\nTHE DATA IS NOT READABLE! This Must've Happened Because Of The Following Reasons:
            1--->You May Have Chosen The Wrong File! Check The File Path Correctly!(or)
            2--->The Encrypted Data In The File Was Modified Manually (corrupted/erased). In This Case, The Decryption Is Not Possible...SORRY!''')

ERROR_MESSAGE_3 = "NO SUCH FILE EXISTS! Check The File Path And Try Again."

ERROR_MESSAGE_4 = "ENTERED PATH IS NOT A '.txt' FILE. Check The File Path And Try Again."

ERROR_MESSAGE_5 = "Decryption Failed!\n\nNO CODE_WORD PROVIDED! Retry with correct inputs.\nIf input is a path, change 'is_path' to 'True'\nIf input is a string, enter code_word."

# The CYPHER_CODE must not be altered. Doing so will break the encryption algorithm and crashes program
CYPHER_CODE = chr(10) + chr(9) + chr(32) + '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' + chr(13)


def del_file_if_exists(file_path):
    ''' Deletes file in file_path if exists '''

    import os

    if os.path.isfile(file_path):
        os.remove(file_path)


def check_path(f_path):
    import os

    # is path file
    if os.path.isfile(f_path) is False:
        print(ERROR_MESSAGE_3)
        print('\n\nuser_error')
        exit()

    # is path text file
    if f_path[-4:] != '.txt':
        print(ERROR_MESSAGE_4)
        print('\n\nuser_error')
        exit()


def get_file_text(f_path):
    with open(f_path, 'r') as text_file:
        return text_file.read()


def put_file_text(f_path, txt):
    del_file_if_exists(f_path)
    with open(f_path, 'w') as text_file:
        text_file.write(txt)


def get_text_data_as_dict(f_path):
    import json
    # If encrypted_json_object is modified (corrupted/erased), then json.decoder.JSONDecodeError will happen while parsing data as json (ie: line 84)
    try:
        with open(f_path, 'r') as file:
            return json.load(file)
    except json.decoder.JSONDecodeError:
        print(ERROR_MESSAGE_2)
        print('\njson.decoder.JSONDecodeError')
        exit()


def put_text_data_as_json(f_path, txt_data):
    import json
    del_file_if_exists(f_path)
    with open(f_path, 'w') as file:
        json.dump(txt_data, file)


def is_supported(letter, cypher='encryption'):
    ''' Checks if letter is supported for encryption (if letter is in CYPHER_CODE)'''

    if letter not in CYPHER_CODE:
        # if unsupported character is found while decryption, prints ERROR_MESSAGE_2
        if cypher == 'decryption':
            print(ERROR_MESSAGE_2)
            print('\nuser_error')
            exit(0)
        # if unsupported character is found while encryption, prints ERROR_MESSAGE_1
        print(ERROR_MESSAGE_1)
        print('\nuser_error')
        exit(0)
    return None


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


def encrypt_shift_list(shft_lst_to_encrypt):
    '''Gets a list of values, change it to string (each elements sepatated with coma)
    Returns the encrypted string (encrypted_shift_value to be precise)'''

    # CHANGING SHIFT FROM LIST TO STRING IN ORDER TO ENCRYPT-------------------------
    shft_str = ''
    last_index = len(shft_lst_to_encrypt) - 1

    for index, shft in enumerate(shft_lst_to_encrypt):
        shft_str += str(shft)
        if index != last_index:
            shft_str += ','

    # ########WARINIG! DO NOT CHANGE THE SHIFT CODE################################
    shift_number_to_cypher_shift_list = 87  # this has to be same for decryption
    # ########WARINIG! DO NOT CHANGE THE SHIFT CODE################################
    cypher_code = CYPHER_CODE
    cypherlimit = cypher_code.index(cypher_code[-1])  # 97 in this case

    # Encrypting shift values (shft_str)--------------------------------------------------
    encrypted_shift = ''

    for letter in shft_str:
        # ########WARINIG! DO NOT CHANGE THE ALGORITHM/LOGIC###############################
        index_number = cypher_code.index(letter)
        index_plus_shift = index_number + shift_number_to_cypher_shift_list

        if index_plus_shift <= cypherlimit:  # if index value(index_plus_shift)exists in cyphercode
            encrypted_shift += cypher_code[index_plus_shift]

        else:
            # if encryption searches for value greater than cypherlimit, then it re-evaluates from start(ie: like modulo) since there is no value after cypherlimit.
            # So bigger shift_code basically gets lowered below 95(cypherlimit). modulo always returns value(remainder) lower than the cypherlimit
            modulo = index_plus_shift % cypherlimit
            encrypted_shift += cypher_code[modulo]
        # ########WARINIG! DO NOT CHANGE THE ALGORITHM/LOGIC###############################

    return encrypted_shift


def decrypt_shift_list(shft_lst_to_decrypt):
    ''' Decrypts the code_word and returns a list containing shift values(int)'''

    # ########WARINIG! DO NOT CHANGE THE SHIFT CODE################################
    shift_number_to_cypher_shift_list = 87  # this has to be same for decryption
    # ########WARINIG! DO NOT CHANGE THE SHIFT CODE################################
    cypher_code = CYPHER_CODE
    cypherlimit = cypher_code.index(cypher_code[-1])  # 97 in this case

    # Decrypting shft_str--------------------------------------------------
    decrypted_shift = ''

    for letter in shft_lst_to_decrypt:
        # ########WARINIG! DO NOT CHANGE THE ALGORITHM/LOGIC###############################
        index_number = cypher_code.index(letter)
        index_minus_shift = index_number - shift_number_to_cypher_shift_list

        if index_minus_shift >= 0:  # if positive;
            if index_minus_shift == 1:  # if decrypted letter points to tab
                # adding tab space manually to make the string more readable.
                decrypted_shift += '        '
            else:
                decrypted_shift += cypher_code[index_minus_shift]

        else:  # if negative;
            modulo = abs(index_minus_shift) % cypherlimit
            if cypherlimit - modulo == 1:  # if decrypted letter points to tab (1 is the index of tab in CYPHER_CODE)
                # adding tab space manually since the logic doesn't.
                decrypted_shift += '        '
            else:
                decrypted_shift += cypher_code[cypherlimit - modulo]

    decrypted_shift_value = []

    # If encrypted_json_object is modified (corrupted/erased), then the IndexError & KeyError may happen while appending decrypted shift value (ie: in line 225)
    try:
        for shift_val in decrypted_shift.split(','):  # making a list of shift values from string and
            decrypted_shift_value.append(int(shift_val))  # typecasting each element with int(). since it is str()
    except IndexError:
        print(ERROR_MESSAGE_2)
        print('\nIndexError')
        exit()
    except ValueError:
        print(ERROR_MESSAGE_2)
        print('\nValueError')
        exit()

    return decrypted_shift_value  # returning as a list (of shift numbers)


def encrypt_text(data_to_encrypt, is_path=False):
    ''' Encrypts the given string (only ASCII). Returns encrypted string along with a code_word which is used for decryption'''

    # Gets text from text file (if given)
    if is_path is True:
        file_path = data_to_encrypt  # this file_path variable is needed below when we write (encrypted) data to file.
        check_path(file_path)  # checks if path is a .txt file
        data_to_encrypt = get_file_text(file_path)

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

            # Checks if letter is supported for encryption (if letter is in CYPHER_CODE). If not supported, exits code program with a error message
            is_supported(letter)
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
            # ########WARINIG! DO NOT CHANGE THE ALGORITHM/LOGIC###############################

    # Encrypting shift list (list containing shift values)---------------------------------
    encrypted_shift_list_ = encrypt_shift_list(shift_list_)

    # Interpreting the encrypted data
    interpreted_data = {'data': encrypted_string, 'code': encrypted_shift_list_}

    # Writing interpreted data to text file (if the input is a file)
    if is_path is True:
        del_file_if_exists(file_path)
        put_text_data_as_json(file_path, interpreted_data)

    # Returning encrypted data & encrypted shift list (encrypted shift list is the code_word for decryption)
    print('Encryption Successful.')
    return interpreted_data


def decrypt_text(data_to_decrypt, code_word=None, is_path=False):
    ''' Decrypts the given string (only ASCII) using the code_word that is given while encryption.
    Returns decrypted string'''

    # Reading the interpreted data from the text file (if given). Getting encryption_string & encryption_shift_list_
    if is_path is True:
        file_path = data_to_decrypt  # this file_path variable is needed below when we write (decrypted) data to file.
        check_path(file_path)  # checks if path is a .txt file
        data_to_decrypt = get_text_data_as_dict(file_path)  # file_path contains a json object (ie: {"data": "encrypted_string", "code": "encrypted_shift_list_"})

        # If encrypted_json_object is modified (corrupted/erased), then KeyError will happen while assigning 'code_word' & 'data_to_decrypt' (ie: in line 308,309)
        try:
            code_word = data_to_decrypt['code']
            data_to_decrypt = data_to_decrypt['data']  # data_to_decrypt changes from a 'dict' containing encrypted_data (ie: encrypted_string & encrypted_shift_list_)-
            # into a 'str' containing only the encrypted_string
        except KeyError:
            print(ERROR_MESSAGE_2)
            print('\nKeyError')
            exit(0)

    # Cheking whether code_word given if input is not a file
    if is_path is False and code_word is None:
        print(ERROR_MESSAGE_5)
        print('\nuser_error')
        exit(0)

    cypher_code = CYPHER_CODE
    cypherlimit = cypher_code.index(cypher_code[-1])  # 97 in this case

    word_list_ = break_string_into_three(data_to_decrypt)  # same break_string_into_three ALGORITHM is followed in encryption

    # the code_word(encrypted shift list) is decrypted using decrypt_shift_list function
    shift_list_ = decrypt_shift_list(code_word)  # element of shift list is used/applied for element of word list respectively
    # same process/steps is followed in encryption!

    # Encrypting string text. MAIN PROCESS----------------------------------------------------------------
    decrypted_string = ''

    for index, word in enumerate(word_list_):  # shift1 for first_word, shift2 for middle_word, shift3 for last_word;
        shift_number = shift_list_[index]  # shift1 for first_word, shift2 for middle_word, shift3 for last_word;

        for letter in word:
            # ########WARINIG! DO NOT CHANGE THE ALGORITHM/LOGIC###############################

            # Checks if letter is supported for decryption (if letter is in CYPHER_CODE).
            is_supported(letter, cypher='decryption')

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
            # ########WARINIG! DO NOT CHANGE THE ALGORITHM/LOGIC################################

    # Writing decrypted data to text file (if the input is a file)
    if is_path is True:
        del_file_if_exists(file_path)
        put_file_text(file_path, decrypted_string)

    # return
    print('Decryption Successful.')
    return decrypted_string


# ---------------------------------------------------------------------------------------------------

d = encrypt_text('txt_file-path', is_path=True)
# e = decrypt_text('txt_file-path', is_path=True)
