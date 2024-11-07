from .ProcFunc import process_htlm

# Basketball
print("Processing basketball")
process_htlm(
    folder_path="Output/raw_html/basketball",
    output_path="Output/clean_json/basketball",
)

# Soccer
print("Processing soccer")
process_htlm(
    folder_path="Output/raw_html/soccer",
    output_path="Output/clean_json/soccer",
)

# American Football
print("Processing american football")
process_htlm(
    folder_path="Output/raw_html/football",
    output_path="Output/clean_json/football",
)
