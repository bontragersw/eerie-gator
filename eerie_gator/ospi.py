import functools
import logging
import RPi.GPIO as gpio


class ShiftRegister:
    def __init__(self, clock, output_disable, data, latch):
        self._clock = clock
        self._output_disable = output_disable
        self._data = data
        self._latch = latch
        self._is_enabled = False

    def __enter__(self):
        self._is_enabled = True
        self.output([False] * 16)
        self._output_disable(False)

    def __exit__(self):
        self._is_enabled = False
        self._output_disable(True)

    def output(self, values):
        assert self._is_enabled
        self._clock(False)
        self._latch(False)
        for value in values:
            self._clock(False)
            self._data(value)
            self._clock(True)
        self._latch(True)


MODE = gpio.BOARD
if MODE == gpio.BOARD:
    D5 = 13
    D6 = 7
    D7 = 15
    A1 = 11
elif MODE == gpio.BCM:
    D5 = 27  # Rev1: 21; Rev2: 27
    D6 = 4
    D7 = 22
    A1 = 17


class OpenSprinklerPi:
    def __init__(self, num_stations=8):
        gpio.setmode(MODE)
        for pin in [A1, D5, D6, D7]:
            gpio.setup(pin, gpio.OUT)
            gpio.output(pin, False)
        self._active_station = None
        self._num_stations = num_stations
        self._shift_register = ShiftRegister(
            clock=functools.partial(gpio.output, D6),
            output_disable=functools.partial(gpio.output, A1),
            data=functools.partial(gpio.output, D5),
            latch=functools.partial(gpio.output, D7),
            )

    @property
    def num_stations(self):
        logging.debug("num_stations is %r", self._num_stations)
        return self._num_stations

    def get_active_station(self):
        logging.debug("active_station is %r", self._active_station)
        return self._active_station

    def set_active_station(self, value):
        logging.debug("active_station = %r", value)
        if value is not None and value not in range(self._num_stations):
            raise ValueError(value)
        self._active_station = value
        self._shift_register.output([
            i == self._active_station
            for i in range(self._num_stations - 1, -1, -1)
            ])

    def __enter__(self):
        self._shift_register.__enter__()
        return self

    def __exit__(self, *args):
        self._shift_register.__exit__()
        gpio.cleanup()


def main():
    import argparse
    import logging
    import time

    ospi = OpenSprinklerPi()
    parser = argparse.ArgumentParser()
    parser.add_argument("duration", type=float)
    parser.add_argument("station", type=int, choices=range(ospi.num_stations))
    parser.add_argument("--debug", "-d", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    with ospi:
        logging.debug(
            "Turning station %r on for %f seconds",
            args.station,
            args.duration,
            )
        ospi.active_station = args.station
        time.sleep(args.duration)
        logging.debug("Turning station %r off", args.station)
        ospi.active_station = None


if __name__ == "__main__":
    main()
