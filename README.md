# Introduction to Rotk2_Python project

This is a remastered version of the Romance of the Three Kingdoms II game, which I partially rewrote using Python and Pygame.
I’ve played this game for 30 years and have always wanted to rewrite it in my favorite programming language, hoping to achieve a 100% restoration of the original game.

Romance of the Three Kingdoms II is a game by the Japanese company Koei, originally designed to run under DOS, and nowadays it is mostly run in Dosbox. My project aims to be cross-platform, running on any system.

For this project, I heavily referenced posts from the GameSpot forums (  https://gamefaqs.gamespot.com/boards/956391-romance-of-the-three-kingdoms-ii ) and am grateful for the years of effort put in by SDragon79 and other guys. Based on his ideas, guidance, and a vast number of disassembly reference documents, I have been reverse-engineering the game bit by bit using IDA. So far, I have completed the basic framework and basic commands 8, 9, 10, 11, 12, 14, 15, 18, and 19. Of course, the most complex command 3—the war part, as well as the AI interactions between different feudal lords, have not yet been started. 

Currently, the most perplexing part is the color rendering of images. I have reverse-engineered the CGA part, but for the EGA section, which involves operations with ports, there has been no progress.

The names of the folders are self-explanatory. In the Screenshot folder, you can find typical screenshots of the current game interface. In the IDA folder, you can find my comments for main.exe and open.exe. 

To run the program, simply right-click on main.py in PyCharm and select Run or Debug.
