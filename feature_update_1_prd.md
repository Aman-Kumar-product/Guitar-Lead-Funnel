# PRD — Feature Update 1: Build Your 5-Song Guitar Setlist

## 1. Feature Summary

Add a small interactive **Build Your 5-Song Guitar Setlist** experience to all three guitar lead-form journeys.

The user is shown a fixed pool of 20 songs and chooses exactly 5 songs they would love to learn/play.

The feature exists to:

- Make the questionnaire more fun and interactive.
- Make the frontend result preview feel personalized.
- Make the emailed report feel personalized.
- Give the user a concrete reason to provide their email and click **Get My Full Report**.
- Create a stronger bridge between the user's current guitar level and the songs they personally want to play.

## 2. Critical Business Rule

This feature is a **personalization feature only**.

It must NOT modify:

- questionnaire score
- HOT / WARM / NURTURE classification
- consultation eligibility
- consultation booking logic
- email/resource routing
- any existing qualification rules

The existing lead-scoring system remains exactly as it is.

The Setlist only contributes selected song names to the personalized report.

---

# 3. User Experience

After the main questionnaire, show:

## 🎵 Build Your Guitar Setlist

**If you could play any 5 songs on guitar, which would you choose?**

Pick the songs you'd genuinely love to play. Don't worry about whether they're easy or difficult.

Display 20 song cards.

Each card contains only:

- Song name

The user selects exactly 5.

Show a visible counter:

**0 / 5 selected**

After each selection:

**1 / 5 selected**

Continue until:

**5 / 5 selected**

Prevent selecting a sixth song.

The user can change their selection before submitting.

Primary CTA:

**Build My Guitar Roadmap →**

---

# 4. Song Data

Every song has exactly two pieces of data:

```text
song_name
type
```

`type` can only be:

```text
beginner
advance
```

No other song metadata is required for this feature.

Do NOT add:

- genre
- language
- artist
- chord count
- difficulty score
- BPM
- skill tags

The frontend only needs the song name.

---

# 5. Fixed Song Pool

Use exactly the 20 songs contained in:

`songs_pool.txt`

The pool intentionally contains a broad mixture of:

- Hindi / Bollywood
- Indian Indie
- English Pop / Acoustic
- Rock / Alternative
- Classical / Instrumental / Fingerstyle

The pool is fixed for the MVP.

Do not dynamically filter the 20 songs based on questionnaire answers.

All users see the same 20-song pool.

The user's current guitar level does NOT change which songs are displayed.

---

# 6. Why Everyone Sees the Same Pool

The purpose is to discover what the user genuinely wants to play.

If the system filters songs based on their current ability, a beginner might only see easy songs and never reveal ambitious goals.

Instead:

**Current level = from questionnaire**

**Desired songs = from Setlist**

The report connects the two.

Example:

Current level:
`beginner`

Selected songs:
- 3 beginner songs
- 2 advance songs

The report can say:

> You're already close to working toward the three beginner-friendly songs you selected. The other two are bigger goals, but they give you something exciting to work toward over the next few months.

This is much more useful than simply telling the user that they are a beginner.

---

# 7. Selection Logic

The user must select exactly 5 songs.

Valid:

```text
5 selected
```

Invalid:

```text
0–4 selected
```

The Continue button should remain disabled until exactly 5 songs are selected.

The user should be able to deselect a song and choose another.

Duplicate selections are impossible because each song is represented by one selectable card.

---

# 8. Data Sent to Backend

When the user submits the Setlist, send:

```text
selected_song_1
selected_song_2
selected_song_3
selected_song_4
selected_song_5
```

The backend already has the user's questionnaire data.

Therefore the backend can combine:

```text
existing questionnaire result
+
current guitar level
+
five selected songs
```

to produce the personalized report.

---

# 9. Frontend Preview

After Setlist selection, show a partial result before requesting the email/report.

Example for a beginner:

> ## 🎸 Your Guitar Roadmap Is Taking Shape
>
> You're already getting close to working toward **Baarishein, Perfect and I'm Yours**.
>
> You've also picked **Hotel California and Sweet Child O' Mine** — two ambitious songs that can become exciting stretch goals as you build your guitar skills.
>
> **Want to see your complete personalized roadmap?**
>
> We'll send your full report to your email.

CTA:

**Get My Full Roadmap →**

The exact wording should be generated from the user's current level and selected song types.

---

# 10. Personalization Rules

The Setlist does not affect qualification.

It only determines which personalization template is used.

There are two inputs:

```text
current_level
selected_song_types
```

For five selected songs, count:

```text
beginner_count
advance_count
```

## Scenario A — Beginner User + Mostly Beginner Songs

Example:

```text
4 beginner
1 advance
```

Report direction:

> Most of your chosen songs are within reach of your current level. You have also picked one ambitious song that can become a longer-term goal.

## Scenario B — Beginner User + Mixed Songs

Example:

```text
3 beginner
2 advance
```

Report direction:

> You're already close to working toward the three beginner-friendly songs you selected. The other two are stretch goals that can give you something bigger to work toward as your skills develop.

## Scenario C — Beginner User + Mostly Advance Songs

Example:

```text
1 beginner
4 advance
```

Report direction:

> You've set your sights high. While most of your selected songs are beyond your current foundation, having ambitious targets is useful. Start with the beginner-friendly song and progressively build toward the others.

## Scenario D — Advanced User + Mostly Beginner Songs

Example:

```text
4 beginner
1 advance
```

Report direction:

