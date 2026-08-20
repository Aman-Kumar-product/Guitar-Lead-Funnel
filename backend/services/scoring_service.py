QUALIFICATION_THRESHOLD = 50

# Scoring logic based on scoringLogic.md
SCORING_MATRICES = {
    "ad_1": {
        "q1": {1: 25, 2: 15, 3: 0, 4: 0},
        "q2": {1: 5, 2: 10, 3: 15, 4: 15},
        "q3": {1: 5, 2: 10, 3: 15, 4: 15},
        "q4": {1: 5, 2: 10, 3: 12, 4: 15}, # Time
        "q5": {1: 5, 2: 8, 3: 12, 4: 15},  # Learning method
        "q6": {1: 3, 2: 7, 3: 12, 4: 15},
    },
    "ad_2": {
        "q1": {1: 25, 2: 15, 3: 0, 4: 0},
        "q2": {1: 5, 2: 10, 3: 13, 4: 15},
        "q3": {1: 7, 2: 10, 3: 13, 4: 15, 5: 10}, # Music preference
        "q4": {1: 7, 2: 10, 3: 13, 4: 15},
        "q5": {1: 5, 2: 10, 3: 12, 4: 15},
        "q6": {1: 3, 2: 7, 3: 12, 4: 15},
    },
    "ad_3": {
        "q1": {1: 25, 2: 15, 3: 0, 4: 0},
        "q2": {1: 5, 2: 8, 3: 12, 4: 15},
        "q3": {1: 5, 2: 10, 3: 12, 4: 15},
        "q4": {1: 5, 2: 10, 3: 13, 4: 15},
        "q5": {1: 3, 2: 7, 3: 12, 4: 15},
        "q6": {1: 3, 2: 7, 3: 12, 4: 15},
    }
}

def calculate_score(campaign_source: str, answers: dict) -> dict:
    matrix = SCORING_MATRICES.get(campaign_source)
    if not matrix:
        # Fallback if campaign source is unknown
        return {"total_score": 0, "is_qualified": False}

    total_score = 0
    # Add up points safely based on answer selections
    total_score += matrix["q1"].get(answers.get("q1", 1), 0)
    total_score += matrix["q2"].get(answers.get("q2", 1), 0)
    total_score += matrix["q3"].get(answers.get("q3", 1), 0)
    total_score += matrix["q4"].get(answers.get("q4", 1), 0)
    total_score += matrix["q5"].get(answers.get("q5", 1), 0)
    total_score += matrix["q6"].get(answers.get("q6", 1), 0)

    is_qualified = total_score >= QUALIFICATION_THRESHOLD

    return {
        "total_score": total_score,
        "is_qualified": is_qualified
    }
