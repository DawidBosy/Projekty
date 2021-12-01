import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, atan, radians, degrees
from scipy import interpolate

RED = '\u001b[31m'
GREEN = '\u001b[32m'


def deriv(f, x):
    h = 0.001
    return (f(x + h) - f(x)) / h


class Engine:
    def __init__(self, thrustForceMin, thrustForceMax):
        # thrustForce constrains
        self.thrustForceMin = thrustForceMin
        self.thrustForceMax = thrustForceMax

        # keeping track of thrust force changes in time
        self.thrustForce = [0.0, ]


class Regulator:
    def __init__(self, uMin, uMax, kp):
        # regulator constrains
        self.uMin = uMin
        self.uMax = uMax

        # amplification factor
        self.kp = kp
        self.e = [0.0, ]
        self.u = [0.0, ]
        self.uPrevious = [0.0, ]

        self.Tp = 0.1
        self.Ti = 0.25
        self.Td = 0.009


class Car:
    def __init__(self, engine, velocityMin, velocityMax, Sd, mass, Cd, wheelRadius):
        # engine component
        self.engine = engine

        # keeping track ofvelocity changes in time
        self.velocity = [0.0, ]

        # car frontal surface
        self.Sd = Sd

        # car mass
        self.mass = mass

        # car air resistance factor
        self.Cd = Cd

        # car's wheels radius
        self.wheelRadius = wheelRadius


class Road:
    def __init__(self, keyPoints):
        # friction factor of the road
        self.frictionFactor = 0.025

        # keeping track of friction force and pull force
        self.frictionForce = [0.0, ]
        self.pullForce = [0.0, ]

        # key points of the road, used to generate road polynomial
        self.keyPoints = keyPoints

        # numpy arrays used to lagrange's interpolation
        self.xPoints = np.array([x for (x, y) in self.keyPoints])
        self.yPoints = np.array([y for (x, y) in self.keyPoints])

        # last xPosition that have been determined by key points
        self.xMaxDetermined = max(self.xPoints)

        # polynomial of lagrange's interpolation
        self.poly = interpolate.lagrange(self.xPoints, self.yPoints)

        # slope angle of last xPosition determined
        self.alphaLast = atan(deriv(self.getYPosition, self.xMaxDetermined))

    # count yPosition determined by polynomial
    def getYPosition(self, xPosition):
        return self.poly(xPosition)

    # get degree of road slope (in radians)
    def getRadiansAngle(self, xPosition):
        if xPosition > self.xMaxDetermined:
            return self.alphaLast

        a = deriv(self.getYPosition, xPosition)
        return atan(a)

        # get degree of road slope (in C degrees)
        def getDegreesAngle(self, xPosition):
            if xPosition > self.xMaxDetermined:
                return degrees(self.alphaLast)

            a = deriv(self.getYPosition, xPosition)
            return degrees(atan(a))


class Wind:
    def __init__(self, velocity):
        self.rho = 1.225
        self.velocity = velocity

        # keeping track of air resistance
        self.airResistance = [0.0, ]


