import pygame, random, time, os, xlsxwriter, scipy
from datetime import datetime

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
TOTAL_TRIALS = 0  # Until Input otherwise

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

# Input for # of Trials After pressing start
def get_trial_count():
    global TOTAL_TRIALS
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render('Enter # of Trials:', True, (255, 255, 255))
    screen.blit(text, (100, 250))
    pygame.display.flip()

    input_number = ''
    entering = True
    while entering:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entering = False
                elif event.key == pygame.K_BACKSPACE:
                    input_number = input_number[:-1]
                else:
                    if event.unicode.isdigit():
                        input_number += event.unicode
        
        screen.fill((0, 0, 0))
        screen.blit(text, (100, 250))
        input_text = font.render(input_number, True, (255, 255, 255))
        screen.blit(input_text, (100, 350))
        pygame.display.flip()

    TOTAL_TRIALS = int(input_number) if input_number else 15
    # Add ISI after the last display
    time.sleep(ISI_TIME)

    # Prompt to press any key to begin the test
    prompt_to_start_test('Press Any Key to Begin Test', (screen.get_width() / 2, screen.get_height() / 2), 60)

def prompt_to_start_test(message, position, font_size):
    font = pygame.font.Font(None, font_size)
    screen.fill((0, 0, 0))
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=position)
    screen.blit(text, text_rect)
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
                
                if event.type == pygame.KEYDOWN and not hit:
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

# This calculates the average for time
def avg():
    avg_hit_time = sum(total_hit_times) / len(total_hit_times) if total_hit_times else 0
    avg_no_go_hit_time = sum(no_go_hit_times) / len(no_go_hit_times) if no_go_hit_times else 0
    return avg_hit_time, avg_no_go_hit_time

def display_results(avg_hit_time, avg_no_go_hit_time):
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

    # Display GAME OVER in red, positioned lower
    font_game_over = pygame.font.Font(None, 100)
    game_over_text = font_game_over.render('GAME OVER', True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(game_over_text, game_over_rect)

    # Display Press any button to restart in white, positioned lower
    font_restart = pygame.font.Font(None, 36)
    restart_text = font_restart.render('Press Any Button to Restart', True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 150))
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False  # Exit the loop to restart the program

def file_output(avg_hit_time, avg_no_go_hit_time):
    timestamp = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    filename = f"Results_{timestamp}.xlsx"
    
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet("Data")
    
    row = 0
    col = 0

    content = {
        "Total Hits": total_hits,
        "Total No Go Hits": total_no_go_hits,
        "Average Hit Time for All Images": avg_hit_time,
        "Average Hit Time for No Go Images": avg_no_go_hit_time
    }

    for name, score in content.items():
        worksheet.write(row, col, name)
        worksheet.write(row, col + 1, score)
        col += 1

    workbook.close()

    print(f"Saved Results to: {os.getcwd()}")

### UNDER ANY CIRCUMSTANCES DO NOT CHANGE THE ORDER OF THESE FUNCTION CALLS ###
### When adding new functions make sure to add them between file_output() and display_results() OR under run_experiment()
### NO WHERE ELSE OTHER THAN THOSE TWO LOCATIONS^^
show_start_screen()
get_trial_count()
run_experiment()

avg_hit_time, avg_no_go_hit_time = avg()

file_output(avg_hit_time, avg_no_go_hit_time)

display_results(avg_hit_time, avg_no_go_hit_time)

pygame.quit()
