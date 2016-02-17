import settings

def create_default_word():
    return decimal_to_word(0)

def bin_to_decimal(string):
    return int(string, 2)

def decimal_to_bin(integer):
    return str(bin(integer))[2:]

def decimal_to_mem_address(integer):
    return decimal_to_bin(integer).zfill(settings.ADDRESS_LENGTH)

def decimal_to_word(integer):
    return decimal_to_bin(integer).zfill(settings.WORD_LENGTH)
    

def check_binary_string(input):
    if (not isinstance(input, basestring)): 
        raise TypeError("all inputs should be strings")

    if ( len(input) != settings.WORD_LENGTH ):
        raise ValueError("inputs should be {} characters long. Is currently {} characters".format(settings.WORD_LENGTH, len(input)))

