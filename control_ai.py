"""
Control AI Module - PC System Control Hub
Integrates voice/text commands to control PC operations like opening apps,
managing system settings, and running OS commands.
"""

import os
import sys
import subprocess
import platform


# ─── Application & System Commands ────────────────────────────
APP_COMMANDS = {
    "chrome": "start chrome",
    "firefox": "start firefox",
    "edge": "start msedge",
    "notepad": "start notepad",
    "calculator": "start calc",
    "paint": "start mspaint",
    "file explorer": "start explorer",
    "explorer": "start explorer",
    "command prompt": "start cmd",
    "cmd": "start cmd",
    "powershell": "start powershell",
    "task manager": "start taskmgr",
    "settings": "start ms-settings:",
    "control panel": "start control",
    "vscode": "start code",
    "word": "start winword",
    "excel": "start excel",
    "powerpoint": "start powerpnt",
    "spotify": "start spotify:",
    "snipping tool": "start snippingtool",
}

SYSTEM_COMMANDS = {
    "shutdown": ("shutdown /s /t 60", "System will shut down in 60 seconds"),
    "restart": ("shutdown /r /t 60", "System will restart in 60 seconds"),
    "cancel shutdown": ("shutdown /a", "Shutdown cancelled"),
    "lock": ("rundll32.exe user32.dll,LockWorkStation", "Screen locked"),
    "sleep": ("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", "Going to sleep"),
    "logoff": ("shutdown /l", "Logging off"),
    "volume up": ("nircmd.exe changesysvolume 5000", "Volume increased"),
    "volume down": ("nircmd.exe changesysvolume -5000", "Volume decreased"),
    "mute": ("nircmd.exe mutesysvolume 2", "Volume toggled mute"),
}


def open_app(app_name):
    """Open an application by name."""
    app_key = app_name.lower().strip()
    if app_key in APP_COMMANDS:
        cmd = APP_COMMANDS[app_key]
        os.system(cmd)
        print(f"[✓] Opened: {app_name}")
        return True
    else:
        print(f"[?] Unknown app: '{app_name}'")
        print(f"    Available: {', '.join(sorted(APP_COMMANDS.keys()))}")
        return False


def run_system_command(command_name):
    """Execute a system command by name."""
    cmd_key = command_name.lower().strip()
    if cmd_key in SYSTEM_COMMANDS:
        cmd, message = SYSTEM_COMMANDS[cmd_key]
        os.system(cmd)
        print(f"[✓] {message}")
        return True
    else:
        print(f"[?] Unknown system command: '{command_name}'")
        return False


def open_website(url):
    """Open a website in the default browser."""
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    os.system(f'start "" "{url}"')
    print(f"[✓] Opened: {url}")


def open_file(filepath):
    """Open a file with its default application."""
    if os.path.exists(filepath):
        os.startfile(filepath)
        print(f"[✓] Opened file: {filepath}")
        return True
    else:
        print(f"[✗] File not found: {filepath}")
        return False


def system_info():
    """Display system information."""
    print(f"\n  💻 System Information:")
    print(f"    OS:        {platform.system()} {platform.release()}")
    print(f"    Version:   {platform.version()}")
    print(f"    Machine:   {platform.machine()}")
    print(f"    Processor: {platform.processor()}")
    print(f"    Node:      {platform.node()}")
    print(f"    Python:    {sys.version.split()[0]}")


def parse_command(text):
    """Parse and execute a text command."""
    cmd = text.lower().strip()

    if cmd.startswith("open "):
        target = cmd[5:].strip()
        # Check if it's a known app
        if target in APP_COMMANDS:
            open_app(target)
        # Check if it's a website
        elif "." in target and " " not in target:
            open_website(target)
        # Check if it's a file path
        elif os.path.exists(text[5:].strip()):
            open_file(text[5:].strip())
        else:
            open_app(target)

    elif cmd.startswith("run "):
        shell_cmd = text[4:].strip()
        print(f"[▶] Running: {shell_cmd}")
        result = subprocess.run(shell_cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"[!] {result.stderr}")

    elif cmd in SYSTEM_COMMANDS:
        run_system_command(cmd)

    elif cmd in ("info", "system info", "sysinfo"):
        system_info()

    elif cmd == "apps":
        print(f"\n  Available apps:")
        for app in sorted(APP_COMMANDS.keys()):
            print(f"    • {app}")

    elif cmd == "help":
        _print_help()

    else:
        # Try as app name
        if cmd in APP_COMMANDS:
            open_app(cmd)
        else:
            print(f"[?] Unknown command: \"{text}\"")
            print("    Type 'help' for available commands.")


def _print_help():
    print("""
  📋 Available Commands:
  ─────────────────────────────────────────
  open <app>         Open an application
  open <url>         Open a website
  open <path>        Open a file
  run <command>      Run a shell command

  shutdown           Shutdown in 60s
  restart            Restart in 60s
  cancel shutdown    Cancel shutdown
  lock               Lock screen
  sleep              Sleep mode
  logoff             Log off

  info               System information
  apps               List available apps
  help               Show this help
  exit               Quit
  ─────────────────────────────────────────""")


def run_control():
    """Interactive PC control prompt."""
    print("=" * 55)
    print("  🎮 PC Control AI — System Control Hub")
    print("=" * 55)
    print(f"  OS: {platform.system()} {platform.release()}")
    print("  Type 'help' for commands, 'exit' to quit")
    print("=" * 55)

    while True:
        try:
            cmd = input("\n🎮 Control > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 PC Control stopped.")
            return

        if cmd.lower() in ("exit", "quit", "stop"):
            print("👋 PC Control stopped.")
            return

        if cmd:
            parse_command(cmd)


if __name__ == "__main__":
    run_control()