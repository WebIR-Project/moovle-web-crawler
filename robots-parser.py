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
		result = {'disallows': [], 'sitemaps': []}
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
						result['disallows'].append(re.compile(disallow))
					line_c += 1
			elif re.match('Sitemap:', line):
				result['disallows'].append(line.replace('Sitemap:', '').strip())
		return result
		
	def is_allowed(self, url):
		parsed_url = urlparse(url)
		result = True
		if self.caching and parsed_url.netloc in self.cache.keys():
			pass
		else:
			root_url = self.get_root_url(parsed_url)
			robots = self.read_robots(root_url)
			parsed_robots = None
			if robots is not None:
				parsed_robots = self.parse_robots(root_url, robots)
				# check regex
			if self.caching:
				self.cache[parsed_url.netloc] = parsed_robots
			
		return result
				