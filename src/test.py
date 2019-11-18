from rocket_data_tracker import RocketData
import krpc
from stats_monitor import Monitor
import fitness
import os

def update_monitor(monitor, rocket_data:RocketData):
    orbit_data = rocket_data.get_orbit_data()
    dist_from_target =  rocket_data.get_distance()
    closest_approach = rocket_data.get_closest_approach()
    speed = rocket_data.get_speed()
    situation = rocket_data.get_situation()

    # Set the values
    monitor.set_closest_landing_dist(dist_from_target)
    monitor.set_closest_approach(closest_approach)
    monitor.set_lowest_speed_at_touchdown(speed)
    monitor.set_final_situation(situation)
    monitor.set_max_ap(orbit_data[1])
    monitor.set_max_pe(orbit_data[2])
    monitor.set_body_name(orbit_data[0])

connection = krpc.connect(name='distance_test')

dataObject = RocketData(connection)
monitor = Monitor()
while True:
    update_monitor(monitor, dataObject)
    score = fitness.calc_fitness(monitor)
    print(score)


connection.close()
print(monitor)
