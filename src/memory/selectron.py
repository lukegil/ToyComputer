import pprint
from utils import settings
#receives input from the selectron matrix and then send it to Control when it wants
# The primary purpose of this register is to assemble a word, from the forty different selectrons that normally exist
# currently, though, the selectron outputs the proper 40bit strings, so this is more of a way station

class SelectronRegister(object):
    
    #there should be a 'build computer' function 
    #that builds th SelectronMatrix and then passes it here
    def __init__(self, s):
        self.selectron_matrix = s

    def check_string_length(self, input):
        if (not isinstance(input, basestring)): 
            raise TypeError("all inputs should be strings")
        
        if ( len(input) != self.selectron_matrix.get_word_length() ):
            raise ValueError("inputs should be {} characters long".format(self.selectron_matrix.get_word_length))
        
    def post_data_to_memory(self, address, data):
        self.check_string_length(data)
        self.selectron_matrix.post_data(address, data)
        

    #Future Feature
    #when the Selectron Matrix is a series of n matrices, this will request from each one. For now, its just requesting it from the one
    def get_data_from_memory(self, address):
        return self.selectron_matrix.get_data(address)



# 1. Build the matrix
# 2. import data # this will be done by a bunch of posts
# 3. get data from a certain address, post to register, return register
# 4. post data to a certain address

class SelectronMatrix(object):
    def __init__(self, x_axis, y_axis, z_axis):
        self.word_count = x_axis * y_axis
        self.word_length = z_axis
        self.selectron_dictionary = {}

        #create the empty default word
        default_word = ""
        for i in range(self.word_length):
            default_word += "0"
        
        #create as many slots in the dict as there ought to be words
        for k in range(self.word_count):
            #turn to binary and pad with as many 0s as the largest address's length
            self.selectron_dictionary[
                str(bin(k))[2:].zfill(
                    len(str(bin(self.word_count))[2:])
                    )] = default_word
            
    def get_word_length(self):
        return self.word_length

    def get_data(self, address):
        try:
            return self.selectron_dictionary[address]
        except KeyError:
            raise KeyError("address is out of range of Selectron. It should be between 0 and {}".format(self.word_count))
        

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
