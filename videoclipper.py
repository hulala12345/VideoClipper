#!/usr/bin/env python3
"""VideoClipper application using PyQt5.

Allows loading a video, selecting start and end points,
and saving the trimmed portion to a new file.
"""

import sys
from PyQt5 import QtWidgets, QtCore, QtMultimedia, QtMultimediaWidgets
from moviepy.editor import VideoFileClip


class VideoClipper(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VideoClipper")
        self.player = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)
        self.video_widget = QtMultimediaWidgets.QVideoWidget()
        self.player.setVideoOutput(self.video_widget)

        self.open_button = QtWidgets.QPushButton("Open Video")
        self.play_button = QtWidgets.QPushButton("Play")
        self.pause_button = QtWidgets.QPushButton("Pause")
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.set_start_button = QtWidgets.QPushButton("Set Start")
        self.set_end_button = QtWidgets.QPushButton("Set End")
        self.save_button = QtWidgets.QPushButton("Save Clip")

        self.position_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.position_slider.setRange(0, 0)

        self.start_label = QtWidgets.QLabel("Start: 0")
        self.end_label = QtWidgets.QLabel("End: 0")

        control_layout = QtWidgets.QHBoxLayout()
        for w in [self.open_button, self.play_button, self.pause_button,
                  self.stop_button, self.set_start_button, self.set_end_button,
                  self.save_button]:
            control_layout.addWidget(w)

        info_layout = QtWidgets.QHBoxLayout()
        info_layout.addWidget(self.start_label)
        info_layout.addWidget(self.end_label)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addWidget(self.position_slider)
        layout.addLayout(control_layout)
        layout.addLayout(info_layout)
        self.setLayout(layout)

        self.start_pos = None
        self.end_pos = None

        self.open_button.clicked.connect(self.open_file)
        self.play_button.clicked.connect(self.player.play)
        self.pause_button.clicked.connect(self.player.pause)
        self.stop_button.clicked.connect(self.player.stop)
        self.set_start_button.clicked.connect(self.set_start)
        self.set_end_button.clicked.connect(self.set_end)
        self.save_button.clicked.connect(self.save_clip)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)

    def open_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Video", "", "Video Files (*.mp4 *.avi *.mov)")
        if path:
            url = QtCore.QUrl.fromLocalFile(path)
            self.player.setMedia(QtMultimedia.QMediaContent(url))
            self.player.play()
            self.start_pos = None
            self.end_pos = None
            self.start_label.setText("Start: 0")
            self.end_label.setText("End: 0")

    def set_start(self):
        self.start_pos = self.player.position()
        self.start_label.setText(f"Start: {self.start_pos/1000:.2f}s")

    def set_end(self):
        self.end_pos = self.player.position()
        self.end_label.setText(f"End: {self.end_pos/1000:.2f}s")

    def save_clip(self):
        if self.start_pos is None or self.end_pos is None:
            QtWidgets.QMessageBox.warning(self, "Error", "Please set start and end points")
            return
        if self.end_pos <= self.start_pos:
            QtWidgets.QMessageBox.warning(self, "Error", "End must be after start")
            return
        out_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Clip", "", "MP4 Video (*.mp4)")
        if not out_path:
            return

        in_path = self.player.media().canonicalUrl().toLocalFile()
        start_sec = self.start_pos / 1000
        end_sec = self.end_pos / 1000

        progress = QtWidgets.QProgressDialog("Trimming...", None, 0, 0, self)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.show()
        QtWidgets.qApp.processEvents()
        try:
            clip = VideoFileClip(in_path)
            subclip = clip.subclip(start_sec, end_sec)
            subclip.write_videofile(out_path, codec="libx264", audio_codec="aac")
            clip.close()
            subclip.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))
        finally:
            progress.close()

    def update_position(self, position):
        self.position_slider.setValue(position)

    def update_duration(self, duration):
        self.position_slider.setRange(0, duration)

    def set_position(self, position):
        self.player.setPosition(position)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = VideoClipper()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
