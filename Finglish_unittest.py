import unittest 
import sys
import re 
import API_Call


class TestStringMethods(unittest.TestCase):
    """testing pronunciation"""

    def test_word_url(self):
        """test word url function"""

        self.assertTrue(API_Call.word_url("کانادا"),(re.match(r"h.*","https://apifree.forvo.com/")))





if __name__ == '__main__':
    unittest.main()