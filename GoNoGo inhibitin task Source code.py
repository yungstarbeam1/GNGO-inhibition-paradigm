import pygame
import random
import time
import os

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('G-NGO Paradigm')

base_dir = os.path.join(os.path.dirname(__file__), 'Images')

# Image set
images = [os.path.join(base_dir, f'image{i}.jpg') for i in range(1, 9)]
no_go_images = [os.path.join(base_dir, 'image6.jpg'),
                os.path.join(base_dir, 'image8.jpg')]

loaded_images = {img: pygame.image.load(img) for img in images}

# Paradigm parameters
DISPLAY_TIME = 0.2
ISI_TIME = 1.3
TOTAL_TRIALS = 15

# Statistics
total_hits = 0
total_no_go_hits = 0
total_hit_times = []
no_go_hit_times = []

def show_start_screen():
    screen.fill((0, 0, 0))
    
    # Use default font
    font = pygame.font.Font(None, 74)
    
    text = font.render('Press Any Key to Start', True, (255, 255, 255))
    screen.blit(text, (100, 250))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def run_experiment():
    global total_hits, total_no_go_hits, total_hit_times, no_go_hit_times
    stim_order = random.choices(images, k=TOTAL_TRIALS)
    
    for stimulus in stim_order:
        # Start with ISI before displaying each image
        screen.fill((0, 0, 0))  # Clear screen for ISI
        pygame.display.flip()
        time.sleep(ISI_TIME)
        
        screen.blit(loaded_images[stimulus], (350, 250))
        pygame.display.flip()
        start_time = time.time()

        hit = False
        while time.time() - start_time < DISPLAY_TIME:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    hit = True
                    reaction_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                    total_hit_times.append(reaction_time)
                    total_hits += 1
                    if stimulus in no_go_images:
                        total_no_go_hits += 1
                        no_go_hit_times.append(reaction_time)
        
        screen.fill((0, 0, 0))  # Clear screen after displaying image
        pygame.display.flip()

    # Add ISI after the last display
    time.sleep(ISI_TIME)

def display_results():
    avg_hit_time = sum(total_hit_times) / len(total_hit_times) if total_hit_times else 0
    avg_no_go_hit_time = sum(no_go_hit_times) / len(no_go_hit_times) if no_go_hit_times else 0
    
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    text_lines = [
        f"Total Hits: {total_hits}",
        f"Total No-Go Hits: {total_no_go_hits}",
        f"Average Hit Time (All Images): {avg_hit_time:.2f} ms",
        f"Average Hit Time (No-Go Images): {avg_no_go_hit_time:.2f} ms"
    ]
    for i, line in enumerate(text_lines):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (50, 50 + i * 40))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

show_start_screen()

run_experiment()
display_results()

pygame.quit()