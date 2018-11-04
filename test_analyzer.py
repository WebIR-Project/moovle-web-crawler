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

if __name__ == '__main__':
    unittest.main()