import argparse
import multiprocessing as mp
import os
import ffmpeg
from functools import partial
from time import time as timer

from pytube import YouTube
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--input_list', type=str, default='./data_list/small_video_ids.txt',
                    help='List of youtube video ids')
parser.add_argument('--output_dir', type=str, default='data/',
                    help='Location to download videos')
parser.add_argument('--num_workers', type=int, default=2,
                    help='How many multiprocessing workers?')
args = parser.parse_args()

tmp_dir = 'data/tmp'

def download_video(output_dir, video_id):
    r"""Download video."""
    video_path = '%s/%s.mp4' % (output_dir, video_id)
    if not os.path.isfile(video_path):
        try:
            proxy_handler = {
                "http": " http://127.0.0.1:7890",  # 端口在代理设置中查看
                'https': ' http://127.0.0.1:7890'
            }
            # Download the highest quality mp4 stream.
            yt = YouTube('https://www.youtube.com/watch?v=%s' % (video_id), proxies=proxy_handler)

            yt.streams.filter(subtype='mp4', only_video=True).first().download(output_path=tmp_dir, filename=video_id + '.mp4')
            yt.streams.filter(abr="160kbps", only_audio=True).first().download(output_path=tmp_dir, filename=video_id + ".mp3")
            audio = os.path.join(tmp_dir, video_id + ".mp3")
            video = os.path.join(tmp_dir, video_id + ".mp4")
            cmd = 'ffmpeg -y -i %s -i %s -c:v copy -c:a copy %s' % (video, audio, os.path.join(output_dir, video_id + ".mp4"))
            os.system(cmd)

        except Exception as e:
            print(e)
            print('Failed to download %s' % (video_id))
    else:
        print('File exists: %s' % (video_id))


if __name__ == '__main__':
    # Read list of videos.
    video_ids = []
    with open(args.input_list) as fin:
        for line in fin:
            video_ids.append(line.strip())

    # Create output folder.
    os.makedirs(args.output_dir, exist_ok=True)

    # Download videos.
    downloader = partial(download_video, args.output_dir)

    start = timer()
    pool_size = args.num_workers
    print('Using pool size of %d' % (pool_size))
    with mp.Pool(processes=pool_size) as p:
        _ = list(tqdm(p.imap_unordered(downloader, video_ids), total=len(video_ids)))
    print('Elapsed time: %.2f' % (timer() - start))
