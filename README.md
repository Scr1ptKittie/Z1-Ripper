# Z1 Ripper

Z1 Ripper is a Python script that monitors a specific directory for new avatar folders created by VR Chat. When a new avatar folder is detected, the script copies the folder to a new location, processes the contents, and notifies the user.

## Features

- **Avatar Monitoring**: Monitors a directory for new avatar folders.
- **Avatar Processing**: Copies the avatar folder to a new location and processes the contents.
- **Notification**: Sends a notification when a new avatar is found.
- **Hotkey Toggle**: Allows the user to toggle searching for avatars using the 'q' key.

## Requirements

- Python 3.x
- watchdog
- colorama
- keyboard
- plyer
- pywin32

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install the required Python packages by running the following commands in your terminal:

```bash
