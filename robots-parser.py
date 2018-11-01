import re
from urllib.parse import urlparse, urljoin
import downloader

class RobotParser :
	def __init__(self, user_agent=None, caching=True, use_proxies=True):
		self.user_agent = user_agent
		self.caching = caching
		self.downloader = downloader.Downloader(use_proxies=use_proxies)
		if caching:
			self.cache = {}

	def get_root_url(self, parsed_url):
		return f'{parsed_url.scheme}://{parsed_url.netloc}'

	def read_robots(self, root_url):
		robots_url = urljoin(root_url, 'robots.txt')
		while True:
			try:
				robots = self.downloader.get_page(robots_url)
				break
			except downloader.PageNotFound:
				robots = None
				break
			except downloader.NetworkError:
				pass
		return robots

	def parse_robots(self, root_url, robots):
		result = {'disalloweds': [], 'sitemaps': []}
		lines = robots.split('\n')
		line_c = 0
		while line_c < len(lines):
			line = lines[line_c]
			if re.match('User-agent:', line):
				line_c += 1
				while (re.match('Allow:', line) or re.match('Disallow:', line)) and line_c < len(lines):
					line = line[line_c]
					if re.match('Disallow:', line):
						disallow = urljoin(root_url, line.replace('Disallow:', '').strip())
						disallow = disallow.replace('*', '.*')
						result['disalloweds'].append(re.compile(disallow))
					line_c += 1
			elif re.match('Sitemap:', line):
				result['disalloweds'].append(line.replace('Sitemap:', '').strip())
		return result
		
	def is_allowed(self, url):
		parsed_url = urlparse(url)
		result = True
		parsed_robots = None

		if self.caching and parsed_url.netloc in self.cache.keys():
			parsed_robots = self.cache[parsed_url.netloc]
		else:
			root_url = self.get_root_url(parsed_url)
			robots = self.read_robots(root_url)
			if robots is not None:
				parsed_robots = self.parse_robots(root_url, robots)

		if parsed_robots is not None and len(parsed_robots['disalloweds']) > 0:
			for disallow in parsed_robots['disalloweds']:
				if disallow.match(url):
					result = False
					break
			if self.caching:
				self.cache[parsed_url.netloc] = parsed_robots
			
		return result
