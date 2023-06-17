from .FetchFunc import fetch_all_html

# Basketball
print("Fetching basketball")
fetch_all_html(
    links_path="Output/basketball_links.csv",
    folder_path="Output/raw/basketball",
    test=True,
)

# Soccer
print("Fetching soccer")
fetch_all_html(
    links_path="Output/soccer_links.csv",
    folder_path="Output/raw/soccer",
    test=True
)

# American Football
print("Fetching american football")
fetch_all_html(
    links_path="Output/football_links.csv",
    folder_path="Output/raw/football",
    test=True
)
