import unittest
import filecmp
import subprocess
from huffman import *

class TestList(unittest.TestCase):

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
