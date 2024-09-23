import logging
import signal
import time
import tracemalloc

from raspi_poe_mon import util
from raspi_poe_mon.monitor import SystemMonitor
from raspi_poe_mon.poe_hat import PoeHat

logger = logging.getLogger('raspi_poe_mon')


class Controller:
    """
    Controller for display and fan of the PoE HAT.

    Contains the main application loop and manages all high level logic like updating display
    frames or changing fan state.

    :param show_display: display will only be used when this is True
    :param control_fan: fan controls will only be enabled when this is True
    :param fan_on_temp: turn on the fan when CPU temperature rises above this value (in °C)
    :param fan_off_temp: turn off the fan when CPU temperature drops below this value (in °C)
    :param frame_time: show a new frame on the display every n seconds (excluding blank time)
    :param blank_time: blank time (seconds) between frames where the display is turned off
    :param brightness: brightness level of the display in percent (0-100)
    :param timeout: terminate after n seconds; 0 means run until interrupted
    :param dry_run: simulate commands without accessing the PoE HAT
    :param profiling: log profiling information, very verbose
    """

    def __init__(
        self,
        show_display=True,
        control_fan=True,
        fan_on_temp=60.0,
        fan_off_temp=50.0,
        frame_time=2.0,
        blank_time=0,
        brightness=100,
        timeout=0,
        dry_run=False,
        profiling=False,
    ):
        self.show_display = show_display
        self.control_fan = control_fan
        self.fan_on_temp = fan_on_temp
        self.fan_off_temp = fan_off_temp
        self.frame_time = frame_time
        self.blank_time = blank_time
        self.timeout = timeout
        self.profiling = profiling
        self.poe_hat = PoeHat(dry_run=dry_run, brightness=brightness)
        self.renderer = SystemMonitor(self.poe_hat)
        self._frame_counter = 0
        self._start_time = time.time()
        self._terminate = False
        self.add_signal_handlers()
        self.profiling_setup()

    def main_loop(self):
        try:
            while not self.should_terminate():
                frame_start = time.time()
                self.before_frame()
                self.update_fan()
                self.update_display()
                self.after_frame()
                self.frame_idle(frame_start)
                self.screen_blank()
        except KeyboardInterrupt:
            pass
        finally:
            logger.info("shutting down")
            self.poe_hat.cleanup()

    def should_terminate(self):
        return (
            self._terminate
            or (self.timeout and time.time() - self._start_time >= self.timeout)
        )

    def frame_idle(self, frame_start: float):
        sleep_time = self.frame_time - (time.time() - frame_start)
        logger.debug(f"update complete, sleeping for {sleep_time:.3f} s")
        if sleep_time > 0:
            time.sleep(sleep_time)

    def update_fan(self):
        if self.control_fan:
            temp = util.get_cpu_temp()
            if not self.poe_hat.is_fan_on() and temp > self.fan_on_temp:
                logger.info(f"CPU temperature at {temp}, turning fan ON")
                self.poe_hat.fan_on()
            elif self.poe_hat.is_fan_on() and temp < self.fan_off_temp:
                logger.info(f"CPU temperature at {temp}, turning fan OFF")
                self.poe_hat.fan_off()

    def update_display(self):
        if self.show_display:
            self.renderer.draw_frame()

    def add_signal_handlers(self):
        try:
            # terminate gracefully on SIGTERM or SIGHUP
            signal.signal(signal.SIGTERM, self.terminate)
            signal.signal(signal.SIGHUP, self.terminate)
        except AttributeError as e:
            logger.warning(f"failed to register signal handlers: {e}")

    def terminate(self, *args):
        self._terminate = True

    def profiling_setup(self):
        if self.profiling:
            tracemalloc.start()
            self._last_snapshot = tracemalloc.take_snapshot()
            self._last_snapshot_time = 0

    def before_frame(self):
        pass

    def after_frame(self):
        self._frame_counter += 1
        if (
            self.profiling
            and self._frame_counter > 0
            and (time.time() - self._last_snapshot_time) > 20
        ):
            current, peak = tracemalloc.get_traced_memory()
            tracer_mem = tracemalloc.get_tracemalloc_memory()
            snapshot = tracemalloc.take_snapshot()
            snapshot = snapshot.filter_traces((
                tracemalloc.Filter(False, tracemalloc.__file__),
            ))
            top_abs = snapshot.statistics('filename')
            top_diff = snapshot.compare_to(self._last_snapshot, 'lineno')

            top_abs_log = '\n'.join(str(stat) for stat in top_abs[:5])
            top_diff_log = '\n'.join(str(stat) for stat in top_diff[:5])
            logger.info(
                f"memory usage: {current / 1024:.2f} kb (current), {peak / 1024:.2f} kb (peak), "
                f"{(current - tracer_mem) / 1024:.2f} kb (without tracer)."
                f"\nTop 5 usage (absolute):\n{top_abs_log}"
                f"\nTop 5 usage (diff since last):\n{top_diff_log}\n"
            )
            self._last_snapshot = snapshot
            self._last_snapshot_time = time.time()

    def screen_blank(self):
        if self.blank_time > 0:
            logger.debug(f"screen blank for {self.blank_time:.1f} s")
            self.poe_hat.display.hide()
            time.sleep(self.blank_time)
            self.poe_hat.display.show()
