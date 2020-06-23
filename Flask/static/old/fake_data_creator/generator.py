# Pablo Fernández R.
import math


def main():
    with open("gen_data.csv", 'w') as outfile:
        outfile.write(
            "latitude, longitude, time, temp, hum, alt, PM2.5, CO2, CO, NO2, NH3 \n")
        radius = 0.0005
        steps = 50.0
        increment = 2.0*math.pi/steps
        angle = 0.0
        while not math.isclose(angle, 2.0*math.pi):
            x = math.sin(angle)*radius
            y = math.cos(angle)*radius
            value = angle
            outfile.write("{},{},17:48:44.00,24,40,634,80,13,{},10,4".format(
                40.4106902+x, -3.6938668+y, value/math.pi)+"\n")
            angle += increment


if __name__ == '__main__':
    main()
