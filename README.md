import subprocess
import time
import argparse
import platform
from datetime import datetime, timedelta

def keep_teams_active_windows():
    """Windows implementation using keyboard input"""
    # Press Scroll Lock key twice (this typically doesn't affect anything visible)
    subprocess.run(["python", "-c", "import ctypes; ctypes.windll.user32.keybd_event(0x91, 0, 0, 0); ctypes.windll.user32.keybd_event(0x91, 0, 2, 0)"])
    return True

def keep_teams_active_mac():
    """Mac implementation using AppleScript"""
    # Using AppleScript to simulate a tiny mouse movement
    script = '''
    tell application "System Events"
        -- Get current mouse position
        set currentPosition to mouse location
        set xPosition to item 1 of currentPosition
        set yPosition to item 2 of currentPosition
        
        -- Move mouse slightly
        set mouse location to {xPosition + 1, yPosition + 1}
        delay 0.1
        
        -- Move mouse back to original position
        set mouse location to currentPosition
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", script], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Error executing AppleScript. Make sure you have the necessary permissions.")
        return False

def keep_teams_active_linux():
    """Linux implementation using xdotool"""
    try:
        # Check if xdotool is installed
        subprocess.run(["which", "xdotool"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Get current mouse position
        position = subprocess.check_output(["xdotool", "getmouselocation"]).decode()
        x = int(position.split()[0].split(':')[1])
        y = int(position.split()[1].split(':')[1])
        
        # Move mouse slightly and back
        subprocess.run(["xdotool", "mousemove", str(x+1), str(y+1)])
        time.sleep(0.1)
        subprocess.run(["xdotool", "mousemove", str(x), str(y)])
        return True
    except subprocess.CalledProcessError:
        print("Error: xdotool not found. Install it with 'sudo apt-get install xdotool' on Debian/Ubuntu.")
        return False
    except Exception as e:
        print(f"Error with Linux implementation: {e}")
        return False

def keep_teams_active(interval_minutes=2, duration_hours=1):
    """
    Keeps Teams active by simulating minimal input periodically.
    
    Args:
        interval_minutes: Time between actions in minutes
        duration_hours: How long to run the script in hours (0 for indefinite)
    """
    print(f"Starting Teams Status Keeper")
    print(f"- Performing action every {interval_minutes} minutes")
    
    if duration_hours > 0:
        end_time = datetime.now() + timedelta(hours=duration_hours)
        print(f"- Will stop after {duration_hours} hours (at {end_time.strftime('%H:%M:%S')})")
    else:
        print("- Running indefinitely (press Ctrl+C to stop)")
    
    # Detect operating system
    system = platform.system()
    print(f"- Detected operating system: {system}")
    
    print("\nAction log:")
    
    try:
        count = 0
        while True:
            success = False
            
            # Execute the appropriate function based on the operating system
            if system == "Windows":
                success = keep_teams_active_windows()
            elif system == "Darwin":  # macOS
                success = keep_teams_active_mac()
            elif system == "Linux":
                success = keep_teams_active_linux()
            else:
                print(f"Unsupported operating system: {system}")
                break
            
            if success:
                count += 1
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"[{current_time}] Action #{count} complete")
            else:
                print("Failed to perform action. Trying again in 5 seconds...")
                time.sleep(5)
                continue
            
            # Check if we've reached the time limit
            if duration_hours > 0:
                if datetime.now() >= end_time:
                    print("\nTime limit reached. Stopping.")
                    break
                
            # Wait for the specified interval
            time.sleep(interval_minutes * 60)
            
    except KeyboardInterrupt:
        print("\nScript stopped by user.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keep Microsoft Teams status active on Windows, macOS, or Linux.")
    parser.add_argument("-i", "--interval", type=float, default=2, help="Time between actions in minutes (default: 2)")
    parser.add_argument("-d", "--duration", type=float, default=1, help="How long to run the script in hours (0 for indefinite, default: 1)")
    
    args = parser.parse_args()
    
    keep_teams_active(interval_minutes=args.interval, duration_hours=args.duration)
