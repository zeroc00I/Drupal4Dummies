#!/bin/python3
"""
Made with love by @zeroc00I
This scripts intends to grab all SA-COR items,
Then generate an updated result table
In order to easily check their respectively attack vectors 
"""

from bs4 import BeautifulSoup
import requests
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings()

class Drupal_Website:
	def __init__(self):
		self.advisories = "https://www.drupal.org/security"
		self.get_advisories_page()
		self.get_pagination_from_advisories_page()
		self.iterate_through_all_pages()

	def get_advisories_page(self,page=0):

		advisories_pagination = self.advisories+"/psa.rss?page={}".format(page)
		
		self.advisories_raw_content = requests.get(
			advisories_pagination,
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
		attack_vector_banner = """
AC: [A]ccess [c]omplexity | A: [A]uthentication
CI: [C]onfidentiality [i]mpact | II: [I]ntegrity [i]mpact 
E: [E]xploit | TD: [T]arget [d]istribution
		"""
		print(attack_vector_banner,end="")

		for page in range(0,self.advisories_max_pagination):
			print("\nPage {}".format(page))
			print("|   SA Number  |    Risk   | Attack Vector")
			self.get_advisories_page(page)
			try:
				self.get_risk_levels(page)
			except Exception as e:
				page+=1 # counter starts in 0
				print("[Warn] Exiting... Couldn't find core items on page {}".format(page))
				print(e)
				exit()

	def get_risk_levels(self,page=0):

		all_div_contents = self.advisories_object_content.select(
		'div[class*="views-row-"]'
		)
		
		for div in all_div_contents:
			sa_core = div.select('a[href*="/sa-core-"]')[0]["href"].replace('/sa-core-','')
			
			print("|   {}   | ".format(sa_core),end = '')
			
			risks = div.find_all("a",{"href":"/security-team/risk-levels"})
			for risk in risks:
				del(risk["title"]) 
				risk_score = re.findall(r'\d{1,2}.*\d{1,2}',risk.prettify())[0]
				attack_vector = re.findall(r'AC.*',risk.prettify())[0]

				print("  {}   | {}".format(risk_score,attack_vector))

drupal = Drupal_Website()
