import RPi.GPIO as GPIO
import time as time
import os
from decimal import Decimal

def calculate_fan_function(t):
  d_c = 100
  ref = 5
  if t < 30:
    d_c = 0
    ref = 5
  if t < 60:
    d_c = max(t + 10, 50)
    ref = 115 - 1.833 * float(t)
  if t >= 60:
    d_c = min(t + 30, 100)
    ref = 5
  return d_c, ref

def spin_up(pwm):
  print 'Spinning up...'
  pwm.ChangeDutyCycle(100)
  time.sleep(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
pwm = GPIO.PWM(14, 100)
pwm.start(0)
spin_up(pwm)
is_on = True
slice_object = slice(13, 17, 1)
try:
  while 1:
    os.system('bash get_temp.sh > tmp')
    s = open('tmp', 'r').read()
    os.remove('tmp')

    temperature = Decimal(s[slice_object])
    fan_speed, sleep_time = calculate_fan_function(temperature)
    pwm.ChangeDutyCycle(fan_speed)

    if (fan_speed > 0) & (not is_on):
      spin_up(pwm)
      is_on = True
    elif (fan_speed == 0) & (is_on):
      is_on = False

    print('{}C -> {}% (next refresh in {}s)'.format(temperature, fan_speed, sleep_time))

    time.sleep(sleep_time)
except KeyboardInterrupt:
  print 'User interrupt'
finally:
  pwm.stop()
  #don't
  #GPIO.cleanup()
  #instead leave high
  GPIO.cleanup()
