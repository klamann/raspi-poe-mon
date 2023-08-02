import logging
import signal
import time

from raspi_poe_mon import util
from raspi_poe_mon.ip import IpDisplay
from raspi_poe_mon.poe_hat import PoeHat

logger = logging.getLogger('raspi_poe_mon')


class Controller:

    def __init__(self, fan_on_temp=50.0, fan_off_temp=45.0, frame_time=1.0):
        self.fan_on_temp = fan_on_temp
        self.fan_off_temp = fan_off_temp
        self.frame_time = frame_time
        self.poe_hat = PoeHat()
        self.display = IpDisplay(self.poe_hat)
        self._terminate = False
        # terminate gracefully on SIGTERM or SIGHUP
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGHUP, self.terminate)

    def main_loop(self):
        try:
            while not self._terminate:
                frame_start = time.time()
                self.update_fan()
                self.display.draw_frame()
                if self._terminate:
                    break
                sleep_time = self.frame_time - (time.time() - frame_start)
                logger.debug(f"update complete, sleeping for {sleep_time:.3f}")
                if sleep_time > 0:
                    time.sleep(sleep_time)
        except KeyboardInterrupt:
            pass
        finally:
            logger.info("shutting down")
            self.poe_hat.cleanup()

    def update_fan(self):
        temp = util.get_cpu_temp()
        if not self.poe_hat.is_fan_on() and temp > self.fan_on_temp:
            logger.info(f"CPU temperature at {temp}, turning fan ON")
            self.poe_hat.fan_on()
        elif self.poe_hat.is_fan_on() and temp < self.fan_off_temp:
            logger.info(f"CPU temperature at {temp}, turning fan OFF")
            self.poe_hat.fan_off()

    def terminate(self, *args):
        self._terminate = True
