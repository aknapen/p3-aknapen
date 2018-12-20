import unittest
import filecmp
import subprocess
from huffman import *

class TestList(unittest.TestCase):

    def test_comes_before(self):
        self.assertTrue(comes_before(HuffmanNode(32, 15), HuffmanNode(97, 21)))
        self.assertTrue(comes_before(HuffmanNode(31, 15), HuffmanNode(32, 15)))
        self.assertFalse(comes_before(HuffmanNode(100, 45), HuffmanNode(18, 20)))
        self.assertFalse(comes_before(HuffmanNode(45, 10), HuffmanNode(13, 10)))

    def test_combine(self):
        node = combine(HuffmanNode(99, 15), HuffmanNode(102, 22))
        self.assertEqual(node.char, 99)
        self.assertEqual(node.freq, 37)
        self.assertEqual(node.left.char, 99)
        self.assertEqual(node.left.freq, 15)
        self.assertEqual(node.right.char, 102)
        self.assertEqual(node.right.freq, 22)
        self.assertNotEqual(node.char, 102)
        self.assertNotEqual(node.left.char, node.right.char)

    def test_cnt_freq(self):
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist)
        freqlist = cnt_freq("file1.txt")
        anslist = [3] + [0]*64
        anslist += [4, 3, 2, 1]
        self.assertListEqual(freqlist[32:101], anslist)
        self.assertNotEqual(freqlist[32:101], [3] + [0]*63 + [4, 2, 3, 1])


    def test_create_huff_tree(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        self.assertTrue(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)
        freqlist2 = cnt_freq("file1.txt")
        hufftree2 = create_huff_tree(freqlist2)
        self.assertEqual(hufftree2.freq, 13)
        self.assertEqual(hufftree2.char, 32)
        left = hufftree2.left
        right = hufftree2.right
        self.assertNotEqual(left.freq, 7)
        self.assertEqual(left.freq, 6)
        self.assertEqual(left.char, 32)
        self.assertNotEqual(left.char, 97)
        self.assertEqual(right.freq, 7)
        self.assertNotEqual(right.freq, 6)
        self.assertEqual(right.char, 97)
        self.assertNotEqual(right.char, 32)
        self.assertTrue(right.char, 97)

    def test_create_header(self):
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")
        freqlist2 = cnt_freq("file1.txt")
        self.assertEqual(create_header(freqlist2), "32 3 97 4 98 3 99 2 100 1")
        freqlist3 = cnt_freq("empty.txt")
        self.assertEqual(create_header(freqlist3), "")
        self.assertNotEqual(create_header(freqlist3), " ")

    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')
        self.assertTrue(codes[ord('f')], '0001')
        self.assertNotEqual(codes[ord('g')], '0')
        freqlist = cnt_freq("file1.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('a')], '11')
        self.assertNotEqual(codes[ord(' ')], '0')
        self.assertNotEqual(codes[ord('a')], '1')
        self.assertNotEqual(codes[ord('c')], '10')
        self.assertEqual(codes[ord('c')], '101')
        self.assertEqual(codes[ord('b')], '01')
        self.assertEqual(codes[ord('d')], '100')
        self.assertEqual(codes[ord(' ')], '00')

    def test_parse_header(self):
        freqlist = parse_header("97 2 99 5 102 3")
        self.assertListEqual(freqlist[97:103], [2, 0, 5, 0, 0, 3])
        header = create_header(cnt_freq("file1.txt"))
        freqlist = parse_header(header)
        headerlist = [3] + [0]*64 + [4, 3, 2, 1]
        self.assertListEqual(freqlist[32:101], headerlist)
        freqlist = parse_header(create_header(cnt_freq("file2.txt")))
        anslist = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist)
        self.assertIsNotNone(freqlist)
        self.assertNotEqual(freqlist, anslist[:-1])

    def test_01_textfile(self):
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file1_out.txt file1_soln.txt", shell = True)
        self.assertEqual(err, 0)
        huffman_decode("file1_soln.txt", "decode.txt")
        err = subprocess.call("diff -wb decode.txt file1.txt", shell = True)
        self.assertEqual(err, 0)

    def test_02_textfile(self):
        huffman_encode("file2.txt", "test.txt")
        err = subprocess.call("diff -wb test.txt file2_soln.txt", shell = True)
        self.assertEqual(err, 0)
        huffman_decode("file2_soln.txt", "decode.txt")
        err = subprocess.call("diff -wb decode.txt file2.txt", shell = True)
        self.assertEqual(err, 0)

    def test_03_textfile(self):
        huffman_encode("multiline.txt", "test.txt")
        err = subprocess.call("diff -wb test.txt multiline_soln.txt", shell = True)
        self.assertEqual(err, 0)
        huffman_decode("multiline_soln.txt", "decode.txt")
        err = subprocess.call("diff -wb decode.txt multiline.txt", shell = True)
        self.assertEqual(err, 0)

    def test_declaration(self):
        huffman_encode("declaration.txt", "test.txt")
        err = subprocess.call("diff -wb test.txt declaration_soln.txt", shell = True)
        self.assertEqual(err, 0)
        huffman_decode("declaration_soln.txt", "decode.txt")
        err = subprocess.call("diff -wb decode.txt declaration.txt", shell = True)
        self.assertEqual(err, 0)

    def test_empty_file(self):
        huffman_encode("empty.txt", "test.txt")
        err = subprocess.call("diff -wb test.txt empty_soln.txt", shell = True)
        self.assertEqual(err, 0)
        huffman_decode("empty_soln.txt", "decode.txt")
        err = subprocess.call("diff -wb decode.txt empty_soln.txt", shell = True)
        self.assertEqual(err, 0)

    def test_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            huffman_encode("not_existing.txt", "test.txt")
        with self.assertRaises(FileNotFoundError):
            huffman_decode("not_existing.txt", "decode.txt")

    def test_single_char_file(self):
        huffman_encode("single_char.txt", "test.txt")
        err = subprocess.call("diff -wb test.txt single_char_soln.txt", shell = True)
        self.assertEqual(err, 0)
        huffman_decode("single_char_soln.txt", "decode.txt")
        err = subprocess.call("diff -wb decode.txt single_char.txt", shell = True)
        self.assertEqual(err, 0)

    def test_single_letter_file(self):
        huffman_encode("single_letter.txt", "test.txt")
        err = subprocess.call("diff -wb test.txt single_letter_soln.txt", shell = True)
        self.assertEqual(err, 0)
        huffman_decode("single_letter_soln.txt", "decode.txt")
        err = subprocess.call("diff -wb decode.txt single_letter.txt", shell = True)
        self.assertEqual(err, 0)

    # def test_war_and_peace(self):
    #     huffman_encode("file_WAP.txt", "test.txt")
    #     huffman_decode("test.txt", "decode.txt")
    #     err = subprocess.call("diff -wb decode.txt file_WAP.txt", shell = True)
    #     self.assertEqual(err, 0)


if __name__ == '__main__':
   unittest.main()
