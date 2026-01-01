import customtkinter as ctk
import psutil
from tkinter import messagebox, Canvas
import copy
from collections import defaultdict
import random
import threading

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Process:
    """Represents a process with scheduling attributes"""
    def __init__(self, pid, name, priority, burst_time=0, arrival_time=0):
        self.pid = pid
        self.name = name
        self.priority = priority
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.start_time = -1


class SchedulingSimulator:
    """Implements various CPU scheduling algorithms"""
    
    @staticmethod
    def fcfs(processes):
        """First Come First Serve scheduling"""
        processes = sorted(processes, key=lambda p: p.arrival_time)
        current_time = 0
        gantt_chart = []
        
        for process in processes:
            if current_time < process.arrival_time:
                gantt_chart.append(("IDLE", current_time, process.arrival_time))
                current_time = process.arrival_time
            
            process.start_time = current_time
            gantt_chart.append((process.pid, current_time, current_time + process.burst_time))
            current_time += process.burst_time
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
        
        return processes, gantt_chart
    
    @staticmethod
    def sjf_preemptive(processes):
        """Shortest Job First (Preemptive) scheduling"""
        processes = [copy.deepcopy(p) for p in processes]
        n = len(processes)
        current_time = 0
        completed = 0
        gantt_chart = []
        last_process = None
        
        while completed < n:
            available = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
            
            if not available:
                next_arrival = min([p.arrival_time for p in processes if p.remaining_time > 0])
                if last_process != "IDLE":
                    gantt_chart.append(("IDLE", current_time, next_arrival))
                    last_process = "IDLE"
                current_time = next_arrival
                continue
            
            current_process = min(available, key=lambda p: p.remaining_time)
            
            if current_process.start_time == -1:
                current_process.start_time = current_time
            
            if last_process != current_process.pid:
                if gantt_chart and last_process == current_process.pid:
                    gantt_chart[-1] = (gantt_chart[-1][0], gantt_chart[-1][1], current_time + 1)
                else:
                    gantt_chart.append((current_process.pid, current_time, current_time + 1))
                last_process = current_process.pid
            else:
                gantt_chart[-1] = (gantt_chart[-1][0], gantt_chart[-1][1], current_time + 1)
            
            current_process.remaining_time -= 1
            current_time += 1
            
            if current_process.remaining_time == 0:
                completed += 1
                current_process.completion_time = current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
        
        return processes, gantt_chart
    
    @staticmethod
    def priority_preemptive(processes):
        """Priority (Preemptive) scheduling - Lower priority number = higher priority"""
        processes = [copy.deepcopy(p) for p in processes]
        n = len(processes)
        current_time = 0
        completed = 0
        gantt_chart = []
        last_process = None
        
        while completed < n:
            available = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
            
            if not available:
                next_arrival = min([p.arrival_time for p in processes if p.remaining_time > 0])
                if last_process != "IDLE":
                    gantt_chart.append(("IDLE", current_time, next_arrival))
                    last_process = "IDLE"
                current_time = next_arrival
                continue
            
            current_process = min(available, key=lambda p: p.priority)
            
            if current_process.start_time == -1:
                current_process.start_time = current_time
            
            if last_process != current_process.pid:
                gantt_chart.append((current_process.pid, current_time, current_time + 1))
                last_process = current_process.pid
            else:
                gantt_chart[-1] = (gantt_chart[-1][0], gantt_chart[-1][1], current_time + 1)
            
            current_process.remaining_time -= 1
            current_time += 1
            
            if current_process.remaining_time == 0:
                completed += 1
                current_process.completion_time = current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
        
        return processes, gantt_chart
    
    @staticmethod
    def round_robin(processes, time_quantum):
        """Round Robin scheduling"""
        processes = [copy.deepcopy(p) for p in processes]
        queue = []
        current_time = 0
        gantt_chart = []
        completed = 0
        n = len(processes)
        
        for p in sorted(processes, key=lambda x: x.arrival_time):
            if p.arrival_time == 0:
                queue.append(p)
        
        while completed < n or queue:
            if not queue:
                next_process = min([p for p in processes if p.remaining_time > 0], 
                                  key=lambda p: p.arrival_time)
                gantt_chart.append(("IDLE", current_time, next_process.arrival_time))
                current_time = next_process.arrival_time
                queue.append(next_process)
            
            current_process = queue.pop(0)
            
            if current_process.start_time == -1:
                current_process.start_time = current_time
            
            execution_time = min(time_quantum, current_process.remaining_time)
            gantt_chart.append((current_process.pid, current_time, current_time + execution_time))
            current_process.remaining_time -= execution_time
            current_time += execution_time
            
            for p in processes:
                if p.arrival_time <= current_time and p.remaining_time > 0 and p not in queue and p != current_process:
                    queue.append(p)
            
            if current_process.remaining_time == 0:
                completed += 1
                current_process.completion_time = current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            else:
                queue.append(current_process)
        
        return processes, gantt_chart


