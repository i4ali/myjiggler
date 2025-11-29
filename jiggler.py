#!/usr/bin/env python3
"""
Mac Mouse Jiggler - Prevents your Mac from going to sleep
A simple command-line tool to keep your computer awake by moving the mouse periodically.
"""

import sys
import time
import argparse
import signal
from datetime import datetime, timedelta
from Quartz.CoreGraphics import (
    CGEventCreateMouseEvent,
    CGEventPost,
    kCGEventMouseMoved,
    kCGHIDEventTap,
    CGEventGetLocation
)


class MouseJiggler:
    """Mouse jiggler that uses native macOS Core Graphics API"""

    def __init__(self, interval=60, distance=1, duration=None, pattern='gentle', verbose=True):
        """
        Initialize the mouse jiggler

        Args:
            interval: Seconds between each jiggle (default: 60)
            distance: Pixels to move (default: 1)
            duration: Total duration in minutes (None for infinite)
            pattern: Movement pattern ('gentle', 'circular', 'random')
            verbose: Print status messages
        """
        self.interval = interval
        self.distance = distance
        self.duration = duration
        self.pattern = pattern
        self.verbose = verbose
        self.running = False
        self.jiggle_count = 0
        self.start_time = None

    def get_mouse_position(self):
        """Get current mouse position"""
        from Quartz import CGEventCreate, kCGEventMouseMoved
        event = CGEventCreate(None)
        point = CGEventGetLocation(event)
        return int(point.x), int(point.y)

    def move_mouse(self, x, y):
        """Move mouse to absolute position"""
        event = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (x, y), 0)
        CGEventPost(kCGHIDEventTap, event)

    def jiggle_gentle(self):
        """Gentle jiggle - move right then back left"""
        x, y = self.get_mouse_position()

        # Move right
        self.move_mouse(x + self.distance, y)
        time.sleep(0.05)

        # Move back left
        self.move_mouse(x - self.distance, y)

    def jiggle_circular(self):
        """Circular jiggle pattern"""
        x, y = self.get_mouse_position()
        steps = 8
        radius = self.distance

        for i in range(steps):
            angle = (i / steps) * 2 * 3.14159
            import math
            new_x = x + int(radius * math.cos(angle))
            new_y = y + int(radius * math.sin(angle))
            self.move_mouse(new_x, new_y)
            time.sleep(0.02)

        # Return to original position
        self.move_mouse(x, y)

    def jiggle_random(self):
        """Random small movements"""
        import random
        x, y = self.get_mouse_position()

        # Random movement within distance range
        dx = random.randint(-self.distance, self.distance)
        dy = random.randint(-self.distance, self.distance)

        self.move_mouse(x + dx, y + dy)
        time.sleep(0.05)
        self.move_mouse(x, y)

    def jiggle(self):
        """Execute a jiggle based on selected pattern"""
        if self.pattern == 'gentle':
            self.jiggle_gentle()
        elif self.pattern == 'circular':
            self.jiggle_circular()
        elif self.pattern == 'random':
            self.jiggle_random()
        else:
            self.jiggle_gentle()

        self.jiggle_count += 1

    def print_status(self, message):
        """Print status message if verbose mode is on"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")

    def should_stop(self):
        """Check if duration has been reached"""
        if self.duration is None:
            return False

        elapsed = (datetime.now() - self.start_time).total_seconds() / 60
        return elapsed >= self.duration

    def start(self):
        """Start the jiggler"""
        self.running = True
        self.start_time = datetime.now()

        self.print_status("🖱️  Mouse Jiggler started")
        self.print_status(f"   Interval: {self.interval}s | Distance: {self.distance}px | Pattern: {self.pattern}")

        if self.duration:
            end_time = self.start_time + timedelta(minutes=self.duration)
            self.print_status(f"   Running until: {end_time.strftime('%H:%M:%S')} ({self.duration} minutes)")
        else:
            self.print_status("   Running indefinitely (Press Ctrl+C to stop)")

        print()

        try:
            while self.running and not self.should_stop():
                self.jiggle()

                if self.verbose:
                    next_jiggle = datetime.now() + timedelta(seconds=self.interval)
                    self.print_status(f"Jiggle #{self.jiggle_count} completed. Next jiggle at {next_jiggle.strftime('%H:%M:%S')}")

                time.sleep(self.interval)

            if self.should_stop():
                self.print_status(f"✓ Duration reached. Completed {self.jiggle_count} jiggles.")

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the jiggler"""
        self.running = False
        print()
        self.print_status(f"✓ Mouse Jiggler stopped. Completed {self.jiggle_count} jiggles.")
        elapsed = (datetime.now() - self.start_time).total_seconds()
        self.print_status(f"   Total runtime: {elapsed:.1f} seconds")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Mac Mouse Jiggler - Keep your computer awake by moving the mouse',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Run with defaults (60s interval, gentle pattern)
  %(prog)s -i 30                    # Jiggle every 30 seconds
  %(prog)s -i 120 -d 5              # Jiggle every 2 minutes, move 5 pixels
  %(prog)s -i 60 -t 30              # Run for 30 minutes then stop
  %(prog)s -p circular -i 45        # Use circular pattern every 45 seconds
  %(prog)s -p random -i 90 -q       # Random pattern, quiet mode
        """
    )

    parser.add_argument(
        '-i', '--interval',
        type=int,
        default=60,
        metavar='SECONDS',
        help='seconds between each jiggle (default: 60)'
    )

    parser.add_argument(
        '-d', '--distance',
        type=int,
        default=1,
        metavar='PIXELS',
        help='pixels to move the mouse (default: 1)'
    )

    parser.add_argument(
        '-t', '--time',
        type=int,
        default=None,
        metavar='MINUTES',
        help='total duration in minutes (default: run indefinitely)'
    )

    parser.add_argument(
        '-p', '--pattern',
        choices=['gentle', 'circular', 'random'],
        default='gentle',
        help='movement pattern (default: gentle)'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='quiet mode - suppress status messages'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Validate arguments
    if args.interval < 1:
        print("Error: Interval must be at least 1 second", file=sys.stderr)
        sys.exit(1)

    if args.distance < 1:
        print("Error: Distance must be at least 1 pixel", file=sys.stderr)
        sys.exit(1)

    if args.time is not None and args.time < 1:
        print("Error: Duration must be at least 1 minute", file=sys.stderr)
        sys.exit(1)

    # Create and start jiggler
    jiggler = MouseJiggler(
        interval=args.interval,
        distance=args.distance,
        duration=args.time,
        pattern=args.pattern,
        verbose=not args.quiet
    )

    # Set up signal handler for graceful shutdown
    def signal_handler(sig, frame):
        jiggler.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start jiggling
    jiggler.start()


if __name__ == '__main__':
    main()
