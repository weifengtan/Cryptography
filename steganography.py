# steganography
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from codec import Codec, CaesarCypher, HuffmanCodes

class Steganography():
    
    def __init__(self):
        self.text = ''
        self.binary = ''
        self.delimiter = '#'
        self.codec = None

    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein)
        print(image) # for debugging
        
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)

        # convert into binary
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            self.codec = HuffmanCodes()
        binary = self.codec.encode(message)
        
        # check if possible to encode the message
        num_bytes = ceil(len(binary)//8) + 1 
        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes) 
            self.text = message + self.delimiter
            self.binary = binary
            binary = self.codec.encode(message + self.delimiter)
            
            bit_index = 0
            
            
            # your code goes here
            # you may create an additional method that modifies the image array
            
            
            for one, i in enumerate(image) :
                for two, j in enumerate(i) :
                    for three, num in enumerate(j) :
                        
                        if bit_index == len(binary) :
                            break
                        else:
                            if binary[bit_index] == '1' :
                                num |= 1
                                image[one][two][three] = num
                                
                                
                            elif binary[bit_index] == '0' :
                                num &= 254
                                image[one][two][three] = num
                                
                            bit_index += 1
                            
                            
                                

            
            
            
            cv2.imwrite(fileout, image)
                   
    def decode(self, filein, codec):
        image = cv2.imread(filein)
        print(image) # for debugging      
        flag = True
        
        # convert into text
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False
        if flag == True:
            # your code goes here
            # you may create an additional method that extract bits from the image array
            binary_data = ''
            for i in image :
                for j in i :
                    for num in j :
                        binary_number = format(num, "08b")
                        binary_data += binary_number[-1]
                        
            # update the data attributes:
            self.text = self.codec.decode(binary_data)
            self.binary = self.codec.encode(self.text)
            
            
        
    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary)          

    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()

