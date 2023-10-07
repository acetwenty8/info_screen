from tkinter import *
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import time as t
from time import strftime
from time import mktime
from datetime import datetime, date, time, timedelta
import pytz
from tkcalendar import Calendar
import calendar
from urllib.request import urlopen
from urllib.error import URLError, HTTPError, ContentTooShortError
import json
from info_screen_libTable import *
from astral import LocationInfo
from astral.sun import sun
from string import Formatter
import pygame
import sys
import os
import threading
from metar import Metar
import metpy.calc as mpcalc
from metpy.units import units
import re
import string
from PIL import ImageTk, Image
from skyfield.api import N, S, E, W, load, wgs84
from skyfield.framelib import ecliptic_frame
from skyfield.trigonometry import position_angle_of
from skyfield import almanac
import math
from math import sin, cos
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import numpy as np
from bs4 import BeautifulSoup
import asyncio
from pyairnow import WebServiceAPI
from info_screen_config import *

def lcl_clock():
    #s = strftime('%H:%M:%S %Z')
    s = strftime('%H:%M  %Z')
    lcl_clock_label.config(text=s,
                           font=('Lucida Console', 30, 'bold'),
                           background='black',
                           foreground='#00c800',
                           justify='center',
                           highlightthickness=2,
                           highlightbackground='#00c800',
                           highlightcolor='#00c800',
                           width=9,
                           padx=15,
                           pady=0,
                           anchor='center')
    lcl_clock_label.after(1000, lcl_clock)

def utc_clock():
    utc = pytz.utc
    dt = datetime.now(utc)
    #s = dt.strftime('%H:%M:%S %Z')
    s = dt.strftime('%H:%M  %Z')
    utc_clock_label.config(text=s,
                           font=('Lucida Console', 30, 'bold'),
                           background='black',
                           foreground='#00c800',
                           justify='center',
                           highlightthickness=2,
                           highlightbackground='#00c800',
                           highlightcolor='#00c800',
                           width=9,
                           padx=15,
                           pady=0,
                           anchor='center')
    utc_clock_label.after(1000, utc_clock)

def india_clock():
    india = pytz.timezone('Asia/Kolkata')
    dt = datetime.now(india)
    #s = dt.strftime('%H:%M:%S %Z')
    s = dt.strftime('%H:%M  %Z')
    india_clock_label.config(text=s,
                           font=('Lucida Console', 30, 'bold'),
                           background='black',
                           foreground='#00c800',
                           justify='center',
                           highlightthickness=2,
                           highlightbackground='#00c800',
                           highlightcolor='#00c800',
                           width=9,
                           padx=15,
                           pady=0,
                           anchor='center')
    india_clock_label.after(1000, india_clock)

def airnow():

    async def main() -> None:
        global O3
        global pm25
        O3 = 0
        pm25 = 0
        client = WebServiceAPI(airnow_api_key)

        def async_error(e):
            airnow_data = ""
            error_date = datetime.now().isoformat()
            print(str(error_date) + " airnow Error:" + str(e))
            root.after(300000, airnow)

        try:
            airnow_data = await client.observations.zipCode('01464')
        except OSError as e:
            async_error(e)
        except TimeoutError as e:
            async_error(e)
        except CancelledError as e:
            async_error(e)
        except InvalidStateError as e:
            async_error(e)
        except SendfileNotAvailableError as e:
            async_error(e)
        except LimitOverrunError as e:
            async_error(e)

        airnow_json_dumps = json.dumps(airnow_data)
        airnow_json_loads = json.loads(airnow_json_dumps)

        for key in airnow_json_loads:
            if "O3" == key['ParameterName']:
                O3 = int(key['AQI'])

        for key in airnow_json_loads:
            if "PM2.5" == key['ParameterName']:
                pm25 = int(key['AQI'])
    asyncio.run(main())

    if O3 > 301:
        O3_bg_color = '#7E0023'
        O3_fg_color = 'white'
    elif O3 > 201:
        O3_bg_color = '#8F3F97'
        O3_fg_color = 'white'
    elif O3 > 151:
        O3_bg_color = '#ff0000'
        O3_fg_color = 'white'
    elif O3 > 101:
        O3_bg_color = '#FF7E00'
        O3_fg_color = 'black'
    elif O3 > 51:
        O3_bg_color = '#FFFF00'
        O3_fg_color = 'black'
    else:
        O3_bg_color = '#00E400'
        O3_fg_color = 'black'

    if pm25 > 301:
        pm25_bg_color = '#7E0023'
        pm25_fg_color = 'white'
    elif pm25 > 201:
        pm25_bg_color = '#8F3F97'
        pm25_fg_color = 'white'
    elif pm25 > 151:
        pm25_bg_color = '#ff0000'
        pm25_fg_color = 'white'
    elif pm25 > 101:
        pm25_bg_color = '#FF7E00'
        pm25_fg_color = 'black'
    elif pm25 > 51:
        pm25_bg_color = '#FFFF00'
        pm25_fg_color = 'black'
    else:
        pm25_bg_color = '#00E400'
        pm25_fg_color = 'black'


    airnow_label_nw.config(text="Ozone",
			   font=('Arial', 30, 'bold'),
			   background='black',
			   foreground='#00c800',
			   justify='center',
			   highlightthickness=2,
			   highlightbackground='#00c800',
			   highlightcolor='#00c800',
			   width=3,
			   padx=0,
			   pady=0,
			   anchor='center')
    airnow_label_ne.config(text=O3,
                           font=('Arial', 30, 'bold'),
                           #background='black',
                           background=O3_bg_color,
                           foreground=O3_fg_color,
                           justify='center',
                           highlightthickness=2,
                           highlightbackground='#00c800',
                           highlightcolor='#00c800',
                           width=3,
                           padx=0,
                           pady=0,
                           anchor='center')
    airnow_label_sw.config(text="PM2.5",
                           font=('Arial', 30, 'bold'),
                           background='black',
                           foreground='#00c800',
                           justify='center',
                           highlightthickness=2,
                           highlightbackground='#00c800',
                           highlightcolor='#00c800',
                           width=3,
                           padx=0,
                           pady=0,
                           anchor='center')
    airnow_label_se.config(text=pm25,
                           font=('Arial', 30, 'bold'),
                           #background='black',
                           background=pm25_bg_color,
                           foreground=pm25_fg_color,
                           justify='center',
                           highlightthickness=2,
                           highlightbackground='#00c800',
                           highlightcolor='#00c800',
                           width=3,
                           padx=0,
                           pady=0,
                           anchor='center')
    root.after(300000, airnow)

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(tz=None)

def load_metar():
    with urlopen( 'https://tgftp.nws.noaa.gov/data/observations/metar/stations/KFIT.TXT' ) as webpage:
        kfit_metar = webpage.read().decode()
    with urlopen( 'https://tgftp.nws.noaa.gov/data/observations/metar/stations/KBED.TXT' ) as webpage:
        kbed_metar = webpage.read().decode()
    with urlopen( 'https://tgftp.nws.noaa.gov/data/observations/metar/stations/KORH.TXT' ) as webpage:
        korh_metar = webpage.read().decode()
    with urlopen( 'https://tgftp.nws.noaa.gov/data/observations/metar/stations/KPSF.TXT' ) as webpage:
        kpsf_metar = webpage.read().decode()
    with urlopen( 'https://tgftp.nws.noaa.gov/data/forecasts/taf/stations/KBED.TXT' ) as webpage:
        kbed_taf = webpage.read().decode()

    metar_label.config(text=kfit_metar.split("\n",1)[1] + korh_metar.split("\n",1)[1] + kpsf_metar.split("\n",1)[1] + kbed_metar.split("\n",1)[1] + kbed_taf.split("\n",1)[1],
                       #font=('Lucida Console', 18, 'bold'),
                       font=('Arial', 22, 'bold'),
                       background='black',
                       foreground='#00c800',
                       justify='left',
                       highlightthickness=2,
                       highlightbackground='#00c800',
                       highlightcolor='#00c800',
                       padx=8,
                       pady=2,
                       anchor='nw')
    root.after(300000, load_metar)


#def load_date_display():

    #date_display_str= strftime("%A %B %d, %Y")
    ##print('date_display_str=' + date_display_str)
    #datedisplay_label.config(text=date_display_str,
    #                         font=('Charcoal', 25),
    #                         background='black',
    #                         foreground='#00c800',
    #                         justify='left',
    #                         highlightthickness=2,
    #                         highlightbackground='#00c800',
    #                         highlightcolor='#00c800',
    #                         padx=7,
    #                         pady=4,
    #                         anchor='center')

