from .CrawlerFunc import request_link, create_csv

# Basketball
url_wiki, other_url, broken_url = request_link(
    url="https://basketball.fandom.com/wiki/Special:AllPages",
    url_base="https://basketball.fandom.com",
    url_wiki = list(),
)
print("basketball:", len(url_wiki), len(other_url), len(broken_url))
create_csv(filename="Output/basketball_links.csv", urls=url_wiki)

# Soccer
url_wiki, other_url, broken_url = request_link(
    url="https://football.fandom.com/wiki/Special:AllPages",
    url_base="https://football.fandom.com",
    url_wiki = list(),
)
print("soccer:", len(url_wiki), len(other_url), len(broken_url))
create_csv(filename="Output/soccer_links.csv", urls=url_wiki)

# American Football
url_wiki, other_url, broken_url = request_link(
    url="https://americanfootball.fandom.com/wiki/Special:AllPages",
    url_base="https://americanfootball.fandom.com",
    url_wiki = list(),
)
print("football:", len(url_wiki), len(other_url), len(broken_url))
create_csv(filename="Output/football_links.csv", urls=url_wiki)
