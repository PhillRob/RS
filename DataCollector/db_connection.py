import os
from influxdb import InfluxDBClient


class DBClient:
    def __init__(self):
        self.__addr = os.environ.get('INFLUX_ADDRESS')
        self.__port = os.environ.get('INFLUX_PORT')
        self.__user = os.environ.get('INFLUX_USER')
        self.__passwd = os.environ.get('INFLUX_PASS')
        self.__dbname = 'sentinel_data'
        self.client = InfluxDBClient(
            self.__addr,
            self.__port,
            self.__user,
            self.__passwd,
            self.__dbname
        )
        dbnames = [x['name'] for x in self.client.get_list_database()]
        if self.__dbname not in dbnames:
            self.client.create_database(self.__dbname)


    def push_measurement(self, time, measurement: dict):
        body = \
            [{
                 "measurement":"satellite_measurements",
                 "tags":{},
                 "time":time,
                 "fields":measurement
            }]
        # print("points: {}".format(body))
        self.client.write_points(body)


    def measurement_exists(self, mid):
        query = self.client.query('SELECT * FROM "sentinel_data"."autogen"."satellite_measurements" WHERE id=$id', bind_params={'id': mid.uuid})
        duplicate = len(query.items()) > 0
        return duplicate
