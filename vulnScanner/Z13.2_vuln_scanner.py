#!/usr/bin/env python

import requests, re, urlparse
from bs4 import BeautifulSoup

class Scanner:
	def __init__(self,url,ignore_links):
		self.session = requests.Session()
		self.target_url = url
		self.target_links = []
		self.links_to_ignore = ignore_links

	def extract_links_from(self,url):
		response = self.session.get(url)
		return re.findall('(?:href=")(.*?)"', response.content)

	def extract_forms(self,url):
		response = self.session.get(url)
		parsed_html = BeautifulSoup(response.content, 'html.parser')
		return parsed_html.findAll("form")

	def submit_form(self, form, value, url):
		action = form.get("action") 
		post_url = urlparse.urljoin(url,action)
		method = form.get("method")


		inputs_list = form.findAll("input")
		post_data = {}
		for inpt in inputs_list:
			inpt_name = inpt.get("name")

			input_type = inpt.get("type")

			inpt_value = inpt.get("value")
			if input_type == "text":
				inpt_value = value

			post_data[inpt_name] = inpt_value
		if method == "post":
			return self.session.post(post_url, data=post_data)
		return self.session.get(post_url,params=post_data)

	def crawl(self,url=None):
		if url == None:
			url = self.target_url

		href_links = self.extract_links_from(url)

		for link in href_links:
			link = urlparse.urljoin(url, link)

			if "#" in link:
				link = link.split("#")[0]

			if url in link and link not in self.target_links and link not in self.links_to_ignore:
				self.target_links.append(link)
				print(link)
				self.crawl(link) 

	def run_scanner(self):
		for link in self.target_links:
			forms = self.extract_forms(link)
			for form in forms:
				print("[+] Testing form in "+ link)
				#  here you can call the function that you will make to test for vulnerabilities
				is_vulnerable_to_xss = self.test_xss_in_form(form,link)
				if is_vulnerable_to_xss:
					print("\n\n[*] XSS vulnerability deiscovered in: "+link+"in the following form")
					print(form)

			if "=" in link:
				print("[+] Testing "+link)
				#  here you can call the function that you will make to test for vulnerabilities in the link
				is_vulnerable_to_xss = self.test_xss_in_link(link)
				if is_vulnerable_to_xss:
					print("\n\n[*] XSS vulnerability deiscovered in: "+link)
					

	def test_xss_in_link(self,url):
		xss_test_script = "<script>alert('XSS')</script>"
		url = url.replace("=","="+xss_test_script)
		response = self.session.get(url)
		return xss_test_script in response.content

	def test_xss_in_form(self,form,url):
		xss_test_script = "<script>alert('XSS')</script>"
		response = self.submit_form(form,xss_test_script,url)
		return xss_test_script in response.content
			  


# --------------------------------------------------------------------------------------------------------#
# for the webpages that requieres login :

target_url = "http://localhost/dvwa/"
links_to_ignore = ["http://localhostdvwa/logout.php"]
data_dict = {"username":"admin","password":"password","Login":"submit"}

vuln_scanner = Scanner(target_url,links_to_ignore)
vuln_scanner.session.post("http://localhost/dvwa/login.php", data=data_dict)

vuln_scanner.crawl()
vuln_scanner.run_scanner()

# forms = vuln_scanner.extract_forms("http://localhost/dvwa/vulnerabilities/xss_r/")
# print(forms)
# response = vuln_scanner.test_xss_in_form(forms[0],"http://localhost/dvwa/vulnerabilities/xss_r/")
# response = vuln_scanner.test_xss_in_link("http://localhost/dvwa/vulnerabilities/xss_r/?name=test")

# print(response)



#------------------------------------------------------------------------------------------------------------#

'''
for the webpages that doesn't requires any login:
target_url = "http://localhost/mutillidae/"
vuln_scanner = Scanner(target_url)
vuln_scanner.crawl()
'''

#-----------------------------------------------------------------------------------------------------------#