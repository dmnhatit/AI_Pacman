#%%
import pygame
import sys

pygame.init()

# Initialize the mixer
pygame.mixer.init()

# Set the display (not necessary for playing music)
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Music Player")

# Load the music file
pygame.mixer.music.load("mp3\playing_pacman.mp3")  # Replace with your actual music file

# Play the music
pygame.mixer.music.play()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Your game logic goes here

# Quit the game
pygame.quit()
sys.exit()

# %%
