import os
from PyPDF2 import PdfFileReader, PdfFileWriter

# Huffman Tree Node
class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        # probability of symbol
        self.prob = prob

        # symbol 
        self.symbol = symbol

        # left node
        self.left = left

        # right node
        self.right = right

        # tree direction (0/1)
        self.code = ''

# Print the codes of symbols by traveling Huffman Tree #
codes = dict()

def Calculate_Codes(node, val=''):
    # huffman code for the current node
    newVal = val + str(node.code)

    if(node.left):
        Calculate_Codes(node.left, newVal)
    if(node.right):
        Calculate_Codes(node.right, newVal)

    if(not node.left and not node.right):
        codes[node.symbol] = newVal
         
    return codes        

# Calculate the probabilities of symbols in the given data #
def Calculate_Probability(data):
    symbols = dict()
    for element in data:
        if symbols.get(element) == None:
            symbols[element] = 1
        else: 
            symbols[element] += 1     
    return symbols

# Get the encoded output #
def Output_Encoded(data, coding):
    encoding_output = []
    for c in data:
        encoding_output.append(coding[c])
        
    string = ''.join([str(item) for item in encoding_output])    
    return string
        
# Calculate the space difference between compressed and non compressed data #
def size(data, coding):
    before_compression = len(data) * 8 # total bit space to stor the data before compression
    after_compression = 0
    symbols = coding.keys()
    for symbol in symbols:
        count = data.count(symbol)
        after_compression += count * len(coding[symbol]) #calculate how many bit is required for that symbol in total

    gain = "{:.2f}".format((after_compression/before_compression))
    reduction = (1-(after_compression/before_compression))*100

    print("\nSize usage before compression (in bits):", before_compression)    
    print("Size usage after compression (in bits):",  after_compression)
    print("Compression gain : ", gain)
    print("Size reduction : ", reduction)

# writing the size in an external text file
    with open('size.txt', 'w', encoding='utf-8') as f:
        
        f.write('Size before encoding (in bits):\t')
        f.write('{}'.format(before_compression))
        f.write('\t(in kb : {:.3f})'.format(before_compression/1024))
        f.write('\nSize after encoding (in bits):\t')
        f.write('{}'.format(after_compression))
        f.write('\t(in kb : {:.3f})'.format(after_compression/1024))
        f.write('\nCompression gain : {}'.format(gain))
        f.write('\nSize reduction : {:0.2f}%'.format(reduction))
        f.close()
    os.startfile(r"C:\Users\LENOVO\size.txt")
           

# Main function, Huffman code
def Huffman_coding(data):
    symbol_with_probs = Calculate_Probability(data)
    symbols = symbol_with_probs.keys()
    probabilities = symbol_with_probs.values()
    print("\nsymbols: ", symbols)
    print("probabilities: ", probabilities)
    
    nodes = []
    
    # converting symbols and probabilities into huffman tree nodes
    for symbol in symbols:
        nodes.append(Node(symbol_with_probs.get(symbol), symbol))
    
    while len(nodes) > 1:
        # sort all the nodes in ascending order based on their probability
        nodes = sorted(nodes, key=lambda x: x.prob)
    
        # pick smallest 2 nodes
        right = nodes[0]
        left = nodes[1]
    
        left.code = 0
        right.code = 1
    
        # combine the smallest 2 nodes to create new node
        newNode = Node(left.prob+right.prob, left.symbol+right.symbol, left, right)
    
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)
            
    huffman_encoding = Calculate_Codes(nodes[0])
    print("\nsymbols with codes", huffman_encoding)
    size(data, huffman_encoding)
    encoded_output = Output_Encoded(data,huffman_encoding)

# Writing the codes and the encoded output to an external text files #
    with open('symbols and problities.txt', 'w', encoding='utf-8') as f:
        sym = symbols
        prob = probabilities
        f.write('Symbols:\n')
        f.write('{}'.format(sym))
        f.write('\nProbablities:\n')
        f.write('{}'.format(prob))
        f.close()
    os.startfile(r"C:\Users\LENOVO\symbols and problities.txt")

    CODES = open('codes.txt', 'w')
    CODES.write('symbols with codes:\n{}'.format(huffman_encoding))
    os.startfile("C://Users/LENOVO/codes.txt")

    with open('encoded.txt', 'w', encoding='utf-8') as f:
        txt = encoded_output
        f.write('Encoded '+ 'output:\n')
        f.write(txt)
        f.close()
    os.startfile("C://Users/LENOVO/encoded.txt")

    return encoded_output, nodes[0]  
    
# Huffman decoding
def Huffman_Decoding(encoded_data, huffman_tree):
    tree_head = huffman_tree
    decoded_output = []
    for x in encoded_data:
        if x == '1':
            huffman_tree = huffman_tree.right   
        elif x == '0':
            huffman_tree = huffman_tree.left
        try:
            if huffman_tree.left.symbol == None and huffman_tree.right.symbol == None:
                pass
        except AttributeError:
            decoded_output.append(huffman_tree.symbol)
            huffman_tree = tree_head
        
    string = ''.join([str(item) for item in decoded_output])

