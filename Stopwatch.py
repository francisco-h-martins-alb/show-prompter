class Stopwatch():

    def __init__(self, widget, stopwatch_time=0):
        self.w = widget
        self._current_time = stopwatch_time
        self.w.setText(self.convert())

    def reset(self):
        self._current_time = 0
        self.w.setText('00:00:00')

    def convert(self):
        hour = int(self._current_time/3600000)
        minute = int((self._current_time/60000)%60)
        second = int((self._current_time%60000)/1000)
        fmt = '{:0>2d}:{:0>2d}:{:0>2d}'
        return fmt.format(hour, minute, second)

    def display(self):
        self._current_time += 10
        self.w.setText(self.convert())
