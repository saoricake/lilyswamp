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

class Post:
	def __init__(self, path: str):
		with open(f"posts/{path}", encoding="utf8") as openpost:
			self.path = path
			self.title = search("(?<=: ).*", openpost.readline()).group()
			self.date = search("(?<=: ).*", openpost.readline()).group()
			self.datestr = date.fromisoformat(self.date).strftime("%b %d, %Y")
			self.author = search("(?<=: ).*", openpost.readline()).group()
			self.category = search("(?<=: ).*", openpost.readline()).group()
			openpost.readline()
			self.main = openpost.read()
	
	def __repr__(self):
		return f"{self.date} - {self.author:6} - {self.title}"

posts = [Post(p) for p in listdir("posts")[::-1] if "Post-Template" not in p]
# for p in posts: print(p)

env.globals = {
	"POSTLIST": posts,
	# "ROOTURL": "https://proflily.games/"
}

for page in (t for t in env.list_templates() if t[0] != "_"):
	with open(f"_lilylab/{page}", "w", encoding="utf8") as output:
		output.write(env.get_template(page).render())

for post in posts:
	with open(f"_lilylab/blog/{post.path}", "w", encoding="utf8") as output:
		output.write(env.get_template("_article.html").render(post=post))