def cal_set_date():
    cal_display.selection_clear()
    cal_date = datetime.today()
    cal_display.selection_set(cal_date)
    #print(str(cal_date))

def fixed_map(style, style_name, option):
    # Returns the style map for 'option' with any styles starting with
    # ("!disabled", "!selected", ...) filtered out

    # style.map() returns an empty list for missing options, so this should
    # be future-safe
    return [elm for elm in style.map(style_name, query_opt=option)
            if elm[:2] != ("!disabled", "!selected")]

def query_json_temp(sensor_json, sensor_id):
    for key in sensor_json:
        if sensor_id == key['sensor_id']:
            #print(key['id'])
            return key['tempf']

def query_json_humid(sensor_json, sensor_id):
    for key in sensor_json:
        if sensor_id  == key['sensor_id']:
            #print(key['id'])
            return key['humidity']

def load_sensor_data():
    #st_count = 0

    class sensor_station:
        def __init__(self, name, temp, humid):
            self.name = name
            self.temp = temp
            self.humid = humid

    with urlopen( 'http://172.16.100.10/temp_data.php' ) as webpage:
        sensor_text = webpage.read().decode()

    sensor_json=json.loads(sensor_text)
    sensor_json.sort(key = lambda json: json['id'], reverse=True)

    st_office = sensor_station('Office', query_json_temp(sensor_json, str(10)), query_json_humid(sensor_json, str(10)))
    st_living = sensor_station('Living', query_json_temp(sensor_json, str(11)), query_json_humid(sensor_json, str(11)))
    st_dining = sensor_station('Dining', query_json_temp(sensor_json, str(12)), query_json_humid(sensor_json, str(12)))
    st_bedroom = sensor_station('Bedroom', query_json_temp(sensor_json, str(13)), query_json_humid(sensor_json, str(13)))

    #st_object_list_add = [st_office, st_living, st_dining, st_bedroom]
    #st_object_list.clear()
    #st_object_list.extend(st_object_list_add)

    degree_sign = u'\N{DEGREE SIGN}'

    sensor_tableV2.set_data([[st_office.name, st_office.temp + degree_sign + ' F', st_office.humid + '%'],
                             [st_living.name, st_living.temp + degree_sign + ' F', st_living.humid + '%'],
                             [st_dining.name, st_dining.temp + degree_sign + ' F', st_dining.humid + '%'],
                             [st_bedroom.name, st_bedroom.temp + degree_sign + ' F', st_bedroom.humid + '%']])

    #root_update()
    #sensor_frame_height = sensor_frame.winfo_height()
    #sensor_frame_width = sensor_frame.winfo_width()
    #print('sensor_frame h:' + str(sensor_frame_height) + ' sensor_frame w:' + str(sensor_frame_width))


    #tag_value = 'norm'
    #sensor_table.delete(*sensor_table.get_children())
    #for st_object in st_object_list:
    #    sensor_table.insert(parent='', index='end', iid=st_count, text=f'{st_count +1}', tags=(tag_value,), values=(st_object.name, st_object.temp + degree_sign + ' F', st_object.humid + '%'))
    #    #print('Count:' + str(st_count) + ' Station:' + st_object.name + ' Temp:' + str(st_object.temp) + ' Humidity:' + str(st_object.humid))
    #    st_count += 1
    #    if(tag_value == 'norm'):
    #        tag_value = 'alt'
    #    else:
    #        tag_value = 'norm'
    #
    #del st_office
    #del st_living
    #del st_dining
    #del st_bedroom
    root.after(60000, load_sensor_data)

