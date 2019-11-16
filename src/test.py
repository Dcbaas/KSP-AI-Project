from rocket_data_tracker import RocketData
import krpc

connection = krpc.connect(name='distance_test')

dataObject = RocketData(connection)
print(dataObject.get_distance())