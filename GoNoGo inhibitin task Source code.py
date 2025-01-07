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

# Statistics
total_hits = 0
total_no_go_hits = 0
total_hit_times = []
no_go_hit_times = []

def show_start_screen():
    screen.fill((0, 0, 0))
    
    # Use default font
    font = pygame.font.Font(None, 60)  # Adjusted font size
    text = font.render('Press Any Key to Start Program', True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
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

    # Prompt to press any key to start the test with blinking colors bc blinking colours are always fun
    blinking_text('Press Any Key to Begin Test', (screen.get_width() / 2, screen.get_height() / 2), 60)

def blinking_text(message, position, font_size):
    font = pygame.font.Font(None, font_size)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return

        screen.fill((0, 0, 0))
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=position)
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)  #not too fast ofc


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
    
    blinking_text_restart()

def blinking_text_restart():
    font = pygame.font.Font(None, 36)
    position = (screen.get_width() / 2, screen.get_height() - 50)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                main()  # Restart the entire program

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        text = font.render('Press Any Button to Restart', True, color)
        text_rect = text.get_rect(center=position)
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)

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
        row += 1

    workbook.close()

    print(f"Saved Results to: {os.getcwd()}")

def main():
    global total_hits, total_no_go_hits, total_hit_times, no_go_hit_times
    total_hits = 0
    total_no_go_hits = 0
    total_hit_times = []
    no_go_hit_times = []
    
    show_start_screen()
    get_trial_count()
    run_experiment()
    avg_hit_time, avg_no_go_hit_time = avg()
    file_output(avg_hit_time, avg_no_go_hit_time)
    display_results(avg_hit_time, avg_no_go_hit_time)

if __name__ == "__main__":
    main()
    pygame.quit()
