import time
from lsm6dsox import LSM6DSOX
from machine import Pin, I2C, PWM
import StressClassifier
clf = StressClassifier.RandomForestClassifier()

red_pin = 25
green_pin = 15 
blue_pin = 16

sw_pin = 17
dt_pin = 18
clk_pin = 19

btn_pin = 20

buzz_pin = 26

led_pin = 6

screenr_pin = 4
screeng_pin = 7
screenb_pin = 5

# Init devices
red = PWM(Pin(red_pin))
green = PWM(Pin(green_pin))
blue = PWM(Pin(blue_pin))

led = Pin(6, Pin.OUT)

screenr = Pin(screenr_pin, Pin.OUT)
screeng = Pin(screeng_pin, Pin.OUT)
screenb = Pin(screenb_pin, Pin.OUT)

# Set frequency for PWM
red.freq(1000)
green.freq(1000)
blue.freq(1000)

sw = Pin(sw_pin, Pin.IN, Pin.PULL_UP)
dt = Pin(dt_pin, Pin.IN, Pin.PULL_UP)
clk = Pin(clk_pin, Pin.IN, Pin.PULL_UP)

btn = Pin(btn_pin, Pin.IN)

lsm = LSM6DSOX(I2C(0, scl=Pin(13), sda=Pin(12)))
beeper = PWM(Pin(26, Pin.OUT))

# Init state variables
last_sw_value = sw.value()
last_dt_value = dt.value()
last_clk_value = clk.value()

last_btn_value = btn.value()

debounce_time = 10  # ms

samples = []
deltas = []
prev_stress = 0
stress_level = 0
overall_stress = 0
last_stress_level = stress_level

flipped_state = 0
last_flipped_state = flipped_state

screen_flag = True

# define the sampling rate and duration
count = 0
sampling_rate = 5  # samples per second
sampling_interval = 1 / sampling_rate  # time between samples in seconds
collection_duration = 30  # total collection time in seconds

# define accel and gyro parameters 
prev_accel_data = [ 0, 0, 0 ]
prev_prev_accel_data = [ 0, 0, 0 ]

prev_gyro_data = [ 0, 0, 0 ]
prev_prev_gyro_data = [ 0, 0, 0 ] 

# calculate the number of samples to collect
total_samples = int(collection_duration * sampling_rate)

flipped_time = 0

def toggle_leds(red_state, green_state, blue_state):
    if red_state:
        ledR.off()
    else:
        ledR.on()
        
    if green_state:
        ledG.off()
    else:
        ledG.on()
        
    if blue_state:
        ledB.off()
    else:
        ledB.on()

def detect_flip(accel_data, gyro_data, prev_accel_data, prev_prev_accel_data, prev_gyro_data, prev_prev_gyro_data, beeper):
    """
    Detects flipping based on accelerometer and gyroscope data.

    Parameters:
    - lsm (object): Object for interacting with the accelerometer and gyroscope.
    - prev_accel_data (list): List containing previous accelerometer data [prev_accel_x, prev_accel_y, prev_accel_z].
    - prev_prev_accel_data (list): List containing accelerometer data from two time steps ago [prev_prev_accel_x, prev_prev_accel_y, prev_prev_accel_z].
    - prev_gyro_data (list): List containing previous gyroscope data [prev_gyro_x, prev_gyro_y, prev_gyro_z].
    - prev_prev_gyro_data (list): List containing gyroscope data from two time steps ago [prev_prev_gyro_x, prev_prev_gyro_y, prev_prev_gyro_z].
    - beeper (object): Object for controlling the buzzer.

    Returns:
    - None
    """
    
    global flipped_state
    global flipped_time
    
    delta_accel_x = accel_data[0] - prev_accel_data[0]
    delta_accel_y = accel_data[1] - prev_accel_data[1]
    delta_accel_z = accel_data[2] - prev_accel_data[2]
    
    prev_delta_accel_x = accel_data[0] - prev_prev_accel_data[0]
    prev_delta_accel_y = accel_data[1] - prev_prev_accel_data[1]
    prev_delta_accel_z = accel_data[2] - prev_prev_accel_data[2]

    delta_gyro_x = gyro_data[0] - prev_gyro_data[0]
    delta_gyro_y = gyro_data[1] - prev_gyro_data[1]
    delta_gyro_z = gyro_data[2] - prev_gyro_data[2]
    
    prev_delta_gyro_x = gyro_data[0] - prev_prev_gyro_data[0]
    prev_delta_gyro_y = gyro_data[1] - prev_prev_gyro_data[1]
    prev_delta_gyro_z = gyro_data[2] - prev_prev_gyro_data[2]
    
    # Condition for flip detection
    if (abs(delta_accel_x) < 1.5 and abs(delta_accel_y) < 1.5 and abs(delta_accel_z) < 1.5 and
        abs(prev_delta_accel_x) < 1.5 and abs(prev_delta_accel_y) < 1.5 and abs(prev_delta_accel_z) < 1.5 and
        abs(delta_gyro_x) < 300 and abs(delta_gyro_y) < 300 and abs(delta_gyro_z) < 300 and
        abs(prev_delta_gyro_x) < 300 and abs(prev_delta_gyro_y) < 300 and abs(prev_delta_gyro_z) < 300):
        # No flip detected
        # ledB.off()
        pass
    else:
        current_time = time.time()
        if current_time != flipped_time:
            print("flipped")
            flipped_time = current_time
            if flipped_state == 0:
                flipped_state = 1
                led.on()
            else:
                flipped_state = 0
                led.off()
        
    # Update previous data
    prev_prev_accel_data[:] = prev_accel_data[:]
    prev_accel_data[:] = accel_data[:]
    
    prev_prev_gyro_data[:] = prev_gyro_data[:]
    prev_gyro_data[:] = gyro_data[:]


