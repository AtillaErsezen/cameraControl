# Hand Gesture Mouse Controller

This is a Python application that allows you to control your mouse cursor and perform clicks or scroll actions through hand gestures. It uses [OpenCV](https://opencv.org/), [MediaPipe](https://google.github.io/mediapipe/), and [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) to capture and interpret hand gestures through a webcam.

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Gesture Mapping](#gesture-mapping)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features
- **Real-time hand gesture recognition** using MediaPipe's Hand Tracking solution.
- **Mouse movement** controlled by the position of your index finger.
- **Configurable gestures** to trigger actions like:
  - Left click
  - Right click
  - Double click
  - Scroll up
  - Scroll down

## Demo
While running the program, a window will show your webcam feed and you can:
- Move your index finger to control the mouse pointer.
- Perform gestures (fist, peace sign, thumbs up/down, etc.) to trigger predefined actions.

## How It Works
1. The webcam feed is captured using OpenCV.
2. MediaPipe processes the frames to detect hand landmarks.
3. Each detected hand landmark is analyzed to classify a gesture (for example, "fist" or "peace").
4. Depending on the recognized gesture, PyAutoGUI is used to control the mouse actions on your screen.
5. The index finger coordinates are mapped to your screen size for cursor movement.

## Requirements
Before you begin, ensure you have the following installed:
- **Python 3.7+**
- **pip** (Python package manager)

You also need the following packages:
- [OpenCV](https://pypi.org/project/opencv-python/) (`opencv-python`)
- [MediaPipe](https://pypi.org/project/mediapipe/)
- [PyAutoGUI](https://pypi.org/project/PyAutoGUI/)
- [Pillow](https://pypi.org/project/Pillow/) (needed for the image preview in Tkinter)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (usually included with most Python distributions)
- [threading](https://docs.python.org/3/library/threading.html) (comes with standard Python)
- [queue](https://docs.python.org/3/library/queue.html) (comes with standard Python)

**Important**: PyAutoGUI might require additional system-specific dependencies to handle mouse events. Refer to the [PyAutoGUI documentation](https://pyautogui.readthedocs.io/en/latest/install.html) if you encounter issues.

## Installation
1. **Clone or download** this repository.
2. Open a terminal (or command prompt) in the directory containing the files.
3. Install all required dependencies:
   ```bash
   pip install -r requirements.txt
