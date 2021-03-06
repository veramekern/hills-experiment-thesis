#! /usr/bin/env python

import pygame
import cv2
import os
import sys
import random
from timeit import default_timer as timer

# Constants
color_font = (30, 30, 30)
background_color = (255, 255, 255)
screen_w = 640
screen_h = 500
fps = 30
screen = pygame.display.set_mode((screen_w, screen_h), pygame.HWSURFACE |
                                 pygame.DOUBLEBUF | pygame.FULLSCREEN)


class Stimulus:
    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.font = pygame.font.Font(None, 20)
        self.font_cross = pygame.font.Font(None, 300)

    def intro(self):
        self.surface.fill(background_color)
        image = pygame.image.load(os.path.join("images",
                                               "EBR_intro_3.jpg")).convert()
        self.surface.blit(image, (50, 50))
        pygame.display.flip()

        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

    def outro(self):
        self.surface.fill(background_color)
        image = pygame.image.load(os.path.join("images",
                                               "EBR_outro_3.jpg")).convert()
        self.surface.blit(image, (50, 50))
        pygame.display.flip()

        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

    def draw_fixation(self):
        self.surface.fill(background_color)
        image = pygame.image.load(os.path.join("images", "fixation.jpg")).convert()
        self.surface.blit(image, (50, 50))
        pygame.display.flip()


class Main:
    def __init__(self, subjectID, condition, ebr_time):
        self.subjectID = subjectID
        self.condition = condition
        self.ebr_time = ebr_time

        filename = str(self.subjectID) + "_EBR_3" + ".txt"
        f = open(filename, 'w')
        output = 'subjectID,condition,time_start,time_end\n'
        f.write(output)
        f.close()

        # Init task
        pygame.init()
        pygame.mouse.set_visible(False)
        self.surface = screen
        self.surface.fill(background_color)
        self.running = True
        self.start = 0

        # Initiate objects
        self.stimulus = Stimulus(screen)

    def main(self):
        # Main loop

        clock = pygame.time.Clock()
        self.stimulus.intro()
        self.stimulus.draw_fixation()

        cap = cv2.VideoCapture(0)

        # Define the codec and create VideoWriter object
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        out = cv2.VideoWriter(str(self.subjectID) + '_EBR3.avi', fourcc, 30.0, (640, 480))

        self.start = timer()

        while (cap.isOpened()):
            ret, frame = cap.read()

            if ret == True:
                out.write(frame)
                event = pygame.event.poll()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif timer() - self.start > self.ebr_time:
                    self.running = False

                if self.running == False:
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        self.stimulus.outro()
        self.end = timer()

        clock.tick(60)

        filename = str(self.subjectID) + "_EBR_3" + ".txt"
        f = open(filename, 'a')
        output = str(self.subjectID) + "," + \
                 self.condition + "," + \
                 str(self.start) + "," + \
                 str(self.end) + "\n"
        f.write(output)
        f.close()

if __name__ == '__main__':
    debug = sys.argv[3]
    if debug == "f":
        ebr_time = 360.0
    else:
        ebr_time = 10.0

    subject_ID = sys.argv[1]
    if sys.argv[2] == "r":
        condition = random.choice(("c", "d"))
    else:
        condition = sys.argv[2]
    run = Main(subject_ID, condition, ebr_time)
    run.main()
