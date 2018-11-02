import unittest
from urllib.parse import urlparse
from robots_parser import RobotParser
import analyzer



class TestNormalizeUrl(unittest.TestCase):

    def test_normalize(self):
        normal_url = analyzer.normalize_url('http://www.testurl.com','mytest')
        self.assertEqual(normal_url, ['http://www.testurl.com/mytest'])

if __name__ == '__main__':
    unittest.main()