# Writing the decoded output to an external text file
    with open('decoded.txt', 'w') as f:
            txt = string
            f.write('Decoded '+ 'output:\n')
            f.write(txt)
            f.close()

    os.startfile("C://Users/LENOVO/decoded.txt")

    return string        

# convering the pdf into a text file
def pdf2text(path):
    
    pdf = PdfFileReader('{}'.format(path))

    with open('Out.txt', 'w', encoding='utf-8') as f:
        for page_num in range(pdf.numPages):

            pageObj = pdf.getPage(page_num)

            try: 
                txt = pageObj.extractText()
                print(''.center(100, '-'))
            except:
                pass
            else:
                f.write('Page {0}\n'.format(page_num+1))
                f.write(''.center(100, '-'))
                f.write(txt)
        f.close()

    print("\nPdf converted to text successfully")

    os.startfile("{}".format(path))
    os.startfile("C://Users/LENOVO/Out.txt")

# Data input 

flag = True
while(flag == True):

    # ask the user for thier target
    print("\nEnter [1 - 4] to test the program\nEnter [5] to encode a text file\nEnter [6] to encode a pdf file")
    print("Enter [0] to end the program\t")
    num = int(input())

    if(num == 0):
        flag = False

    elif(num == 1):

        # First Test #
        data0 = "AAAAAAABCCCCCCDDEEEEEFFGHIIIJKKKKLLLLLLMMN010123462483" #the data for the 1st test
        print("Test 1 data input : ",data0)
        encoding, tree = Huffman_coding(data0) # calling the encoding function
        print("\nEncoded output :\n", encoding)
        reverse = input("\nWould you like to decode the file ?\tType (y) for yes and (n) for no\t")
        if(reverse == 'y'):
            print("\nDecoded Output :\n", Huffman_Decoding(encoding,tree)) # calling the decoding function

    elif(num == 2):

        # Second Test #
        f=open("C://Users/LENOVO/Desktop/TEST.txt") 
        data1 = f.read()
        print("\nTest 2 data input : ",data1)
        encoding1, tree1 = Huffman_coding(data1) # calling the encoding function
        print("\nEncoded output :\n", encoding1)
        reverse = input("\nWould you like to decode the file ?\tType (y) for yes and (n) for no\t")
        if(reverse == 'y'):
            print("\nDecoded Output :\n", Huffman_Decoding(encoding1,tree1)) # calling the decoding function

    elif(num == 3):

        # Third Test #
        f = open("C://Users/LENOVO/Desktop/TEST2.txt")
        data2 = f.read()
        print("\nTest 3 data input : ", data2)
        encoding2, tree2 = Huffman_coding(data2) # calling the encoding function
        print("\nEncoded output :\n", encoding2)
        reverse = input("\nWould you like to decode the file ?\tType (y) for yes and (n) for no\t")
        if(reverse == 'y'):
            print("\nDecoded Output :\n", Huffman_Decoding(encoding2,tree2)) # calling the decoding function

    elif(num == 4):

        # PDF Test #
    
        pdf2text('C://Users/LENOVO/Desktop/EMP214.pdf') # path to the pdf 

        f = open(r"C:\Users\LENOVO\Out.txt", "r") # path to the text after converting the pdf
        data3 = f.read()
        print("\nPDF test data input :\n",data3)
        encoding3, tree3 = Huffman_coding(data3) # calling the encoding function
        print("\nEncoded output :\n", encoding3)
        reverse = input("\nWould you like to decode the file ?\tType (y) for yes and (n) for no\t")
        if(reverse == 'y'):
            print("\nDecoded Output :\n", Huffman_Decoding(encoding3,tree3)) # calling the decoding function

    elif(num == 5):

        # custom text file #
        path = input("Enter the text file path as the following format c://pthon/\n") # path to the text 
        f=open("{}".format(path)) 
        data4 = f.read()
        print("\nTest 2 data input : ",data4)
        encoding4, tree4 = Huffman_coding(data4) # calling the encoding function
        print("\nEncoded output :\n", encoding4)
        reverse = input("\nWould you like to decode the file ?\tType (y) for yes and (n) for no\t")
        if(reverse == 'y'):
            print("\nDecoded Output :\n", Huffman_Decoding(encoding4,tree4)) # calling the decoding function

    elif(num == 6):

        # custom pdf file #
        path = input("Enter the pdf file path as the following format c://pthon/\n") # path to the pdf 
        pdf2text(path)

        f = open(r"C:\Users\LENOVO\Out.txt", "r") # path to the text after converting the pdf 
        data5 = f.read()
        print("\nPDF test data input :\n",data5)
        encoding5, tree5 = Huffman_coding(data5) # calling the encoding function
        print("\nEncoded output :\n", encoding5)
        reverse = input("\nWould you like to decode the file ?\tType (y) for yes and (n) for no\t")
        if(reverse == 'y'):
            print("\nDecoded Output :\n", Huffman_Decoding(encoding5,tree5)) # calling the decoding function