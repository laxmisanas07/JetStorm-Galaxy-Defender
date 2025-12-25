🚀 Project J: JetStorm - Galaxy Defender
"The stars are silent, but the war is loud."

JetStorm is a high-octane **Arcade Space Shooter** designed to simulate high-speed galactic combat. It places you in the cockpit of a futuristic starfighter, tasked with defending the cosmos against endless waves of alien invaders using precision, reflexes, and heavy firepower.



🚀 How It Works
This game utilizes the **Pygame** engine to render real-time graphics and handle physics-based interactions.

- **Game Loop Engine:** The core loop runs at **60 FPS**, constantly updating the positions of the player, enemies, and projectiles to create smooth animation logic.

- **Collision Detection:** Uses `Rect.colliderect()` algorithms to calculate precise intersections between bullets and enemies, triggering damage or destruction instantly.

- **Particle System:** Features a dynamic **Explosion Engine** that spawns and scatters randomized pixel particles whenever an enemy is destroyed.

- **State Management:** Implements a robust state machine to handle transitions between the **Menu**, **Active Gameplay**, and **Game Over** screens seamlessly.

🛠️ Tech Stack
a. Language: Python 3

b. Library: Pygame

c. Concepts: 2D Vector Math, Event Handling, UI State Logic

⚡ Usage
Run the script to launch into space:

```bash
python main.py

1.Start Mission: Click the "START MISSION" button on the main GUI menu.

2.Controls:

	Left/Right Arrows: Pilot the ship.

	Spacebar: Fire dual-laser cannons.

3.Observe: Watch how the background starfield animates to create a parallax effect while the particle system handles explosions.

4.Exit: Click "ABORT (QUIT)" to close the application.

❤️ Built by Laxmi Sanas
