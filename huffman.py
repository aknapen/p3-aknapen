class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def __lt__(self, other):
        return comes_before(self, other)

def comes_before(a, b):
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    return a.freq < b.freq or (a.freq == b.freq and a.char < b.char)

def combine(a, b):
    """Creates and returns a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lesser of the a and b char ASCII values"""
    new_node = HuffmanNode(min(a.char, b.char), a.freq + b.freq)
    if comes_before(a, b):
        new_node.set_left(a)
        new_node.set_right(b)
    # else:
    #     new_node.set_left(b)
    #     new_node.set_right(a)
    return new_node

def cnt_freq(filename):
    """Opens a text file with a given file name (passed as a string) and counts the
    frequency of occurrences of all the characters within that file"""
    freqs = [0]*256
    file = open(filename, "r")
    for line in file:
        for char in line:
            freqs[ord(char)] += 1
    file.close()
    return freqs

def create_huff_tree(char_freq):
    """Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree"""
    huffman_nodes = []
    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            new_node = HuffmanNode(i, char_freq[i])
            huffman_nodes.append(new_node)
    huffman_nodes.sort()
    while len(huffman_nodes) > 1:
        first, second = huffman_nodes.pop(0), huffman_nodes.pop(0)
        new_node = combine(first, second)
        huffman_nodes.append(new_node)
        huffman_nodes.sort()
    if len(huffman_nodes) < 1:
        return None
    return huffman_nodes[0]

def create_code_helper(node, code_string, code_list):
    # Base Case
    if node.left is None and node.right is None:
        code_list[node.char] = code_string

    # Recursive Step
    if node.left:
        left = create_code_helper(node.left, code_string+"0", code_list)
    if node.right:
        right = create_code_helper(node.right, code_string+"1", code_list)
    return code_list

def create_code(node):
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    as the index into the array, with the resulting Huffman code for that character stored at that location"""
    #print("NODE:", node)
    code_string = ""
    code_list = [""]*256
    if node is None:
        return code_list
    return create_code_helper(node, code_string, code_list)

def create_header(freqs):
    """Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list associated with "aaabbbbcc, would return "97 3 98 4 99 2" """
    header = ""
    for i in range(len(freqs)):
        if freqs[i] != 0:
            header += str(i) + " " + str(freqs[i]) + " "
    return header[:-1]

def huffman_encode(in_file, out_file):
    """Takes input file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take not of special cases - empty file and file with only one unique character"""
    try:
        header = create_header(cnt_freq(in_file))
    except FileNotFoundError:
        raise FileNotFoundError("file does not exist")
    hufftree = create_huff_tree(cnt_freq(in_file))
    code_list = create_code(hufftree)
    code_string = ""
    file1 = open(in_file, "r")
    for line in file1:
        for char in line:
            code_string += code_list[ord(char)]
    if code_string != "":
        header += "\n"
    file1.close()
    file2 = open(out_file, "w")
    file2.writelines([header, code_string])
    file2.close()

def parse_header(header_string):
    """Takes header string as input
    Outputs the translated frequency list for the given header"""
    freqs = [0]*256
    header_list = header_string.split()
    for i in range(0, len(header_list)-1, 2):
        freqs[int(header_list[i])] = int(header_list[i+1])
    return freqs


def huffman_decode(encoded_file, decode_file):
    """Takes encoded file name and decode file as parameters
    Reverses the Huffman coding process on the text from the input file and writes decoded test to output file"""
    try:
        file1 = open(encoded_file, "r")
    except FileNotFoundError:
        raise FileNotFoundError("file does not exist")
    header = file1.readline()
    if header == "":
        chars = ""
    else:
        freq_list = parse_header(header)
        hufftree = create_huff_tree(freq_list)
        chars = ""
        code = file1.readline()
        if code == "":
            chars = str(chr(hufftree.char)) * freq_list[hufftree.char]
        else:
            node = hufftree
            for char in code:
                if node.left is None and node.right is None:
                    chars += chr(node.char)
                    node = hufftree
                if char == "0":
                    node = node.left
                elif char == "1":
                    node = node.right
            chars += chr(node.char)
    file2 = open(decode_file, "w")
    file2.write(chars)
    file2.close()
    file1.close()