def strfdelta(tdelta, fmt='{D:02}d {H:02}h {M:02}m {S:02}s', inputtype='timedelta'):
    """Convert a datetime.timedelta object or a regular number to a custom-
    formatted string, just like the stftime() method does for datetime.datetime
    objects.

    The fmt argument allows custom formatting to be specified.  Fields can
    include seconds, minutes, hours, days, and weeks.  Each field is optional.

    Some examples:
        '{D:02}d {H:02}h {M:02}m {S:02}s' --> '05d 08h 04m 02s' (default)
        '{W}w {D}d {H}:{M:02}:{S:02}'     --> '4w 5d 8:04:02'
        '{D:2}d {H:2}:{M:02}:{S:02}'      --> ' 5d  8:04:02'
        '{H}h {S}s'                       --> '72h 800s'

    The inputtype argument allows tdelta to be a regular number instead of the
    default, which is a datetime.timedelta object.  Valid inputtype strings:
        's', 'seconds',
        'm', 'minutes',
        'h', 'hours',
        'd', 'days',
        'w', 'weeks'
    """
    if tdelta < timedelta(0):
        return '-' + strfdelta(-tdelta, fmt.replace('+',''))
    else:
        # Convert tdelta to integer seconds.
        if inputtype == 'timedelta':
            remainder = int(tdelta.total_seconds())
        elif inputtype in ['s', 'seconds']:
            remainder = int(tdelta)
        elif inputtype in ['m', 'minutes']:
            remainder = int(tdelta)*60
        elif inputtype in ['h', 'hours']:
            remainder = int(tdelta)*3600
        elif inputtype in ['d', 'days']:
            remainder = int(tdelta)*86400
        elif inputtype in ['w', 'weeks']:
            remainder = int(tdelta)*604800

        f = Formatter()
        desired_fields = [field_tuple[1] for field_tuple in f.parse(fmt)]
        possible_fields = ('W', 'D', 'H', 'M', 'S')
        constants = {'W': 604800, 'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
        values = {}
        for field in possible_fields:
            if field in desired_fields and field in constants:
                values[field], remainder = divmod(remainder, constants[field])
        return f.format(fmt, **values)

def load_sun_data():

    global dawn_18
    global dawn_6
    global sunrise
    global noon
    global sunset
    global dusk_6
    global dusk_18

    astral_home_city = astral_location_info
    sun_info_today = sun(astral_home_city.observer, date=datetime.now(), tzinfo=astral_home_city.timezone)
    sun_info_tomorrow = sun(astral_home_city.observer, date=(datetime.now() + timedelta(days=1)), tzinfo=astral_home_city.timezone)
    sun_info_today_ast = sun(astral_home_city.observer, date=datetime.now(), dawn_dusk_depression=18, tzinfo=astral_home_city.timezone)
    sun_info_tomorrow_ast = sun(astral_home_city.observer, date=(datetime.now() + timedelta(days=1)), dawn_dusk_depression=18, tzinfo=astral_home_city.timezone)
    sun_info_aftertom_ast = sun(astral_home_city.observer, date=(datetime.now() + timedelta(days=2)), dawn_dusk_depression=18, tzinfo=astral_home_city.timezone)

    degree_sign = u'\N{DEGREE SIGN}'

    dawn_18 = sun_info_today_ast['dawn']
    dawn_6 = sun_info_today['dawn']
    sunrise = sun_info_today['sunrise']
    noon = sun_info_today['noon']
    sunset = sun_info_today['sunset']
    dusk_6 = sun_info_today['dusk']
    dusk_18 = sun_info_today_ast['dusk']

    sun_table.set_data([['Dawn(-18' + degree_sign + ')', sun_info_today_ast['dawn'].strftime('%H:%M'), sun_info_tomorrow_ast['dawn'].strftime('%H:%M'), strfdelta(sun_info_tomorrow_ast['dawn'] - sun_info_today_ast['dawn'] - timedelta(seconds=86400),'{M:+}:{S:02}')],
                    ['Dawn(-6' + degree_sign + ')', sun_info_today['dawn'].strftime('%H:%M'), sun_info_tomorrow['dawn'].strftime('%H:%M'), strfdelta(sun_info_tomorrow['dawn'] - sun_info_today['dawn'] - timedelta(seconds=86400),'{M:+}:{S:02}')],
                    ['Sunrise', sun_info_today['sunrise'].strftime('%H:%M'), sun_info_tomorrow['sunrise'].strftime('%H:%M'), strfdelta(sun_info_tomorrow['sunrise'] - sun_info_today['sunrise'] - timedelta(seconds=86400),'{M:+}:{S:02}')],
                    ['Noon', sun_info_today['noon'].strftime('%H:%M'), sun_info_tomorrow['noon'].strftime('%H:%M'), strfdelta(sun_info_tomorrow['noon'] - sun_info_today['noon'] - timedelta(seconds=86400),'{M:+}:{S:02}')],
                    ['Sunset', sun_info_today['sunset'].strftime('%H:%M'), sun_info_tomorrow['sunset'].strftime('%H:%M'), strfdelta(sun_info_tomorrow['sunset'] - sun_info_today['sunset'] - timedelta(seconds=86400),'{M:+}:{S:02}')],
                    ['Dusk(-6' + degree_sign + ')', sun_info_today['dusk'].strftime('%H:%M'), sun_info_tomorrow['dusk'].strftime('%H:%M'), strfdelta(sun_info_tomorrow['dusk'] - sun_info_today['dusk'] - timedelta(seconds=86400),'{M:+}:{S:02}')],
                    ['Dusk(-18' + degree_sign + ')', sun_info_today_ast['dusk'].strftime('%H:%M'), sun_info_tomorrow_ast['dusk'].strftime('%H:%M'), strfdelta(sun_info_tomorrow_ast['dusk'] - sun_info_today_ast['dusk'] - timedelta(seconds=86400),'{M:+}:{S:02}')],
                    ['Daylight', strfdelta((sun_info_today['sunset'] - sun_info_today['sunrise']),'{H:}:{M:02}:{S:02}'), strfdelta((sun_info_tomorrow['sunset'] - sun_info_tomorrow['sunrise']),'{H:}:{M:02}:{S:02}'), strfdelta(((sun_info_tomorrow['sunset'] - sun_info_tomorrow['sunrise']) - (sun_info_today['sunset'] - sun_info_today['sunrise'])),'{M:+02}:{S:02}')],
                    ['Darkness', strfdelta((sun_info_tomorrow_ast['dawn'] - sun_info_today_ast['dusk']),'{H:}:{M:02}:{S:02}'), strfdelta((sun_info_aftertom_ast['dawn'] - sun_info_tomorrow_ast['dusk']),'{H:}:{M:02}:{S:02}'), strfdelta(((sun_info_aftertom_ast['dawn'] - sun_info_tomorrow_ast['dusk']) - (sun_info_tomorrow_ast['dawn'] - sun_info_today_ast['dusk'])),'{M:+}:{S:02}')]])

    #root_update()
    #sun_frame_height = sun_frame.winfo_height()
    #sun_frame_width = sun_frame.winfo_width()
    #print('sun_frame h:' + str(sun_frame_height) + ' sun_frame w:' + str(sun_frame_width))

def datetime_to_unix(date_time):
    unixtime = mktime(date_time.timetuple())
    return unixtime

def month_progressbar_update():
    month_range = calendar.monthrange(datetime.now().year, datetime.now().month)
    last_day_of_month = month_range[1]
    monthstart_datetime = datetime(datetime.now().year, datetime.now().month, 1, 1, 00, 00)
    monthend_datetime = datetime(datetime.now().year, datetime.now().month, last_day_of_month, 23, 59, 59)
    monthnow_datetime = datetime.now()
    monthstart_unix = datetime_to_unix(monthstart_datetime)
    monthend_adj_unix = (datetime_to_unix(monthend_datetime)) - monthstart_unix
    monthnow_adj_unix = (datetime_to_unix(datetime.now())) - monthstart_unix
    monthnow_percentage = (monthnow_adj_unix / monthend_adj_unix) * 100

    month_progressbar['value'] = monthnow_percentage
    month_progressbar_label['text'] = '{:05.2f}'.format(round(monthnow_percentage, 2)) + '%  '
    root.after(1000, month_progressbar_update)

def year_progressbar_update():
    yearstart_datetime = datetime(datetime.now().year, 1, 1, 00, 00)
    yearend_datetime = datetime(datetime.now().year, 12, 31, 23, 59, 59)
    yearnow_datetime = datetime.now()
    yearstart_unix = datetime_to_unix(yearstart_datetime)
    yearend_adj_unix = (datetime_to_unix(yearend_datetime)) - yearstart_unix
    yearnow_adj_unix = (datetime_to_unix(datetime.now())) - yearstart_unix
    yearnow_percentage = (yearnow_adj_unix / yearend_adj_unix) * 100

    year_progressbar['value'] = yearnow_percentage
    year_progressbar_label['text'] = '{:05.2f}'.format(round(yearnow_percentage, 2)) + '%  '
    root.after(1000, year_progressbar_update)

def crop(png_image_name):
    pil_image = Image.open(png_image_name)
    np_array = np.array(pil_image)
    blank_px = [255, 255, 255, 0]
    mask = np_array != blank_px
    coords = np.argwhere(mask)
    x0, y0, z0 = coords.min(axis=0)
    x1, y1, z1 = coords.max(axis=0) + 1
    cropped_box = np_array[x0:x1, y0:y1, z0:z1]
    pil_image = Image.fromarray(cropped_box, 'RGBA')
    #print(pil_image.width, pil_image.height)
    pil_image.save(png_image_name)
    #print(png_image_name)

def function_scheduler():
    est = pytz.timezone('US/Eastern')
    current_time = datetime.now(est)

    if current_time.second == 00:

        #crescent_converted = (crescent_angle + 180)%360
        crescent_converted = (-270 + (crescent_angle * -1))%360
        moon_crescent(moon_ill/100, crescent_converted, 1000)
        crop('moon_phase.png')
        moon_image = ImageTk.PhotoImage(Image.open('moon_phase.png'))
        moon_image_label.configure(image=moon_image)
        moon_image_label.image=moon_image

        if current_time.minute == 00:
            #print('it is now minute 00, second 00')
            #load_date_display()
            cal_set_date()
            load_sun_data()
            moon_query()

        def sub_min(datetime):
            datetime_minus_one = datetime - timedelta(minutes=1)
            return datetime_minus_one

        #voice announcements
       # if abs(current_time > sub_min(dawn_18)) and (current_time - sub_min(dawn_18)) < timedelta(minutes=1):
       #     os.system('aplay -q ./sounds/dawn18.wav')
       # if abs(current_time > sub_min(dawn_6)) and (current_time - sub_min(dawn_6)) < timedelta(minutes=1):
       #     os.system('aplay -q ./sounds/dawn6.wav')
        if abs(current_time >  sub_min(sunrise)) and (current_time - sub_min(sunrise)) < timedelta(minutes=1):
            os.system('aplay -q ./sounds/sunrise.wav')
        if abs(current_time > sub_min(noon)) and (current_time - sub_min(noon)) < timedelta(minutes=1):
            os.system('aplay -q ./sounds/noon.wav')
        if abs(current_time > sub_min(sunset)) and (current_time - sub_min(sunset)) < timedelta(minutes=1):
            os.system('aplay -q ./sounds/sunset.wav')
       # if abs(current_time > sub_min(dusk_6)) and (current_time - sub_min(dusk_6)) < timedelta(minutes=1):
       #     os.system('aplay -q ./sounds/dusk6.wav')
       # if abs(current_time > sub_min(dusk_18)) and (current_time - sub_min(dusk_18)) < timedelta(minutes=1):
       #     os.system('aplay -q ./sounds/dusk18.wav')

        if moonrise_dt is not None:
            if abs(current_time > sub_min(moonrise_dt)) and (current_time - sub_min(moonrise_dt)) < timedelta(minutes=1):
                os.system('aplay -q ./sounds/moonrise.wav')
        if moonset_dt is not None:
            if abs(current_time > sub_min(moonset_dt)) and (current_time - sub_min(moonset_dt)) < timedelta(minutes=1):
                os.system('aplay -q ./sounds/moonset.wav')
        if moon_transit_dt is not None:
            if abs(current_time > sub_min(moon_transit_dt)) and (current_time - sub_min(moon_transit_dt)) < timedelta(minutes=1):
                os.system('aplay -q ./sounds/moontransit.wav')

    root.after(1000, function_scheduler)

def load_metarV2():
    global wind_degrees
    global wind_calm
    global wind_variable
    global wind_speed
    try:
        wind_degrees
    except NameError:
        wind_degrees=0
    try:
        wind_calm
    except NameError:
        wind_calm=False
    try:
        wind_variable
    except NameError:
        wind_variable=False
    try:
        wind_speed
    except NameError:
        wind_speed=0

    degree_sign = u'\N{DEGREE SIGN}'

    BASE_URL = "https://tgftp.nws.noaa.gov/data/observations/metar/stations"

    stations = ['KBED']

    def write_metar_error_label(e):
        error_date = datetime.now().isoformat()
        print(str(error_date) + " load_metarV2 Error:" + str(e))
        metar_label_str = "Error:" + str(e)
        metar_label.config(text=metar_label_str,
            font=('Arial', 20, 'bold'),
            background='black',
            foreground='#FF0000',
            justify='left',
            highlightthickness=2,
            highlightbackground='#00c800',
            highlightcolor='#00c800',
            padx=8,
            pady=2,
            anchor='w')
        root.after(300000, load_metarV2)

    for name in stations:
        url = "%s/%s.TXT" % (BASE_URL, name)
        try:
            with urlopen(url, timeout=5) as webpage:
                metar_data = webpage.read().decode()
        except URLError as e:
            write_metar_error_label(e)
        except HTTPError as e:
            write_metar_error_label(e)
        except ContentTooShortError as e:
            write_metar_error_label(e)
        except TimeoutError as e:
            write_metar_error_label(e)
        except SSLError as e:
            write_metar_error_label(e)

        report = ""
        #report = 'KPSF 222234Z AUTO VRB006KT 4SM VCTS +RA FEW008 BKN011 OVC065 40/40 A2997 RMK AO2 PRESFR P0011 T00940078'
        for line in metar_data.splitlines():
            if line.startswith(name):
                obs = Metar.Metar(line)
                report = line
                #obs = Metar.Metar(report)
                #print(line)
                #print(obs.string())
                if str(obs.wind_dir) == 'None':
                    wind_degrees=0
                    wind_degrees_string='Variable'
                    wind_variable=True

                else:
                    wind_degrees = int(re.sub(r'(\d+).*', r'\1', str(obs.wind_dir)))
                    wind_degrees_string = str(wind_degrees) + degree_sign
                    wind_variable=False
                if str(obs.wind_dir_from) != 'None' and str(obs.wind_dir_to) != 'None':
                    wind_dir_from = int(re.sub(r'(\d+).*', r'\1', str(obs.wind_dir_from)))
                    wind_dir_to = int(re.sub(r'(\d+).*', r'\1', str(obs.wind_dir_to)))
                    wind_degrees_string = wind_degrees_string + ' V ' + str(wind_dir_from) + degree_sign + ' ' + str(wind_dir_to) + degree_sign
                if str(obs.wind_speed) == 'None':
                    wind_speed = -1
                else:
                    wind_speed = int(re.sub(r'(\d+).*', r'\1', str(obs.wind_speed)))
                if obs.wind_gust:
                    wind_gust = int(re.sub(r'(\d+).*', r'\1', str(obs.wind_gust)))
                else:
                    wind_gust=0
                if wind_speed == 0:
                    wind_degrees_string=''
                    wind_calm=True
                    wind_speed_string='Calm'
                elif wind_speed == -1:
                    wind_degrees_string=''
                    wind_calm=True
                    wind_speed_string='Wind Missing'
                elif wind_gust > 0:
                    wind_calm=False
                    wind_speed_string=str(wind_speed) + 'KT G ' + str(wind_gust) + 'KT'
                else:
                    wind_calm=False
                    wind_speed_string= str(wind_speed) + 'KT'

    wind_direction_label.config(text=str(wind_degrees_string),
                                font=('Arial', 35, 'bold'),
                                background='black',
                                foreground='#00c800',
                                justify='left',
                                padx=8,
                                pady=2,
                                anchor='nw')

    wind_speed_label.config(text=str(wind_speed_string),
                            font=('Arial', 35, 'bold'),
                            background='black',
                            foreground='#00c800',
                            justify='left',
                            padx=8,
                            pady=2,
                            anchor='sw')

    temp_c = float(re.sub(r'(-?\d+\.\d+).*', r'\1', str(obs.temp)))
    dewpt_c = float(re.sub(r'(-?\d+\.\d+).*', r'\1', str(obs.dewpt)))
    r_humid = int(round(mpcalc.relative_humidity_from_dewpoint((temp_c * units.degC), (dewpt_c * units.degC)) * 100, 0))
    vis_str = str(obs.vis).replace('miles', 'SM')
    press_hg = float(re.sub(r'(\d+\.\d+).*', r'\1', str(obs.press)))

    temp_f = round(9.0/5.0 * temp_c + 32, 1)
    dewpt_f = round(9.0/5.0 * dewpt_c + 32, 1)

    metar_string = obs.string()
    if obs.weather_string is not None:
        cur_wx = ', '.join(obs.weather_string)
        cur_wx = string.capwords(cur_wx)
        #cur_wx = cur_wx.replace('Ts', 'TS')
        #cur_wx = re.sub(r'(\S?)(Vc )(.*)', r'\1VC\3', cur_wx, flags=re.I)
    else:
        #metar_label_str = str(obs.station_id) + ' ' + 'Observation: ' + str(utc_to_local(obs.time).strftime("%m/%d/%Y %H:%M"))
        cur_wx = 'No Significant Weather'
        #cur_wx = metar_label_str

    metar_label_str = str(obs.station_id) + ' ' + 'Observation: ' + str(utc_to_local(obs.time).strftime("%m/%d/%Y %H:%M"))


    if str(obs.sky_string) == 'None':
        sky_condition = 'Sky Condition Missing'
    else:
        sky_condition = "\n".join(str(tup) for tup in obs.sky_string)
        sky_condition = sky_condition.replace('at ', '')
        sky_condition = sky_condition.replace('to ', '')
        sky_condition = re.sub(r'(indefinite ceiling, )(.*)', r'\1\n\2', sky_condition)
        sky_condition = re.sub(r'(\d?\d)(\d\d\d)(.*)', r'\1,\2\3', sky_condition)

    if temp_c > 37:
        _temp_f = str(f"{temp_f:4.1f}").replace(' ', '\u2007').replace('-', ' \u2212')
        _temp_c = str(f"{temp_c:4.1f}").replace(' ', '\u2007').replace('-', '\u2212')

        if dewpt_c > 37:
            _dewpt_f = str(f"{dewpt_f:4.1f}").replace(' ', '\u2007').replace('-', '\u2212')
            _dewpt_c = str(f"{dewpt_c:3.1f}").replace(' ', '\u2007').replace('-', '\u2212')
        else:
            _dewpt_f = str(f"{dewpt_f: 3.1f}").replace(' ', '\u2007').replace('-', '\u2212')
            _dewpt_c = str(f"{dewpt_c:3.1f}").replace(' ', '\u2007').replace('-', '\u2212')
    else:
        _temp_f = str(f"{temp_f: 05.1f}").replace(' ', '\u2007').replace('-', ' \u2212')
        _temp_c = str(f"{temp_c: 05.1f}").replace(' ', '\u2007').replace('-', '\u2212')

        _dewpt_f = str(f"{dewpt_f: 05.1f}").replace(' ', '\u2007').replace('-', '\u2212')
        _dewpt_c = str(f"{dewpt_c: 05.1f}").replace(' ', '\u2007').replace('-', '\u2212')


    metar_info_table.set_data([['Temp', _temp_f + degree_sign + 'F\u2007\u2007' + _temp_c + degree_sign + 'C'],
                               ['Dewpoint', _dewpt_f + degree_sign + 'F\u2007\u2007'  + _dewpt_c + degree_sign + 'C'],
                               ['Humidity', '\u2007' + str(r_humid) + '%'],
                               ['Visibility', '\u2007' + str(vis_str)],
                               #['Weather', str(cur_wx)],
                               ['Pressure', '\u2007' + str(f"{press_hg:5.2f}")]])

    sky_lines = len(sky_condition.splitlines())
    if sky_lines >= 3:
        sky_font = ('Arial', 24, 'bold')
        sky_anchor='w'
    elif sky_lines == 2:
        sky_font = ('Arial', 30, 'bold')
        sky_anchor='w'
    else:
        sky_font = ('Arial', 30, 'bold')
        sky_anchor='nw'

    wxdisplay_label.config(text=cur_wx,
                            font=('Arial', 30, 'bold'),
                            background='black',
                            foreground='#00c800',
                            justify='left',
                            highlightthickness=2,
                            highlightbackground='#00c800',
                            highlightcolor='#00c800',
                            padx=8,
                            pady=2,
                            anchor='nw')

    skydisplay_label.config(text=sky_condition.title(),
                            font=sky_font,
                            background='black',
                            foreground='#00c800',
                            justify='left',
                            highlightthickness=2,
                            highlightbackground='#00c800',
                            highlightcolor='#00c800',
                            padx=8,
                            pady=2,
                            anchor=sky_anchor)

    metar_label.config(text=metar_label_str,
                       font=('Arial', 30, 'bold'),
                       background='black',
                       foreground='#00c800',
                       justify='left',
                       highlightthickness=2,
                       highlightbackground='#00c800',
                       highlightcolor='#00c800',
                       padx=8,
                       pady=2,
                       anchor='nw')

    #Now handle the forecast section

    def write_wx_error_label(e):
        error_date = datetime.now().isoformat()
        print(str(error_date) + " load_metarV2 Error:" + str(e))
        wx_error_str = "Error:" + str(e)

        wx_today_label.config(text=wx_error_str,
                                    font=('Arial', 20, 'bold'),
                                    background='black',
                                    foreground='#FF0000',
                                    justify='left',
                                    highlightthickness=2,
                                    highlightbackground='#00c800',
                                    highlightcolor='#00c800',
                                    padx=8,
                                    pady=2,
                                    anchor='nw')

        wx_tomorrow_label.config(text=wx_error_str,
                                    font=('Arial', 20, 'bold'),
                                    background='black',
                                    foreground='#FF0000',
                                    justify='left',
                                    highlightthickness=2,
                                    highlightbackground='#00c800',
                                    highlightcolor='#00c800',
                                    padx=8,
                                    pady=2,
                                    anchor='nw')


        root.after(300000, load_metarV2)

    wx_url = 'https://forecast.weather.gov/MapClick.php?lat=42.5818&lon=-71.7923#.YydtFrTMJeM'
    try:
        with urlopen(wx_url, timeout=5) as webpage:
            wx_page = webpage.read().decode()
    except URLError as e:
        write_wx_error_label(e)
    except HTTPError as e:
        write_wx_error_label(e)
    except ContentTooShortError as e:
        write_wx_error_label(e)
    except TimeoutError as e:
        write_wx_error_label(e)
    except SSLError as e:
        write_wx_error_label(e)

    def strip_html_tags(string):
        string = re.sub(r'(<p.*">)(.*)(<span)(.*)(<\/p>)', r'\2', str(string))
        string = re.sub(r'(<p.*">)(.*)(<\/p>)', r'\2', str(string))
        string = re.sub(r'<br\/>', r' ', str(string))
        string = re.sub(r'⇓', r' ', str(string))
        string = re.sub(r'\s+:$', r':', str(string))
        string = re.sub(r' °F', r'°F', str(string))
        return string

    def format_forecast(list_index):
        return_list = []
        return_string = ""

        loop_list = [period_list, temp_list, desc_list]
        for list in loop_list:
            try:
                if list[list_index] is not None:
                    return_list.append(strip_html_tags(list[list_index]))
            except IndexError as e:
                write_wx_error_label(e)
                pass

        for list in return_list:
            return_string += str(list)
            if return_list.index(list) != len(return_list)-1:
                return_string += '\n'

        return return_string

    try:
        wx_page
    except NameError:
        #root.after(300000, load_metarV2)
        wx_page = ""

    period_list = []
    desc_list = []
    temp_list = []
    alt_list = []

    soup = BeautifulSoup(wx_page, features="html.parser")
    for div in soup.find_all('div', {'class': 'tombstone-container'}):
        for period in div.find_all('p', {'class': 'period-name'}):
            period_list.append(str(period) + ':')

        for desc in div.find_all('p', {'class': 'short-desc'}):
            desc_list.append(desc)

        for temp in div.find_all('p', {'class': 'temp'}):
            temp_list.append(temp)
        try:
            temp
        except NameError:
            temp_list.append(None)

        for img in div.find_all('img', alt=True):
            alt_list.append(img['alt'])

    wx_today_label.config(text=format_forecast(0),
                                font=('Arial', 30, 'bold'),
                                background='black',
                                foreground='#00c800',
                                justify='left',
                                highlightthickness=2,
                                highlightbackground='#00c800',
                                highlightcolor='#00c800',
                                padx=8,
                                pady=2,
                                anchor='nw')

    wx_tomorrow_label.config(text=format_forecast(1),
                                    font=('Arial', 30, 'bold'),
                                    background='black',
                                    foreground='#00c800',
                                    justify='left',
                                    highlightthickness=2,
                                    highlightbackground='#00c800',
                                    highlightcolor='#00c800',
                                    padx=8,
                                    pady=2,
                                    anchor='nw')


    root.after(300000, load_metarV2)

def blitRotate(surf, image, pos, originPos, angle):

    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)

    # draw rectangle around the image
    #pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)

