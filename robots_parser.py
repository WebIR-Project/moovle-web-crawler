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
		result = ''
		if parsed_url.netloc != '' and parsed_url.scheme != '':
			result = f'{parsed_url.scheme}://{parsed_url.netloc}'
		return result

	def read_robots(self, root_url):
		robots_url = urljoin(root_url, 'robots.txt')
		robots = None
		while True:
			try:
				robots = self.downloader.get_page(robots_url)
				break
			except downloader.PageNotFound:
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
				user_agent = line.replace('User-agent:', '').strip().replace('*', '.*')
				if re.match(user_agent, self.user_agent):
					line_c += 1
					while line_c < len(lines):
						line = lines[line_c]
						if not re.match('Allow:', line) and not re.match('Disallow:', line):
							break
						if re.match('Disallow:', line):
							disallow = urljoin(root_url, line.replace('Disallow:', '').strip())
							disallow = disallow.replace('*', '.*')
							result['disalloweds'].append(re.compile(disallow))
						line_c += 1
					line_c -= 1
			elif re.match('Sitemap:', line):
				result['disalloweds'].append(line.replace('Sitemap:', '').strip())
			line_c += 1
		return result

	def read_parse_robots(self, root_url):
		robots = self.read_robots(root_url)
		parsed_robots = None
		if robots is not None:
			parsed_robots = self.parse_robots(root_url, robots)
		if self.caching:
				self.cache[urlparse(root_url).netloc] = parsed_robots
		return parsed_robots
		
	def is_allowed(self, url):
		parsed_url = urlparse(url)
		result = True
		parsed_robots = None

		if self.caching and parsed_url.netloc in self.cache.keys():
			parsed_robots = self.cache[parsed_url.netloc]
		else:
			root_url = self.get_root_url(parsed_url)
			parsed_robots = self.read_parse_robots(root_url)

		if parsed_robots is not None and len(parsed_robots['disalloweds']) > 0:
			for disallow in parsed_robots['disalloweds']:
				if disallow.match(url):
					result = False
					break
		return result

	def get_sitemap(self, root_url):
		parsed_url = urlparse(root_url)
		parsed_robots = None
		if self.caching and parsed_url.netloc in self.cache.keys():
			parsed_robots = self.cache[parsed_url.netloc]
		else:
			parsed_robots = self.read_parse_robots(root_url)
		if parsed_robots is not None:
			return parsed_robots['sitemaps']
		else:
			return None
