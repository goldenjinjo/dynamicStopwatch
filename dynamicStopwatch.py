import tkinter as tk
import time
from definitions import *


class DynamicLapTimer(tk.Tk):
    def __init__(self, total_laps, total_duration):
        super().__init__()
        self.total_laps = total_laps
        self.total_duration = total_duration  # in seconds
        self.current_lap = 1
        self.lap_times = []
        
        # Define a static lap target for performance calculations.
        self.static_lap_target = total_duration / total_laps
        self.cumulative_diff = 0.0  # Total time saved/lost
        
        # Global start time
        self.global_start_time = time.time()
        self.current_lap_target = self.static_lap_target
        self.lap_start_time = time.time()
        
        # GUI Setup
        self.title("Dynamic Lap Timer")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(True, True)
        
        # Main frame (center content)
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(pady=20)
        
        self.info_label = tk.Label(self.main_frame, text=f"Lap {self.current_lap} of {self.total_laps}", font=("Helvetica", TITLE_FONT_SIZE))
        self.info_label.pack(pady=10)
        
        self.overall_label = tk.Label(self.main_frame, text="Overall Remaining Time: --", font=("Helvetica", LABEL_FONT_SIZE))
        self.overall_label.pack(pady=5)
        
        self.lap_target_label = tk.Label(self.main_frame, text=f"Lap Target: {self.current_lap_target:.2f} s | Countdown: -- s", font=("Helvetica", LABEL_FONT_SIZE))
        self.lap_target_label.pack(pady=5)
        
        self.overall_performance_label = tk.Label(self.main_frame, text="Overall Performance: --", font=("Helvetica", LABEL_FONT_SIZE))
        self.overall_performance_label.pack(pady=5)
        
        self.finish_button = tk.Button(self.main_frame, text="Finish Lap", command=self.finish_lap, width=20, height=2, font=("Helvetica", BUTTON_FONT_SIZE))
        self.finish_button.pack(pady=15)
        
        # Stats log (below)
        self.stats_text = tk.Text(self, height=10, width=60, font=("Helvetica", TEXT_FONT_SIZE))
        self.stats_text.pack(pady=10)
        
        # Static Lap Time at the bottom
        self.static_lap_label = tk.Label(self, text=f"Static Lap Time: {self.static_lap_target:.2f} s", font=("Helvetica", LABEL_FONT_SIZE), fg="blue")
        self.static_lap_label.pack(pady=10)
        
        self.update_countdown()
    
    def format_time(self, seconds):
        """Format seconds into m:ss format."""
        if seconds < 0:
            seconds = 0
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    
    def update_countdown(self):
        """Update overall remaining time and lap countdown continuously."""
        current_time = time.time()
        overall_elapsed = current_time - self.global_start_time
        overall_remaining = self.total_duration - overall_elapsed
        
        # Update overall remaining time
        overall_formatted = self.format_time(overall_remaining)
        self.overall_label.config(text=f"Overall Remaining Time: {overall_formatted}")
        
        # Update current lap countdown
        current_lap_elapsed = current_time - self.lap_start_time
        lap_countdown = self.current_lap_target - current_lap_elapsed
        
        if lap_countdown < 0:
            countdown_str = f"{lap_countdown:.2f} s (Over time)"
            self.lap_target_label.config(fg="red")
        else:
            countdown_str = f"{lap_countdown:.2f} s"
            self.lap_target_label.config(fg="black")
            
        self.lap_target_label.config(text=f"Lap Target: {self.current_lap_target:.2f} s | Countdown: {countdown_str}")
        
        if self.current_lap <= self.total_laps:
            self.after(100, self.update_countdown)
    
    def finish_lap(self):
        """Handles lap completion and updates performance tracking."""
        current_time = time.time()
        lap_time = current_time - self.lap_start_time
        self.lap_times.append(lap_time)
        
        # Calculate overall performance
        lap_diff = self.static_lap_target - lap_time  # Positive if ahead, negative if behind
        self.cumulative_diff += lap_diff
        
        # Determine total time saved/lost message
        if self.cumulative_diff > 0:
            overall_perf = f"Total time saved: {self.cumulative_diff:.2f} s"
        else:
            overall_perf = f"Total time lost: {abs(self.cumulative_diff):.2f} s"
        
        # **Calculate extra questions correctly**
        cumulative_questions = self.cumulative_diff / self.static_lap_target
        
        performance_msg = (f"{overall_perf} | Extra Questions Possible: {cumulative_questions:.2f}")
        self.overall_performance_label.config(text=performance_msg)
        
        # Update stats text
        overall_elapsed = current_time - self.global_start_time
        overall_remaining = self.total_duration - overall_elapsed
        remaining_laps = self.total_laps - self.current_lap
        new_target = overall_remaining / remaining_laps if remaining_laps > 0 else 0
        
        stats = (f"Lap {self.current_lap}: {lap_time:.2f} s | "
                 f"New Target: {new_target:.2f} s | {overall_perf}\n")
        self.stats_text.insert(tk.END, stats)
        self.stats_text.see(tk.END)
        
        self.current_lap += 1
        if self.current_lap > self.total_laps:
            self.info_label.config(text="All laps completed!")
            self.finish_button.config(state=tk.DISABLED)
        else:
            self.info_label.config(text=f"Lap {self.current_lap} of {self.total_laps}")
            self.current_lap_target = new_target
            self.lap_start_time = current_time
