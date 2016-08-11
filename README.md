# tado_domoticz
Tado &lt;> Domoticz integration

1. tado_setpoint.py: Publishes current value of the desired temperature to a
   temperature virtual device in Domoticz
2. tado_heathum.py: Publishes current values of internal temperature sensor
   and humidity sensor to a temp/hum virtual device in Domoticz

Both scripts use a cookiefile, which by default is /tmp/tadocookie.
