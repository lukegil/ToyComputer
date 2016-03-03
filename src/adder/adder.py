from utils import settings, util_functions

class Accumulator(object):
    """The slot where the current, active number exists. When something is added, it is added to this."""
    def __init__(self):
        """set to binary string of 0s"""
        self.accumulator = self.clear_accumulator()
        
    def get_accumulator_value(self):
        """returns binary string"""
        return self.accumulator

    def clear_accumulator(self):
        """reset to binary string of 0s"""
        self.accumulator = util_functions.create_default_word()
        
    def set_accumulator(self, value):
        """ set to binary string, the length of settings.WORD_LENGTH"""
        self.accumulator = value

    def add(self, value):
        """ add a new binary string to the current one in the acc"""
        ai = ArithmeticInstructions()
        self.set_accumulator(ai.add(value, self.get_accumulator_value()))

    def subtract(self, value):
        """ subtract a new binary string to the current one in the acc"""
        ai = ArithmeticInstructions()
        self.set_accumulator(ai.subtract(self.get_accumulator_value(), value))



class ArithmeticInstructions(object):
    """ add and subtract instructions. converts binary to decimal, adds/subs, converts to bin and returns"""
    def __init__(self):
        pass

    def add(self, addend1, addend2):
        """ returns binary string"""
        addend1 = util_functions.bin_to_decimal(addend1)
        addend2 = util_functions.bin_to_decimal(addend2)
        return util_functions.decimal_to_word(addend1 + addend2)
        
    def subtract(self, minuend, subtrahend):
        """ returns binary string"""
        minuend = util_functions.bin_to_decimal(minuend)
        subtrahend = util_functions.bin_to_decimal(subtrahend)
        return util_functions.decimal_to_word(minuend - subtrahend)


def test():
    acc = Accumulator()
    
    delim = "====="

    print delim
    print "clear acc and get value"
    acc.clear_accumulator()
    print acc.get_accumulator_value()

    print delim
    print "add 0000000111 / 7 to it"
    acc.add("0000000111")
    print acc.get_accumulator_value()

    print delim
    print "subtract 0000000010 / 2 to it"
    acc.subtract("0000000010")
    print acc.get_accumulator_value()
    
    print delim
    print "clear acc and get value"
    acc.clear_accumulator()
    print acc.get_accumulator_value()
    



