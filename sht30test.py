import board
import adafruit_sht31d

# dhtDevice = adafruit_dht.DHT22(board.D17)
i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

temperature_c = sensor.temperature
temperature_f = temperature_c * (9 / 5) + 32
humidity = sensor.relative_humidity
print("Temp: {:.1f} F / {:.1f} C Humidity: {}% ".format(temperature_f, temperature_c,
humidity))
