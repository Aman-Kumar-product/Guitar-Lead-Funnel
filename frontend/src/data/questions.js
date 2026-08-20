// This file contains the question logic for the 3 distinct ad campaigns.

export const adCampaigns = {
  ad_1: {
    id: "ad_1",
    title: "Discover Your Guitar Learning Profile 🎸",
    subtitle: "A 2-minute personalized assessment to map your path from scratch to soloist.",
    questions: [
      {
        id: "q1",
        title: "Do you currently own a guitar?",
        options: [
          { value: 1, label: "Yes, I own an acoustic guitar" },
          { value: 2, label: "Yes, I own an electric guitar" },
          { value: 3, label: "No, but I plan to buy one soon" },
          { value: 4, label: "No, I am just exploring" }
        ]
      },
      {
        id: "q2",
        title: "What is your current experience level?",
        options: [
          { value: 1, label: "Never held a guitar" },
          { value: 2, label: "Know a few chords" },
          { value: 3, label: "Self-taught / Intermediate" },
          { value: 4, label: "Returning after a long break" }
        ]
      },
      {
        id: "q3",
        title: "What is your happiest outcome in 6 months?",
        options: [
          { value: 1, label: "Playing my favorite songs alone" },
          { value: 2, label: "Jamming with friends" },
          { value: 3, label: "Writing my own music" },
          { value: 4, label: "Performing live on stage" }
        ]
      },
      {
        id: "q4",
        title: "How much time can you practice daily?",
        options: [
          { value: 1, label: "Less than 10 minutes" },
          { value: 2, label: "10-20 minutes" },
          { value: 3, label: "20-30 minutes" },
          { value: 4, label: "30+ minutes consistently" }
        ]
      },
      {
        id: "q5",
        title: "How would you prefer to learn?",
        options: [
          { value: 1, label: "Figure it out myself" },
          { value: 2, label: "Free YouTube videos" },
          { value: 3, label: "Structured online course" },
          { value: 4, label: "1-on-1 expert feedback" }
        ]
      },
      {
        id: "q6",
        title: "When are you hoping to start?",
        options: [
          { value: 1, label: "Just researching for now" },
          { value: 2, label: "Sometime next month" },
          { value: 3, label: "This week" },
          { value: 4, label: "Right now" }
        ]
      }
    ]
  },
  ad_2: {
    id: "ad_2",
    title: "Find Your Signature Sound 🎵",
    subtitle: "Tell us what you listen to, and we'll tell you exactly how to play it.",
    questions: [
      {
        id: "q1",
        title: "Do you currently own a guitar?",
        options: [
          { value: 1, label: "Yes, I own an acoustic guitar" },
          { value: 2, label: "Yes, I own an electric guitar" },
          { value: 3, label: "No, but I plan to buy one soon" },
          { value: 4, label: "No, I am just exploring" }
        ]
      },
      {
        id: "q2",
        title: "How would you rate your current ability?",
        options: [
          { value: 1, label: "Total beginner" },
          { value: 2, label: "Can play some open chords" },
          { value: 3, label: "Can play barre chords" },
          { value: 4, label: "Advanced lead player" }
        ]
      },
      {
        id: "q3",
        title: "What kind of music do you want to play most?",
        options: [
          { value: 1, label: "Bollywood Acoustic" },
          { value: 2, label: "Indie Pop" },
          { value: 3, label: "Classic Rock" },
          { value: 4, label: "Fingerstyle" }
        ]
      },
      {
        id: "q4",
        title: "How many full songs can you currently play without stopping?",
        options: [
          { value: 1, label: "Zero" },
          { value: 2, label: "1-3 songs" },
          { value: 3, label: "4-10 songs" },
          { value: 4, label: "10+ songs easily" }
        ]
      },
      {
        id: "q5",
        title: "How much time can you dedicate to practice daily?",
        options: [
          { value: 1, label: "Less than 10 minutes" },
          { value: 2, label: "10-20 minutes" },
          { value: 3, label: "20-30 minutes" },
          { value: 4, label: "30+ minutes consistently" }
        ]
      },
      {
        id: "q6",
        title: "When do you want to start building your repertoire?",
        options: [
          { value: 1, label: "Just looking around" },
          { value: 2, label: "Next month" },
          { value: 3, label: "This week" },
          { value: 4, label: "Right now" }
        ]
      }
    ]
  },
  ad_3: {
    id: "ad_3",
    title: "Calculate Your Guitar Timeline ⏱️",
    subtitle: "Find out exactly how long it will take you to reach your guitar goals.",
    questions: [
      {
        id: "q1",
        title: "Do you currently own a guitar?",
        options: [
          { value: 1, label: "Yes, I own an acoustic guitar" },
          { value: 2, label: "Yes, I own an electric guitar" },
          { value: 3, label: "No, but I plan to buy one soon" },
          { value: 4, label: "No, I am just exploring" }
        ]
      },
      {
        id: "q2",
        title: "Where are you starting from?",
        options: [
          { value: 1, label: "Starting from zero" },
          { value: 2, label: "Stuck on basic chords" },
          { value: 3, label: "Stuck on rhythm and strumming" },
          { value: 4, label: "Stuck on solos and theory" }
        ]
      },
      {
        id: "q3",
        title: "How much time can you commit daily?",
        options: [
          { value: 1, label: "Less than 10 minutes" },
          { value: 2, label: "10-20 minutes" },
          { value: 3, label: "20-30 minutes" },
          { value: 4, label: "30+ minutes consistently" }
        ]
      },
      {
        id: "q4",
        title: "What is the major goal you want to hit first?",
        options: [
          { value: 1, label: "Learn my first full song" },
          { value: 2, label: "Sing and play at the same time" },
          { value: 3, label: "Learn to improvise" },
          { value: 4, label: "Join a band" }
        ]
      },
      {
        id: "q5",
        title: "Be honest: how consistent have you been in the past?",
        options: [
          { value: 1, label: "I usually quit after a week" },
          { value: 2, label: "I practice on and off" },
          { value: 3, label: "I try to stick to a schedule" },
          { value: 4, label: "I am highly disciplined" }
        ]
      },
      {
        id: "q6",
        title: "When do you want to start the clock on your timeline?",
        options: [
          { value: 1, label: "Not sure yet" },
          { value: 2, label: "Next month" },
          { value: 3, label: "This week" },
          { value: 4, label: "Right now" }
        ]
      }
    ]
  }
};
