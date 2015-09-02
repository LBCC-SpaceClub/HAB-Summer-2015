This is a cutdown timer for the Arduino Uno, which engages jpmolden's circuit to heat a thin nichrome wire and burn through the nylon string holding our payload aloft.

The design intent was to write a simple piece of code which would allow us to easily enter a number of minutes until cutdown, without messing around with converting units. It uses the onboard LED on pin 13 as a debugging light.

The LED blink patterns indicate:
  Blinking every half second - Waiting for cutdown time.
  Solid - Heating circuit engaged.
  Off - Cutdown complete, idling.

If connected to a serial port, the on screen debugging statements look something like this:

Burn timer set for 15 minutes.
Current time: 0 minutes and 0 seconds.
Current time: 0 minutes and 1 seconds.
Current time: 0 minutes and 2 seconds.
Current time: 0 minutes and 3 seconds.

And so on, until the burn circuit engages:

Current time: 14 minutes and 59 seconds.
Beginning burn.. burn complete.

Our current experiments indicate at least 2 seconds of burn time is necessary, but this can easily be changed in the code. We're currently using 5 seconds to give ourselves some leeway due to cold temperatures at high altitude.
