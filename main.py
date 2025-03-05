
from dynamicStopwatch import DynamicLapTimer

if __name__ == "__main__":
    # Example: 51 laps over 20 minutes (1200 seconds)
    total_laps = 51
    total_duration = 20 * 60
    app = DynamicLapTimer(total_laps, total_duration)
    app.mainloop()