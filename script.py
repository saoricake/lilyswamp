import os
import re

siteName = "Lily Lab"

def listinputfiles() -> list:
	"""Create a list of all the files in /_content and its immediate subdirectories."""
	result = []

	for entry in os.listdir("content"):
		if ".html" in entry:
			result.append(entry)
		else:
			for subentry in os.listdir(f"content/{entry}"):
				result.append(f"{entry}/{subentry}")

	return result

def readpage(page) -> dict:
	"""Create a dictionary containing the metadata and html of a file from the /input directory."""

	def getpagedata(pageline: str) -> str:
		"""Interpret one of the first four lines in a file from the /input directory and return its appropriate data value."""
		return re.search("(?<=: ).*", pageline).group()

	pagedict = {
		"title": getpagedata(page.readline()),
		"date": getpagedata(page.readline()),
		"author": getpagedata(page.readline()),
		"tags": getpagedata(page.readline())
	}
	page.readline()
	pagedict["html"] = page.read()
	return pagedict

# TODO: create a postheader.html so posts' headers are consistent
# TODO: create a postfooter.html and figure out how to create the next/previous post links dynamically
# TODO: maybe put all the templates in a single dictionary?

with (
	open("templates/root.html", encoding="utf8") as rootTemplate,
	open("templates/head.html", encoding="utf8") as headTemplate,
	open("templates/siteheader.html", encoding="utf8") as siteHeaderTemplate,
	open("templates/sitefooter.html", encoding="utf8") as siteFooterTemplate
):
	contentList = listinputfiles()

	for listEntry in contentList:
		with (
			open(f"content/{listEntry}", encoding="utf8") as content,
			open(f"_lilylab/{listEntry}", "w", encoding="utf8") as output
		):
			rootTemplate.seek(0)
			headTemplate.seek(0)
			siteHeaderTemplate.seek(0)
			siteFooterTemplate.seek(0)

			root = rootTemplate.read()
			head = headTemplate.read()
			siteHeader = siteHeaderTemplate.read()
			siteFooter = siteFooterTemplate.read()
			main = readpage(content)

			baseURL = "." if "posts/" not in listEntry else ".."

			head = head.format(PAGE_TITLE=main["title"], SITE_NAME=siteName, PAGE_AUTHOR=main["author"], BASE_URL=baseURL)
			root = root.format(HEAD=head, SITE_HEADER=siteHeader, SITE_FOOTER=siteFooter, MAIN=main["html"])
			output.write(root)