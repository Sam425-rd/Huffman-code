import os
from PyPDF2 import PdfFileReader, PdfFileWriter

# A Huffman Tree Node
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

# A function to print the codes of symbols by traveling Huffman Tree #
codes = dict()

def Calculate_Codes(node, val=''):
    # huffman code for current node
    newVal = val + str(node.code)

    if(node.left):
        Calculate_Codes(node.left, newVal)
    if(node.right):
        Calculate_Codes(node.right, newVal)

    if(not node.left and not node.right):
        codes[node.symbol] = newVal
         
    return codes        

# A function to calculate the probabilities of symbols in given data #
def Calculate_Probability(data):
    symbols = dict()
    for element in data:
        if symbols.get(element) == None:
            symbols[element] = 1
        else: 
            symbols[element] += 1     
    return symbols

# A function to obtain the encoded output #
def Output_Encoded(data, coding):
    encoding_output = []
    for c in data:
        encoding_output.append(coding[c])
        
    string = ''.join([str(item) for item in encoding_output])    
    return string
        
# A helper function to calculate the space difference between compressed and non compressed data #
def size(data, coding):
    before_compression = len(data) * 8 # total bit space to stor the data before compression
    after_compression = 0
    symbols = coding.keys()
    for symbol in symbols:
        count = data.count(symbol)
        after_compression += count * len(coding[symbol]) #calculate how many bit is required for that symbol in total
    print("\nSpace usage before compression (in bits):", before_compression)    
    print("Space usage after compression (in bits):",  after_compression)           

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
    
        # pick 2 smallest nodes
        right = nodes[0]
        left = nodes[1]
    
        left.code = 0
        right.code = 1
    
        # combine the 2 smallest nodes to create new node
        newNode = Node(left.prob+right.prob, left.symbol+right.symbol, left, right)
    
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)
            
    huffman_encoding = Calculate_Codes(nodes[0])
    print("\nsymbols with codes", huffman_encoding)
    size(data, huffman_encoding)
    encoded_output = Output_Encoded(data,huffman_encoding)
    return encoded_output, nodes[0]  
    
 
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
    return string        

# Data input 

flag = False
while(flag == False):

    num = int(input("\nEnter a test number [1 - 4]. Enter 0 to end the program\t"))

    if(num == 0):
        flag = True

    elif(num == 1):

        """ First Test """
        data0 = "AAAAAAABCCCCCCDDEEEEEFFGHIIIJKKKKLLLLLLMMN010123462483" #the data for the 1st test
        print("Test 1 data input : ",data0)
        encoding, tree = Huffman_coding(data0)
        print("\nEncoded output :\n", encoding)
        print("\nDecoded Output :\n", Huffman_Decoding(encoding,tree))

#You can replace the file path with your own file between "" or ''

    elif(num == 2):

        """ Second Test """
        #       "paste the new location here ⬇"
        f=open(r"D:\Engineering\Curriculams\Level 2\Probability\Project\Codes\H.txt", "r") 
        data1 = f.read()
        print("\nTest 2 data input : ",data1)
        encoding, tree = Huffman_coding(data1)
        print("\nEncoded output :\n", encoding)
        print("\nDecoded Output :\n", Huffman_Decoding(encoding,tree))

    elif(num == 3):

        """ Third Test """
        #         "paste the new location here ⬇    "
        f = open(r"D:\Engineering\Curriculams\Level 2\Probability\Project\Codes\TEST2.txt", "r")
        data2 = f.read()
        print("\nTest 3 data input : ", data2)
        encoding, tree = Huffman_coding(data2)
        print("\nEncoded output :\n", encoding)
        print("\nDecoded Output :\n", Huffman_Decoding(encoding,tree))

    elif(num == 4):

        """ PDF Test """
        #          'paste the new location for a PDF file here ⬇'
        pdf = PdfFileReader(r'D:\Engineering\Curriculams\Level 2\Probability\Project\EMP214 Probability Project.pdf')

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
        print("Pdf converted to text successfully")
        #             "paste the location for the PDF file here ⬇" same as above
        os.startfile(r"C:\Users\LENOVO\Out.txt")
        #         "paste the location for the PDF file here ⬇"  same as above
        f = open(r"C:\Users\LENOVO\Out.txt", "r")
        data3 = f.read()
        print("\nPDF test data input :\n",data3)
        encoding, tree = Huffman_coding(data3)
        print("\nEncoded output :\n", encoding)
        print("\nDecoded Output :\n", Huffman_Decoding(encoding,tree))
