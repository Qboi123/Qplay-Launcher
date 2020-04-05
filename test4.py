from sdl2 import *
from sys import stderr

# Open the first available controller.
controller: SDL_GameController
i = 0

display_count: int = 0
display_index: int = 0
mode_index: int = 0;
mode: SDL_DisplayMode = (SDL_PIXELFORMAT_UNKNOWN, 0, 0, 0, 0)


def GetVideoMode():
    if (display_count = SDL_GetNumVideoDisplays()) < 1:
        SDL_Log("SDL_GetNumVideoDisplays returned: %i", display_count);
        return 1
    }

    if SDL_GetDisplayMode(display_index, mode_index, mode) != 0:
        SDL_Log("SDL_GetDisplayMode failed: %s", SDL_GetError());
        return 1
    SDL_Log("SDL_GetDisplayMode(0, 0, &mode):\t\t%i bpp\t%i x %i")
    SDL_BITSPERPIXEL(mode.format), mode.w, mode.h)

print("Video Drivers:", SDL_GetNumVideoDrivers())
print("Display DPI", SDL_GetDisplayDPI())
print("Controllers", SDL_NumJoysticks())
while i < int(SDL_NumJoysticks()):
    print(i)
    if SDL_IsGameController(i):
        controller = SDL_GameControllerOpen(i)
        if controller:
            break
        else:
            print("Could not open gamecontroller %i: %s" % (i, SDL_GetError()), end="\n")
            exit(1)
    i += 1


while True:
    for i in range(0, 50):
        GameContollerAxis = SDL_GameControllerAxis()

        Value = SDL_GameControllerGetButton(controller, SDL_CONTROLLER_BUTTON_A)

        if Value == 1:
            print(Value)