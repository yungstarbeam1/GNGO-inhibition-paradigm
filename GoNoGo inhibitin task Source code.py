import pygame
import random
import time
import os


pygame.init()
screen=pygame.display.set_mode((800, 600))
pygame.display.set_caption('G-NGO Paradigm')

base_dir = r''

#Image set, Sample folder provided on sources jpg folder, small cross and triangle no Gos for this setting
images=['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg', 'image6.jpg', 'image7.jpg', 'image8.jpg']
no_go_images=['image6.jpg', 'image8.jpg']

loaded_images={img: pygame.image.load(img) for img in images}

###########Paradigm parameters###############

#Display time for each stimulus
DISPLAY_TIME = 0.2
#Interstimulus interval
ISI_TIME = 1.3
#Total number of stimuli trials
TOTAL_TRIALS = 150

def run_experiment():
    #random pick of 150 trials amongst the images
    stim_order = random.choices(images, k=TOTAL_TRIALS) 
    
    for stimulus in stim_order:
        # Display the stimulus (currently set as random)
        screen.blit(loaded_images[stimulus], (400, 300)) #This is where the image is displayed, as the dispplay is 800x600 and image is 100x1000: Center of Screen: (800/2, 600/2) = (400, 300), edit accordingly if you change!!
        pygame.display.flip()
        start_time = time.time()

        # Handle stimulus display duration
        while time.time() - start_time < DISPLAY_TIME:  # 200 ms stimulus display
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Handle response logic here
                    pass

        # Display blank screen during isi
        screen.fill((255, 255, 255))
        pygame.display.flip()
        time.sleep(ISI_TIME)


run_experiment()
pygame.quit()

