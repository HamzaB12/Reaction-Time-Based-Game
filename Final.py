import pygame
import random
import time
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
red = (255, 17, 0)

# Initialize font
pygame.font.init()
font = pygame.font.Font(None, 32)


# Function to render text on the screen at a specified position
def render_text(input_text, font, color, surface, x, y):
    textobj = font.render(input_text, True, color)
    surface.blit(textobj, (x, y))

# Function to get user input with optional prompts and default values.
def get_input(prompt, default, is_color=False, color_options=None):
    screen.fill(white)
    render_text(prompt, font, black, screen, 10, 10)
    pygame.display.flip()
    input_string = str(default)
    if not color_options:
        color_options = {'r': red, 'g': (0, 255, 0), 'b': (0, 0, 255), 'k': black}  # Default colors for the rectangle

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_string:  # Enter to finish
                    if is_color:
                        return color_options.get(input_string[-1].lower(), black)
                    return int(input_string) if input_string.isdigit() else default
                elif event.key is pygame.K_BACKSPACE:  # Backspace to delete
                    input_string = input_string[:-1]
                else:
                    if not is_color or (is_color and event.unicode.lower() in color_options.keys()):
                        input_string += event.unicode
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(white)  # Clear screen
        render_text(prompt + ' (' + input_string + ')', font, black, screen, 10, 50)
        pygame.display.flip()


# Timer function to calculate remaining time
def get_remaining_time(start_time, duration):
    elapsed_time = time.time() - start_time
    remaining_time = max(duration - elapsed_time, 0)
    return remaining_time

# •	Defines background colors and gathers user input for various game parameters.
background_colors = {'w': white, 'l': (211, 211, 211), 'd': (169, 169, 169)}  # Light gray and dark gray
user_name = get_input("Please enter your name:", "User")
game_duration = get_input("Enter timer duration in seconds:", 60)
rect_width = get_input("Enter rectangle width:", 100)
rect_height = get_input("Enter rectangle height:", 50)
rect_color = get_input("Enter rectangle color (r, g, b, k):", 'k', is_color=True)
background_color = get_input("Choose background color (w=white, l=light gray, d=dark gray):", 'w', is_color=True, color_options=background_colors)

# Ensure rectangle does not overlap with counter display
rect_x = random.randint(0, screen_width - rect_width - 200)
rect_y = random.randint(0, screen_height - rect_height)

# Counter for clicks and score
score = 0
click_count = 0

# Additional counters for misclicks and timeouts
misclick_count = 0
timeout_count = 0

# Time when the rectangle was last reset
last_reset_time = time.time()

# Font for displaying the counters
counter_font = pygame.font.Font(None, 36)  # Default font, size 36

# Start the timer
start_time = time.time()

# Game loop flag
running = True

# Levels configuration
levels = [
    {'speed': 1, 'timeout': 1},  # Level 1
    {'speed': 2, 'timeout': 0.8},  # Level 2
    {'speed': 3, 'timeout': 0.6}  # Level 3
]
current_level = 0

# Lists to store performance metrics for generating the line graph
metric_names = ['Score', 'Clicks', 'Misclicks', 'Timeouts']
metric_values = {metric_name: [] for metric_name in metric_names}

# Main application loop
while running:
    remaining_time = get_remaining_time(start_time, game_duration)

    # Check if time is up
    if remaining_time <= 0:
        print(f"Time's up! {user_name}'s final score: Clicks - {click_count}, Misclicks - {misclick_count}, Timeouts - {timeout_count}")
        running = False
        break  # Exit the game loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_count += 1
            # Get the mouse position
            mouse_x, mouse_y = event.pos
            # Check if the rectangle is clicked
            if rect_x < mouse_x < rect_x + rect_width and rect_y < mouse_y < rect_y + rect_height:
                score += 1
                last_reset_time = time.time()
            else:
                # Misclick: clicked outside the rectangle
                misclick_count += 1
                score = max(0, score - 1)  # Prevent negative count
                last_reset_time = time.time()
            # Move the rectangle to a new random position, avoiding the counter display area
            rect_x = random.randint(0, screen_width - rect_width - 200)
            rect_y = random.randint(0, screen_height - rect_height)

    current_time = time.time()
    if current_time - last_reset_time >= levels[current_level]['timeout']:
        # Timeout: passed the specified time without clicking the rectangle
        timeout_count += 1
        score = max(0, score - 1)  # Ensure click_count doesn't go below 0
        rect_x = random.randint(0, screen_width - rect_width - 200)  # Adjust to prevent overlap
        rect_y = random.randint(0, screen_height - rect_height)
        last_reset_time = time.time()

    # Append current performance metrics to the lists
    metric_values['Score'].append(score)
    metric_values['Clicks'].append(click_count)
    metric_values['Misclicks'].append(misclick_count)
    metric_values['Timeouts'].append(timeout_count)

    # Fill the screen with the chosen background color
    screen.fill(background_color)

    # Draw the counter display background
    pygame.draw.rect(screen, gray, (screen_width - 200, 0, 200, screen_height))

    # Draw the rectangle
    pygame.draw.rect(screen, rect_color, (rect_x, rect_y, rect_width, rect_height))

    # Render the counters text
    score_text = counter_font.render(f"Score: {score}", True, black)
    click_counter_text = counter_font.render(f"Clicks: {click_count}", True, black)
    misclick_counter_text = counter_font.render(f"Misclicks: {misclick_count}", True, black)
    timeout_counter_text = counter_font.render(f"Timeouts: {timeout_count}", True, black)
    screen.blit(score_text, (screen_width - 195, 10))
    screen.blit(click_counter_text, (screen_width - 195, 50))
    screen.blit(misclick_counter_text, (screen_width - 195, 90))
    screen.blit(timeout_counter_text, (screen_width - 195, 130))

    # Draw the timer
    timer_text = counter_font.render(f"Time left: {int(remaining_time)}s", True, black)
    screen.blit(timer_text, (10, screen_height - 30))  # Adjust position as needed

    # Update the display
    pygame.display.flip()

    # Check if it's time to increase the level
    if remaining_time <= game_duration / 3 and current_level == 0:
        current_level = 1
        print("Level 2")
    elif remaining_time <= game_duration / 3 * 2 and current_level == 1:
        current_level = 2
        print("Level 3")

# Generate line graph for performance metrics
plt.figure(figsize=(10, 6))
for metric_name in metric_names:
    plt.plot(metric_values[metric_name], label=metric_name)
plt.title(f"Performance Metrics for {user_name}")
plt.xlabel("Time (seconds)")
plt.ylabel("Count")
plt.legend()
plt.grid(True)
plt.show()

# File name for the user's results
user_file_name = f"{user_name}_results.txt"

# Write the user's results to their file
with open(user_file_name, "w") as user_file:
    user_file.write(f"User: {user_name}\n")
    user_file.write(f"Score: {score}\n")
    user_file.write(f"Clicks: {click_count}\n")
    user_file.write(f"Misclicks: {misclick_count}\n")
    user_file.write(f"Timeouts: {timeout_count}\n")

# Append the user's results to the master file
with open("all.txt", "a") as master_file:
    master_file.write(f"User: {user_name}\n")
    master_file.write(f"Score: {score}, Clicks: {click_count}, Misclicks: {misclick_count}, Timeouts: {timeout_count}\n")
    master_file.write("----------\n")

# Quit Pygame
pygame.quit()