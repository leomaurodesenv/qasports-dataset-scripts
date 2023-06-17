from .CrawlerFunc import Request, create_csv

# Basketball
url_wiki, other_url, broken_url = Request(
    url="https://basketball.fandom.com/wiki/Special:AllPages",
    url_base="https://basketball.fandom.com",
)
print("basketball:", len(url_wiki), len(other_url), len(broken_url))
create_csv(filename="Output/basketball_links.csv", urls=url_wiki)

# Soccer
url_wiki, other_url, broken_url = Request(
    url="https://football.fandom.com/wiki/Special:AllPages",
    url_base="https://football.fandom.com",
)
print("soccer:", len(url_wiki), len(other_url), len(broken_url))
create_csv(filename="Output/soccer_links.csv", urls=url_wiki)

# American Football
url_wiki, other_url, broken_url = Request(
    url="https://americanfootball.fandom.com/wiki/Special:AllPages",
    url_base="https://americanfootball.fandom.com",
)
print("football:", len(url_wiki), len(other_url), len(broken_url))
create_csv(filename="Output/football_links.csv", urls=url_wiki)
