# CPU Scheduling Simulator

You can test, visualize, and compare the CPU scheduling algorithms learned in operating systems courses on real processes running on your computer.

---

## 🎯 What It Does?

This application fetches real processes running on your computer (Chrome, Discord, VS Code, etc.) and simulates how they would be managed using the CPU scheduling algorithm of your choice. 

**Main Features:**
- Automatically fetches active processes from your system
- Calculates burst time (CPU usage time) for each process, or allows you to edit them
- Runs simulations with 4 different algorithms
- Visualizes the timeline with a Gantt Chart
- Calculates and compares performance metrics

---

## 📊 Supported Algorithms

### 1. **FCFS (First Come First Serve)**
- The simplest algorithm
- Processes jobs in arrival order
- Fair but sometimes inefficient (convoy effect)
- **When to use:** Simple batch processing

### 2. **SJF (Shortest Job First - Preemptive)**
- Executes the shortest job first
- Provides optimal average waiting time
- Long processes may suffer from starvation
- **When to use:** When aiming for minimum waiting time

### 3. **Priority Scheduling (Preemptive)**
- Processes based on priority (uses priority values fetched from the system)
- High-priority jobs jump the queue
- Risk of priority inversion
- **When to use:** Real-time systems, critical tasks

### 4. **Round Robin**
- Each process gets a fixed time slot (quantum)
- Ensures fair distribution
- Choice of time quantum is critical
- **When to use:** Time-sharing systems, interactive applications

---

## 🚀 Installation & Execution

### Windows Users (.exe)
1. **Download:** Download the `CPUSchedulingSimulator.exe` file
2. **Run:** Double-click the file
3. **If a warning appears:** Select "More info" → "Run anyway"
4. **That's it!** No Python installation is required

### Linux/macOS or Running from Source Code

**Step 1: Check Python**
```bash
python --version  # Must be 3.8 or higher
```

**Step 2: Install Dependencies**
```bash
pip install customtkinter psutil
```

**Step 3: Run the Application**
```bash
python CPUSchedulingSimulator.py
```

**If you get a permission error on Linux:**
```bash
sudo python CPUSchedulingSimulator.py
```

---

## 💻 How to Use?

### Step 1: Fetch Processes
1. Click the **"🔄 Fetch PC Processes"** button on the left panel
2. A brief loading animation appears
3. A list of 30 processes will appear on the right
4. Burst time is automatically calculated for each process (between 0-100)

**How is Burst Time Calculated?**
- Real CPU usage + Random factor
- Heavy processes (like Chrome) get higher values
- Lightweight processes (system services) get lower values

### Step 2: Edit Burst Time (Optional)
- Click on any value in the **"Burst Time"** column of the table
- Enter a new value (between 0-100)
- Press Enter
- Very useful for creating educational scenarios

### Step 3: Select Algorithm
- Select an algorithm from the dropdown menu:
  - FCFS
  - SJF
  - Priority
  - Round Robin
- If Round Robin is selected, enter a **Time Quantum** (default: 2)

### Step 4: Run Simulation
- Click the **"▶ Run Simulation"** button
- Results will appear instantly

### Step 5: Analyze Results

**Interactive Gantt Chart:**
- Each process is displayed in a different color
- Visualizes the execution timeline
- **Zoom In/Out:** Zoom to see details
- **Pan:** Drag with your mouse
- **Scroll:** Horizontal scrolling

**KPI Metrics (4 Cards):**
1. **CPU Utilization** - How busy the CPU is (%)
2. **Throughput** - Number of processes completed per unit of time
3. **Avg Turnaround Time** - Average time taken to complete processes
4. **Avg Waiting Time** - Average time processes spend waiting in the queue

**Detailed Results Table:**
- Completion, turnaround, and waiting time for each process
- Click on column headers to sort the data

---
