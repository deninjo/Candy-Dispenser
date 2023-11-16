import pygame
pygame.init()

# Create screen
WIDTH = 700
HEIGHT = 770
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Dispenser")
icon = pygame.image.load('sweet.png')
pygame.display.set_icon(icon)

font = pygame.font.SysFont('Calibri', 30)

# Global variables
clicked = False
counter = 0


# Stack (initially empty)
stack = []

# Dictionary Colors for circles
circle_colors = {
    (186, 26, 229): "Purple",
    (115, 226, 89): "Green",
    (222, 141, 50): "Orange",
    (30, 207, 225): "Cyan",
    (218, 1, 41): "Red",
    (237, 47, 145): "Pink",
}

# Buttons
class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, WIN, outline=None):
        if outline:
            pygame.draw.rect(WIN, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.height), 0)

        # displaying text on button
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 28)
            text = font.render(self.text, 1, (0, 0, 0))
            WIN.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    # checking if mouse cursor is over button
    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


# creating buttons
push_button = Button((0, 255, 0), 30, 100, 80, 50, 'Push')
pop_button = Button((255, 0, 0), 150, 100, 80, 50, 'Pop')
peek_button = Button((0, 0, 255), 270, 100, 80, 50, 'Peek')
size_button = Button((255, 255, 0), 390, 100, 80, 50, 'Size')
isempty_button = Button((255, 165, 0), 510, 100, 120, 50, 'IsEmpty')

# Initialize spring length, maximum spring length, and zigzag spacing
spring_length = 387
max_spring_length = 387
zigzag_spacing = 10

# Draw the window
def draw_win():
    WIN.fill((27, 170, 192))

    for button in [push_button, pop_button, peek_button, size_button, isempty_button]:
        button.draw(WIN, (0, 0, 0))

    # Draw the container
    pygame.draw.line(WIN, (144, 12, 63), (300, 256), (300, 650), width=8)
    pygame.draw.line(WIN, (144, 12, 63), (297, 650), (390, 650), width=8)
    pygame.draw.line(WIN, (144, 12, 63), (390, 654), (390, 256), width=8)

    # Calculate the spring's current position
    spring_x = 362
    spring_y = 648 - spring_length

    # Calculate the maximum spring length for 6 candies
    max_spring_length = 390 - 6 * 63

    # Update the zigzag spacing based on the number of candies
    zigzag_spacing = max(2, int(spring_length / 40))

    # Calculate the y position for the first candy so that it's on top of the zigzag
    candy_y = spring_y + zigzag_spacing - 31

    # Draw the spring structure as zigzag lines
    for i in range(0, int(spring_length), zigzag_spacing):
        if i // zigzag_spacing % 2 == 0:
            pygame.draw.line(WIN, (0, 0, 0), (spring_x, spring_y + i), (spring_x - 35, spring_y + i + zigzag_spacing), width=2)  # creating a diagonal to the left
        else:
            pygame.draw.line(WIN, (0, 0, 0), (spring_x - 35, spring_y + i), (spring_x, spring_y + i + zigzag_spacing), width=2)  # creating a diagonal to the right

    # Draw the circles on top of each other
    for color in stack:
        candy_x = 347
        pygame.draw.circle(WIN, color, (candy_x, candy_y), 31)
        candy_y -= 63

    pygame.display.update()

# Main loop
def main():
    global spring_length, zigzag_spacing

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for button in [push_button, pop_button, peek_button, size_button, isempty_button]:
                        if button.is_over(pos):
                            if button.text == 'Push':
                                if len(stack) < 6:
                                    # Add a circle of the specified color
                                    stack.append(list(circle_colors.keys())[len(stack)])

                                    # Adjust spring and zigzag spacing
                                    spring_length -= 63
                                    zigzag_spacing = max(2, int(spring_length / 40))


                                else:
                                    print("Candy Dispenser is full!")

                            elif button.text == 'Pop':
                                if len(stack) > 0:
                                    removed_color = stack.pop()

                                    # Adjust spring and zigzag spacing
                                    spring_length += 63
                                    zigzag_spacing = max(2, int(spring_length / 40))

                                    color_name = circle_colors.get(removed_color, "Unknown")
                                    print(f"Removed candy of color: {color_name}")
                                else:
                                    print("Candy Dispenser is empty!")

                            elif button.text == 'Peek':
                                if len(stack) > 0:
                                    top_color = stack[-1]
                                    color_name = circle_colors.get(top_color, "Unknown")
                                    print(f"Top candy color is {color_name}")
                                else:
                                    print("Candy Dispenser is empty!")
                            elif button.text == 'Size':
                                print(f"Dispenser size: {len(stack)}")
                            elif button.text == 'IsEmpty':
                                print(f"Is Dispenser empty: {len(stack) == 0}")

        # Ensure that spring length does not go below zero and does not exceed the maximum
        spring_length = max(0, min(spring_length, max_spring_length))

        draw_win()

    pygame.quit()

# Running the game from this file
if __name__ == "__main__":
    main()
