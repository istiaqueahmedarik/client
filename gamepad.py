import pygame


def main():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No joystick detected.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Initialized joystick:", joystick.get_name())

    axes = joystick.get_numaxes()
    buttons = joystick.get_numbuttons()

    print("Number of axes:", axes)
    print("Number of buttons:", buttons)

    while True:
        pygame.event.pump()

        # Read axis values
        for i in range(axes):
            axis_value = joystick.get_axis(i)
            print(f"Axis {i}: {axis_value}")

        # Read button values
        for i in range(buttons):
            button_value = joystick.get_button(i)
            if button_value == 1:
                print(f"Button {i} pressed")


if __name__ == "__main__":
    main()