class wind_rose_class():
    def __init__(self):
        self.thread = threading.Thread(target=self.start_wind_rose)
        self.thread.start()

    def start_wind_rose(self):
        os.environ['SDL_WINDOWID'] = str(wind_rose_frame.winfo_id())
        if platform.system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.init()
        pygame.display.init()
        clock = pygame.time.Clock()
        pygame_width, pygame_height = 275, 275
        wind_circle_surface = pygame.display.set_mode((pygame_width, pygame_height))
        wind_circle = pygame.image.load('wind-circle.png')

        wind_arrow_surface = pygame.display.set_mode((pygame_width, pygame_height))
        wind_arrow_surface.fill(0)
        wind_arrow = pygame.image.load('wind-arrow.png')
        wind_arrow = wind_arrow.convert_alpha()

        #arrow_angle = (wind_degrees * -1)
        arrow_angle = 0

        wind_calm_state=False
        wind_variable_state=False

        while True :
            wind_arrow_surface.fill(0)
            if wind_calm is True:
                if wind_calm_state is False:
                    wind_arrow.fill((0,0,0,0))
                    wind_calm_state=True
            elif wind_variable is True:
                if wind_variable_state is False:
                    wind_arrow = pygame.image.load('wind-variable.png')
                    wind_arrow = wind_arrow.convert_alpha()
                    wind_variable_state=True
            else:
                if wind_calm is False and wind_calm_state is True:
                    wind_arrow = pygame.image.load('wind-arrow.png')
                    wind_arrow = wind_arrow.convert_alpha()
                    wind_calm_state=False
                elif wind_variable is False and wind_variable_state is True:
                    wind_arrow = pygame.image.load('wind-arrow.png')
                    wind_arrow = wind_arrow.convert_alpha()
                    wind_variable_state=False
            if arrow_angle == 1:
                arrow_angle = -359
            if arrow_angle == -361:
                arrow_angle == -1
            if arrow_angle != (wind_degrees * -1) and wind_calm_state is False:
                rotation_angle = (arrow_angle - (wind_degrees * -1))
                if rotation_angle > 0:
                    if rotation_angle > 180:
                        rotation_angle -= 360
                else:
                    if rotation_angle < -180:
                        rotation_angle += 360
                if rotation_angle > 0:
                    arrow_angle -=1
                elif rotation_angle < 0:
                    arrow_angle +=1

            pos = (wind_circle_surface.get_width()/2, wind_circle_surface.get_height()/2)
            blitRotate(wind_circle_surface, wind_circle, pos, (wind_circle.get_height()/2, wind_circle.get_width()/2), 0)
            pos = (wind_arrow_surface.get_width()/2, wind_arrow_surface.get_height()/2)
            blitRotate(wind_arrow_surface, wind_arrow, pos, (wind_arrow.get_width()/2, wind_arrow.get_height()/2), arrow_angle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.display.update()
            clock.tick(20)

def ts_to_dt(ts_value):
    datetime_utc = datetime.strptime(ts_value, "%Y-%m-%dT%H:%M:%S%z")
    datetime_local = utc_to_local(datetime_utc)
    return datetime_local

def moon_query():

    global last_new_moon
    global last_first_quarter
    global last_full_moon
    global last_last_quarter

    global next_new_moon
    global next_first_quarter
    global next_full_moon
    global next_last_quarter

    global moonrise_dt
    global moonset_dt
    global moonrise_az
    global moonset_az
    global moon_transit_dt
    global moon_transit_alt

    moonrise_dt=None
    moonset_dt=None
    moon_transit_dt=None

    ts = load.timescale()

    #eph = load('de440.bsp')
    #sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

    home = wgs84_lat_lon
    boston = sf_earth + home

    #t1 = datetime.now(pytz.timezone("US/Eastern")).replace(hour=23, minute=59, second=59, microsecond=0).astimezone(pytz.utc)
    t1 = datetime.now(pytz.timezone("US/Eastern")).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(pytz.utc)
    t1 = datetime.now(pytz.timezone("US/Eastern"))
    t0 = t1 - timedelta(days=30)

    t0 = ts.utc(t0)
    t1 = ts.utc(t1)

    tt, yy = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))
    for tti, yyi in zip(tt, yy):
        if yyi == 0:
            last_new_moon = ts_to_dt(tti.utc_iso())
        elif yyi == 1:
            last_first_quarter = ts_to_dt(tti.utc_iso())
        elif yyi == 2:
            last_full_moon = ts_to_dt(tti.utc_iso())
        elif yyi == 3:
            last_last_quarter = ts_to_dt(tti.utc_iso())

    t0 = datetime.now(pytz.timezone("US/Eastern")).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(pytz.utc)
    #t0 = datetime.now(pytz.timezone("US/Eastern"))
    #t0 = t0 - timedelta(days=1)
    t1 = t0 + timedelta(days=30)

    t0 = ts.utc(t0)
    t1 = ts.utc(t1)

    tt, yy = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))
    for tti, yyi in zip(tt, yy):
        if yyi == 0:
            next_new_moon = ts_to_dt(tti.utc_iso())
        elif yyi == 1:
            next_first_quarter = ts_to_dt(tti.utc_iso())
        elif yyi == 2:
            next_full_moon = ts_to_dt(tti.utc_iso())
        elif yyi == 3:
            next_last_quarter = ts_to_dt(tti.utc_iso())

    t0 = datetime.now(pytz.timezone("US/Eastern")).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(pytz.utc)
    t1 = datetime.now(pytz.timezone("US/Eastern")).replace(hour=23, minute=59, second=59, microsecond=0).astimezone(pytz.utc)

    t0 = ts.utc(t0)
    t1 = ts.utc(t1)

    ff = almanac.risings_and_settings(eph, eph['moon'], home)
    tt, yy = almanac.find_discrete(t0, t1, ff)

    for tti, yyi in zip(tt, yy):
        est_moon = ts_to_dt(tti.utc_iso())

        rs = boston.at(tti)
        _, rs_az, _ = rs.observe(sf_moon).apparent().altaz()
        if yyi:
            moonrise_dt = est_moon
            moonrise_az = rs_az.degrees
        else:
            moonset_dt = est_moon
            moonset_az = rs_az.degrees

    ff = almanac.meridian_transits(eph, eph['moon'], home)
    tt, yy = almanac.find_discrete(t0, t1, ff)
    for tti, yyi in zip(tt, yy):
        if yyi == 1:
            moon_transit_ts = tti
            moon_transit_dt = ts_to_dt(tti.utc_iso())
            b = boston.at(moon_transit_ts)
            moon_apparent = b.observe(sf_moon).apparent()
            moon_transit_alt, _, _ = moon_apparent.altaz()
            break


