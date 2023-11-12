### Defines the constants related to the LENGTH of the bar
LENGTH = 10
DX = 0.01
N = int(LENGTH / DX)

### Defines the constants related to the TIME and the STARTING TEMPERATURE
TOTAL_TIME = 60
TEMPERATURE_START = 100

### Sets all the extra constants
ALPHA = 1
TEMPERATURE_BEGIN = 0
TEMPERATURE_END = 0

### Parameters for 2D heat equation
LENGTH_2D = 20
DX_2D = 1
N_2D = int(LENGTH_2D / DX_2D)
TEMPERATURE_START_2D = 100
FINAL_TIME_2D = 30
DT_2D = 0.5
NUMBER_OF_STEPS_2D = int(FINAL_TIME_2D / DT_2D)