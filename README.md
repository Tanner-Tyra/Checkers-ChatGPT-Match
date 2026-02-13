# Checkers-ChatGPT-Match

A **proof of concept** Python Checkers game where you can play against **ChatGPT**.  
This project was made with less than half a year of programming experience, so it’s a learning experiment more than a polished product — but it’s fully playable!  

## ⚠️ Warning

This game uses **OpenAI API** to power the AI moves.  
Running the game will **consume API credits** every time ChatGPT makes a move. Make sure you understand your usage limits before playing.

## Features

- **Player vs AI:** You play as red, ChatGPT plays as white.  
- **Standard checkers rules:** Moves, captures, and king promotions are implemented.  
- **AI powered by OpenAI:** ChatGPT calculates moves based on board state.  
- **Simple GUI:** Built with `pygame` for interactive gameplay.  
- **Move validation:** Only legal moves are allowed.  
- **Win detection:** Game ends when one side has no pieces or no valid moves.  

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/Checkers-ChatGPT-Match.git
   cd Checkers-ChatGPT-Match
2. Install dependencies:
   ```
   pip install pygame openai==0.28.0
3. Add your OpenAI API key (at your own risk):
   ```
   openai.api_key = "YOUR_KEY_HERE"
4. Run the game
