# Guitar Lead Funnel - Result Logic Mapping

This logic dictates exactly how the Antigravity frontend and FastAPI backend should map user answers to the 12 specific result outcomes.

---

## Ad 1: The Learning Profile Engine

**Core Variables Used:** `Q2` (Current Experience) & `Q4` (Preferred Learning Method)

### Variable Mapping

| Question | Option | Mapped Group |
| :--- | :--- | :--- |
| **Q2 (Experience)** | Option 1 (Complete beginner) | Beginner Group |
| | Option 2 (Tried learning before) | Beginner Group |
| | Option 3 (Know basic chords) | Advanced Group |
| | Option 4 (Can already play songs) | Advanced Group |
| **Q4 (Method)** | Option 1 (Explore by myself) | Self-Guided Group |
| | Option 2 (YouTube/tutorials) | Self-Guided Group |
| | Option 3 (Structured course) | Instructed Group |
| | Option 4 (Teacher guiding me) | Instructed Group |

### Result Matrix

1. **The Solo Explorer** = Beginner Group + Self-Guided Group
2. **The Structured Starter** = Beginner Group + Instructed Group
3. **The Intuitive Player** = Advanced Group + Self-Guided Group
4. **The Guided Performer** = Advanced Group + Instructed Group

---

## Ad 2: The Song Repertoire Matrix

**Core Variables Used:** `Q2` (Current Playing Ability) & `Q4` (Preferred Music Type)

### Variable Mapping

| Question | Option | Mapped Group |
| :--- | :--- | :--- |
| **Q2 (Ability)** | Option 1 (Nothing yet) | Beginner Group |
| | Option 2 (A few chords) | Beginner Group |
| | Option 3 (Chords + basic strumming) | Advanced Group |
| | Option 4 (Complete songs) | Advanced Group |
| **Q4 (Music Type)** | Option 1 (Simple songs) | Pop/Indie Group *(Fallback)* |
| | Option 2 (Bollywood/acoustic songs) | Bollywood Group |
| | Option 3 (Pop/indie songs) | Pop/Indie Group |
| | Option 4 (Challenging songs/solos) | Bollywood Group *(Fallback/Advanced)* |

> [!NOTE]
> To keep the matrix to 4 clean results, Opt 1 & 3 trigger Indie/Pop, Opt 2 & 4 trigger Bollywood/Acoustic.

### Result Matrix

5. **Bollywood Foundation** = Beginner Group + Bollywood Group
6. **Indie Chord Builder** = Beginner Group + Pop/Indie Group
7. **Bollywood Unplugged** = Advanced Group + Bollywood Group
8. **Indie Rhythm Master** = Advanced Group + Pop/Indie Group

---

## Ad 3: The Timeline Estimator

**Core Variables Used:** `Q2` (Current Level) & `Q5` (Consistency)

### Variable Mapping

| Question | Option | Mapped Group |
| :--- | :--- | :--- |
| **Q2 (Level)** | Option 1 (Never played) | Beginner Group |
| | Option 2 (Tried occasionally) | Beginner Group |
| | Option 3 (Know basic chords) | Advanced Group |
| | Option 4 (Can play songs) | Advanced Group |
| **Q5 (Consistency)** | Option 1 (Whenever I get time) | Low Consistency Group |
| | Option 2 (1–2 days/week) | Low Consistency Group |
| | Option 3 (3–4 days/week) | High Consistency Group |
| | Option 4 (Almost every day) | High Consistency Group |

### Result Matrix

9. **The Steady Builder Path** = Beginner Group + Low Consistency Group
10. **The Fast-Track Foundation** = Beginner Group + High Consistency Group
11. **The Weekend Warrior Path** = Advanced Group + Low Consistency Group
12. **The Momentum Pathway** = Advanced Group + High Consistency Group