def stress_level_detection(overall_stress):
    if  overall_stress == 0:
        stress_level = -1
    elif 0 < overall_stress <= 25:
        stress_level = 0
    elif 25 < overall_stress < 75:
        stress_level = 1
    elif 75 <= overall_stress < 100:
        stress_level = 2
    elif overall_stress == 100:
        stress_level = 3 
    return stress_level

def stress_value_calculation(stress_level, predicted_stress_result, overall_stress):
    
    global screen_flag
    adjustments = {
        -1: [0, 1, 2*3],
        0: [-1, 1, 2*3],
        1: [-1, 0, 1*3],
        2: [-2, 1, 2*3]
    }
    
    if stress_level in adjustments and predicted_stress_result in [0, 1, 2]:
        overall_stress += adjustments[stress_level][predicted_stress_result]
        if overall_stress >= 100:
            overall_stress == 100
            screen_flag = False
            for i in range(3):
                beeper.freq(100)
                beeper.duty_u16(50000)
                time.sleep(.25)
                beeper.deinit()
                time.sleep(.25)
            toggle_screen(screen_flag)
    else:
        overall_stress == 100
        print("Destressing is needed")
    return overall_stress


def calculate_rgb_from_stress(stress_level):
    """
    Calculate the RGB values based on the stress level.
    
    Args:
        stress_level (int): The stress level value ranging from 0 (no stress) to 100 (maximum stress).
    
    Returns:
        tuple: A tuple containing the RGB values (red, green, blue).
    """
    # Ensure the stress_level is within the expected range
    stress_level = max(0, min(stress_level, 100))
    
    # Calculate the red and green components
    red = int((stress_level / 100) * 255)
    green = int((1 - (stress_level / 100)) * 255)
    
    # The blue component remains constant
    blue = 0
    
    return (red, green, blue)

def toggle_screen(enabled):
    if enabled:
        screeng.off()
        screenr.off()
        screenb.off()
    else:
        screeng.on()
        screenr.on()
        screenb.on()

def set_color(r, g, b):
    """
    Set the color of the RGB LED.
    Parameters:
        r (int): Red value (0-255)
        g (int): Green value (0-255)
        b (int): Blue value (0-255)
    """
    # Convert 0-255 range to 0-65535 range for PWM
    red.duty_u16(int(r * 65535 / 255))
    green.duty_u16(int(g * 65535 / 255))
    blue.duty_u16(int(b * 65535 / 255))

def fade_stress(value):
    """
    Fade from green to red based on a value from 0 to 100.
    Parameters:
        value (int): Value from 0 (green) to 100 (red)
    """
    value = max(0, min(value, 100))  # Ensure value is within 0-100
    r = int((value / 100) * 255)
    g = int((1 - (value / 100)) * 255)
    set_color(r, g, 0) 

toggle_screen(screen_flag)
while (True):
       
    if len(deltas) == 25:
        samples.pop(0)
        deltas.pop(0)

    accel_data = lsm.accel()
    gyro_data = lsm.gyro()
    detect_flip(accel_data, gyro_data, prev_accel_data, prev_prev_accel_data, prev_gyro_data, prev_prev_gyro_data, beeper)

    if flipped_state == 0:
        # Add data
        row = [accel_data[0], accel_data[1], accel_data[2], gyro_data[0], gyro_data[1], gyro_data[2]]
        samples.append(row)

        # Calculate deltas
        if len(samples) > 1:
            current_delta = [samples[-1][i] - samples[-2][i] for i in range(6)]
            deltas.append(current_delta)


        # use only the last 5 seconds of samples
        if len(deltas) == 25:
            # Number of columns in your data
            num_columns = len(deltas[0])

            means = []
            ranges = []
            minimums = []
            maximums = []

            # calculate statistics for each column
            for col_index in range(num_columns):
                column_values = [deltas[row][col_index] for row in range(25)]
                col_mean = sum(column_values) / 25
                col_min = min(column_values)
                col_max = max(column_values)
                col_range = col_max - col_min

                # store the statistics
                means.append(col_mean)
                ranges.append(col_range)
                minimums.append(col_min)
                maximums.append(col_max)

            result = means + ranges + minimums + maximums
            # make prediction
            predict_result = clf.predict(result)
            print(f'Class: {predict_result}')

            stress_level = stress_level_detection(overall_stress)
            print(stress_level)
            overall_stress = stress_value_calculation(stress_level, predict_result, overall_stress)
        
    else:
        sw_value = sw.value()
        dt_value = dt.value()
        clk_value = clk.value()

        btn_value = btn.value()

        if dt_value != last_dt_value or clk_value != last_clk_value:
            rotor_multiplier = 5
            overall_stress = overall_stress - 1 * rotor_multiplier
            last_dt_value = dt_value
            last_clk_value = clk_value

        if sw_value != last_sw_value:
            sw_multiplier = 5
            overall_stress = overall_stress - 1 * sw_multiplier
            last_sw_value = sw_value

        if btn_value != last_btn_value:
            btn_multiplier = 5
            overall_stress = overall_stress - 1 * btn_multiplier
            last_btn_value = btn_value
            
        if overall_stress <= 50:
            screen_flag = True
            toggle_screen(screen_flag)

        #stable states
        time.sleep_ms(debounce_time)
    
    overall_stress = max(0, min(overall_stress, 100))

    if last_stress_level != overall_stress:
        print(overall_stress)
        fade_stress(overall_stress)
        last_stress_level = overall_stress
        
    fade_stress(overall_stress)
    print('flipped_state: ' + str(flipped_state))
    print('overall_stress: ' + str(overall_stress))

    time.sleep(sampling_interval)