> Your selected songs are mostly below your current level, so you should be able to approach several of them relatively quickly. If your goal is to keep improving, the advanced choice can be a useful starting point for pushing yourself further.

## Scenario E — Advanced User + Mixed Songs

Example:

```text
3 beginner
2 advance
```

Report direction:

> The three easier songs should be approachable for your current experience, while the two advanced selections give you stronger targets to stretch toward.

## Scenario F — Advanced User + Mostly Advance Songs

Example:

```text
1 beginner
4 advance
```

Report direction:

> You've built an ambitious setlist. Most of your choices should provide enough technical challenge to keep you progressing rather than simply repeating skills you already have.

---

# 11. Important Wording Rule

Do NOT make absolute promises such as:

> "You will learn these songs in exactly 3 months."

Instead use language such as:

> "With consistent practice, these could become realistic near-term milestones."

or:

> "You may be able to work toward these over the next few months."

The existing questionnaire's practice-time and consistency answers can be used elsewhere in the report to make timeline statements more specific.

The Setlist itself does not calculate a timeline.

---

# 12. Email Report Integration

The selected songs should appear prominently in the email.

Example:

## 🎸 Your 5-Song Guitar Goal

1. Baarishein
2. Perfect
3. I'm Yours
4. Hotel California
5. Sweet Child O' Mine

Then:

## Your Roadmap

> Based on your current level, you're already close to working toward **Baarishein, Perfect and I'm Yours**.
>
> **Hotel California and Sweet Child O' Mine** are more ambitious targets. With consistent practice and the right progression, these can become longer-term stretch goals.

This makes the email feel individually written for the lead rather than like a generic automated marketing email.

---

# 13. Use Across All Three Ads

The Setlist interaction is identical across all three ads.

The difference is the surrounding report.

### Ad 1 — Guitar Learning Profile

The Setlist supports the user's learning profile.

Example:

> Your song choices reinforce that you're motivated by learning through real songs rather than isolated exercises.

### Ad 2 — Which Songs Can YOU Play?

The Setlist is the central personalization element.

Example:

> Here's which of your chosen songs are closest to your current level and which ones can become stretch goals.

### Ad 3 — How Long Until YOU Can Play?

The Setlist makes the timeline result concrete.

Example:

> Instead of giving you a generic "learn guitar in X months" estimate, we've mapped your goal around the actual songs you want to play.

The underlying Setlist logic remains identical.

---

# 14. Technical Implementation

## Frontend

The frontend:

1. Loads the 20-song pool.
2. Renders song cards.
3. Tracks selected songs.
4. Enforces exactly 5 selections.
5. Sends the five selected song names to Python backend.
6. Displays the personalized preview returned by the backend.

The frontend should NOT contain qualification logic.

## Python Backend

Python:

1. Receives selected songs.
2. Retrieves the user's existing questionnaire result.
3. Determines the user's existing current-level classification.
4. Counts beginner/advance selections.
5. Selects the appropriate personalization template.
6. Inserts the five song names.
7. Produces the final report content.
8. Stores selected songs with the lead.

---

# 15. Suggested Backend Logic

Conceptually:

```text
current_level = existing_questionnaire_level

beginner_count = count(selected songs where type == beginner)
advance_count = count(selected songs where type == advance)

if current_level == beginner:

    if beginner_count >= 4:
        template = beginner_mostly_beginner

    elif beginner_count >= 3:
        template = beginner_mixed

    else:
        template = beginner_mostly_advance

else:

    if advance_count >= 4:
        template = advanced_mostly_advance

    elif advance_count >= 3:
        template = advanced_mixed

    else:
        template = advanced_mostly_beginner
```

This is intentionally simple and deterministic.

No LLM is required.

---

# 16. Frontend Design Direction

The interaction should feel like a small game, not a form.

Each song should be a visual card.

Example:

```text
┌──────────────────────────┐
│                          │
│       🎵 Baarishein      │
│                          │
│       ○ Select           │
│                          │
└──────────────────────────┘
```

When selected:

```text
┌──────────────────────────┐
│          ✓               │
│       🎵 Baarishein      │
│                          │
│        SELECTED          │
└──────────────────────────┘
```

Show:

**Build your setlist: 3 / 5**

The interaction should be quick enough that it does not feel like another long questionnaire.

---

# 17. MVP Scope

### Must Have

- 20 fixed songs
- Two metadata fields only
- Song cards
- Select/deselect
- Exactly 5 selections
- 5 selected songs sent to Python
- Beginner/advance count
- Personalized frontend preview
- Personalized email section

### Do Not Build Yet

- Drag and drop
- Audio previews
- Song search
- Genre filters
- Difficulty sliders
- User-specific song pools
- AI recommendations
- Dynamic song generation
- Complex music metadata

Keep the first version extremely simple.

---

# 18. Success Metric

The feature should ultimately be measured by:

1. Setlist completion rate
2. Email/report request rate after Setlist
3. Overall lead completion rate
4. Consultation booking rate
5. Course conversion rate

The most important immediate UX metric is:

**% of users who complete the Setlist and click "Get My Full Roadmap".**

If this improves, the feature is doing its job.

---

# 19. Final Product Principle

The user should finish the interaction thinking:

> **"This isn't some generic guitar lead form. They actually understood what I want to play."**

The Setlist therefore creates the bridge:

```text
WHAT I CAN DO
      ↓
WHAT I WANT TO PLAY
      ↓
HOW I CAN GET THERE
```

That becomes the personalized experience shown in the frontend and delivered through email.
