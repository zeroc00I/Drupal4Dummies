#!/bin/python3
"""
Made with love by @zeroc00I
This scripts intends to grab all SA-COR items,
Then generate an updated result table
In order to easily check their respectively attack vectors 
"""

from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings()

class Drupal_Website:
	def __init__(self):
		self.advisories = "https://www.drupal.org/security"
		self.get_advisories_page()
		self.get_pagination_from_advisories_page()
		self.iterate_through_all_pages()

	def get_advisories_page(self,page=False):

		advisories = self.advisories

		if page:
			advisories = self.advisories+"/psa.rss?page={}".format(page)
		
		self.advisories_raw_content = requests.get(
			advisories,
			verify=False
		).text

		self.advisories_object_content = BeautifulSoup(
			self.advisories_raw_content,"html.parser"
		)

	def get_pagination_from_advisories_page(self):
		self.advisories_max_pagination = int(self.advisories_object_content.select(
			"a[href*='page=']"
		)[-1]["href"].split("=")[-1])

	def iterate_through_all_pages(self):
		for page in range(0,self.advisories_max_pagination):
			print("[Info] Page {}".format(page))
			self.get_advisories_page(page)
			self.get_risk_levels(page)

	def get_risk_levels(self,page=0):

		all_div_contents = self.advisories_object_content.select(
		'div[class*="views-row-"]'
		)
		
		for div in all_div_contents:
			t = div.select('a[href*="/sa-core-"]')[0]
			print("[SA] {}".format(t["href"]))
			
			risks = div.find_all("a",{"href":"/security-team/risk-levels"})
			for risk in risks:
				del(risk["title"]) 
				print(risk.text)

drupal = Drupal_Website()
