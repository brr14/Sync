document.addEventListener('DOMContentLoaded', () => {
    // Variables to track selected mood, activity, and emotion
    let selectedMood = null;
    let selectedActivity = null;
    let selectedEmotion = null;
  
    // Welcome Message with Time-Based Greeting
    const welcomeContainer = document.createElement('div');
    welcomeContainer.classList.add('welcome-message');
    const hours = new Date().getHours();
    let greeting = 'Hello';
    if (hours < 12) {
      greeting = 'Good Morning';
    } else if (hours < 18) {
      greeting = 'Good Afternoon';
    } else {
      greeting = 'Good Evening';
    }
    welcomeContainer.textContent = `${greeting}! Welcome to your personalized music experience.`;
    document.body.insertBefore(welcomeContainer, document.body.firstChild);
  
    // Music Quote of the Day
    const musicQuotes = [
      "Music is the universal language of mankind. – Henry Wadsworth Longfellow",
      "Where words fail, music speaks. – Hans Christian Andersen",
      "Music can change the world because it can change people. – Bono",
      "One good thing about music, when it hits you, you feel no pain. – Bob Marley",
      "Music is the divine way to tell beautiful, poetic things to the heart. – Pablo Casals",
    ];
    const randomQuote = musicQuotes[Math.floor(Math.random() * musicQuotes.length)];
    const quoteContainer = document.createElement('div');
    quoteContainer.classList.add('music-quote');
    quoteContainer.textContent = randomQuote;
    document.body.insertBefore(quoteContainer, document.body.children[1]);
  
    // // Quick Mood Presets
    // const moods = ['Happy', 'Relaxed', 'Energetic', 'Focused', 'Melancholy'];
    // const moodPresetContainer = document.createElement('div');
    // moodPresetContainer.classList.add('mood-preset-container');
  
    // moods.forEach(mood => {
    //   const moodButton = document.createElement('button');
    //   moodButton.classList.add('mood-preset');
    //   moodButton.textContent = mood;
    //   moodButton.addEventListener('click', () => {
    //     alert(`Selected Mood: ${mood}`);
    //     // Redirect or perform additional functionality as needed
    //   });
    //   moodPresetContainer.appendChild(moodButton);
    // });
  
    document.body.appendChild(moodPresetContainer);
  
    // Existing functionality
    document.querySelectorAll(".option[data-mood]").forEach(button => {
      button.addEventListener("click", () => {
        document.querySelectorAll(".option[data-mood]").forEach(btn => btn.classList.remove("selected"));
        button.classList.add("selected");
        selectedMood = button.dataset.mood;
        console.log(`Selected mood: ${selectedMood}`);
      });
    });
  
    document.querySelectorAll(".option[data-activity]").forEach(button => {
      button.addEventListener("click", () => {
        document.querySelectorAll(".option[data-activity]").forEach(btn => btn.classList.remove("selected"));
        button.classList.add("selected");
        selectedActivity = button.dataset.activity;
        console.log(`Selected activity: ${selectedActivity}`);
      });
    });
  
    document.querySelectorAll(".emoji").forEach(button => {
      button.addEventListener("click", () => {
        document.querySelectorAll(".emoji").forEach(btn => btn.classList.remove("selected"));
        button.classList.add("selected");
        selectedEmotion = button.dataset.emotion;
        document.getElementById("selected-emotion").textContent = `You are feeling: ${selectedEmotion.charAt(0).toUpperCase() + selectedEmotion.slice(1)}`;
        const params = new URLSearchParams({
          mood: selectedEmotion
        });
        // Redirect to Django's endpoint for generating the playlist
        window.location.href = `../generate_emote/?${params.toString()}`;
      });
    });
  
    const generatePlaylistButton = document.getElementById("generate-playlist");
    if (generatePlaylistButton) {
      generatePlaylistButton.addEventListener("click", () => {
        if (!selectedMood || !selectedActivity) {
          alert("Please select both a mood and an activity!");
        } else {
          const params = new URLSearchParams({
            mood: selectedMood,
            activity: selectedActivity,
          });
          // Redirect to Django's endpoint for generating the playlist
          window.location.href = `../generate/?${params.toString()}`;
        }
      });
    }
  });
  