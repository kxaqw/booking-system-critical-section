"""
Airline Booking System - Demonstrating Overbooking Problem
Critical Section & Race Condition Example

This demonstrates the Centrum Air overbooking incident where
two passengers were left at Istanbul airport due to overselling.
"""

import threading
import time
import random
from typing import List, Dict

# ============================================================================
# CASE 1: WITHOUT PROTECTION (Race Condition - Causes Overbooking)
# ============================================================================

class UnsafeBookingSystem:
    """
    This class demonstrates the overbooking problem without synchronization.
    Multiple threads can access and modify available_seats simultaneously,
    causing race conditions.
    """
    
    def __init__(self, total_seats: int):
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.bookings: List[Dict] = []
        self.booking_id = 0
    
    def book_ticket(self, passenger_name: str, num_tickets: int) -> bool:
        """
        UNSAFE booking without synchronization
        This creates a CRITICAL SECTION problem
        """
        print(f"[UNSAFE] {passenger_name} requesting {num_tickets} ticket(s)...")
        
        # CRITICAL SECTION BEGINS - Reading shared resource
        current_available = self.available_seats
        
        # Simulate network delay or processing time
        # This delay makes race condition more likely to occur
        time.sleep(random.uniform(0.01, 0.1))
        
        # Check if seats available
        if current_available >= num_tickets:
            print(f"[UNSAFE] {passenger_name} sees {current_available} seats available")
            
            # Another delay - this is where race condition happens!
            time.sleep(random.uniform(0.01, 0.1))
            
            # CRITICAL SECTION - Writing to shared resource
            self.available_seats -= num_tickets
            self.booking_id += 1
            
            booking = {
                'id': self.booking_id,
                'passenger': passenger_name,
                'tickets': num_tickets,
                'status': 'CONFIRMED'
            }
            self.bookings.append(booking)
            
            print(f"✓ [UNSAFE] {passenger_name} BOOKED {num_tickets} ticket(s). "
                  f"Remaining: {self.available_seats}")
            return True
        else:
            print(f"✗ [UNSAFE] {passenger_name} - Not enough seats!")
            return False
    
    def get_status(self):
        """Display current system status"""
        print(f"\n{'='*60}")
        print(f"UNSAFE SYSTEM STATUS")
        print(f"{'='*60}")
        print(f"Total Seats: {self.total_seats}")
        print(f"Available Seats: {self.available_seats}")
        print(f"Total Bookings: {len(self.bookings)}")
        print(f"Overbooking: {len(self.bookings) * 1 - self.total_seats} seats")
        print(f"\nBookings:")
        for booking in self.bookings:
            print(f"  {booking}")
        print(f"{'='*60}\n")


# ============================================================================
# CASE 2: WITH PROTECTION (Using Mutex/Lock)
# ============================================================================

class SafeBookingSystem:
    """
    This class demonstrates proper synchronization using mutex (threading.Lock).
    Only one thread can access the critical section at a time.
    """
    
    def __init__(self, total_seats: int):
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.bookings: List[Dict] = []
        self.booking_id = 0
        
        # MUTEX - This is our synchronization mechanism
        self.lock = threading.Lock()
    
    def book_ticket(self, passenger_name: str, num_tickets: int) -> bool:
        """
        SAFE booking with mutex synchronization
        Lock ensures only one thread enters critical section
        """
        print(f"[SAFE] {passenger_name} requesting {num_tickets} ticket(s)...")
        
        # ACQUIRE LOCK - Only one thread can proceed
        with self.lock:
            # CRITICAL SECTION BEGINS - Protected by mutex
            current_available = self.available_seats
            
            # Simulate processing time
            time.sleep(random.uniform(0.01, 0.1))
            
            # Check if seats available
            if current_available >= num_tickets:
                print(f"[SAFE] {passenger_name} sees {current_available} seats available")
                
                time.sleep(random.uniform(0.01, 0.1))
                
                # Update shared resource - still protected by lock
                self.available_seats -= num_tickets
                self.booking_id += 1
                
                booking = {
                    'id': self.booking_id,
                    'passenger': passenger_name,
                    'tickets': num_tickets,
                    'status': 'CONFIRMED'
                }
                self.bookings.append(booking)
                
                print(f"✓ [SAFE] {passenger_name} BOOKED {num_tickets} ticket(s). "
                      f"Remaining: {self.available_seats}")
                return True
            else:
                print(f"✗ [SAFE] {passenger_name} - Not enough seats!")
                return False
            # LOCK RELEASED automatically when exiting 'with' block
    
    def get_status(self):
        """Display current system status"""
        print(f"\n{'='*60}")
        print(f"SAFE SYSTEM STATUS")
        print(f"{'='*60}")
        print(f"Total Seats: {self.total_seats}")
        print(f"Available Seats: {self.available_seats}")
        print(f"Total Bookings: {len(self.bookings)}")
        
        total_tickets_sold = sum(b['tickets'] for b in self.bookings)
        if total_tickets_sold > self.total_seats:
            print(f"Overbooking: {total_tickets_sold - self.total_seats} seats")
        else:
            print(f"No overbooking - System working correctly!")
        
        print(f"\nBookings:")
        for booking in self.bookings:
            print(f"  {booking}")
        print(f"{'='*60}\n")


# ============================================================================
# CASE 3: Using Semaphore (Alternative synchronization method)
# ============================================================================

