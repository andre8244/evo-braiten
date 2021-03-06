import random
import math

from robot.actuator import Actuator
from robot.motor_controller import MotorController
from robot.sensor_driven_robot import SensorDrivenRobot
from sensor.proximity_sensor import ProximitySensor

ROBOT_WHEEL_RADIUS_MIN = 8
ROBOT_WHEEL_RADIUS_MAX = 30

MOTOR_CTRL_COEFFICIENT_MIN = 50
MOTOR_CTRL_COEFFICIENT_MAX = 600

MOTOR_CTRL_MIN_ACTUATOR_VALUE_MIN = 10
MOTOR_CTRL_MIN_ACTUATOR_VALUE_MAX = 40

SENSOR_DELTA_DIRECTION_MIN = 0
SENSOR_DELTA_DIRECTION_MAX = math.pi / 2

SENSOR_SATURATION_VALUE_MIN = 20
SENSOR_SATURATION_VALUE_MAX = 100

SENSOR_MAX_DISTANCE_MIN = 20
SENSOR_MAX_DISTANCE_MAX = 150


class Genome:

    def __init__(self, robot_wheel_radius, motor_ctrl_coefficient, motor_ctrl_min_actuator_value,
                 sensor_delta_direction, sensor_saturation_value, sensor_max_distance, generation_num=None):
        self.robot_wheel_radius = robot_wheel_radius
        self.motor_ctrl_coefficient = motor_ctrl_coefficient
        self.motor_ctrl_min_actuator_value = motor_ctrl_min_actuator_value
        self.sensor_delta_direction = sensor_delta_direction
        self.sensor_saturation_value = sensor_saturation_value
        self.sensor_max_distance = sensor_max_distance
        self.generation_num = generation_num
        self.fitness = None

    @staticmethod
    def random(generation_num):
        robot_wheel_radius = random.uniform(ROBOT_WHEEL_RADIUS_MIN, ROBOT_WHEEL_RADIUS_MAX)
        motor_ctrl_coefficient = random.uniform(MOTOR_CTRL_COEFFICIENT_MIN, MOTOR_CTRL_COEFFICIENT_MAX)
        motor_ctrl_min_actuator_value = random.uniform(MOTOR_CTRL_MIN_ACTUATOR_VALUE_MIN,
                                                       MOTOR_CTRL_MIN_ACTUATOR_VALUE_MAX)
        sensor_delta_direction = random.uniform(SENSOR_DELTA_DIRECTION_MIN, SENSOR_DELTA_DIRECTION_MAX)
        sensor_saturation_value = random.uniform(SENSOR_SATURATION_VALUE_MIN, SENSOR_SATURATION_VALUE_MAX)
        sensor_max_distance = random.uniform(SENSOR_MAX_DISTANCE_MIN, SENSOR_MAX_DISTANCE_MAX)

        return Genome(robot_wheel_radius, motor_ctrl_coefficient, motor_ctrl_min_actuator_value,
                      sensor_delta_direction, sensor_saturation_value, sensor_max_distance, generation_num)

    def crossover(self, other_parent, generation_num):
        # apply uniform crossover to generate a new genome
        robot_wheel_radius = self.robot_wheel_radius if random.random() < 0.5 else other_parent.robot_wheel_radius
        motor_ctrl_coefficient = self.motor_ctrl_coefficient if random.random() < 0.5 else \
            other_parent.motor_ctrl_coefficient
        motor_ctrl_min_actuator_value = self.motor_ctrl_min_actuator_value if random.random() < 0.5 else \
            other_parent.motor_ctrl_min_actuator_value
        sensor_delta_direction = self.sensor_delta_direction if random.random() < 0.5 else \
            other_parent.sensor_delta_direction
        sensor_saturation_value = self.sensor_saturation_value if random.random() < 0.5 else \
            other_parent.sensor_saturation_value
        sensor_max_distance = self.sensor_max_distance if random.random() < 0.5 else other_parent.sensor_max_distance

        return Genome(robot_wheel_radius, motor_ctrl_coefficient, motor_ctrl_min_actuator_value,
                      sensor_delta_direction, sensor_saturation_value, sensor_max_distance, generation_num)

    def mutation(self, mutation_probability, mutation_coefficient):
        self.robot_wheel_radius = self.mutate_with_probability(self.robot_wheel_radius, mutation_probability,
                                                               mutation_coefficient)
        self.motor_ctrl_coefficient = self.mutate_with_probability(self.motor_ctrl_coefficient, mutation_probability,
                                                                   mutation_coefficient)
        self.motor_ctrl_min_actuator_value = self.mutate_with_probability(self.motor_ctrl_min_actuator_value,
                                                                          mutation_probability, mutation_coefficient)
        self.sensor_delta_direction = self.mutate_with_probability(self.sensor_delta_direction, mutation_probability,
                                                                   mutation_coefficient)
        self.sensor_saturation_value = self.mutate_with_probability(self.sensor_saturation_value, mutation_probability,
                                                                    mutation_coefficient)
        self.sensor_max_distance = self.mutate_with_probability(self.sensor_max_distance, mutation_probability,
                                                                mutation_coefficient)
        self.check_parameter_bounds()

    def mutate_with_probability(self, value, mutation_probability, mutation_coefficient):
        if random.random() < mutation_probability:
            mutation_std_dev = mutation_coefficient * value
            return random.gauss(value, mutation_std_dev)
        else:
            return value

    def check_parameter_bounds(self):
        if self.robot_wheel_radius < ROBOT_WHEEL_RADIUS_MIN:
            self.robot_wheel_radius = ROBOT_WHEEL_RADIUS_MIN
        elif self.robot_wheel_radius > ROBOT_WHEEL_RADIUS_MAX:
            self.robot_wheel_radius = ROBOT_WHEEL_RADIUS_MAX

        if self.motor_ctrl_coefficient < MOTOR_CTRL_COEFFICIENT_MIN:
            self.motor_ctrl_coefficient = MOTOR_CTRL_COEFFICIENT_MIN
        elif self.motor_ctrl_coefficient > MOTOR_CTRL_COEFFICIENT_MAX:
            self.motor_ctrl_coefficient = MOTOR_CTRL_COEFFICIENT_MAX

        if self.motor_ctrl_min_actuator_value < MOTOR_CTRL_MIN_ACTUATOR_VALUE_MIN:
            self.motor_ctrl_min_actuator_value = MOTOR_CTRL_MIN_ACTUATOR_VALUE_MIN
        elif self.motor_ctrl_min_actuator_value > MOTOR_CTRL_MIN_ACTUATOR_VALUE_MAX:
            self.motor_ctrl_min_actuator_value = MOTOR_CTRL_MIN_ACTUATOR_VALUE_MAX

        if self.sensor_delta_direction < SENSOR_DELTA_DIRECTION_MIN:
            self.sensor_delta_direction = SENSOR_DELTA_DIRECTION_MIN
        elif self.sensor_delta_direction > SENSOR_DELTA_DIRECTION_MAX:
            self.sensor_delta_direction = SENSOR_DELTA_DIRECTION_MAX

        if self.sensor_saturation_value < SENSOR_SATURATION_VALUE_MIN:
            self.sensor_saturation_value = SENSOR_SATURATION_VALUE_MIN
        elif self.sensor_saturation_value > SENSOR_SATURATION_VALUE_MAX:
            self.sensor_saturation_value = SENSOR_SATURATION_VALUE_MAX

        if self.sensor_max_distance < SENSOR_MAX_DISTANCE_MIN:
            self.sensor_max_distance = SENSOR_MAX_DISTANCE_MIN
        elif self.sensor_max_distance > SENSOR_MAX_DISTANCE_MAX:
            self.sensor_max_distance = SENSOR_MAX_DISTANCE_MAX

    def __repr__(self):
        fitness_value = None if self.fitness is None else round(self.fitness, 2)
        return self.__class__.__name__ + '(fitness:' + repr(fitness_value) + ' generation_num:' + repr(
            self.generation_num) + ')'

    def to_string(self):
        fitness_value = None if self.fitness is None else round(self.fitness, 2)
        return self.__class__.__name__ + '(fitness:' + repr(fitness_value) + ' generation_num:' + repr(
            self.generation_num) + ' robot_wheel_radius:' + repr(
            round(self.robot_wheel_radius, 2)) + ' motor_ctrl_coefficient:' + repr(
            round(self.motor_ctrl_coefficient, 2)) + ' motor_ctrl_min_actuator_value:' + repr(
            round(self.motor_ctrl_min_actuator_value, 2)) + ' sensor_delta_direction:' + repr(
            round(self.sensor_delta_direction, 2)) + ' sensor_saturation_value:' + repr(
            round(self.sensor_saturation_value, 2)) + ' sensor_max_distance:' + repr(
            round(self.sensor_max_distance, 2)) + ')'

    def get_saved_genome_repr(self):
        return str(self.robot_wheel_radius) + ' ' + str(self.motor_ctrl_coefficient) + ' ' + \
               str(self.motor_ctrl_min_actuator_value) + ' ' + str(self.sensor_delta_direction) + ' ' + \
               str(self.sensor_saturation_value) + ' ' + str(self.sensor_max_distance) + ' ' + \
               str(self.generation_num) + ' ' + str(self.fitness)

    def build_obstacle_avoidance_robot(self, x, y, robot_size, sensor_error, scene):
        robot = SensorDrivenRobot(x, y, robot_size, self.robot_wheel_radius)

        left_obstacle_sensor = ProximitySensor(robot, self.sensor_delta_direction, self.sensor_saturation_value,
                                               sensor_error, self.sensor_max_distance, scene)
        right_obstacle_sensor = ProximitySensor(robot, -self.sensor_delta_direction, self.sensor_saturation_value,
                                                sensor_error, self.sensor_max_distance, scene)
        left_wheel_actuator = Actuator()
        right_wheel_actuator = Actuator()
        left_motor_controller = MotorController(left_obstacle_sensor, self.motor_ctrl_coefficient, left_wheel_actuator,
                                                self.motor_ctrl_min_actuator_value)
        right_motor_controller = MotorController(right_obstacle_sensor, self.motor_ctrl_coefficient, right_wheel_actuator,
                                                 self.motor_ctrl_min_actuator_value)

        robot.set_left_motor_controller(left_motor_controller)
        robot.set_right_motor_controller(right_motor_controller)
        return robot
