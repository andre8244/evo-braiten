import time
import pygame

from geometry.point import Point
from scene.wall import Wall
from scene.box import Box
from geometry.color import Color


class Scene:

    def __init__(self, width, height, speed, screen):
        self.width = width
        self.height = height
        self.speed = speed
        self.screen = screen
        self.objects = []

    def put(self, obj):
        if isinstance(obj, list):
            self.objects.extend(obj)
        else:
            self.objects.append(obj)

    def remove(self, obj):
        self.objects.remove(obj)

    def save(self):
        date_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = "scene_" + date_time + ".txt"
        file_path = 'saved_scenes/' + file_name

        with open(file_path, 'w') as f:
            f.write(self.get_saved_scene_repr() + '\n')  # first line with scene size

            for obj in self.objects:
                if hasattr(obj, 'get_saved_scene_repr'):
                    line = obj.get_saved_scene_repr()
                    f.write(line + '\n')
                else:
                    print('Object unsaved:', obj)
        f.closed
        print('Scene saved:', file_path)

    def get_saved_scene_repr(self):
        return self.__class__.__name__ + ' ' + str(self.width) + ' ' + str(self.height)

    @staticmethod
    def load_from_file(file_path, scene_speed):
        with open(file_path) as f:
            line_number = 1

            for line in f:
                words = line.split()

                if words[0] == 'Scene':
                    width = int(words[1])
                    height = int(words[2])
                    screen = pygame.display.set_mode((width, height))
                    scene = Scene(width, height, scene_speed, screen)
                # elif words[0] == 'SensorDrivenRobot':
                #     x = float(words[1])
                #     y = float(words[2])
                #     robot = SensorDrivenRobot(x, y, ROBOT_SIZE, ROBOT_WHEEL_RADIUS)
                #     robot.set_label(line_number)
                #     scene.put(robot)
                elif words[0] == 'Box':
                    x = int(words[1])
                    y = int(words[2])
                    size = int(words[3])
                    box = Box(x, y, size, Color.random_bright())
                    box.set_label(line_number)
                    scene.put(box)
                elif words[0] == 'Wall':
                    x1 = int(words[1])
                    y1 = int(words[2])
                    x2 = int(words[3])
                    y2 = int(words[4])

                    point1 = Point(x1, y1)
                    point2 = Point(x2, y2)
                    wall = Wall(point1, point2, Color.random_bright())
                    wall.set_label(line_number)
                    scene.put(wall)

                line_number += 1

        f.closed
        return scene, screen