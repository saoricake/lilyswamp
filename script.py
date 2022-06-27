import os
import re

siteName = "Lily Lab"

def listcontent(contentDir: str = "content") -> list[dict]:
	"""Creates a list of dicts, each referring to a file in the /content directory."""

	def getcontentdata(contentPath: str) -> dict:
		"""Create a dict containing information about a file in the /content directory."""

		with open(f'{contentDir}/{contentPath}', encoding="utf8") as contentPage:
			returnDict = {}

			returnDict["path"] = contentPath
			returnDict["title"] = re.search("(?<=: ).*", contentPage.readline()).group()
			returnDict["date"] = re.search("(?<=: ).*", contentPage.readline()).group()
			returnDict["author"] = re.search("(?<=: ).*", contentPage.readline()).group()
			returnDict["tags"] = re.search("(?<=: ).*", contentPage.readline()).group()
			contentPage.readline()
			returnDict["main"] = contentPage.read()

			return returnDict

	returnList = []

	for entry in os.listdir(contentDir):
		if ".html" in entry:
			returnList.append(getcontentdata(entry))
		else:
			for subEntry in os.listdir(f"{contentDir}/{entry}"):
				returnList.append(getcontentdata(f"{entry}/{subEntry}"))
	
	return returnList

contentList = listcontent()

def definetemplates(templatesDir: str = "templates") -> dict:
	"""Create a dict, with each entry referring to a file in the /templates directory."""

	returnDict = {}

	for entry in os.listdir(templatesDir):
		with open(f'{templatesDir}/{entry}') as template:
			returnDict[re.search(".*(?=\.)", entry).group()] = template.read()
	
	return returnDict

templates = definetemplates()

for contentPage in contentList:
	with open(f'_lilylab/{contentPage["path"]}', "w", encoding="utf8") as output:
		root = templates["root"]
		head = templates["head"]
		siteHeader = templates["siteheader"]
		siteFooter = templates["sitefooter"]

		baseURL = "." if "posts/" not in contentPage["path"] else ".."

		head = head.format(
			PAGE_TITLE=contentPage["title"],
			SITE_NAME=siteName,
			PAGE_AUTHOR=contentPage["author"],
			BASE_URL=baseURL
		)
		root = root.format(
			HEAD=head,
			SITE_HEADER=siteHeader,
			SITE_FOOTER=siteFooter,
			MAIN=contentPage["main"]
		)

		output.write(root)



# # TODO: create a postheader.html so posts' headers are consistent
# # TODO: create a postfooter.html and figure out how to create the next/previous post links dynamically
# # TODO: maybe put all the templates in a single dictionary?