def moon_update():

    global moon_ill
    global crescent_angle

    est = pytz.timezone('US/Eastern')
    degree_sign = u'\N{DEGREE SIGN}'

    ts = load.timescale()
    t = ts.utc(datetime.now(est))

    #eph = load('de440.bsp')
    #sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

    e = sf_earth.at(t)
    _, slon, _ = e.observe(sf_sun).apparent().frame_latlon(ecliptic_frame)
    _, mlon, _ = e.observe(sf_moon).apparent().frame_latlon(ecliptic_frame)
    phase = (mlon.degrees - slon.degrees) % 360.0

    home = wgs84_lat_lon
    boston = sf_earth + home
    b = boston.at(t)
    m = b.observe(sf_moon).apparent()
    s = b.observe(sf_sun).apparent()

    if last_new_moon.date() == date.today() or next_new_moon.date() == datetime.today().date():
        moon_event_str = 'New Moon'
    if last_first_quarter.date() == date.today() or next_first_quarter.date() == datetime.today().date():
        moon_event_str = 'First Quarter'
    if last_full_moon.date() == date.today() or next_full_moon.date() == datetime.today().date():
        moon_event_str = 'Full Moon'
    if last_last_quarter.date() == date.today() or next_last_quarter.date() == datetime.today().date():
        moon_event_str = 'Last Quarter'

    try:
        phase_str = moon_event_str
    except NameError:
        if phase < 90:
            phase_str = 'Waxing Crescent'
        elif phase < 180:
            phase_str = 'Waxing Gibbous'
        elif phase < 270:
            phase_str = 'Waning Gibbous'
        elif phase < 360:
            phase_str = 'Waning Crescent'

    moon_apparent = b.observe(sf_moon).apparent()
    moon_alt, moon_az, _ = moon_apparent.altaz()
    e_moon = e.observe(sf_moon).apparent()
    moon_ill = e_moon.fraction_illuminated(sf_sun)
    moon_ill = round(moon_ill * 100,1)
    _, _, moon_distance = e_moon.radec()
    moon_distance_miles = moon_distance.km * 0.621371
    crescent_angle = position_angle_of(m.altaz(), s.altaz())
    crescent_angle = round(crescent_angle.degrees,1)

    if last_new_moon > datetime.now(est):
        moon_age = strfdelta((datetime.now(est) - next_new_moon), '{D:02}d {H:02}h {M:02}m')
    else:
        moon_age = strfdelta((datetime.now(est) - last_new_moon), '{D:02}d {H:02}h {M:02}m')

    if moonrise_dt is None:
        moonrise_str = 'N/A'
    else:
        moonrise_str = str(moonrise_dt.strftime('%H:%M')) + '\u2007\u2007' + str(format(round(moonrise_az,0), '03.0f')) + degree_sign
    if moonset_dt is None:
        moonset_str = 'N/A'
    else:
        moonset_str = str(moonset_dt.strftime('%H:%M')) + '\u2007\u2007' + str(format(round(moonset_az,0), '03.0f')) + degree_sign

    rise_set_1_name = 'Rise'
    rise_set_1_str = moonrise_str
    rise_set_2_name = 'Set'
    rise_set_2_str = moonset_str

    if moonrise_dt is not None and moonset_dt is not None:
        if moonrise_dt > moonset_dt:
            rise_set_2_name = 'Rise'
            rise_set_2_str = moonrise_str
            rise_set_1_name = 'Set'
            rise_set_1_str = moonset_str

    if moon_transit_dt is None:
        moon_transit_str = 'N/A'
    else:
        moon_transit_str = str(moon_transit_dt.strftime('%H:%M')) + '\u2007\u2007' + str(format(round(moon_transit_alt.degrees,0),'03.0f')) + degree_sign

    moon_label_high_left.config(text=str(moon_ill) + '%',
                                    font=('Arial', 35, 'bold'),
                                    background='black',
                                    foreground='#00c800',
                                    justify='left',
                                    padx=8,
                                    pady=2,
                                    anchor='nw')

    moon_label_low.config(text=phase_str,
                               font=('Charcoal', 25),
                               background='black',
                               foreground='#00c800',
                               justify='center',
                               padx=8,
                               pady=10,
                               anchor='s')

    moon_table.set_data([['Bearing', str(format(round(moon_az.degrees,0), '03.0f')) + degree_sign],
                         ['Altitude', str(format(round(moon_alt.degrees,0),'03.0f')) + degree_sign],
                         ['Distance', str('{:,.0f}'.format(moon_distance_miles)) + ' mi'],
                         ['Age', moon_age],
                         [rise_set_1_name, rise_set_1_str],
                         [rise_set_2_name, rise_set_2_str],
                         ['Transit', moon_transit_str],
                         ['Nxt New', next_new_moon.date()],
                         ['Nxt Full', next_full_moon.date()]])


    #root_update()
    #moon_table_frame_height = moon_table_frame.winfo_height()
    #moon_table_frame_width = moon_table_frame.winfo_width()
    #print('moon_table_frame h:' + str(moon_table_frame_height) + ' moon_table_frame w:' + str(moon_table_frame_width))

    root.after(1000, moon_update)

