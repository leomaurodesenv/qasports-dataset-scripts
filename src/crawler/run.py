from ..module import OUTPUT_PATH, wiki_pages
from .module import create_csv, request_link

# Get the URLs
for wiki_page in wiki_pages:
    url, url_base, csv_name = (
        wiki_page["url"],
        wiki_page["url_base"],
        wiki_page["csv_name"],
    )
    url_wiki, broken_url = request_link(url=url, url_base=url_base, url_wiki=list())
    url_wiki.sort()
    print(f"{csv_name}:", len(url_wiki), ", broken urls:", len(broken_url))
    create_csv(filename=(OUTPUT_PATH / csv_name), urls=url_wiki)
