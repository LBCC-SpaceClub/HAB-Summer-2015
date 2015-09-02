This is a cutdown timer for the Arduino Uno, which engages [jpmolden](h$

The design intent was to write a simple piece of code which would allow$

The blink patterns indicate:
  Blinking every half second - Waiting for cutdown time.
  Solid - Heating circuit engaged.
  Off - Cutdown complete, idling.

If connected to a serial port, the on screen debugging statements look $

  Burn timer set for 15 minutes.
  Current time: 0 minutes and 0 seconds.
  Current time: 0 minutes and 1 seconds.
  Current time: 0 minutes and 2 seconds.
  Current time: 0 minutes and 3 seconds.

And so on, until the burn circuit engages:

  Beginning burn.. burn complete.

Our current experiments indicate at least 2 seconds of burn time is nec$



