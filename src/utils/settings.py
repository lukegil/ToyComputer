WORD_LENGTH = 36
INSTRUCTION_LENGTH = 8
SELECTRON_WIDTH = 10
SELECTRON_HEIGHT = 10
WORD_COUNT = 1023
ADDRESS_LENGTH = len(str(bin(WORD_COUNT))[2:])
if ( (INSTRUCTION_LENGTH + ADDRESS_LENGTH) * 2 != WORD_LENGTH):
    raise ValueError("word length incorrect")
