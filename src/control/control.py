import logging
from utils import settings, util_functions
from memory.selectron import SelectronRegister
from adder.adder import Accumulator

class BasicRegister(object):
    """Base class for Control Registers"""

    def __init__(self):
        """defaults to 0{$word_length}"""
        self.register = util_functions.create_default_word()

    def set_register(self, value):
        """sets object register overwriting whatever is there"""
        #util_functions.check_binary_string(value)
        self.register = value

    def get_register(self):
        """returns register value without updating"""
        return self.register
    

class FunctionRegister(BasicRegister):
    """The current instruction/data pair"""

    def execute(self, organs):
        """Returns True for all instructions except 'STOP'"""
        instruction = self.get_register()[:settings.INSTRUCTION_LENGTH]
        memory_address = self.get_register()[settings.INSTRUCTION_LENGTH:]

        logging.debug("Instruction : {}".format(instruction))
        logging.debug("Memory Address : {}".format(memory_address))

        o = Orders()
        return o.do(instruction, memory_address, organs)

class ControlRegister(BasicRegister):
    """Holds the right-half of the current line while left is in FR"""
    pass

class ControlCounter(object):
    """the memory address of the next instruction to pull """
    def __init__(self):
        """sets a string of zeros the length of indices in memory"""
        self.counter = "".zfill(len(str(bin(settings.WORD_COUNT))[2:]))

    def get_counter(self):
        """returns binary string"""
        return self.counter

    def increment_counter(self):
        """increments counter by 1"""
        self.set_counter(
            util_functions.decimal_to_mem_address(util_functions.bin_to_decimal(self.get_counter()) + 1)
            )
        
    #add error checking
    #
    #
    def set_counter(self, value):
        """should receive binary string"""
        self.counter = value

    

class Orders(object):
    """The enumerated orders executable by the computer"""
    
    def do(self, order, memory_address, organs):
        """ if order == "STOP" returns False, else True """
        control = organs["control"]
        memory = organs["memory"]
        adder = organs["adder"]
        
        def gotoleft():
            """Sets counter to a specified memory address"""
            control["control_counter"].set_counter(memory_address)
            control["cff"].read_from_mem()

        def gotoright():
            """Sets counter, ingests memory word, 
            and tells it to use the left-hand on the next iteration
            """
            data = memory["selectron_register"].get_data_from_memory(memory_address)
            control["control_register"].set_register(data[ (settings.WORD_LENGTH / 2): ])
            control["cff"].read_from_register()


        ### Arithmetic ###
            
        #ADDNEW
        if order == "00000001":
            data = memory["selectron_register"].get_data_from_memory(memory_address)
            adder["accumulator"].clear_accumulator()
            adder["accumulator"].add(data)

        #ADD
        elif order == "00000011":
            data = memory["selectron_register"].get_data_from_memory(memory_address)
            adder["accumulator"].add(data)
        
        #SUBNEW
        elif order == "00000010":
            data = memory["selectron_register"].get_data_from_memory(memory_address)
            adder["accumulator"].clear_accumulator()
            adder["accumulator"].subtract(data)

        #SUBTRACT
        elif order == "00000100":
            data = memory["selectron_register"].get_data_from_memory(memory_address)
            adder["accumulator"].subtract(data)
        
        
        ### FLOW CONTROL ###

        #GOTOLEFT
        elif order == "00000101":
            gotoleft()

        #GOTORIGHT
        elif order == "00000111":
            gotoright()

        #LEFTIFZERO
        elif order == "00001000":
            if ( adder["accumulator"].get_accumulator_value() == 0 ):
                gotoleft()

        #RIGHTIFZERO
        elif order == "00001001":
            if ( adder["accumulator"].get_accumulator_value() == 0 ):
                gotoright()


        ### TRANSFERS ###
        
        #SAVE
        elif order == "00001011":
            value = adder["accumulator"].get_accumulator_value()
            control["selectron_register"].post_data_to_memory(memory_address, value)


        #REPLACELEFT
        elif order == "00001111":
            word = control["selectron_register"].get_data_from_memory(memory_address)
            new_word = "{}{}{}".format(word[:settings.INSTRUCTION_LENGTH], adder["accumulator"].get_accumulator_value(), word[ (settings.word_length / 2):])
            control["selectron_register"].post_data_to_memory(memory_address, new_word)

	#REPLACELEFT
        elif order == "00010000":
            word = control["selectron_register"].get_data_from_memory(memory_address)
            new_word = "{}{}{}".format(word[ (settings.word_length / 2):], word[:settings.INSTRUCTION_LENGTH], adder["accumulator"].get_accumulator_value() )
            control["selectron_register"].post_data_to_memory(memory_address, new_word)

        #PRINT
        elif order == "00010001":
            print adder["accumulator"].get_accumulator_value()
        
	#STOP
        elif order == "00010111":
            return False
        else:
            logging.debug("No instruction found")
            return True
        logging.debug("Accumulator value after instruction : {}".format(adder["accumulator"].get_accumulator_value()))
        return True
        
class ControlFlipFlop(object):
    """Should next instruction come from register or selectron?"""
    def __init__(self):
        """defaults to pulling from selectron"""
        self.flipflop = 0

    def read_from_mem(self):
        """set value to read next instruction from memory"""
        self.flipflop = 0

    def read_from_register(self):
        """set value to read next instruction from register"""
        self.flipflop = 1

    def get_flipflop(self):
        """returns 1 / 0"""
        return self.flipflop
    
    def flip(self):
        """turns 1 -> 0 and 0 -> 1. Returns nothing"""
        if self.flipflop:
            self.flipflop = 0
        else:
            self.flipflop = 1

def meta_instructions(organs):
    """execute the next instruction. Return False if the instruction was STOP"""
    control = organs["control"]
    memory = organs["memory"]
    adder = organs["adder"]
    
    if ( not control["cff"].get_flipflop() ):
        logging.debug("============= \n Current Memory line : {}".format(control["control_counter"].get_counter()))
        control["function_register"].set_register(control["control_counter"].get_counter())
        control["control_counter"].increment_counter()
        control["cff"].flip()
        
        memory_address = control["function_register"].get_register()
        word = memory["selectron_register"].get_data_from_memory(memory_address)
        logging.debug("The retrieved word is : {}".format(word))

        #split word between control register and FR
        control["function_register"].set_register(word[:len(word)/2])
        control["control_register"].set_register(word[len(word)/2:])
        logging.debug("Function Register : {}".format(control["function_register"].get_register()))
        logging.debug("Control Register : {}".format(control["control_register"].get_register()))
        

    else:
        control["cff"].flip()
        #move instruction from Control register to FR
        control["function_register"].set_register(control["control_register"].get_register())
    
    return control["function_register"].execute(organs)



    
