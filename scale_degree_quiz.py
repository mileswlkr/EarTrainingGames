# A game to quiz the user on which scale degree a presented note is within a given key.

import pygame
import random
from note_defs import notes_in_major

pygame.font.init()  # Initialises fonts for pygame
pygame.mixer.init()  # Initialises the mixer module

KEYS = ['c', 'g', 'd', 'a', 'e', 'b', 'fs', 'f', 'bf', 'ef', 'af', 'df']  # Quiz keys
# KEYS = ['c', 'g', 'd', 'a', 'e', 'b', 'fs', 'f', 'bf', 'ef', 'af', 'df']
gameKeys = ['K_1', 'K_2', 'K_3', 'K_4', 'K_5', 'K_6', 'K_7']

WIDTH, HEIGHT = 200, 200
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Scale Degree Quiz')

# Settings
num_questions_per_key = 10


def main():

    # Define inner function for redrawing PyGame window
    def redraw_window(_note):
        WIN.fill((255, 255, 255))  # in RGB
        # Draw text
        question_num_label = question_num_font.render(f"Q: {question_in_key}", True, (0, 0, 0))
        question_text = question_font.render(_note, True, (0, 0, 0))
        quiz_key_text = quiz_key_font.render("Key: " + key, True, (0, 0, 0))

        WIN.blit(question_num_label, (WIDTH - question_num_label.get_width() - 10,
                                      HEIGHT - question_num_label.get_height() - 10))
        WIN.blit(question_text, (WIDTH / 2 - question_text.get_width() / 2,
                                 HEIGHT / 2 - question_text.get_height() / 2 - 20))
        WIN.blit(quiz_key_text, (10,
                                 HEIGHT - quiz_key_text.get_height() - 10))

        pygame.display.update()

    # PyGame initialisation stuff:
    fps = 30  # Frames per second
    question_font = pygame.font.SysFont('comicsans', 60)
    question_num_font = pygame.font.SysFont('comicsans', 25)
    quiz_key_font = pygame.font.SysFont('comicsans', 25)
    clock = pygame.time.Clock()

    # Initialise variable for if we want to quit
    quit_game = False

    while not quit_game:

        # Randomly choose the key and create the notes list
        key = random.choice(KEYS)
        notes_dict = notes_in_major(36, 47, key)
        notes = list(notes_dict.values())

        # Reorder notes to start on root
        ind_start = notes.index(key)
        notes = notes[ind_start:] + notes[0:ind_start]

        # Modify appearance of key
        if len(key) > 1:
            if key[1] == 's':
                key = key[0].upper() + '#'
            elif key[1] == 'f':
                key = key[0].upper() + 'b'
        else:
            key = key.upper()

        # Modify appearance of notes:
        for ix in range(0, len(notes)):
            if len(notes[ix]) > 1:
                if notes[ix][1] == 's':
                    notes[ix] = notes[ix][0].upper() + '#'
                elif notes[ix][1] == 'f':
                    notes[ix] = notes[ix][0].upper() + 'b'
            else:
                notes[ix] = notes[ix].upper()

        # Create boolean for when the key is done, and we should move on
        key_done = False

        # Initialise variables required by run loop
        question_in_key = 1
        next_question = True

        # Start while loop for the key questions
        note = []
        ix = []
        while not key_done:
            clock.tick(fps)

            # Only increment question number if the question has been answered
            if next_question:
                ix = random.choice(range(0, len(notes)))
                note = notes[ix]
                next_question = False

            # Update visuals and audio
            redraw_window(note)

            keys = pygame.key.get_pressed()
            key_pressed = eval('keys[pygame.' + gameKeys[ix] + ']')

            # Move to next question if the answer was correct
            if key_pressed:
                next_question = True
                question_in_key += 1

            # Escape if the game is quit!
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    key_done = True
                    quit_game = True

            # Finish key question loop if we have done enough questions
            if question_in_key >= 11:
                key_done = True


main()
