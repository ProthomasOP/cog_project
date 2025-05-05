# Museum Guide Robot

This project contains the finite state machine (FSM) logic for a museum guide 
robot. The robot is designed to navigate a museum environment and respond to 
user commands, such as leading tours or showing specific artworks.

## Features

- FSM-based behavioral control
- Ability to guide users through predefined waypoints (e.g., exhibits, doorways)
- GPT integration for natural language command interpretation 
- Support for both individual painting visits and full tour modes

## Folder Structure

├── .git/ # Git repository metadata
├── pycache/ # Compiled Python bytecode
├── snapshots/ # (Optional) FSM snapshot data
├── MuseumGuide.fsm # Main FSM script controlling robot behavior
├── MuseumGuide.py # Python script with helper functions or FSM interface
├── wall_defs.py # Wall/obstacle definitions for environment navigation
├── README.md # Project documentation

## Requirements
- Python 3.8+
- git pull vex-aim-tool

## How to Run

1. In your terminal, `cd` into the project directory:

   ```bash
   cd cog_project
   ``` 

2. To generate the Python file, run the following in your shell:

   ```bash
   genfsm MuseumGuide.fsm
   ``` 

3. To launch the robot to run FSM programs:

   ```bash
   simple_cli
   ``` 

4. In the simple_cli shell, run the FSM:

   ```bash
   runfsm("MuseumGuide")
   ``` 
5. Robot Initialization

   Make sure the robot is placed at the correct location in front of the two 
   doors of the museum gallery (check the robot camera to see both doors with 
   all of its respective aruco markers). The setup of the gallery is exactly as
   shown in the video. 

## What You Can Say to Celeste

You can talk to Celeste like you would to a real museum guide. Here are some 
examples:

- **Gallery selection:**
  - "I want to go to the Classic gallery"
  - "Take me to the Modern gallery"

- **Specific painting requests:**
  - "Show me the leftmost painting"
  - "Take me to the middleleft one"
  - "Can we see all of them?"

- **Tour flow and navigation:**
  - "Let's move on to the next painting"
  - "Can we go to the other gallery?"
  - "End the tour"

- **Follow-up questions:**
  - "What is this painting about?"
  - "Who painted this?"
  - "Can you tell me more?"

Celeste internally translates your commands using GPT and a structured tour 
logic engine. For example, saying "Show me all the paintings in the Classic 
gallery" triggers a multi-step FSM that navigates through ArUco markers in a 
left-to-right or right-to-left flow, depending on the entrance path.

This interaction system makes the robot feel like a true tour guide, capable of 
adaptive conversation, spatial reasoning, and real-time control—all powered by 
a combination of GPT logic and structured FSM behavior.

## Author

- **Thomas Chun Fai Lee**  
  Email: [chunfai2@andrew.cmu.edu](mailto:chunfai2@andrew.cmu.edu)
- **Ziyan Xin** 
  Email: [ziyanxin@andrew.cmu.edu](mailto:ziyanxin@andrew.cmu.edu)

---

Feel free to contribute or suggest improvements!