class SortableTable(ctk.CTkFrame):
    """A sortable table widget with editable cells"""
    
    def __init__(self, master, headers, editable_columns=None, **kwargs):
        super().__init__(master, **kwargs)
        self.headers = headers
        self.editable_columns = editable_columns or []
        self.data = []
        self.widgets = []
        self.sort_order = {header: True for header in headers}  # True = ascending
        self.entry_widgets = {}  # Store entry widgets for editable cells
        
        self.setup_header()
    
    def setup_header(self):
        """Create sortable header"""
        self.header_frame = ctk.CTkFrame(self, fg_color=("#1E1E1E", "#0D0D0D"))
        self.header_frame.pack(fill="x", padx=2, pady=2)
        
        for col, header in enumerate(self.headers):
            btn = ctk.CTkButton(self.header_frame, text=f"{header} ▲▼",
                               command=lambda c=col: self.sort_by_column(c),
                               font=ctk.CTkFont(size=12, weight="bold"),
                               width=140, height=35,
                               fg_color=("#2B2B2B", "#1A1A1A"),
                               hover_color=("#3A3A3A", "#2A2A2A"))
            btn.grid(row=0, column=col, padx=5, pady=5, sticky="ew")
    
    def set_data(self, data):
        """Set table data"""
        self.data = data
        self.render_table()
    
    def sort_by_column(self, col):
        """Sort table by column"""
        if not self.data:
            return
        
        header = self.headers[col]
        ascending = self.sort_order[header]
        
        # Sort data
        try:
            self.data.sort(key=lambda x: float(x[col]) if str(x[col]).replace('.', '').replace('-', '').isdigit() else str(x[col]), 
                          reverse=not ascending)
        except:
            self.data.sort(key=lambda x: str(x[col]), reverse=not ascending)
        
        self.sort_order[header] = not ascending
        self.render_table()
    
    def render_table(self):
        """Render table with current data"""
        # Clear existing rows (but not header)
        for widget_row in self.widgets:
            for widget in widget_row:
                widget.destroy()
        self.widgets = []
        self.entry_widgets = {}
        
        # Clear any existing row frames
        for widget in self.winfo_children():
            if widget != self.header_frame:
                widget.destroy()
        
        # Create rows
        for idx, row_data in enumerate(self.data):
            row_color = ("#252525", "#151515") if idx % 2 == 0 else ("#2B2B2B", "#1A1A1A")
            row_frame = ctk.CTkFrame(self, fg_color=row_color)
            row_frame.pack(fill="x", padx=2, pady=1)
            
            row_widgets = []
            for col, value in enumerate(row_data):
                # Check if this column is editable
                if self.headers[col] in self.editable_columns:
                    entry = ctk.CTkEntry(row_frame, width=140, height=30,
                                        font=ctk.CTkFont(size=11))
                    entry.insert(0, str(value))
                    entry.grid(row=0, column=col, padx=5, pady=5)
                    row_widgets.append(entry)
                    # Store reference to entry widget with row index
                    self.entry_widgets[idx] = self.entry_widgets.get(idx, {})
                    self.entry_widgets[idx][col] = entry
                else:
                    label = ctk.CTkLabel(row_frame, text=str(value), width=140,
                                        font=ctk.CTkFont(size=11))
                    label.grid(row=0, column=col, padx=5, pady=5)
                    row_widgets.append(label)
            
            self.widgets.append(row_widgets)
    
    def get_data(self):
        """Get current table data including edits"""
        result = []
        for idx, row_data in enumerate(self.data):
            row = []
            for col, value in enumerate(row_data):
                if idx in self.entry_widgets and col in self.entry_widgets[idx]:
                    row.append(self.entry_widgets[idx][col].get())
                else:
                    row.append(value)
            result.append(row)
        return result


