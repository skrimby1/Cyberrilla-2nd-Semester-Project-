class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, hovering_image):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.hovering_image = hovering_image
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        if self.hovering_image is None:
            self.hovering_image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.is_hovered = False

    def update(self, screen):
        if self.is_hovered:
            screen.blit(self.hovering_image, self.rect)
        else:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.is_hovered = True
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.is_hovered = False