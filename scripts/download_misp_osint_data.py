misp_url = 'https://misppriv.circl.lu'
misp_key = ''
misp_verifycert = True

from pymisp import ExpandedPyMISP

misp = ExpandedPyMISP(misp_url, misp_key, misp_verifycert)
events = misp.search(tags=['osint:source-type="blog-post"'], last="1095d", pythonify=True)

sources = []

for e in events:
    for a in e.attributes:
        if a.category == "External analysis":
            if a.type == "link":
                if not "twitter.com" in a.value:
                    if not "github.com" in a.value:
                        sources.append(a.value)

import newspaper, csv

with open('data.csv', 'w', encoding="UTF-8") as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['url', 'title', 'text', 'meta-lang', 'publish-date'])

for s in sources:
    article = newspaper.Article(s)
    try:
        article.download()
        article.parse()
        article.title

        with open('data.csv', 'a', encoding="UTF-8") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([article.canonical_link, article.title, article.text.replace('\n',''), article.meta_lang, article.publish_date])

    except Exception as e:
        print("Silence is golden")