class InteractiveGanttChart(ctk.CTkFrame):
    """Interactive Gantt Chart with zoom and pan capabilities"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.gantt_data = []
        self.process_colors = {}
        self.colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8",
            "#F7DC6F", "#BB8FCE", "#85C1E2", "#F8B195", "#C06C84",
            "#96CEB4", "#FFEAA7", "#DFE6E9", "#74B9FF", "#A29BFE"
        ]
        
        self.zoom_level = 1.0
        self.pan_offset = 0
        self.canvas_width = 1400
        self.canvas_height = 200
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup Gantt chart UI"""
        # Title and controls container
        top_container = ctk.CTkFrame(self, fg_color="transparent")
        top_container.pack(pady=10, fill="x")
        
        # Title on left
        ctk.CTkLabel(top_container, text="📅 Interactive Gantt Chart Timeline", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(side="left", padx=20)
        
        # Controls on right
        controls_frame = ctk.CTkFrame(top_container, fg_color="transparent")
        controls_frame.pack(side="right", padx=20)
        
        ctk.CTkButton(controls_frame, text="🔍 Zoom In", command=self.zoom_in,
                     width=100, height=30).pack(side="left", padx=5)
        ctk.CTkButton(controls_frame, text="🔍 Zoom Out", command=self.zoom_out,
                     width=100, height=30).pack(side="left", padx=5)
        ctk.CTkButton(controls_frame, text="↺ Reset View", command=self.reset_view,
                     width=100, height=30).pack(side="left", padx=5)
        
        # Canvas container
        canvas_container = ctk.CTkFrame(self)
        canvas_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Create canvas
        self.canvas = Canvas(canvas_container, bg="#1A1A1A", height=self.canvas_height,
                            highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand=True)
        
        # Bind mouse events for panning
        self.canvas.bind("<ButtonPress-1>", self.on_pan_start)
        self.canvas.bind("<B1-Motion>", self.on_pan_move)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        
        self.drag_start_x = 0
        
        # Scrollbar below canvas
        scrollbar = ctk.CTkScrollbar(canvas_container, orientation="horizontal",
                                    command=self.canvas.xview)
        scrollbar.pack(side="bottom", fill="x", pady=(5, 0))
        self.canvas.configure(xscrollcommand=scrollbar.set)
        
        # Legend - scrollable for many processes
        legend_container = ctk.CTkFrame(self, fg_color="transparent")
        legend_container.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(legend_container, text="Legend: ", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10)
        
        # Scrollable legend frame
        self.legend_scroll = ctk.CTkScrollableFrame(legend_container, 
                                                    orientation="horizontal",
                                                    height=40,
                                                    fg_color="transparent")
        self.legend_scroll.pack(side="left", fill="x", expand=True, padx=5)
    
    def set_data(self, gantt_chart):
        """Set Gantt chart data and render"""
        self.gantt_data = gantt_chart
        
        # Create color mapping
        self.process_colors = {}
        color_idx = 0
        for pid, _, _ in gantt_chart:
            if pid not in self.process_colors and pid != "IDLE":
                self.process_colors[pid] = self.colors[color_idx % len(self.colors)]
                color_idx += 1
        
        self.render_gantt()
        self.render_legend()
    
    def zoom_in(self):
        """Zoom in on Gantt chart"""
        self.zoom_level *= 1.3
        self.render_gantt()
    
    def zoom_out(self):
        """Zoom out on Gantt chart"""
        self.zoom_level = max(0.3, self.zoom_level / 1.3)
        self.render_gantt()
    
    def reset_view(self):
        """Reset zoom and pan"""
        self.zoom_level = 1.0
        self.pan_offset = 0
        self.canvas.xview_moveto(0)
        self.render_gantt()
    
    def on_pan_start(self, event):
        """Start panning"""
        self.drag_start_x = event.x
    
    def on_pan_move(self, event):
        """Pan the canvas"""
        delta = event.x - self.drag_start_x
        self.canvas.xview_scroll(int(-delta / 10), "units")
        self.drag_start_x = event.x
    
    def on_mousewheel(self, event):
        """Handle mouse wheel for horizontal scrolling"""
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def render_gantt(self):
        """Render the Gantt chart"""
        self.canvas.delete("all")
        
        if not self.gantt_data:
            return
        
        # Calculate dimensions
        total_time = max([end for _, _, end in self.gantt_data])
        base_width = 1200
        chart_width = int(base_width * self.zoom_level)
        scale = chart_width / total_time if total_time > 0 else 1
        
        margin_left = 50
        margin_top = 40
        bar_height = 80
        
        # Configure scroll region
        self.canvas.configure(scrollregion=(0, 0, chart_width + 200, self.canvas_height))
        
        # Draw timeline background
        self.canvas.create_rectangle(0, 0, chart_width + 200, self.canvas_height,
                                     fill="#1A1A1A", outline="")
        
        # Draw time axis
        self.canvas.create_line(margin_left, margin_top + bar_height + 20,
                               margin_left + chart_width, margin_top + bar_height + 20,
                               fill="#555555", width=2)
        
        # Draw Gantt bars
        for pid, start, end in self.gantt_data:
            x1 = margin_left + (start * scale)
            x2 = margin_left + (end * scale)
            y1 = margin_top
            y2 = margin_top + bar_height
            
            # Choose color
            if pid == "IDLE":
                fill_color = "#3A3A3A"
                outline_color = "#555555"
            else:
                fill_color = self.process_colors.get(pid, "#4ECDC4")
                outline_color = "#FFFFFF"
            
            # Draw shadow
            self.canvas.create_rectangle(x1 + 3, y1 + 3, x2 + 3, y2 + 3,
                                        fill="#000000", outline="", tags="shadow")
            
            # Draw main rectangle
            rect_id = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                   fill=fill_color, outline=outline_color,
                                                   width=3, tags="gantt_bar")
            
            # Add process label
            label = f"P{pid}" if pid != "IDLE" else "IDLE"
            text_x = (x1 + x2) / 2
            text_y = (y1 + y2) / 2
            
            self.canvas.create_text(text_x, text_y, text=label,
                                   fill="black", font=("Arial", 12, "bold"),
                                   tags="label")
            
            # Add time duration below label
            duration = end - start
            self.canvas.create_text(text_x, text_y + 20, text=f"({duration}u)",
                                   fill="black", font=("Arial", 9),
                                   tags="duration")
            
            # Time markers
            self.canvas.create_text(x1, y2 + 35, text=str(start),
                                   fill="#AAAAAA", font=("Arial", 10), tags="time")
            self.canvas.create_line(x1, y2 + 20, x1, y2 + 25,
                                   fill="#555555", width=1, tags="tick")
        
        # Final time marker
        x_end = margin_left + (total_time * scale)
        self.canvas.create_text(x_end, margin_top + bar_height + 35, text=str(total_time),
                               fill="#AAAAAA", font=("Arial", 10), tags="time")
        self.canvas.create_line(x_end, margin_top + bar_height + 20, 
                               x_end, margin_top + bar_height + 25,
                               fill="#555555", width=1, tags="tick")
        
        # Add grid lines for better readability
        grid_interval = max(1, total_time // 20)
        for i in range(0, total_time + 1, grid_interval):
            x = margin_left + (i * scale)
            self.canvas.create_line(x, margin_top, x, margin_top + bar_height,
                                   fill="#2A2A2A", dash=(2, 4), tags="grid")
    
    def render_legend(self):
        """Render legend for all processes"""
        # Clear existing legend
        for widget in self.legend_scroll.winfo_children():
            widget.destroy()
        
        # Show ALL process colors
        all_pids = sorted(list(set([pid for pid, _, _ in self.gantt_data if pid != "IDLE"])))
        
        for pid in all_pids:
            color = self.process_colors.get(pid, "#4ECDC4")
            
            legend_item = ctk.CTkFrame(self.legend_scroll, fg_color="transparent")
            legend_item.pack(side="left", padx=5)
            
            color_box = ctk.CTkLabel(legend_item, text="  ", 
                                    fg_color=color, corner_radius=4,
                                    width=40, height=20)
            color_box.pack(side="left", padx=2)
            
            ctk.CTkLabel(legend_item, text=f"P{pid}",
                        font=ctk.CTkFont(size=10)).pack(side="left", padx=2)


class CPUSchedulerApp(ctk.CTk):
    """Main application class for CPU Scheduling Simulator"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("Advanced CPU Scheduling Simulator")
        self.geometry("1600x950")
        
        # Data storage
        self.processes = []
        self.process_table = None
        self.results_table = None
        self.gantt_chart = None
        
        # Loading overlay
        self.loading_overlay = None
        
        self.setup_ui()
    
    def show_loading(self, message="Loading..."):
        """Show modern loading popup with animation"""
        if self.loading_overlay:
            self.loading_overlay.destroy()
        
        # Create ONLY the popup card, no full-screen overlay
        self.loading_overlay = ctk.CTkFrame(self, 
                                           fg_color=("#2B2B2B", "#1E1E1E"),
                                           corner_radius=20,
                                           width=280, height=200,
                                           border_width=3,
                                           border_color="#4ECDC4")
        
        # Position it in the center, on top of everything
        self.loading_overlay.place(relx=0.5, rely=0.5, anchor="center")
        self.loading_overlay.lift()
        
        # Prevent resizing
        self.loading_overlay.pack_propagate(False)
        
        # Circular progress indicator
        self.loading_canvas = Canvas(self.loading_overlay, 
                                     width=100, height=100,
                                     bg="#2B2B2B", 
                                     highlightthickness=0)
        self.loading_canvas.pack(pady=(25, 10))
        
        # Loading message
        ctk.CTkLabel(self.loading_overlay, 
                    text=message,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#FFFFFF").pack(pady=5)
        
        ctk.CTkLabel(self.loading_overlay, 
                    text="Please wait...",
                    font=ctk.CTkFont(size=11),
                    text_color="#AAAAAA").pack(pady=(0, 20))
        
        # Start animation with scale effect
        self.loading_scale = 0.5
        self.loading_angle = 0
        self.spinner_running = True
        self.animate_popup_entrance()
        
        # Force update
        self.update()
    
    def animate_popup_entrance(self):
        """Animate popup entrance with scale effect"""
        if self.loading_scale < 1.0:
            self.loading_scale += 0.1
            # Scale effect (simulated by adjusting size)
            scale_width = int(280 * self.loading_scale)
            scale_height = int(200 * self.loading_scale)
            
            self.loading_overlay.configure(width=scale_width, height=scale_height)
            self.after(20, self.animate_popup_entrance)
        else:
            # Start spinner animation after entrance
            self.animate_loading()
    
    def animate_loading(self):
        """Animate modern circular loading indicator"""
        if not self.spinner_running or not self.loading_overlay:
            return
        
        # Clear canvas
        self.loading_canvas.delete("all")
        
        # Draw circular spinner
        center_x, center_y = 50, 50
        radius = 35
        
        # Background circle (faded)
        self.loading_canvas.create_oval(center_x - radius, center_y - radius,
                                       center_x + radius, center_y + radius,
                                       outline="#444444", width=3)
        
        # Animated arc with gradient effect (multiple arcs)
        # Main arc
        extent1 = 270
        self.loading_canvas.create_arc(center_x - radius, center_y - radius,
                                      center_x + radius, center_y + radius,
                                      start=self.loading_angle, extent=extent1,
                                      outline="#4ECDC4", width=5, style="arc")
        
        # Secondary arc for depth
        extent2 = 90
        self.loading_canvas.create_arc(center_x - radius, center_y - radius,
                                      center_x + radius, center_y + radius,
                                      start=self.loading_angle + 180, extent=extent2,
                                      outline="#45B7D1", width=4, style="arc")
        
        # Dot at the end for extra flair
        dot_angle = self.loading_angle + extent1
        dot_x = center_x + radius * 0.85 * (1 if dot_angle % 360 < 180 else -1) * abs(((dot_angle % 180) / 90) - 1)
        dot_y = center_y + radius * 0.85 * (1 if (dot_angle + 90) % 360 < 180 else -1) * abs((((dot_angle + 90) % 180) / 90) - 1)
        
        import math
        dot_x = center_x + radius * math.cos(math.radians(dot_angle))
        dot_y = center_y - radius * math.sin(math.radians(dot_angle))
        
        self.loading_canvas.create_oval(dot_x - 4, dot_y - 4, dot_x + 4, dot_y + 4,
                                       fill="#4ECDC4", outline="#4ECDC4")
        
        # Update angle for rotation
        self.loading_angle = (self.loading_angle + 10) % 360
        
        # Continue animation
        if self.spinner_running:
            self.after(40, self.animate_loading)
    
    def hide_loading(self):
        """Hide loading overlay immediately"""
        self.spinner_running = False
        if self.loading_overlay:
            try:
                self.loading_overlay.destroy()
                self.loading_overlay = None
            except:
                pass
    
    def setup_ui(self):
        """Setup the user interface"""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_left_panel()
        self.setup_right_panel()
    
    def setup_left_panel(self):
        """Setup the left control panel"""
        left_frame = ctk.CTkFrame(self, width=320, corner_radius=0)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        left_frame.grid_propagate(False)
        
        # Title
        title_label = ctk.CTkLabel(left_frame, text="Controls Panel", 
                                   font=ctk.CTkFont(size=22, weight="bold"))
        title_label.pack(pady=20, padx=20)
        
        # Process Fetching Section
        fetch_frame = ctk.CTkFrame(left_frame, fg_color=("#2B2B2B", "#1E1E1E"))
        fetch_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(fetch_frame, text="Process Fetching", 
                    font=ctk.CTkFont(size=15, weight="bold")).pack(pady=10, padx=10)
        
        self.fetch_button = ctk.CTkButton(fetch_frame, text="🔄 Fetch PC Processes",
                                         command=self.fetch_processes,
                                         height=45, font=ctk.CTkFont(size=14, weight="bold"),
                                         corner_radius=10)
        self.fetch_button.pack(pady=10, padx=15, fill="x")
        
        # Burst time info
        info_label = ctk.CTkLabel(fetch_frame, 
                                 text="Burst times (0-100) auto-generated\nYou can edit them in the table",
                                 font=ctk.CTkFont(size=10),
                                 text_color="#888888")
        info_label.pack(pady=(0, 10), padx=10)
        
        # Algorithm Selection Section
        algo_frame = ctk.CTkFrame(left_frame, fg_color=("#2B2B2B", "#1E1E1E"))
        algo_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(algo_frame, text="Algorithm Selection", 
                    font=ctk.CTkFont(size=15, weight="bold")).pack(pady=10, padx=10)
        
        self.algorithm_var = ctk.StringVar(value="FCFS")
        self.algorithm_menu = ctk.CTkOptionMenu(algo_frame, 
                                                values=["FCFS", "SJF (Preemptive)", 
                                                       "Priority (Preemptive)", "Round Robin"],
                                                variable=self.algorithm_var,
                                                command=self.on_algorithm_change,
                                                height=35,
                                                font=ctk.CTkFont(size=13),
                                                corner_radius=8)
        self.algorithm_menu.pack(pady=10, padx=15, fill="x")
        
        # Time Quantum (for Round Robin)
        self.quantum_frame = ctk.CTkFrame(algo_frame, fg_color="transparent")
        ctk.CTkLabel(self.quantum_frame, text="Time Quantum:",
                    font=ctk.CTkFont(size=12)).pack(side="left", padx=5)
        self.quantum_entry = ctk.CTkEntry(self.quantum_frame, width=80, height=30)
        self.quantum_entry.insert(0, "20")
        self.quantum_entry.pack(side="left", padx=5)
        
        # Action Buttons
        action_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        action_frame.pack(pady=20, padx=20, fill="x")
        
        self.run_button = ctk.CTkButton(action_frame, text="▶ Run Simulation",
                                       command=self.run_simulation,
                                       fg_color="#28a745", hover_color="#218838",
                                       height=50, font=ctk.CTkFont(size=15, weight="bold"),
                                       corner_radius=10)
        self.run_button.pack(pady=5, padx=10, fill="x")
        
        self.reset_button = ctk.CTkButton(action_frame, text="🔄 Reset Data",
                                         command=self.reset_data,
                                         fg_color="#dc3545", hover_color="#c82333",
                                         height=45, font=ctk.CTkFont(size=14, weight="bold"),
                                         corner_radius=10)
        self.reset_button.pack(pady=5, padx=10, fill="x")
        
        # Info Section
        info_frame = ctk.CTkFrame(left_frame, fg_color=("#2B2B2B", "#1E1E1E"))
        info_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(info_frame, text="📋 Instructions", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        info_text = """1. Click 'Fetch PC Processes'
   
2. Edit burst times directly
   in the table (0-100 range)
   
3. Select scheduling algorithm
   
4. Run simulation to see
   interactive Gantt chart"""
        
        ctk.CTkLabel(info_frame, text=info_text, justify="left",
                    font=ctk.CTkFont(size=11), 
                    text_color="#CCCCCC").pack(pady=5, padx=15)
    
    def setup_right_panel(self):
        """Setup the right data and results panel"""
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Process List Title
        self.process_title = ctk.CTkLabel(self.right_frame, text="Process List", 
                                         font=ctk.CTkFont(size=20, weight="bold"))
        self.process_title.pack(pady=15)
    
    def on_algorithm_change(self, choice):
        """Handle algorithm selection change"""
        if choice == "Round Robin":
            self.quantum_frame.pack(pady=5, padx=10, fill="x")
        else:
            self.quantum_frame.pack_forget()
    
    def fetch_processes(self):
        """Fetch currently running processes from the system"""
        # Auto-reset if processes already exist
        if self.processes:
            # Clear existing data automatically
            self.processes = []
            
            # Clear process table
            if self.process_table:
                self.process_table.destroy()
                self.process_table = None
            
            # Clear results if any
            for widget in self.right_frame.winfo_children():
                if widget != self.process_title:
                    widget.destroy()
        
        # Show loading screen
        self.show_loading("Fetching processes from your PC...")
        
        # Disable fetch button during operation
        self.fetch_button.configure(state="disabled")
        
        # Run fetch in separate thread to avoid freezing UI
        thread = threading.Thread(target=self._do_fetch_processes, daemon=True)
        thread.start()
    
    def _do_fetch_processes(self):
        """Actually fetch the processes in background thread"""
        try:
            processes = []
            
            # Get all running processes
            for proc in psutil.process_iter(['pid', 'name', 'nice', 'cpu_percent']):
                try:
                    pid = proc.info['pid']
                    name = proc.info['name']
                    priority = proc.info['nice'] if proc.info['nice'] is not None else 0
                    
                    # Generate burst time between 0-100
                    try:
                        cpu_percent = proc.cpu_percent(interval=0.1)
                    except:
                        cpu_percent = 0
                    
                    # Generate burst time: weighted by CPU usage with randomization
                    base_burst = random.randint(5, 50)
                    cpu_influence = int(cpu_percent / 2) if cpu_percent > 0 else 0
                    burst_time = min(100, max(0, base_burst + cpu_influence + random.randint(-10, 10)))
                    
                    process = Process(pid, name, priority, burst_time=burst_time, arrival_time=0)
                    processes.append(process)
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Limit to first 30 processes
            processes = processes[:30]
            
            # Update UI in main thread
            self.after(0, lambda: self._finish_fetch(processes))
            
        except Exception as e:
            self.after(0, lambda: self._fetch_error(str(e)))
    
    def _finish_fetch(self, processes):
        """Complete the fetch operation in main thread"""
        self.processes = processes
        self.hide_loading()
        self.display_process_table()
        self.fetch_button.configure(state="normal")
        messagebox.showinfo("Success", f"✓ Fetched {len(self.processes)} processes!")
    
    def _fetch_error(self, error_msg):
        """Handle fetch error"""
        self.hide_loading()
        self.fetch_button.configure(state="normal")
        messagebox.showerror("Error", f"Failed to fetch processes: {error_msg}")
    
    def display_process_table(self):
        """Display the process table with sortable columns and editable burst times"""
        # Clear existing table
        if self.process_table:
            self.process_table.destroy()
        
        # Create table container
        table_container = ctk.CTkFrame(self.right_frame, fg_color=("#2B2B2B", "#1E1E1E"))
        table_container.pack(pady=10, fill="both", expand=False, padx=10)
        
        # Prepare data
        headers = ["PID", "Process Name", "OS Priority", "Burst Time"]
        table_data = []
        for p in self.processes:
            name_display = p.name[:25] + "..." if len(p.name) > 25 else p.name
            table_data.append([p.pid, name_display, p.priority, p.burst_time])
        
        # Create sortable table with editable burst time column
        self.process_table = SortableTable(table_container, headers, 
                                          editable_columns=["Burst Time"],
                                          fg_color="transparent")
        self.process_table.pack(fill="both", expand=True, padx=5, pady=5)
        self.process_table.set_data(table_data)
    
    def run_simulation(self):
        """Run the selected scheduling algorithm"""
        if not self.processes:
            messagebox.showwarning("Warning", "Please fetch processes first!")
            return
        
        # Update burst times from table
        try:
            table_data = self.process_table.get_data()
            for idx, p in enumerate(self.processes):
                burst_time = int(table_data[idx][3])
                if burst_time < 0 or burst_time > 100:
                    raise ValueError("Burst time must be between 0 and 100")
                p.burst_time = burst_time
                p.remaining_time = burst_time
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid burst times (0-100)!")
            return
        
        # Filter out processes with 0 burst time
        valid_processes = [p for p in self.processes if p.burst_time > 0]
        if not valid_processes:
            messagebox.showwarning("Warning", "No processes with valid burst times!")
            return
        
        # Run simulation
        algorithm = self.algorithm_var.get()
        simulator = SchedulingSimulator()
        
        try:
            if algorithm == "FCFS":
                results, gantt_chart = simulator.fcfs(valid_processes)
            elif algorithm == "SJF (Preemptive)":
                results, gantt_chart = simulator.sjf_preemptive(valid_processes)
            elif algorithm == "Priority (Preemptive)":
                results, gantt_chart = simulator.priority_preemptive(valid_processes)
            elif algorithm == "Round Robin":
                time_quantum = int(self.quantum_entry.get())
                if time_quantum <= 0:
                    raise ValueError("Time quantum must be positive")
                results, gantt_chart = simulator.round_robin(valid_processes, time_quantum)
            
            self.display_results(results, gantt_chart, algorithm)
            
        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed: {str(e)}")
    
    def display_results(self, results, gantt_chart, algorithm):
        """Display simulation results"""
        # Clear previous results
        for widget in self.right_frame.winfo_children():
            if widget != self.process_title and widget != self.process_table.master:
                widget.destroy()
        
        # Results Title
        results_header = ctk.CTkFrame(self.right_frame, fg_color=("#1E1E1E", "#0D0D0D"),
                                     corner_radius=10)
        results_header.pack(pady=15, fill="x", padx=10)
        
        ctk.CTkLabel(results_header, 
                    text=f"📊 Simulation Results - {algorithm}", 
                    font=ctk.CTkFont(size=22, weight="bold"),
                    text_color="#4ECDC4").pack(pady=15)
        
        # Interactive Gantt Chart
        gantt_container = ctk.CTkFrame(self.right_frame, fg_color=("#2B2B2B", "#1E1E1E"),
                                      corner_radius=10)
        gantt_container.pack(pady=15, fill="both", expand=True, padx=10)
        
        self.gantt_chart = InteractiveGanttChart(gantt_container, fg_color="transparent")
        self.gantt_chart.pack(fill="both", expand=True, padx=5, pady=5)
        self.gantt_chart.set_data(gantt_chart)
        
        # KPIs
        self.display_kpis(results, gantt_chart)
        
        # Results Table
        self.display_results_table(results)
    
    def display_kpis(self, results, gantt_chart):
        """Display Key Performance Indicators in single row"""
        kpi_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        kpi_container.pack(pady=15, fill="x", padx=10)
        
        ctk.CTkLabel(kpi_container, text="📈 Key Performance Indicators", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Calculate metrics
        total_time = max([end for _, _, end in gantt_chart])
        idle_time = sum([end - start for pid, start, end in gantt_chart if pid == "IDLE"])
        cpu_utilization = ((total_time - idle_time) / total_time * 100) if total_time > 0 else 0
        
        throughput = len(results) / total_time if total_time > 0 else 0
        avg_turnaround = sum([p.turnaround_time for p in results]) / len(results)
        avg_waiting = sum([p.waiting_time for p in results]) / len(results)
        
        # Display metrics in single row (1x4 layout)
        metrics_grid = ctk.CTkFrame(kpi_container, fg_color="transparent")
        metrics_grid.pack(pady=10, padx=20, fill="x")
        
        # Configure grid columns to be equal width
        for i in range(4):
            metrics_grid.grid_columnconfigure(i, weight=1)
        
        metrics = [
            ("CPU Utilization", f"{cpu_utilization:.2f}%", "#28a745"),
            ("Throughput", f"{throughput:.3f} proc/unit", "#4ECDC4"),
            ("Avg Turnaround", f"{avg_turnaround:.2f} units", "#FFA07A"),
            ("Avg Waiting", f"{avg_waiting:.2f} units", "#BB8FCE")
        ]
        
        for idx, (label, value, color) in enumerate(metrics):
            card = ctk.CTkFrame(metrics_grid, fg_color=("#2B2B2B", "#1E1E1E"),
                               corner_radius=10, height=100)
            card.grid(row=0, column=idx, padx=10, pady=0, sticky="ew")
            
            ctk.CTkLabel(card, text=label, 
                        font=ctk.CTkFont(size=13, weight="bold"),
                        text_color="#CCCCCC").pack(pady=(15, 5))
            
            ctk.CTkLabel(card, text=value, 
                        font=ctk.CTkFont(size=20, weight="bold"), 
                        text_color=color).pack(pady=(0, 15))
    
    def display_results_table(self, results):
        """Display detailed results table with sorting"""
        table_container = ctk.CTkFrame(self.right_frame, fg_color=("#2B2B2B", "#1E1E1E"),
                                      corner_radius=10)
        table_container.pack(pady=15, fill="x", padx=10)
        
        ctk.CTkLabel(table_container, text="📋 Detailed Process Metrics", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)
        
        # Prepare data
        headers = ["PID", "Process Name", "Completion", "Turnaround", "Waiting"]
        table_data = []
        for p in results:
            name_display = p.name[:20] + "..." if len(p.name) > 20 else p.name
            table_data.append([p.pid, name_display, p.completion_time, 
                             p.turnaround_time, p.waiting_time])
        
        # Create sortable table
        self.results_table = SortableTable(table_container, headers,
                                          fg_color="transparent")
        self.results_table.pack(fill="both", expand=True, padx=10, pady=10)
        self.results_table.set_data(table_data)
    
    def reset_data(self):
        """Reset all data and clear the interface"""
        self.processes = []
        
        # Clear tables
        if self.process_table:
            self.process_table.destroy()
            self.process_table = None
        
        # Clear results
        for widget in self.right_frame.winfo_children():
            if widget != self.process_title:
                widget.destroy()
        
        messagebox.showinfo("Reset Complete", "✓ All data has been reset!")


if __name__ == "__main__":
    app = CPUSchedulerApp()
    app.mainloop()