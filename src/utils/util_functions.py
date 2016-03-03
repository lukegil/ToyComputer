import settings

def create_default_word():
    return decimal_to_word(0)

def bin_to_decimal(string):
    if string[0] == 1:
        return int("0" + string[1:], 2) * -1 
    return int(string, 2)

def decimal_to_bin(integer):
    integer = int(integer)

    if int(integer) < 0:
        integer = integer * -1
        return "-" + str(bin(int(integer)))[2:]

    return str(bin(int(integer)))[2:]
    
def decimal_to_mem_address(integer):
    return decimal_to_bin(integer).zfill(settings.ADDRESS_LENGTH)

def decimal_to_word(integer):
    bnry = decimal_to_bin(integer)
    if "-" in bnry:
        return "1" + bnry[1:].zfill(settings.WORD_LENGTH - 1)
    return decimal_to_bin(integer).zfill(settings.WORD_LENGTH)
    

def check_binary_string(input):
    if (not isinstance(input, basestring)): 
        raise TypeError("all inputs should be strings")

    if ( len(input) != settings.WORD_LENGTH ):
        raise ValueError("inputs should be {} characters long. Is currently {} characters".format(settings.WORD_LENGTH, len(input)))

