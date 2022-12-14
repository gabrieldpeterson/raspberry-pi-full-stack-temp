from flask import Flask, request, render_template
import time
import datetime
import sys
import board
import adafruit_sht31d
import sqlite3


app = Flask(__name__)
app.debug = True # Make this False if you are no longer debugging


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/lab_temp")
def lab_temp():
    i2c = board.I2C()
    sensor = adafruit_sht31d.SHT31D(i2c)

    temperature = sensor.temperature
    humidity = sensor.relative_humidity

    if humidity is not None and temperature is not None:
        return render_template("lab_temp.html",temp=temperature,hum=humidity)
    else:
        return render_template("no_sensor.html")


@app.route("/lab_env_db", methods = ['GET'])
def lab_env_db():
    from_date_str   = request.args.get('from',time.strftime("%Y-%m-%d %H:%M")) #Get the from date value from the URL
    to_date_str     = request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))   #Get the to date value from the URL

    if not validate_date(from_date_str):
        from_date_str = time.strftime("%Y-%m-%d 00:00")
    if not validate_date(to_date_str):
        to_date_str = time.strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect('/var/www/lab_app/lab_app.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM temperatures WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
    temperatures = curs.fetchall()
    curs.execute("SELECT * FROM humidities WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
    humidities = curs.fetchall()
    conn.close()
    return render_template("lab_env_db.html",temp=temperatures,hum=humidities)


def validate_date(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

