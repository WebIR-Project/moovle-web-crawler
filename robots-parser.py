import re
from urllib.parse import urlparse, urljoin
import downloader

class RobotParser :
	def __init__(self, caching=True, use_proxies=True):
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

	def parse_robots(self, robots):
		pass
		
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
				parsed_robots = self.parse_robots(robots)
				# check regex
			if self.caching:
				self.cache[parsed_url.netloc] = parsed_robots
			
		return result
				