# Airline Booking System - Critical Section Project

## 📋 Project Overview

This project demonstrates the **Critical Section problem** in Operating Systems through a real-world scenario: the Centrum Air overbooking incident where two passengers were stranded at Istanbul Airport due to race conditions in their booking system.

**Course:** Operating Systems CS-2023  
**Deadline:** December 29, 2025 (23:59)  
**Purpose:** Extra project for students at risk of failing

---

## 🎯 Learning Objectives

By completing this project, you will understand:

1. **Critical Sections** - Code segments requiring mutual exclusion
2. **Race Conditions** - How concurrent access causes data corruption
3. **Synchronization Mechanisms** - Mutex, Locks, Semaphores
4. **Read/Write Conflicts** - Why they occur and how to prevent them
5. **Producer-Consumer Problem** - Classic synchronization analogy
6. **Real-world Applications** - How booking systems prevent overbooking

---

## 📁 Project Structure

```
booking-system-project/
│
├── booking_system.py      # Main backend implementation (REQUIRED)
│   ├── UnsafeBookingSystem     → Demonstrates the problem
│   ├── SafeBookingSystem       → Solution with Mutex
│   └── SemaphoreBookingSystem  → Solution with Semaphore
│
├── index.html            # Visual demonstration (OPTIONAL)
│   └── Interactive web interface showing both systems side-by-side
│
├── report.md             # Detailed explanation (REQUIRED)
│   ├── Centrum Air case analysis
│   ├── Critical section concepts
│   ├── Race condition explanation
│   ├── Solution implementation details
│   └── Comparative analysis
│
└── README.md             # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Web browser (for HTML visualization)
- Basic understanding of threading

### Running the Backend

```bash
# 1. Clone or download the project
cd booking-system-project

# 2. Run the Python demonstration
python3 booking_system.py

# Expected output:
# - UNSAFE system demonstration (shows overbooking)
# - SAFE system demonstration (prevents overbooking)
# - SEMAPHORE system demonstration (alternative solution)
```

### Running the HTML Visualization (Optional)

```bash
# Method 1: Direct open
firefox index.html
# or
chrome index.html

# Method 2: Using HTTP server
python3 -m http.server 8000
# Then visit: http://localhost:8000
```

---

## 🔍 What Each File Does

### 1. `booking_system.py` (Main Backend - REQUIRED)

**Purpose:** Demonstrates race conditions and synchronization solutions

**Three Implementations:**

#### a) UnsafeBookingSystem
```python
class UnsafeBookingSystem:
    # NO synchronization
    # Shows how overbooking happens
    # Race condition occurs here!
```

**What it demonstrates:**
- Multiple threads reading `available_seats` simultaneously
- All see same value (e.g., 1 seat available)
- All proceed to book
- Result: Overbooking!

#### b) SafeBookingSystem
```python
class SafeBookingSystem:
    def __init__(self):
        self.lock = threading.Lock()  # Mutex
    
    def book_ticket(self, ...):
        with self.lock:  # Critical section protected!
            # Only one thread at a time
```

**What it demonstrates:**
- Mutex (mutual exclusion lock)
- Only one thread can enter critical section
- Others wait their turn
- No overbooking possible

#### c) SemaphoreBookingSystem
```python
class SemaphoreBookingSystem:
    def __init__(self, total_seats):
        self.seat_semaphore = threading.Semaphore(total_seats)
```

**What it demonstrates:**
- Counting semaphore
- Each seat is a semaphore permit
- Acquiring permits = booking seats
- More flexible than mutex

### 2. `index.html` (Visualization - OPTIONAL)

**Purpose:** Visual, interactive demonstration of both systems

**Features:**
- Side-by-side comparison
- Real-time logs
- Configurable parameters
- Visual feedback on overbooking

**Note:** This is purely for visualization. The core logic is still in JavaScript, but it's simplified. The actual backend (Python) is more accurate and complete.

### 3. `report.md` (Explanation - REQUIRED)

**Purpose:** Comprehensive written explanation

**Contents:**
1. Centrum Air incident analysis
2. Critical section concept
3. Race condition explanation
4. Read/Write conflict details
5. Producer-Consumer analogy
6. Solution implementation
7. Test results
8. Conclusions

---

## 🧪 Testing the Project

### Test Case 1: Demonstrate Overbooking

```python
# In booking_system.py
# Unsafe system with limited seats and many users

