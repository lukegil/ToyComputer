from utils import settings, util_functions
from memory.selectron import SelectronRegister

class BasicRegister(object):
    def __init__(self):
        self.register = util_functions.create_default_word()

    def set_register(self, value):
        self.register = value

    def get_register(self):
        return self.register
    

# instruction {{INSTRUCTION}}{{MEM_ADDRESS}}
class FunctionRegister(BasicRegister):
    def execute(self):
        instruction = self.get_register()[:settings.INSTRUCTION_LENGTH]
        o = Orders()
        o.do(instruction)

class ControlRegister(BasicRegister):
    pass

class ControlCounter(object):
    def __init__(self):
        self.counter = "".zfill(len(str(bin(settings.WORD_COUNT))]2:])

    def get_counter(self):
        return self.counter

    def increment_counter(self):
        self.counter = util_functions.decimal_to_bin(util_functions.bin_to_decimal(self.counter) + 1)

    #add error checking
    def set_counter(self, value):
        self.counter = value

    

class Orders(object):
    
    def do(self, order):
        pass

class ControlFlipFlop(object):
    def __init__(self):
        self.flipflop = 0

    def read_from_mem(self):
        self.flipflop = 0

    def read_from_register(self):
        self.flipflop = 1

    def get_flipflop(self):
        return self.flipflop
    
    def flip(self):
        if self.flipflop:
            self.flipflop = 0
        else:
            self.flipflop = 1

def meta_instructions():
    organs = init()
    if ( not organs.cff.get_flipflop() ):
        organs.function_register.set_register(organs.control_counter.get_counter())
        organs.control_counter.increment_counter()
        organs.cff.flip()
        
        word = organs.selectron_register.get_data_from_memory(mem_address)
        
        #split word between control register and FR
        organs.function_register.set_register(word[len(word)/2:])
        organs.control_register.set_register(word[:len(word)/2])
    else:
        #move instruction from Control register to FR
        pass
    
    organs.function_register.execute()

def init():
    cff = ControlFlipFlop()
    control_counter = ControlCounter()
    #need to have inited SelectronMatix
    selectron_register = SelectronRegister(selectron_matrix)
    function_register = FunctionRegister()

    return {"cff" : cff, 
    "control_counter" : control_counter,
    "selectron_register" : selectron_register,
    "function_register" : function_register
    }