class SemaphoreBookingSystem:
    """
    Alternative implementation using Semaphore.
    Semaphore can control access for multiple resources simultaneously.
    """
    
    def __init__(self, total_seats: int):
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.bookings: List[Dict] = []
        self.booking_id = 0
        
        # Semaphore initialized with number of available seats
        self.seat_semaphore = threading.Semaphore(total_seats)
        self.booking_lock = threading.Lock()  # For booking list protection
    
    def book_ticket(self, passenger_name: str, num_tickets: int) -> bool:
        """
        Booking using semaphore synchronization
        """
        print(f"[SEMAPHORE] {passenger_name} requesting {num_tickets} ticket(s)...")
        
        # Try to acquire semaphore tickets
        acquired = []
        for i in range(num_tickets):
            if self.seat_semaphore.acquire(blocking=False):
                acquired.append(i)
            else:
                # Couldn't get all seats, release what we got
                for _ in acquired:
                    self.seat_semaphore.release()
                print(f"✗ [SEMAPHORE] {passenger_name} - Not enough seats!")
                return False
        
        # Got all seats, now update booking
        with self.booking_lock:
            self.available_seats -= num_tickets
            self.booking_id += 1
            
            booking = {
                'id': self.booking_id,
                'passenger': passenger_name,
                'tickets': num_tickets,
                'status': 'CONFIRMED'
            }
            self.bookings.append(booking)
            
            print(f"✓ [SEMAPHORE] {passenger_name} BOOKED {num_tickets} ticket(s). "
                  f"Remaining: {self.available_seats}")
        
        return True
    
    def get_status(self):
        """Display current system status"""
        print(f"\n{'='*60}")
        print(f"SEMAPHORE SYSTEM STATUS")
        print(f"{'='*60}")
        print(f"Total Seats: {self.total_seats}")
        print(f"Available Seats: {self.available_seats}")
        print(f"Total Bookings: {len(self.bookings)}")
        print(f"\nBookings:")
        for booking in self.bookings:
            print(f"  {booking}")
        print(f"{'='*60}\n")


# ============================================================================
# DEMONSTRATION & TESTING
# ============================================================================

def run_unsafe_demo():
    """
    Demonstrate the overbooking problem (like Centrum Air incident)
    """
    print("\n" + "="*80)
    print("DEMONSTRATION 1: UNSAFE SYSTEM (Race Condition)")
    print("="*80)
    print("This simulates the Centrum Air incident where overbooking occurred\n")
    
    # Create system with only 10 seats
    system = UnsafeBookingSystem(total_seats=10)
    
    # Simulate multiple passengers trying to book simultaneously
    passengers = [
        ("Passenger_A", 2),
        ("Passenger_B", 3),
        ("Passenger_C", 2),
        ("Passenger_D", 4),
        ("Passenger_E", 2),
        ("Passenger_F", 3),
    ]
    
    threads = []
    for name, tickets in passengers:
        thread = threading.Thread(target=system.book_ticket, args=(name, tickets))
        threads.append(thread)
        thread.start()
    
    # Wait for all bookings to complete
    for thread in threads:
        thread.join()
    
    # Show final status
    time.sleep(0.5)
    system.get_status()


def run_safe_demo():
    """
    Demonstrate proper synchronization preventing overbooking
    """
    print("\n" + "="*80)
    print("DEMONSTRATION 2: SAFE SYSTEM (With Mutex Protection)")
    print("="*80)
    print("This shows how proper synchronization prevents overbooking\n")
    
    # Create system with only 10 seats
    system = SafeBookingSystem(total_seats=10)
    
    # Same passengers trying to book
    passengers = [
        ("Passenger_A", 2),
        ("Passenger_B", 3),
        ("Passenger_C", 2),
        ("Passenger_D", 4),
        ("Passenger_E", 2),
        ("Passenger_F", 3),
    ]
    
    threads = []
    for name, tickets in passengers:
        thread = threading.Thread(target=system.book_ticket, args=(name, tickets))
        threads.append(thread)
        thread.start()
    
    # Wait for all bookings to complete
    for thread in threads:
        thread.join()
    
    # Show final status
    time.sleep(0.5)
    system.get_status()


def run_semaphore_demo():
    """
    Demonstrate semaphore-based synchronization
    """
    print("\n" + "="*80)
    print("DEMONSTRATION 3: SEMAPHORE SYSTEM")
    print("="*80)
    print("Alternative synchronization using semaphores\n")
    
    system = SemaphoreBookingSystem(total_seats=10)
    
    passengers = [
        ("Passenger_A", 2),
        ("Passenger_B", 3),
        ("Passenger_C", 2),
        ("Passenger_D", 4),
        ("Passenger_E", 2),
        ("Passenger_F", 3),
    ]
    
    threads = []
    for name, tickets in passengers:
        thread = threading.Thread(target=system.book_ticket, args=(name, tickets))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    time.sleep(0.5)
    system.get_status()


if __name__ == "__main__":
    print("\n" + "="*80)
    print("AIRLINE BOOKING SYSTEM - CRITICAL SECTION DEMONSTRATION")
    print("Based on Centrum Air Overbooking Incident (26 September)")
    print("="*80)
    
    # Run all demonstrations
    run_unsafe_demo()
    run_safe_demo()
    run_semaphore_demo()
    
    print("\n" + "="*80)
    print("SUMMARY:")
    print("="*80)
    print("1. UNSAFE system allows race conditions → overbooking")
    print("2. SAFE system uses mutex → prevents overbooking")
    print("3. SEMAPHORE system provides alternative protection")
    print("="*80 + "\n")
