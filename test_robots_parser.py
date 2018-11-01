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

    def test_disallowed_count(self):
        root_url = 'http://www.test.com'
        robots = 'User-agent: *\nDisallow: /test/\nDisallow: /*/secret\nDisallow: /no/*'
        parsed_robots = self.robots_parser.parse_robots(root_url, robots)
        self.assertEqual(len(parsed_robots['disalloweds']), 3)

    def test_disallowed_directly(self):
        root_url = 'http://www.test.com'
        robots = 'User-agent: *\nDisallow: /test/\nDisallow: /*/secret\nDisallow: /no/*'
        parsed_robots = self.robots_parser.parse_robots(root_url, robots)
        test_url = 'http://www.test.com/test/'
        self.assertRegex(test_url, parsed_robots['disalloweds'][0])

    def test_disallowed_child(self):
        root_url = 'http://www.test.com'
        robots = 'User-agent: *\nDisallow: /test/\nDisallow: /*/secret\nDisallow: /no/*'
        parsed_robots = self.robots_parser.parse_robots(root_url, robots)
        test_url = 'http://www.test.com/test/data'
        self.assertRegex(test_url, parsed_robots['disalloweds'][0])

    def test_disallowed_regex_before(self):
        root_url = 'http://www.test.com'
        robots = 'User-agent: *\nDisallow: /test/\nDisallow: /*/secret\nDisallow: /no/*'
        parsed_robots = self.robots_parser.parse_robots(root_url, robots)
        test_url = 'http://www.test.com/doc/secret'
        self.assertRegex(test_url, parsed_robots['disalloweds'][1])

    def test_disallowed_regex_after(self):
        root_url = 'http://www.test.com'
        robots = 'User-agent: *\nDisallow: /test/\nDisallow: /*/secret\nDisallow: /no/*'
        parsed_robots = self.robots_parser.parse_robots(root_url, robots)
        test_url = 'http://www.test.com/no/data'
        self.assertRegex(test_url, parsed_robots['disalloweds'][2])

    def test_allowed(self):
        root_url = 'http://www.test.com'
        robots = 'User-agent: *\nDisallow: /test\nDisallow: /*/secret\nDisallow: /no/*'
        parsed_robots = self.robots_parser.parse_robots(root_url, robots)
        test_url = 'http://www.test.com/test2/data'
        self.assertNotRegex(test_url, parsed_robots['disalloweds'][0])
        self.assertNotRegex(test_url, parsed_robots['disalloweds'][1])
        self.assertNotRegex(test_url, parsed_robots['disalloweds'][2])

if __name__ == '__main__':
    unittest.main()