def moon_crescent(moon_illumination, crescent_angle, num_points):
    my_dpi = 72
    fig = plt.figure(figsize=(275/my_dpi, 275/my_dpi), dpi=my_dpi)
    ax = fig.add_subplot()
    plt.axis('off')

    moon_image = mpimg.imread('moon.png')
    imagebox = OffsetImage(moon_image, zoom=1)
    ab = AnnotationBbox(imagebox, (0.0, 0.0), frameon=False, zorder=-1)
    ax.add_artist(ab)
    plt.draw()

    plt.xlim(-1.03, 1.03)
    plt.ylim(-1.03, 1.03)
    r=1
    theta = np.deg2rad(crescent_angle)
    rot = np.array([[cos(theta), sin(theta)]])
    step=r/(num_points - 1)

    x_lst = np.array([])
    y_lst = np.array([])

    for j in range(1, num_points+1):
        x = 2.0 * (step * (j - 1)) - 1.0
        y = (2.0 * moon_illumination - 1.0) * math.sqrt(r ** 2 - x ** 2)
        w = np.array([x, -y])
        v = np.array([y, x])
        v2 = np.dot(rot, v)
        w2 = np.dot(rot, w)
        x_lst = np.append(x_lst, [v2[0]], axis=0)
        y_lst = np.append(y_lst, [w2[0]], axis=0)

    r=1
    h=0
    k=0

    x0 = h - r  # determine x start
    x1 = h + r  # determine x finish
    x = np.linspace(x0, x1, num_points)  # many points to solve for y

    # use numpy for array solving of the semicircle equation
    y = k + np.sqrt(r**2 - (x - h)**2)

    theta = np.deg2rad(crescent_angle)
    rot = np.array([[cos(theta), sin(theta)]])
    w = np.array([x, -y])
    v = np.array([y, x])
    cv2 = np.dot(rot, v)
    cw2 = np.dot(rot, w)

    x_lst = np.concatenate((x_lst[::-1], cv2[0]))
    y_lst = np.concatenate((y_lst[::-1], cw2[0]))

    i=0
    while i < num_points * 2:
        plt.plot(x_lst[i:i + 2], y_lst[i:i + 2], linestyle='None')
        i+=1

    ax.set_aspect('equal', adjustable='box')

    ax.fill(x_lst, y_lst, c='black', alpha=0.8)

    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.savefig('moon_phase.png', transparent=True, bbox_inches='tight', pad_inches=0)
    #plt.show()
    plt.close()

