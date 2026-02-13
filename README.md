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
## How to Play

1. **Red Player (Human) goes first**  
   - Click on one of your red pieces to select it.  
   - Click on a highlighted square (blue circle) to move the piece.  
   - Only legal moves are allowed.

2. **White Player (ChatGPT AI)**  
   - After your move, ChatGPT automatically chooses and executes its move.  
   - The AI follows standard checkers rules, including mandatory jumps.

3. **King Promotion**  
   - If a piece reaches the opponent’s back row, it becomes a king.  
   - Kings are marked with a crown and can move forwards and backwards diagonally.

4. **Captures**  
   - Jump over an opponent's piece to capture it.  
   - Multiple jumps are possible in a single turn if the moves are legal.

5. **Game Over**  
   - The game ends when a player has no pieces left or no valid moves remaining.  
   - A message will display the winner.
## Notes
- This is a **learning project** - it may have quirks or rare edge cases.
- AI moves are generated using OpenAI, so ensure your API key is set correctly.
- Feedback and suggestions are welcome!

