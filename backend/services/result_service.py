# Define the actual content for the 12 result archetypes based on results.md
from data.songs_pool import SONG_TYPES

RESULTS_DATA = {
    "1": {
        "title": "The Solo Explorer 🎸",
        "content": "Your Profile: You are starting fresh and love figuring things out at your own pace. The trap for Solo Explorers is getting overwhelmed by too many random tutorials. Your immediate focus shouldn't be complex theory—it should be building finger strength and muscle memory.\n\n- Current Stage: Ground zero (building the foundation).\n- Next Milestone 1: Mastering proper guitar posture and pick grip.\n- Next Milestone 2: Memorizing your first 3 open chords (E minor, A suspended, D major).\n- Next Milestone 3: Switching between those 3 chords without pausing.\n- Practice Pattern: 10–15 minutes of highly focused chord-switching drills daily."
    },
    "2": {
        "title": "The Structured Starter 🎸",
        "content": "Your Profile: You are a beginner who thrives on a clear, step-by-step roadmap. Without a structured path, you might feel lost or frustrated. The best approach for you is a linear progression where every new skill builds directly on the last one.\n\n- Current Stage: Ready for a guided foundation.\n- Next Milestone 1: Understanding how to read chord charts and basic tabs.\n- Next Milestone 2: Playing your first 4-chord progression in a loop.\n- Next Milestone 3: Playing a simplified, one-string melody to build dexterity.\n- Practice Pattern: Consistent 20-minute sessions following a predefined weekly goal."
    },
    "3": {
        "title": "The Intuitive Player 🎸",
        "content": "Your Profile: You already know your way around the fretboard and pick up concepts visually. However, you've likely hit the \"YouTube Plateau\"—knowing isolated riffs and chords, but struggling to play full songs seamlessly. Your focus now is bridging the gap between chords and rhythm.\n\n- Current Stage: The transition zone (moving from chords to music).\n- Next Milestone 1: Locking in a consistent strumming pattern with a metronome.\n- Next Milestone 2: Conquering your first major barre chord (F Major).\n- Next Milestone 3: Playing a full 3-minute song from start to finish without stopping.\n- Practice Pattern: 20–30 minutes blending new chord shapes with rhythm exercises."
    },
    "4": {
        "title": "The Guided Performer 🎸",
        "content": "Your Profile: You have the basics down and you learn best with expert feedback. You aren't just looking to play alone in your room; you want the confidence to perform. Your next steps involve cleaning up your technique and adding dynamic expression to your playing.\n\n- Current Stage: Technique polish and repertoire building.\n- Next Milestone 1: Smoothing out chord transitions for zero hesitation.\n- Next Milestone 2: Adding dynamics (loud and soft strumming) to breathe life into songs.\n- Next Milestone 3: Mastering a complete, performance-ready track.\n- Practice Pattern: 30+ minutes split between warm-ups, repertoire, and performance simulation."
    },
    "5": {
        "title": "Bollywood Foundation 🎵",
        "content": "Your Next Steps: As a beginner who loves Bollywood, you don't need to learn complicated scales yet. Many of your favorite acoustic Hindi tracks are built on just 3 or 4 simple chords. We need to get your fingers comfortable with these core shapes so you can start singing along.\n\n- Current Level: Building the chord vocabulary.\n- Target Skill: Open chord clarity and basic down-strumming.\n- Recommended Songs: \"Tum Hi Ho\" (simplified version), \"Kabira\" (intro chords), \"Shaayad\".\n- Your Next Challenge Song: \"Channa Mereya\" (requires faster chord changes)."
    },
    "6": {
        "title": "Indie Chord Builder 🎵",
        "content": "Your Next Steps: You love the acoustic, indie-pop sound, which relies heavily on rhythm and vibe. Right now, your foundation is a blank slate. Your fastest path to playing this genre is mastering the \"magic four\" chords (G, D, Em, C) that power thousands of pop and indie hits.\n\n- Current Level: Establishing chord muscle memory.\n- Target Skill: Clean transitions and keeping a steady beat.\n- Recommended Songs: \"Riptide\", \"Yellow\" (Coldplay), \"Let Her Go\" (simplified).\n- Your Next Challenge Song: \"Wonderwall\" (focusing entirely on that iconic strumming pattern)."
    },
    "7": {
        "title": "Bollywood Unplugged 🎵",
        "content": "Your Next Steps: You already know your basic chords and can navigate a fretboard. To capture that authentic Bollywood unplugged sound, it is time to move beyond basic open chords. You are ready to introduce barre chords, fingerpicking, and more emotional strumming dynamics.\n\n- Current Level: Intermediate transition phase.\n- Target Skill: Barre chord stamina and arpeggio picking.\n- Recommended Songs: \"Pee Loon\", \"Ilahi\", \"Agar Tum Saath Ho\".\n- Your Next Challenge Song: \"Zaalima\" (requires moving barre chord shapes smoothly)."
    },
    "8": {
        "title": "Indie Rhythm Master 🎵",
        "content": "Your Next Steps: You already have the foundation to play complete songs. Now, you need to make them groove. The best indie and pop tracks aren't just strummed; they use percussive slaps, palm muting, and complex syncopation. \n\n- Current Level: Advanced rhythm and stylization.\n- Target Skill: Percussive strumming and dynamic control.\n- Recommended Songs: \"Fast Car\" (Tracy Chapman), \"Ho Hey\", \"Shape of You\" (percussive acoustic version).\n- Your Next Challenge Song: \"Stop This Train\" (John Mayer - introducing slap-picking technique)."
    },
    "9": {
        "title": "The Steady Builder Path ⏱️",
        "content": "Your Timeline: 8 to 12 Weeks to Your First Song\nYour first milestone is not rushing into a full song—it is building a physical foundation. Because your practice time will be spread out, the secret is making those short sessions highly intentional. Focus purely on basic chord shapes and simple rhythm. \n\n- Starting Point: Blank slate, building finger calluses.\n- Learn Next: 3 core open chords and how to press the strings without buzzing.\n- Song Targets: \"Stand By Me\" or \"A Thousand Years\" (simplified).\n- The Accelerator: Leaving your guitar out on a stand. Picking it up for just 5 minutes a day will cut this timeline by 20%."
    },
    "10": {
        "title": "The Fast-Track Foundation ⏱️",
        "content": "Your Timeline: 4 to 6 Weeks to Your First Song\nYou have the absolute best asset a beginner can have: consistency. With regular practice, muscle memory forms rapidly. You will surpass the frustrating \"buzzing strings\" phase quickly, allowing you to focus on the fun part: making actual music.\n\n- Starting Point: Highly motivated beginner.\n- Learn Next: Chord transitions using a metronome to force your fingers to move in time.\n- Song Targets: \"Perfect\" (Ed Sheeran) or \"Love Yourself\" (Justin Bieber).\n- The Accelerator: Dedicating the first 5 minutes of your daily practice strictly to a finger-stretching warm-up."
    },
    "11": {
        "title": "The Weekend Warrior Path ⏱️",
        "content": "Your Timeline: 6 to 8 Weeks to Smooth Performance\nYou already know your basic chords, so you are past the hardest phase of learning guitar. However, inconsistent practice can make progress feel stagnant. Your roadmap involves maximizing your weekend sessions to string those chords together into fluid, recognizable songs.\n\n- Starting Point: Familiar with basics, needs fluidity.\n- Learn Next: Syncopated strumming patterns (learning how to miss the strings on purpose for better rhythm).\n- Song Targets: \"Hotel California\" (acoustic chords) or \"Boulevard of Broken Dreams\".\n- The Accelerator: Recording yourself playing on your phone to instantly spot where your rhythm slows down."
    },
    "12": {
        "title": "The Momentum Pathway ⏱️",
        "content": "Your Timeline: 3 to 5 Weeks to Your Next Level\nYou're closer than you might think. With your current foundation and highly consistent practice routine, you are perfectly positioned for a breakthrough. Your timeline is incredibly short because you just need the right expert adjustments to your technique, not a complete overhaul.\n\n- Starting Point: Capable player ready for intermediate techniques.\n- Learn Next: Barre chord transitions and hybrid picking.\n- Song Targets: \"Blackbird\" (The Beatles) or advanced John Mayer acoustic covers.\n- The Accelerator: Booking a structured session to map out exactly which bad habits are currently slowing your fingers down."
    }
}