root = ThemedTk(theme='default')
#root = Tk()
#style = ttk.Style(root)
#style.theme_use('default')
root.wm_overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg='black', cursor='none')
root.bind("<Button-1>", lambda evt: root.destroy())

lcl_clock_frame = Frame(root,
                        background='black',
                        width='263',
                        height='60')
lcl_clock_frame.place(x=(1920 - 263), y=0)
lcl_clock_frame.pack_propagate(0)

lcl_clock_label = Label(lcl_clock_frame)
lcl_clock_label.pack(side=LEFT, fill=BOTH, expand=True)


utc_clock_frame = Frame(root,
                        background='black',
                        width='263',
                        height='60')
utc_clock_frame.place(x=(1920 - 263), y=60)
utc_clock_frame.pack_propagate(0)

utc_clock_label = Label(utc_clock_frame)
utc_clock_label.pack(side=LEFT, fill=BOTH, expand=True)


india_clock_frame = Frame(root,
                        background='black',
                        width='263',
                        height='60')
india_clock_frame.place(x=(1920 - 263), y=120)
india_clock_frame.pack_propagate(0)

india_clock_label = Label(india_clock_frame)
india_clock_label.pack(side=LEFT, fill=BOTH, expand=True)

airnow_frame_north = Frame(root,
                        background='black',
                        width='263',
                        height='51')
airnow_frame_north.place(x=(1920 - 263), y=180)
airnow_frame_north.pack_propagate(0)

airnow_frame_south = Frame(root,
                        background='black',
                        width='263',
                        height='51')
airnow_frame_south.place(x=(1920 - 263), y=231)
airnow_frame_south.pack_propagate(0)

#y=282)
airnow_label_nw = Label(airnow_frame_north)
airnow_label_ne = Label(airnow_frame_north)
airnow_label_sw = Label(airnow_frame_south)
airnow_label_se = Label(airnow_frame_south)
airnow_label_nw.pack(anchor='n', side=LEFT, fill=X, expand=True)
airnow_label_ne.pack(anchor='n', side=RIGHT, fill=X, expand=True)
airnow_label_sw.pack(anchor='s', side=LEFT, fill=X, expand=True)
airnow_label_se.pack(anchor='s', side=RIGHT, fill=X, expand=True)

#datedisplay_frame = Frame(root,
#                          background='black',
#                          width='524',
#                          height='68')
#datedisplay_frame.place(relx=0.0, rely=0.259)
#datedisplay_frame.pack_propagate(0)
#
#
#datedisplay_label = Label(datedisplay_frame)
#datedisplay_label.pack(side=LEFT, fill=BOTH, expand=True)

cal_frame = Frame(root,
                  background='black',
                  width=520,
                  height=512,
                  highlightthickness=2,
                  highlightbackground='#00c800',
                  highlightcolor='#00c800')
cal_frame.pack(fill=BOTH, expand=True)
cal_frame.pack_propagate(0)
cal_frame.place(x=400, y=(1080 - 512))
today = datetime.today()
cal_display = Calendar(cal_frame,
                       selectmode='day',
                       year=today.year,
                       month=today.month,
                       day=today.day,
                       firstweekday='sunday',
                       showweeknumbers=False,
                       font=('Charcoal', 22),
                       background='black',
                       foreground='#00c800',
                       bordercolor='#00c800',
                       normalbackground='black',
                       normalforeground='#00c800',
                       weekendbackground='#1e1e1e',
                       weekendforeground='#00c800',
                       showothermonthdays=True,
                       othermonthbackground='black',
                       othermonthforeground='#00c800',
                       othermonthwebackground='#1e1e1e',
                       othermonthweforeground='#00c800',
                       selectbackground='#00c800',
                       selectforeground='black')
cal_display.pack(fill=BOTH, expand=True)

#sensor_frame = Frame(root,
#                     width=523,
#                     height=251,
#                     highlightthickness=2,
#                     highlightbackground='#00c800',
#                     highlightcolor='#00c800')
sensor_frame = Frame(root, background='black')
#sensor_frame.pack(fill=BOTH, expand=True)
#sensor_frame.pack_propagate(0)
sensor_frame.place(x=(1920 - 520 - 263 - 48), y=0)

sensor_tableV2 = Table(sensor_frame,
              ["Station", "Temp", "RH"],
              column_minwidths=[180, 170, 170],
              cell_foreground='#00c800',
              cell_anchor_list=['w', 'center', 'center', 'center'],
              stripped_rows=("black", '#1e1e1e'),
              header_foreground='black',
              header_background='#c2c2c2',
              padx=8,
              pady=2,
              cell_font=('Charcoal', 25),
              header_font=('Charcoal', 25),
              bordercolor='#00c800')
sensor_tableV2.pack(anchor=NW)

#sensor_table_style = ttk.Style()
#sensor_table_style.configure('sensor_table_style.Treeview',
#                             foreground='#00c800',
#                             background='black',
#                             fieldbackground='black',
#                             rowheight=50,
#                             font=('Charcoal', 25))
#sensor_table_style.configure('sensor_table_style.Treeview.Heading',
#                             background='#c1c1c1',
#                             font=('Charcoal', 25),
#                             relief='raised')
#sensor_table_style.configure('sensor_table_style.Treeview.Item',
#                             indicatorsize=0)
#
#sensor_table_style.map('Treeview',
#                       foreground=fixed_map(sensor_table_style, 'Treeview', 'foreground'),
#                       background=fixed_map(sensor_table_style, 'Treeview', 'background'))
#
#sensor_table = ttk.Treeview(sensor_frame, style='sensor_table_style.Treeview')
#
#sensor_table['columns'] = ('Station', 'Temp', 'Humidity')
#
#sensor_table.column('#0', width=0, stretch=NO)
#sensor_table.column('Station', anchor='w', width=150)
#sensor_table.column('Temp', anchor=CENTER, width=150)
#sensor_table.column('Humidity', anchor=CENTER, width=150)
#
#sensor_table.heading('#0', text='header', anchor=CENTER)
#sensor_table.heading('Station', text='Station', anchor=CENTER)
#sensor_table.heading('Temp', text='Temp', anchor=CENTER)
#sensor_table.heading('Humidity', text='Humidity', anchor=CENTER)
#
#sensor_table['show'] = 'headings'
#sensor_table['displaycolumns']=('Station', 'Temp', 'Humidity')
#sensor_table.tag_configure('alt', background='#1e1e1e')
#
#sensor_table.pack(fill=BOTH, expand=True)
#
sun_frame = Frame(root, background='black')
sun_frame.place(x=400, y=0)

sun_table = Table(sun_frame,
              ["Event", "2Day", "Tmrw", "Delta"],
              column_minwidths=[200, 150, 150, 125],
              cell_foreground='#00c800',
              cell_anchor_list=['w', 'center', 'center', 'center'],
              stripped_rows=("black", '#1e1e1e'),
              header_foreground='black',
              header_background='#c2c2c2',
              padx=8,
              pady=3,
              cell_font=('Charcoal', 25),
              header_font=('Charcoal', 25),
              bordercolor='#00c800')
sun_table.pack(anchor=NW)

