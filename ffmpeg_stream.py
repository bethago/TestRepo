from picamera2 import Picamera2, Preview
import subprocess
import signal

# 카메라 설정
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (1280, 720)})
picam2.configure(config)

# FFmpeg 프로세스 시작
ffmpeg_command = [
    'ffmpeg',
    '-f', 'rawvideo',
    '-pix_fmt', 'yuv420p',
    '-s', '1280x720',
    '-r', '30',
    '-i', '-',
    '-f', 'rtsp',
    'rtsp://localhost:8554/unicast'
]
ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

# 카메라에서 데이터를 읽어와 FFmpeg 프로세스에 전달
picam2.start()

try:
    while True:
        frame = picam2.capture_array("main")
        ffmpeg_process.stdin.write(frame.tobytes())
except KeyboardInterrupt:
    pass
finally:
    picam2.stop()
    ffmpeg_process.stdin.close()
    ffmpeg_process.terminate()
