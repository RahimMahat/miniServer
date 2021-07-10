#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup   # to extract any part from any html page
import urlparse
	 



def request(url):
	try:
		return requests.get(url)
	except requests.exception.ConnectionError:
		pass


target_url = "http://localhost/mutillidae/index.php?page=dns-lookup.php?"
response = request(target_url)
content = response.content.decode('utf-8')
parsed_html = BeautifulSoup(content, 'html.parser')
forms_list = parsed_html.findAll("form")  # findAll will return the list of elements from the html page

for form in forms_list:
	# print(form)
	action = form.get("action")  # to get a specific attribute from the extracted form
	post_url = urlparse.urljoin(target_url,action)
	# print(post_url)
	method = form.get("method")
	# print(method)

	inputs_list = form.findAll("input")
	post_data = {}
	for inpt in inputs_list:
		inpt_name = inpt.get("name")
		# print(inpt_name)
		input_type = inpt.get("type")

		inpt_value = inpt.get("value")
		if input_type == "text":
			inpt_value = "test"

		post_data[inpt_name] = inpt_value

	result = requests.post(post_url, data=post_data)
	print(result.content)






	