month_progressbar_frame = Frame(root,
                              highlightthickness=2,
                              highlightbackground='black',
                              highlightcolor='black')
month_progressbar_frame.pack(fill=BOTH, expand=True)
month_progressbar_frame.pack_propagate(0)
month_progressbar_frame.place(x=0.0, y=(1080 - 200))

month_progressbar_style = ttk.Style()
month_progressbar_style.configure("day.Horizontal.TProgressbar", background='#5f92fc')
month_progressbar = ttk.Progressbar(
    month_progressbar_frame,
    orient='horizontal',
    mode='determinate',
    length=276,
    style="day.Horizontal.TProgressbar")

month_progressbar.grid(column=0, row=2, columnspan=1, padx=10, pady=18)

month_progressbar_name = ttk.Label(month_progressbar_frame, text='Month Progress', font=('Charcoal', 18))
month_progressbar_name.grid(column=0, row=0, columnspan=1, pady=5)
month_progressbar_label = ttk.Label(month_progressbar_frame, text='', font=('Charcoal', 18))
month_progressbar_label.grid(column=1, row=2, columnspan=1)

year_progressbar_frame = Frame(root,
                              highlightthickness=2,
                              highlightbackground='black',
                              highlightcolor='black')
year_progressbar_frame.pack(fill=BOTH, expand=True)
year_progressbar_frame.pack_propagate(0)
year_progressbar_frame.place(x=0, y=(1080 - 100))

year_progressbar_style = ttk.Style()
year_progressbar_style.configure("year.Horizontal.TProgressbar", background='#5f92fc')
year_progressbar = ttk.Progressbar(
    year_progressbar_frame,
    orient='horizontal',
    mode='determinate',
    length=276,
    style='year.Horizontal.TProgressbar')

year_progressbar.grid(column=0, row=2, columnspan=1, padx=10, pady=18)

year_progressbar_name = ttk.Label(year_progressbar_frame, text='Year Progress', font=('Charcoal', 18))
year_progressbar_name.grid(column=0, row=0, columnspan=1, pady=5)
year_progressbar_label = ttk.Label(year_progressbar_frame, text='', font=('Charcoal', 18))
year_progressbar_label.grid(column=1, row=2, columnspan=1)

wind_info_frame = Frame(root,
                         background='black',
                         width='400',
                         height='400',
                         highlightthickness=2,
                         highlightbackground='#00c800',
                         highlightcolor='#00c800')
wind_info_frame.place(x=(1920 - 400), y=(1080-400))
wind_info_frame.pack_propagate(0)

wind_direction_label=Label(wind_info_frame)
wind_direction_label.grid(row=0, column=0)
wind_direction_label.pack(side=TOP, fill=BOTH, expand=True)

wind_speed_label=Label(wind_info_frame)
wind_speed_label.grid(row=1, column=0)
wind_speed_label.pack(side=BOTTOM, fill=BOTH, expand=True)

def root_update():
    global root_updated
    root_updated=1
    root.update()

try:
    root_updated
except NameError:
    root_update()

wind_info_x = wind_info_frame.winfo_rootx()
wind_info_y = wind_info_frame.winfo_rooty()
wind_rose_x = (wind_info_x + 200) - 138
wind_rose_y = (wind_info_y + 200) - 138

wind_rose_frame = Frame(root,
                        background='black',
                        width='275',
                        height='275')
wind_rose_frame.place(x=(wind_rose_x + 5), y=wind_rose_y)
wind_rose_frame.pack_propagate(0)

metar_info_frame = Frame(root,
                         background='black')
                         #width='602',
                         #height='400')
metar_info_frame.place(x=(1920 - 1000), y=(1080-401))

metar_info_table = Table(metar_info_frame,
              ["Item", "Value"],
              column_minwidths=[225, 375],
              cell_foreground='#00c800',
              cell_anchor_list=['w', 'w'],
              #stripped_rows=("black", '#1e1e1e'),
              stripped_rows=("black", 'black'),
              cell_font=('Arial', 30, 'bold'),
	      header_enable=False,
              padx=8,
              pady=2,
              outerborder_width=1,
              bordercolor='#00c800')
metar_info_table.pack(anchor=NW)

wxdisplay_frame = Frame(root,
                          background='black',
                          width='1000',
                          height='58')
#wxdisplay_frame.place(relx=0.479, rely=0.837)
wxdisplay_frame.place(x=(1920 - 1000), y=(1080-456))
wxdisplay_frame.pack_propagate(0)


wxdisplay_label = Label(wxdisplay_frame)
wxdisplay_label.pack(side=LEFT, fill=BOTH, expand=True)

skydisplay_frame = Frame(root,
                          background='black',
                          width='601',
                          height='120')
skydisplay_frame.place(relx=0.479, rely=0.889)
skydisplay_frame.pack_propagate(0)


skydisplay_label = Label(skydisplay_frame)
skydisplay_label.pack(side=LEFT, fill=BOTH, expand=True)

metar_frame = Frame(root,
                    background='black',
                    #width='1397',
                    width='1000',
                    height='58')
metar_frame.place(x=920, y=568)
metar_frame.pack_propagate(0)

metar_label = Label(metar_frame, justify=LEFT, wraplength=1397)
metar_label.pack(side=LEFT, fill=BOTH, expand=True)

moon_table_frame = Frame(root,
                         background='black')
                         #width='602',
                         #height='400')
moon_table_frame.place(relx=0.0, rely=0.368)
#moon_table_frame.pack()
#moon_table_frame.pack_propagate(0)
#moon_table_frame.pack(anchor=NW)

moon_table = Table(moon_table_frame,
              ["Item", "Value"],
              column_minwidths=[149, 233],
              cell_foreground='#00c800',
              cell_anchor_list=['w', 'w'],
              #stripped_rows=("black", '#1e1e1e'),
              stripped_rows=("black", 'black'),
              cell_font=('Charcoal', 25),
              header_enable=False,
              padx=8,
              pady=2,
              outerborder_width=2,
              bordercolor='#00c800')
moon_table.pack(anchor=NW)

moon_info_frame = Frame(root,
                        background='black',
                        width='400',
                        height='400',
                        highlightthickness=2,
                        highlightbackground='#00c800',
                        highlightcolor='#00c800')
moon_info_frame.place(relx=0.0, rely=0.0)
moon_info_frame.pack_propagate(0)

moon_label_high_left=Label(moon_info_frame)
moon_label_high_left.grid(row=0, column=1)
moon_label_high_left.pack(side=TOP, fill=BOTH, expand=True)

moon_label_low=Label(moon_info_frame)
moon_label_low.grid(row=1, column=0, columnspan=1)
moon_label_low.pack(side=BOTTOM, fill=BOTH, expand=True)

root.update()
moon_info_x = moon_info_frame.winfo_rootx()
moon_info_y = moon_info_frame.winfo_rooty()
moon_x = (moon_info_x + 200) - 138
moon_y = (moon_info_y + 200) - 138

moon_frame = Frame(root,
                        background='black',
                        width='275',
                        height='275')
moon_frame.place(x=(moon_x), y=moon_y)
moon_frame.pack_propagate(0)

moon_image = Image.open("moon_phase.png")
moon_image = ImageTk.PhotoImage(moon_image)
moon_image_label = Label(moon_frame, image=moon_image)
moon_image_label.pack()

wx_today_frame = Frame(root,
                          background='black',
                          width='437',
                          height='283')
wx_today_frame.place(x=1045, y=282)
wx_today_frame.pack_propagate(0)


wx_today_label = Label(wx_today_frame, wraplength=421)
wx_today_label.pack(side=LEFT, fill=BOTH, expand=True)

wx_tomorrow_frame = Frame(root,
                          background='black',
                          width='436',
                          height='283')
wx_tomorrow_frame.place(x=(1045 + 437), y=282)
wx_tomorrow_frame.pack_propagate(0)


wx_tomorrow_label = Label(wx_tomorrow_frame, wraplength=419)
wx_tomorrow_label.pack(side=LEFT, fill=BOTH, expand=True)

lcl_clock()
utc_clock()
india_clock()
airnow()

#load_date_display()
cal_set_date()

st_object_list = []
load_sensor_data()

load_sun_data()

month_progressbar_update()
year_progressbar_update()

eph = load('de440.bsp')
sf_sun, sf_moon, sf_earth = eph['sun'], eph['moon'], eph['earth']
moon_query()
moon_update()

load_metarV2()
wind_rose = wind_rose_class()

function_scheduler()

root.mainloop()