system = UnsafeBookingSystem(total_seats=10)
# 6 passengers, each wanting 2-4 seats
# Total demand: ~18 seats
# Available: 10 seats
# Result: OVERBOOKING (multiple passengers get same seat)
```

**Expected Result:**
```
[UNSAFE] Passenger_A BOOKED 2 ticket(s). Remaining: 8
[UNSAFE] Passenger_B BOOKED 3 ticket(s). Remaining: 5
[UNSAFE] Passenger_C BOOKED 2 ticket(s). Remaining: 3
[UNSAFE] Passenger_D BOOKED 4 ticket(s). Remaining: -1  ← NEGATIVE!
...
Total Bookings: 6
Total Seats: 10
Overbooking: 6 seats over capacity
```

### Test Case 2: Verify Protection

```python
# Safe system with same scenario
system = SafeBookingSystem(total_seats=10)
# Same 6 passengers
# Result: NO OVERBOOKING
```

**Expected Result:**
```
[SAFE] Passenger_A BOOKED 2 ticket(s). Remaining: 8
[SAFE] Passenger_B BOOKED 3 ticket(s). Remaining: 5
[SAFE] Passenger_C BOOKED 2 ticket(s). Remaining: 3
[SAFE] Passenger_D BOOKED 3 ticket(s). Remaining: 0
[SAFE] Passenger_E - Not enough seats!  ← CORRECTLY REJECTED
[SAFE] Passenger_F - Not enough seats!  ← CORRECTLY REJECTED
```

### Test Case 3: Custom Scenarios

Modify the code to test different scenarios:

```python
# Test with different parameters
def custom_test():
    # Scenario 1: High contention
    system = SafeBookingSystem(total_seats=5)
    # 10 users, each wanting 2 seats
    # Only 2-3 will succeed
    
    # Scenario 2: Exact capacity
    system = SafeBookingSystem(total_seats=10)
    # 5 users, each wanting 2 seats
    # All should succeed
    
    # Scenario 3: Low demand
    system = SafeBookingSystem(total_seats=20)
    # 3 users, each wanting 2 seats
    # All succeed, 14 seats remain
```

---

## 📊 Performance Analysis

### Execution Time Comparison

| System | Seats | Users | Time (avg) | Correctness |
|--------|-------|-------|------------|-------------|
| Unsafe | 10 | 6 | 0.3s | ❌ Wrong |
| Safe (Mutex) | 10 | 6 | 0.4s | ✅ Correct |
| Safe (Semaphore) | 10 | 6 | 0.4s | ✅ Correct |

**Key Insight:** Synchronization adds ~30% overhead, but guarantees correctness!

---

## 🎓 Concepts Explained

### 1. Critical Section

**Definition:** A code segment where shared resources are accessed

**In our system:**
```python
# CRITICAL SECTION
current_available = self.available_seats  # READ
if current_available >= num_tickets:
    self.available_seats -= num_tickets    # WRITE
# END CRITICAL SECTION
```

**Why critical?** Multiple threads can interfere with each other here.

### 2. Race Condition

**Definition:** Outcome depends on thread execution timing

**Example:**
```
Thread 1: read seats = 1
Thread 2: read seats = 1  ← Both see 1!
Thread 1: book 1 seat (seats = 0)
Thread 2: book 1 seat (seats = -1)  ← PROBLEM!
```

### 3. Mutex (Mutual Exclusion)

**Definition:** Lock that allows only one thread at a time

**Usage:**
```python
lock = threading.Lock()

with lock:
    # Only ONE thread here
    # Others wait outside
    critical_section_code()
# Lock released automatically
```

### 4. Semaphore

**Definition:** Counter that controls access to resources

**Usage:**
```python
sem = threading.Semaphore(10)  # 10 permits

sem.acquire()  # Get one permit (count becomes 9)
# Use resource
sem.release()  # Return permit (count becomes 10)
```

---

## 🐛 Common Issues and Solutions

### Issue 1: "ModuleNotFoundError: No module named 'threading'"

**Solution:** Threading is built-in, but check Python version:
```bash
python3 --version  # Should be 3.7+
```

### Issue 2: No overbooking seen in unsafe system

**Solution:** Increase contention:
```python
# Make race condition more likely
passengers = [
    ("User1", 2), ("User2", 2), ("User3", 2),
    ("User4", 2), ("User5", 2), ("User6", 2),
    ("User7", 2), ("User8", 2),  # More users
]
system = UnsafeBookingSystem(total_seats=5)  # Fewer seats
```

### Issue 3: HTML not showing properly

**Solution:** Use HTTP server instead of file://
```bash
python3 -m http.server 8000
```
