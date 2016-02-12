import settings

def create_default_word():
    return "".zfill(settings.WORD_LENGTH)

def bin_to_decimal(self, string):
    return int(string, 2)

def decimal_to_bin(self, integer):
    return str(bin(integer))[2:].zfill(settings.WORD_LENGTH)

