import unittest
import analyzer

class TestIsHtmlPage(unittest.TestCase):
    def setUp(self):
        pass

    def test_root_url(self):
        url = 'http://www.example.com'
        self.assertEqual(analyzer.is_html_page(url), True)

    def test_root_url_with_slash(self):
        url = 'http://www.example.com/'
        self.assertEqual(analyzer.is_html_page(url), True)

    def test_html(self):
        url = 'http://www.example.com/test.html'
        self.assertEqual(analyzer.is_html_page(url), True)

    def test_php(self):
        url = 'http://www.example.com/test.php'
        self.assertEqual(analyzer.is_html_page(url), True)

    def test_dir(self):
        url = 'http://www.example.com/test'
        self.assertEqual(analyzer.is_html_page(url), True)

    def test_dir_with_slash(self):
        url = 'http://www.example.com/test/'
        self.assertEqual(analyzer.is_html_page(url), True)

    def test_pdf(self):
        url = 'http://www.example.com/test.pdf'
        self.assertEqual(analyzer.is_html_page(url), False)

class TestNormalizeUrl(unittest.TestCase):
    def test_normal_url(self):
        url = analyzer.normalize_url('http://www.testurl.com','/mytest')
        self.assertEqual(url, 'http://www.testurl.com/mytest/')

    def test_url_with_query(self):
        url = analyzer.normalize_url('http://www.testurl.com','/mytest?q=1')
        self.assertEqual(url, 'http://www.testurl.com/mytest/')

    def test_index_html(self):
        url = analyzer.normalize_url('http://www.testurl.com','/index.html')
        self.assertEqual(url, 'http://www.testurl.com')

    def test_index_htm(self):
        url = analyzer.normalize_url('http://www.testurl.com','/test/index.htm')
        self.assertEqual(url, 'http://www.testurl.com/test/')

    def test_index_php(self):
        url = analyzer.normalize_url('http://www.testurl.com','/index.php')
        self.assertEqual(url, 'http://www.testurl.com')

    def test_index_php_with_query(self):
        url = analyzer.normalize_url('http://www.testurl.com','/index.php?q=5')
        self.assertEqual(url, 'http://www.testurl.com')

    def test_other_html(self):
        url = analyzer.normalize_url('http://www.testurl.com','/test.html')
        self.assertEqual(url, 'http://www.testurl.com/test.html')

    def test_dir_slash(self):
        url = analyzer.normalize_url('http://www.testurl.com','/test/')
        self.assertEqual(url, 'http://www.testurl.com/test/')

    def test_dir_without_slash(self):
        url = analyzer.normalize_url('http://www.testurl.com','/test')
        self.assertEqual(url, 'http://www.testurl.com/test/')


if __name__ == '__main__':
    unittest.main()