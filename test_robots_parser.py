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

class TestParsedRobot(unittest.TestCase):
    def setUp(self):
        self.robots_parser = RobotParser(user_agent='unittest')

    def test_disallow_count(self):
        root_url = 'http://www.test.com'
        robots = 'User-agent: *\nDisallow: /test\nDisallow: /*/secret\nDisallow: /no/*'
        parsed_robots = self.robots_parser.parse_robots(root_url, robots)
        self.assertEqual(len(parsed_robots['disalloweds']), 3)

        # label = [False, False, False, False, True]
        # test_urls = ['http://www.test.com/test', 'http://www.test.com/doc/secret', 'http://www.test.com/no/data', 
        #     'http://www.test.com/test/data', 'http://www.test.com/test2/data']
        # alloweds = []
        # for i in range(5):
        #     alloweds.append(True)
        # for disallow in disalloweds:
        #     for i in range(len(test_urls)):
        #         url = test_urls[i]
        #         if disallow.match(url):
        #             alloweds[i] = False
        # self.assertRegex(test_urls[0], disalloweds[0])

if __name__ == '__main__':
    unittest.main()