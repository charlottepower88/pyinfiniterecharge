#!/usr/bin/env python3

# Copyright (c) 2017-2018 FIRST. All Rights Reserved.
# Open Source Software - may be modified and shared by FRC teams. The code
# must be accompanied by the FIRST BSD license file in the root directory of
# the project.

import wpilib
import rev
import rev.color

import magicbot

from controllers.shooter import ShooterController
from controllers.spinner import SpinnerController
from components.indexer import Indexer
from components.shooter import Shooter
from components.spinner import Spinner
from components.vision import Vision


class MyRobot(magicbot.MagicRobot):
    shooter_controller: ShooterController
    spinner_controller: SpinnerController
    indexer: Indexer
    shooter: Shooter
    spinner: Spinner

    def createObjects(self):
        """Robot initialization function"""
        # object that handles basic drive operations
        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)
        self.spinner_joystick = wpilib.Joystick(2)

        self.shooter_outer_motor = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.shooter_centre_motor = rev.CANSparkMax(2, rev.MotorType.kBrushless)

        self.loading_piston = wpilib.Solenoid(0)

        self.indexer_motors = [wpilib.Spark(9), wpilib.Spark(8), wpilib.Spark(7)]
        self.indexer_switches = [
            wpilib.DigitalInput(9),
            wpilib.DigitalInput(8),
            wpilib.DigitalInput(7),
        ]

        self.spinner_motor = wpilib.Spark(2)
        self.spinner_solenoid = wpilib.DoubleSolenoid(2, 3)
        self.colour_sensor = rev.color.ColorSensorV3(wpilib.I2C.Port.kOnboard)

        self.vision = Vision()

    def teleopInit(self):
        """Executed at the start of teleop mode"""

    def teleopPeriodic(self):
        """Executed every cycle"""
        outer_throttle = ((-self.joystick_left.getThrottle() + 1) / 2) * 5000
        inner_throttle = -((-self.joystick_right.getThrottle() + 1) / 2) * 5000

        self.shooter.set_motor_rpm(outer_throttle, inner_throttle)

        wpilib.SmartDashboard.putNumber("outerError", self.shooter.get_outer_error())
        wpilib.SmartDashboard.putNumber("centreError", self.shooter.get_centre_error())

        wpilib.SmartDashboard.putNumber("outerVelocity", outer_throttle)
        wpilib.SmartDashboard.putNumber("centreVelocity", inner_throttle)

        if self.joystick_left.getRawButtonPressed(11):
            self.loading_piston.startPulse()

        if self.joystick_left.getRawButtonPressed(7):
            if self.indexer.indexing:
                self.indexer.disable_indexing()
            else:
                self.indexer.enable_indexing()


        self.handle_spinner_inputs(self.spinner_joystick)

    def handle_spinner_inputs(self, joystick):
        if joystick.getRawButtonPressed(7):
            self.spinner_controller.run(test=True, task="position")
            print(f"Spinner Running")
        if joystick.getRawButtonPressed(9):
            self.spinner.piston_up()
            print("Spinner Piston Up")
        if joystick.getRawButtonPressed(10):
            self.spinner.piston_down()
            print("Spinner Piston Down")
        if joystick.getRawButtonPressed(8):
            print(f"Detected Colour: {self.spinner_controller.get_current_colour()}")
            print(f"Distance: {self.spinner_controller.get_wheel_dist()}")


if __name__ == "__main__":
    wpilib.run(MyRobot)
