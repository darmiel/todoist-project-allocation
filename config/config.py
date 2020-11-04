API_KEY: str = "a8f2f6ff4416d4d259ca7c3acd6878f3e4a59700"
PROJECT_ID: int = 2249063489

USERS: dict = {
    "daniel": {
        "uid": 30148411,
        "name": "Daniel",
        "ignored_sections": [
            24516623, # Französisch
            24516667 # eGK Zivilcourage
        ]
    },
    "simon": {
        "uid": 30542704,
        "name": "Simon",
        "ignored_sections": []
    }
}

"""
Unfortunately I did not find a page with the exact flood restrictions. 
I just hope that every 30 seconds is not too much. 😅
"""
DELAY: int = 30 # seconds

"""
Automatically close tasks
when sub tasks finished
"""
AUTO_CLOSE: bool = True