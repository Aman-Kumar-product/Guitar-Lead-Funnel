import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.scoring_service import calculate_score
from backend.services.result_service import generate_result
import itertools

def test_all_combinations():
    campaigns = ["ad_1", "ad_2", "ad_3"]
    options = [1, 2, 3, 4] # Assuming 4 options per question max
    
    for campaign in campaigns:
        for combo in itertools.product(options, repeat=6):
            answers = {
                "q1": combo[0],
                "q2": combo[1],
                "q3": combo[2],
                "q4": combo[3],
                "q5": combo[4],
                "q6": combo[5]
            }
            try:
                score = calculate_score(campaign, answers)
                res = generate_result(campaign, answers)
            except Exception as e:
                print(f"FAILED on {campaign} with {answers}: {e}")
                return
    print("All combinations tested successfully!")

if __name__ == "__main__":
    test_all_combinations()