def generate_result(campaign_source: str, answers: dict, selected_songs: list = None) -> dict:
    if selected_songs is None:
        selected_songs = []
    
    result_id = "1" # Default fallback
    
    if campaign_source == "ad_1":
        # Core variables: Q2 (Experience) & Q5 (Preferred Learning)
        q2_exp = answers.get("q2", 1)
        q5_learn = answers.get("q5", 1)
        
        is_beginner = q2_exp in [1, 2]
        is_self_guided = q5_learn in [1, 2]
        
        if is_beginner and is_self_guided:
            result_id = "1"
        elif is_beginner and not is_self_guided:
            result_id = "2"
        elif not is_beginner and is_self_guided:
            result_id = "3"
        elif not is_beginner and not is_self_guided:
            result_id = "4"
            
    elif campaign_source == "ad_2":
        # Core variables: Q2 (Ability) & Q3 (Music Preference)
        q2_ability = answers.get("q2", 1)
        q3_music = answers.get("q3", 1)
        
        is_beginner = q2_ability in [1, 2]
        is_bollywood = q3_music in [2, 4] # Assuming 1,3,5 are Pop/Indie
        
        if is_beginner and is_bollywood:
            result_id = "5"
        elif is_beginner and not is_bollywood:
            result_id = "6"
        elif not is_beginner and is_bollywood:
            result_id = "7"
        elif not is_beginner and not is_bollywood:
            result_id = "8"
            
    elif campaign_source == "ad_3":
        # Core variables: Q2 (Level) & Q5 (Consistency)
        q2_level = answers.get("q2", 1)
        q5_consistency = answers.get("q5", 1)
        
        is_beginner = q2_level in [1, 2]
        is_highly_consistent = q5_consistency in [3, 4]
        
        if is_beginner and not is_highly_consistent:
            result_id = "9"
        elif is_beginner and is_highly_consistent:
            result_id = "10"
        elif not is_beginner and not is_highly_consistent:
            result_id = "11"
        elif not is_beginner and is_highly_consistent:
            result_id = "12"
            
    is_beginner_result = result_id in ["1", "2", "5", "6", "9", "10"]
    
    # Personalization Logic based on selected_songs
    personalization_text = ""
    if selected_songs and len(selected_songs) == 5:
        beginner_songs = [song for song in selected_songs if SONG_TYPES.get(song) == "beginner"]
        advance_songs = [song for song in selected_songs if SONG_TYPES.get(song) != "beginner"]
        
        beginner_count = len(beginner_songs)
        advance_count = len(advance_songs)
        
        beginner_names = ", ".join(beginner_songs) if beginner_songs else "None"
        advance_names = ", ".join(advance_songs) if advance_songs else "None"
        
        song_summary = ""
        if beginner_count > 0 and advance_count > 0:
            song_summary = f"You selected {beginner_count} easy song{'s' if beginner_count > 1 else ''} ({beginner_names}) and {advance_count} advanced song{'s' if advance_count > 1 else ''} ({advance_names}). "
        elif beginner_count > 0:
            song_summary = f"You selected {beginner_count} easy song{'s' if beginner_count > 1 else ''} ({beginner_names}). "
        elif advance_count > 0:
            song_summary = f"You selected {advance_count} advanced song{'s' if advance_count > 1 else ''} ({advance_names}). "
            
        if is_beginner_result:
            if beginner_count >= 4:
                personalization_text = f"{song_summary}Most of your chosen songs are within reach of your current level. You have also picked ambitious goals that can become longer-term targets."
            elif beginner_count >= 3:
                personalization_text = f"{song_summary}You're already close to working toward the beginner-friendly songs you selected. The others are stretch goals that can give you something bigger to work toward as your skills develop."
            else:
                personalization_text = f"{song_summary}You've set your sights high. While most of your selected songs are beyond your current foundation, having ambitious targets is useful. Start with the beginner-friendly songs and progressively build toward the others."
        else:
            if advance_count >= 4:
                personalization_text = f"{song_summary}You've built an ambitious setlist. Most of your choices should provide enough technical challenge to keep you progressing rather than simply repeating skills you already have."
            elif advance_count >= 3:
                personalization_text = f"{song_summary}The easier songs should be approachable for your current experience, while the advanced selections give you stronger targets to stretch toward."
            else:
                personalization_text = f"{song_summary}Your selected songs are mostly below your current level, so you should be able to approach several of them relatively quickly. If your goal is to keep improving, the advanced choices can be a useful starting point for pushing yourself further."
    
    base_content = RESULTS_DATA[result_id]["content"]
    
    # Create short content from the first paragraph
    lines = base_content.split('\n- ')
    intro_paragraph = lines[0] if lines else base_content
    
    if personalization_text:
        intro_paragraph += f"\n\n{personalization_text}"
        base_content += f"\n\n{personalization_text}"

    return {
        "archetype_id": result_id,
        "is_beginner": is_beginner_result,
        "title": RESULTS_DATA[result_id]["title"],
        "short_content": intro_paragraph,
        "content": base_content
    }
def get_result_by_title(title: str) -> dict:
    for res_id, data in RESULTS_DATA.items():
        if data["title"] == title:
            return {
                "archetype_id": res_id,
                "is_beginner": res_id in ["1", "2", "5", "6", "9", "10"],
                "title": data["title"],
                "content": data["content"]
            }
    return None
