import unittest 
import sys
import re 
import API_Call


class TestAPI(unittest.TestCase):
    """testing pronunciation"""

    def test_word_url(self):
        """test word url function"""

        self.assertTrue(API_Call.word_url("کانادا"),(re.match(r"h.*","https://apifree.forvo.com/")))


    def test_index()



if __name__ == '__main__':
    unittest.main()