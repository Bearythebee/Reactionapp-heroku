from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os

def convert_timestring_to_seconds(tup):
    start, end = tup[0], tup[1]
    start_min, start_sec = start.split(':')
    end_min, end_sec = end.split(':')
    start_time = 60 * (int(start_min)) + int(start_sec)
    end_time = 60 * (int(end_min)) + int(end_sec)
    return start_time, end_time

def trim_video(video_, timings):
    os.mkdir('tmp/')
    # write bytes to video
    f = open('tmp/tmpfile.mp4', 'wb')
    f.write(video_)
    f.close()

    video_ranges = timings.split(';')
    video_timings = []
    subvideos = []

    for subvideo in video_ranges:
        pd_start, pd_end = subvideo.split('-')
        video_timings.append([pd_start, pd_end])

    count = 1
    for times in video_timings:
        start_time, end_time = convert_timestring_to_seconds(times)
        ffmpeg_extract_subclip('tmp/tmpfile.mp4',
                               start_time,
                               end_time,targetname='tmp/tmp_{}.mp4'.format(count))

        count+=1

    return subvideos
