# VideoClipper

VideoClipper is a simple GUI application for trimming sections from video files.
It supports common formats like MP4, AVI and MOV using PyQt5 for the user
interface and MoviePy/FFmpeg for processing.

## Requirements

- Python 3
- PyQt5
- moviepy (requires FFmpeg installed)

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run the application with:

```bash
python3 videoclipper.py
```

Use **Open Video** to load a video file. Use **Set Start** and **Set End** while
playing to mark the desired section. Click **Save Clip** to choose an output
filename and trim the selected portion.

