import krpc
from time_warp_helper import TimeWarpHelper
from rocket_data_tracker import RocketData

if __name__ == '__main__':
    connection = krpc.connect(name="YOUR NAME HERE")
    rocket_data = RocketData(connection)
    print()
    connection.close()