class CruiseControl:
    def __init__(self, regulator, car, road, wind, velocityRequired, simulationTime):
        # G constant
        self.gConstant = 9.81

        # Components of CruiseControl PID
        self.regulator = regulator
        self.car = car
        self.road = road
        self.wind = wind

        # keeping track of distance, xPosition, yPosition
        self.distanceTraveled = [0.0, ]
        self.xPosition = [0.0, ]
        self.yPosition = [0.0, ]

        # simulation time and number of iterations
        self.simulationTime = simulationTime
        self.N = int(self.simulationTime / self.regulator.Tp)

        # velocity required
        self.velocityRequired = velocityRequired

        # slopes used for PID
        self.straightA = (self.car.engine.thrustForceMax - self.car.engine.thrustForceMin) / \
            (self.regulator.uMax - self.regulator.uMin)

        self.straightB = self.car.engine.thrustForceMin - \
            self.straightA * self.regulator.uMin

    def simulate(self):
        for _ in range(self.N):
            # wyznaczanie wartosci uchybu
            self.regulator.e.append(
                self.velocityRequired - self.car.velocity[-1])

            # wyznaczanie wielkosci sterujacej
            self.regulator.uPrevious.append(self.regulator.kp * (self.regulator.e[-1] + (self.regulator.Tp / self.regulator.Ti) * sum(
                self.regulator.e) + (self.regulator.Td / self.regulator.Tp) * (self.regulator.e[-1] - self.regulator.e[-2])))

            self.regulator.u.append(max(self.regulator.uMin, min(
                self.regulator.uMax, self.regulator.uPrevious[-1])))

            # counting thrust Force
            self.car.engine.thrustForce.append(max(self.car.engine.thrustForceMin, min(
                self.car.engine.thrustForceMax, self.straightA * self.regulator.u[-1] + self.straightB)))

            currentSlope = self.road.getRadiansAngle(self.xPosition[-1])

            carThrustForce = self.car.engine.thrustForce[-1]
            airResistance = self.car.Cd * self.car.Sd * \
                (self.wind.rho * (self.wind.velocity -
                                  self.car.velocity[-1])**2) / 2
            frictionForce = self.car.mass * self.gConstant * \
                cos(currentSlope) * self.road.frictionFactor / \
                self.car.wheelRadius
            pullForce = self.car.mass * self.gConstant * \
                sin(currentSlope)

            if self.wind.velocity == 0 and self.car.velocity[-1] > 0:
                airResistance = -abs(airResistance)
            elif self.wind.velocity == 0 and self.car.velocity[-1] < 0:
                airResistance = abs(airResistance)
            elif self.wind.velocity > 0 and self.car.velocity[-1] > 0:
                if self.wind.velocity > self.car.velocity[-1]:
                    airResistance = abs(airResistance)
                elif self.wind.velocity < self.car.velocity[-1]:
                    airResistance = -abs(airResistance)
            elif self.wind.velocity > 0 and self.car.velocity[-1] < 0:
                airResistance = abs(airResistance)
            elif self.wind.velocity < 0 and self.car.velocity[-1] > 0:
                airResistance = -abs(airResistance)
            elif self.wind.velocity < 0 and self.car.velocity[-1] < 0:
                if self.wind.velocity > self.car.velocity[-1]:
                    airResistance = -abs(airResistance)
                elif self.wind.velocity < self.car.velocity[-1]:
                    airResistance = abs(airResistance)

            if self.car.velocity[-1] == 0:
                frictionForce = 0
            elif self.car.velocity[-1] > 0:
                frictionForce = -abs(frictionForce)
            elif self.car.velocity[-1] < 0:
                frictionForce = abs(frictionForce)

            if currentSlope > 0:
                pullForce = -abs(pullForce)
            elif currentSlope < 0:
                pullForce = abs(pullForce)
            elif currentSlope == 0:
                pullForce = 0

            self.wind.airResistance.append(airResistance)
            self.road.frictionForce.append(frictionForce)
            self.road.pullForce.append(pullForce)

            deltaVelocity = ((carThrustForce + frictionForce +
                              pullForce + airResistance) * self.regulator.Tp) / self.car.mass

            self.car.velocity.append(self.car.velocity[-1] + deltaVelocity)

            distancePerdiodTraveled = self.car.velocity[-1] * self.regulator.Tp

            self.distanceTraveled.append(
                self.distanceTraveled[-1] + distancePerdiodTraveled)
            self.xPosition.append(self.xPosition[-1] + abs(cos(
                currentSlope)) * distancePerdiodTraveled)
            self.yPosition.append(self.yPosition[-1] + sin(
                currentSlope) * distancePerdiodTraveled)

        t = [i * self.regulator.Tp for i in range(self.N + 1)]

        forces = [self.car.engine.thrustForce, self.road.frictionForce, self.road.pullForce, self.wind.airResistance]
        xArr = [x for x in range(0, self.road.xMaxDetermined)]
        yArr = self.road.getYPosition(xArr)

        return t, self.car.velocity, self.xPosition, self.yPosition, xArr, yArr, forces

    def drawChart(self):
        t = [i * self.regulator.Tp for i in range(self.N + 1)]
        xArr = [x for x in range(0, self.road.xMaxDetermined)]
        yArr = self.road.getYPosition(xArr)

        plt.subplot(5, 1, 1)
        plt.plot(t, self.car.velocity, label="carVelocity")
        plt.axhline(y=self.velocityRequired, color='r',
                    linestyle='--', label="velocityRequired")
        plt.legend()

        plt.subplot(5, 1, 2)
        plt.plot(t, self.yPosition, label="yPosition [time]")
        plt.legend()

        plt.subplot(5, 1, 3)
        plt.plot(self.xPosition, self.yPosition, label="yPositon [xPosition]")
        plt.legend()

        plt.subplot(5, 1, 4)
        plt.plot(xArr, yArr, label="road")
        plt.legend()

        plt.subplot(5, 1, 5)
        self.road.frictionForce.append(self.road.frictionForce[-1])
        self.road.pullForce.append(self.road.pullForce[-1])
        self.wind.airResistance.append(self.wind.airResistance[-1])
        plt.plot(t, self.car.engine.thrustForce, label="thrustForce")
        plt.plot(t, self.road.frictionForce, label="frictionForce")
        plt.plot(t, self.road.pullForce, label="pullForce")
        plt.plot(t, self.wind.airResistance, label="airResistance")
        plt.legend()

        plt.show()


if __name__ == '__main__':
    regulator = Regulator(uMin=-5, uMax=5, kp=0.0007)
    car = Car(engine=Engine(thrustForceMin=-10000, thrustForceMax=10000),
              velocityMin=0.0, velocityMax=60, Sd=7, mass=1200, Cd=0.25, wheelRadius=0.2)
    road = Road(keyPoints=[(0, 0), (3000,25), (6000,50), (9000,25), (12000,0), (15000,-25), (18000,0), (21000,75), (24000, 0), (27000,-15), (30000,0)])
    wind = Wind(velocity=10)

    cc = CruiseControl(regulator=regulator, car=car, road=road, wind=wind,
                       velocityRequired=35, simulationTime=850)

    cc.simulate()
    cc.drawChart()
