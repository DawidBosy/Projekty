from os.path import dirname, join
import re
import numpy as np
from scipy.interpolate import interp1d
from bokeh.io import curdoc
from bokeh.layouts import column, row, gridplot, layout
from bokeh.models import ColumnDataSource, Div, Select, Slider, RangeSlider, TextInput, Panel, Tabs
from bokeh.plotting import figure
from pid import Regulator, Engine, Car, Road, Wind, CruiseControl

def parse_road_data(road):
    return [(int(a), int(b)) for a, b in re.findall('(\d+)[, ]*(\d+)', road)]


# Nagłówek strony (do edytowania w description.html)
description = Div(text=open(join(dirname(__file__), "description.html")).read(
), sizing_mode="stretch_width")

# Parametry regulatora
uMin = TextInput(title='uMin', value='-5')
uMax = TextInput(title='uMax', value='5')
kp = TextInput(title='kp', value='0.0007')

# Parametry tempomatu
simulation_time = TextInput(title="Czas symulacji (s)", value='850')
velocity_required = TextInput(title='Prędkość zadana (km/h)', value='125')

# Parametry samochodu
thrust_force = RangeSlider(
    title='Siła ciągu (N)', start=-10**5, end=10**5, value=(-10000, 10000), step=1000)
thrust_force_min = TextInput(title='Siła ciągu (N) - min', value='-10000')
thrust_force_max = TextInput(title='Siła ciągu (N) - max', value='10000')
car_frontal_surface = TextInput(
    title="Powierzchnia czołowa samochodu (m^2)", value='7')
car_weight = TextInput(title="Masa samochodu (kg)", value='1200')
drag_coefficient = TextInput(title='Współczynnik oporu', value='0.25')
wheel_radius = TextInput(title='Promień koła (m)', value='0.2')

# Parametry drogi
key_points = TextInput(
    title='Droga', value='(0, 0), (3000,50), (6000,75), (9000,50), (12000,25), (15000,0), (18000,25), (21000,100), (24000, 25), (27000,10), (30000,25)')

# Parametry wiatru
wind_velocity = TextInput(title="Prędkość wiatru (km/h)",
                       value='10')

source = ColumnDataSource(
    data=dict(time=[], velocity=[], x_road=[], y_road=[], thrust=[], friction=[], pull=[], air=[], velocity_required=[]))

road_source = ColumnDataSource(data=dict(x_position=[], y_position=[]))

# Wykres prędkości od czasu
p1 = figure(title="", aspect_ratio=2, sizing_mode='scale_width')
p1.line(x="time", y="velocity", source=source, line_width=2, legend_label='Prędkość samochodu')
p1.line(x="time", y='velocity_required', source=source, line_color='green', legend_label='Prędkość zadana')
p1.xaxis.axis_label = 'Czas (s)'
p1.yaxis.axis_label = 'Prędkość (km/h)'
tab1 = Panel(child=p1, title='Prędkość')

# Wykres sił od czasu
p2 = figure(title="", aspect_ratio=2, sizing_mode='scale_width')
p2.line(x="time", y="thrust", source=source, line_width=2, legend_label='Siła ciągu')
p2.line(x="time", y="friction", source=source, line_color='green', line_width=2, legend_label='Siła tarcia')
p2.line(x="time", y="pull", source=source, line_width=2, line_color='red', legend_label='Siła przyciągania')
p2.line(x="time", y="air", source=source, line_width=2, line_color='orange', legend_label='Opór powietrza')
p2.xaxis.axis_label = 'Czas (s)'
p2.yaxis.axis_label = 'Siła (N)'
tab2 = Panel(child=p2, title='Siła')

# Wykresy drogi
p3 = figure(title="", aspect_ratio=2, sizing_mode='scale_width', toolbar_location=None)
p3.line(x="time", y="y_position", source=source, line_width=2, legend_label='Kształt drogi')
p3.xaxis.axis_label = 'Czas (s)'
p3.yaxis.axis_label = 'Wysokość (m)'

p4 = figure(title="", aspect_ratio=2, sizing_mode='scale_width', toolbar_location=None)
p4.line(x="x_position", y="y_position", source=source, line_width=2, legend_label='Kształt drogi')
p4.xaxis.axis_label = 'Droga (m)'
p4.yaxis.axis_label = 'Wysokość (m)'

p5 = figure(title="", aspect_ratio=4, sizing_mode='scale_width', toolbar_location=None)
p5.line(x="x_road", y="y_road", source=road_source, line_width=2, legend_label='Kształt drogi')
p5.xaxis.axis_label = 'Droga (m)'
p5.yaxis.axis_label = 'Wysokość (m)'

roads = layout([[p3, p4], [p5]], sizing_mode='scale_width')

tab3 = Panel(child=roads, title='Droga')


def update():
    road_data = parse_road_data(key_points.value)

    regulator = Regulator(uMin=float(uMin.value), uMax=float(uMax.value), kp=float(kp.value))
    engine = Engine(
        thrustForceMin=int(thrust_force_min.value), thrustForceMax=int(thrust_force_max.value))
    car = Car(engine=engine, velocityMin=0, velocityMax=0,
              Sd=float(car_frontal_surface.value), mass=float(car_weight.value), Cd=float(drag_coefficient.value), wheelRadius=float(wheel_radius.value))
    road = Road(keyPoints=road_data)
    wind = Wind(velocity=int(wind_velocity.value))

    t = int(simulation_time.value)
    v = int(velocity_required.value)

    v /= 3.6

    cc = CruiseControl(regulator=regulator, car=car, road=road, wind=wind,
                       velocityRequired=v, simulationTime=t)

    (time_data, velocity_data, x_position_data, y_position_data, xArr, yArr, forces) = cc.simulate()

    velocity_data = [v * 3.6 for v in velocity_data]

    thrust_data, friction_data, pull_data, air_data = forces

    source.data = dict(
        time=time_data,
        velocity=velocity_data,
        x_position=x_position_data,
        y_position=y_position_data,
        thrust=thrust_data,
        friction=friction_data,
        pull=pull_data,
        air=air_data,
        velocity_required=[int(velocity_required.value) for _ in range(len(time_data))]
    )

    road_source.data = dict(
        x_road=xArr,
        y_road=yArr
    )

# Przykażdej zmianie danych zostanie wywołana funkcja update()
controls = [simulation_time, velocity_required, thrust_force_min, thrust_force_max,
            car_frontal_surface, car_weight, drag_coefficient, wheel_radius, key_points, wind_velocity, uMin, uMax, kp]

for control in controls:
    control.on_change('value', lambda attr, old, new: update())

# Ustawienie layoutu
inputs = column(*controls[:2], row(thrust_force_min, thrust_force_max), *controls[4:-3])

parameters = Tabs(tabs=[Panel(child=inputs, title='Parametry środowiska'), Panel(child=column(row(*controls[-3:-1]), controls[-1]), title='Parametry regulatora')])

l = column(description, row(parameters, Tabs(tabs=[tab1, tab2, tab3]), sizing_mode='scale_height'), sizing_mode='scale_both')

# Wczytaj dane startowe
update()

curdoc().add_root(l)
curdoc().title = "Tempomat"
