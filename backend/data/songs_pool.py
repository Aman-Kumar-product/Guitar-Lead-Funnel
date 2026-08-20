SONGS_POOL = [
    {"name": "Baarishein", "type": "beginner"},
    {"name": "Gulabi Aankhen", "type": "beginner"},
    {"name": "Kun Faya Kun", "type": "advance"},
    {"name": "Pani Da Rang", "type": "beginner"},
    {"name": "Iktara", "type": "beginner"},
    {"name": "Tum Se Hi", "type": "advance"},
    {"name": "Perfect", "type": "beginner"},
    {"name": "I'm Yours", "type": "beginner"},
    {"name": "A Thousand Years", "type": "beginner"},
    {"name": "Someone You Loved", "type": "advance"},
    {"name": "Wonderwall", "type": "beginner"},
    {"name": "Knockin' on Heaven's Door", "type": "beginner"},
    {"name": "Hotel California", "type": "advance"},
    {"name": "Sweet Child O' Mine", "type": "advance"},
    {"name": "Zombie", "type": "beginner"},
    {"name": "Nothing Else Matters", "type": "advance"},
    {"name": "River Flows in You", "type": "advance"},
    {"name": "Classical Gas", "type": "advance"},
    {"name": "Canon in D", "type": "beginner"},
    {"name": "Tere Bina", "type": "advance"}
]

# Helper to quickly look up a song's type
SONG_TYPES = {song["name"]: song["type"] for song in SONGS_POOL}
