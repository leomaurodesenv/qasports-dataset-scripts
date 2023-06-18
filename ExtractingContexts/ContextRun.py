from .ContextFunc import extract_contexts

# Basketball
print("Extracting basketball contexts")
extract_contexts(
    output_file="Output/basketball_contexts.csv",
    input_folder="Output/clean_json/basketball",
)

# Soccer
print("Extracting soccer contexts")
extract_contexts(
    output_file="Output/soccer_contexts.csv",
    input_folder="Output/clean_json/soccer",
)

# American Football
print("Extracting american football contexts")
extract_contexts(
    output_file="Output/football_contexts.csv",
    input_folder="Output/clean_json/football",
)
