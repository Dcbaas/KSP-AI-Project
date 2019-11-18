import krpc
from time_warp_helper import TimeWarpHelper

if __name__ == '__main__':
    connection = krpc.connect(name="YOUR NAME HERE")
    warp_helper = TimeWarpHelper(connection)
    warp_helper.warp_till_body_shift()
    connection.close()
