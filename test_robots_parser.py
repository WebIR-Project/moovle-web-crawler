import unittest
from urllib.parse import urlparse
from robots_parser import RobotParser

class TestGetRootUrl(unittest.TestCase):

    def setUp(self):
        self.robots_parser = RobotParser(user_agent='unittest')

    def test_normal_url(self):
        parsed_url = urlparse('http://www.testurl.com/mytest/1')
        self.assertEqual(self.robots_parser.get_root_url(parsed_url), 'http://www.testurl.com')

    def test_no_scheme(self):
        parsed_url = urlparse('www.testurl.com/mytest/1')
        self.assertEqual(self.robots_parser.get_root_url(parsed_url), '')

if __name__ == '__main__':
    unittest.main()