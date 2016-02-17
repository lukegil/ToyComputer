import pprint
from utils import settings, util_functions

class SelectronRegister(object):
    """Saves data to Selectron and retrieves data from it

    Normally, the purpose of this would be take a bit from each 
    selectron and assemble it into a single value. In the current
    implementation, however, there is only one, three dimensional 
    selectron, so no assembly required. This therefore simply acts 
    as an api for the Selectron
    """
    def __init__(self, s):
        """requires the SelectronMatrix as an arg"""
        self.selectron_matrix = s

    def post_data_to_memory(self, address, data):
        """address : binary string corresponding to place in memory. 
        data : binary string to be posted.
        """
        util_functions.check_binary_string(data)
        self.selectron_matrix.post_data(address, data)
        
    def get_data_from_memory(self, address):
        """returns a binary string"""
        return self.selectron_matrix.get_data(address)


class SelectronMatrix(object):
    """The fast-memory organ (RAM) for the machine"""
    def __init__(self, x_axis, y_axis, z_axis):
        """Build the selectron. 
        
        x_axis, y_axis : the sum is how many 'words' the memory ought to hold
        z_axis : the 'word length'. 
        	Words are a theoretical minimum of 18 bits. Two sets of 
                instructions (8 bits each) + each instruction has a
                corresponding memory address--the address of the data on
                which its acting. 
        Each slot in memory receives a default value of 0
	"""
        self.word_count = x_axis * y_axis
        self.word_length = z_axis
        self.selectron_dictionary = {}
        default_word = util_functions.create_default_word()
        
        for k in range(settings.WORD_COUNT):
            self.selectron_dictionary[util_functions.decimal_to_mem_address(k)] = default_word
            

    def get_data(self, address):
        try:
            return self.selectron_dictionary[address]
        except KeyError:
            raise KeyError("address is out of range of Selectron. It should be between 0 and {}".format(settings.WORD_COUNT))
        

    def post_data(self, address, value):
        self.selectron_dictionary[address] = value

    def dump_selectron(self):
        return self.selectron_dictionary


  
def test():
    print "5x5x3 matrix:"
    s = SelectronMatrix(5, 5, 3)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(s.dump_selectron())
    print "======"
    print "data posted to memory"
    sr = SelectronRegister(s)
    sr.post_data_to_memory("00010", "110")
    pp.pprint(s.dump_selectron())

    print "===="
    print "get data from memory"
    print sr.get_data_from_memory("00010")

if __name__ == "__main__":    
    test()
