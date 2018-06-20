import requests
import pypandoc
from bs4 import BeautifulSoup

# Get the website, and add a timeout
page = requests.get("https://theashenchapter.enjin.com/home/m/8190140/viewthread/21525056-field-book-tz-davidss", timeout=5)
print(page.status_code)
page.content



soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify)

file = open("entry1.html", "w", encoding="utf-8")
file.write(str(soup))
file.close()

# # entries = page.find(class='post-content')

# output = pypandoc.convert('./entry1.html', format='html', to='docx', outputfile='./example.docx')