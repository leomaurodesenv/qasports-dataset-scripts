from .QAFunc import generate_qa

# Basketball
print("Questions and answers basketball")
generate_qa(
    input_file="Output/basketball_contexts.csv",
    output_file="Output/basketball_qa.csv",
    test=True,
)

# Soccer
print("\n\nQuestions and answers soccer")
generate_qa(
    input_file="Output/soccer_contexts.csv",
    output_file="Output/soccer_qa.csv",
    test=True,
)

# American Football
print("\n\nQuestions and answers american football")
generate_qa(
    input_file="Output/football_contexts.csv",
    output_file="Output/football_qa.csv",
    test=True,
)
