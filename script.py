from datetime import date
from os import listdir
from re import search
from jinja2 import Environment, FileSystemLoader

env = Environment(
	trim_blocks=True,
	lstrip_blocks=True,
	autoescape=False,
	loader=FileSystemLoader("templates")
)

pages = env.list_templates(filter_func=lambda t: t[0] != "_")

def listposts(postdir: str = "posts") -> list[dict]:
	def parsepostdata(postline: str) -> str:
		return search("(?<=: ).*", postline).group()

	returnlist = []

	for post in listdir(postdir):
		with open(f"{postdir}/{post}", encoding="utf8") as openpost:
			postdict = {}

			postdict["path"] = post
			postdict["title"] = parsepostdata(openpost.readline())
			postdict["date"] = parsepostdata(openpost.readline())
			postdict["datestr"] = date.fromisoformat(postdict["date"]).strftime("%b %d, %Y")
			postdict["author"] = parsepostdata(openpost.readline())
			postdict["category"] = parsepostdata(openpost.readline())
			openpost.readline()
			postdict["main"] = openpost.read()

			returnlist.insert(0, postdict)

	returnlist.pop()
	return returnlist

posts = listposts()

env.globals = {
	"POSTLIST": posts
}

for page in pages:
	with open(f"_lilylab/{page}", "w", encoding="utf8") as output:
		output.write(env.get_template(page).render())

for post in posts:
	with open(f"_lilylab/posts/{post['path']}", "w", encoding="utf8") as output:
		output.write(env.get_template("_article.html").render(post=post))