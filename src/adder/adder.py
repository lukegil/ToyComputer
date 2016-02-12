from utils import settings, util_functions

class Accumulator(object):
    def __init__(self):
        self.accumulator = self.clear_accumulator()
        
    def get_accumulator_value(self):
        return self.accumulator

    def clear_accumulator(self):
        self.accumulator = util_functions.create_default_word()
        
    def set_accumulator(self, value):
        self.accumulator = value

    def add(self, value):
        ai = ArithmeticInstructions()
        self.set_accumulator(ai.add(value, self.get_accumulator_value()))

    def subtract(self, value):
        ai = ArithmeticInstructions()
        self.set_accumulator(ai.subtract(self.get_accumulator_value(), value))



class ArithmeticInstructions(object):
    def __init__(self):
        pass


    def add(self, addend1, addend2):
        addend1 = util_functions.bin_to_decimal(addend1)
        addend2 = util_function.bin_to_decimal(addend2)
        return self.decimal_to_bin(addend1 + addend2)
        
    def subtract(self, minuend, subtrahend):
        minuend = util_functions.bin_to_decimal(minuend)
        subtrahend = util_functions.bin_to_decimal(subtrahend)
        return self.decimal_to_bin(minuend - subtrahend)


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
    


test()
