from datetime import date
import os
import re

siteName = "Lily Lab"

def definetemplates(templatesDir: str = "templates") -> dict:
	"""Create a dict, with each entry referring to a file in the /templates directory."""

	returnDict = {}

	for entry in os.listdir(templatesDir):
		with open(f'{templatesDir}/{entry}') as template:
			returnDict[re.search(".*(?=\.)", entry).group()] = template.read()
	
	return returnDict

templates = definetemplates()

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
postList = [p for p in contentList if "posts/" in p["path"]]
postList.reverse()

def createpostlisthtml(listlen: int = len(postList)) -> str:
	htmlListItems = ""

	i = 0
	while i <= listlen - 1:
		if i <= len(postList) - 1:
			htmlListItems += templates["postslist_item"].format(
				POST_PATH=postList[i]["path"],
				POST_DATE=postList[i]["date"],
				POST_TITLE=postList[i]["title"]
			)
			i += 1
		else:
			htmlListItems += templates["postslist_more"]
			break
	
	return templates["postslist"].format(POST_LIST_ITEMS=htmlListItems)

for contentPage in contentList:
	with open(f'_lilylab/{contentPage["path"]}', "w", encoding="utf8") as output:
		root = templates["root"]
		head = templates["head"]
		siteHeader = templates["siteheader"]
		siteFooter = templates["sitefooter"]
		baseURL = "."

		if "posts/" in contentPage["path"]:
			postHeader = templates["postheader"]
			baseURL = ".."

			postHeader = postHeader.format(
				PAGE_TITLE=contentPage["title"],
				PAGE_DATE=contentPage["date"],
				PAGE_DATE_STRING=date.fromisoformat(contentPage["date"]).strftime("%b %d, %Y"),
				PAGE_AUTHOR=contentPage["author"]
			)
			contentPage["main"] = contentPage["main"].format(POST_HEADER=postHeader)

		contentPage["main"] = contentPage["main"].format(POSTS_LIST=createpostlisthtml(5))
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



# # TODO: create a postfooter.html and figure out how to create the next/previous post links dynamically