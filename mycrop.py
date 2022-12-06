import argparse
import pickle, os, subprocess

parser = argparse.ArgumentParser(description="CropVideo");
parser.add_argument('--data_dir', type=str, default='./output', help='Output direcotry');
parser.add_argument('--videofile', type=str, default='', help='Input video file');
parser.add_argument('--reference', type=str, default='test001', help='Video reference');
opt = parser.parse_args();

# opt.reference = 'c1DRo3tPDG4'
# opt.videofile = 'D:\\0xz\\code\\TalkingHead-1KH\\data\\c1DRo3tPDG4.mp4'

file = pickle.load(open('./output/pywork/' + opt.reference + '/tracks.pckl', 'rb'))
count = 1
os.makedirs('output/myout/' + opt.reference)
print(len(file))

for f in file:
    frames = f['track']['frame']
    start = (frames[0]) / 25
    end = (frames[-1] + 1) / 25
    print(end-start, 'sec')
    output = 'output/myout/' + opt.reference + '/' + str(count).zfill(3) + '.mp4'
    command = ("ffmpeg -y -i %s -ss %.3f -to %.3f %s" % (opt.videofile, start, end, output))
    output = subprocess.call(command, shell=True, stdout=None)
    count += 1

# filelist = "output/myout/" + id + "/filelist.txt"
# writer = open(filelist, 'w')
# files = os.listdir('output/myout/' + id)
# for f in files:
#     if f.endswith('.txt'):
#         continue
#     writer.writelines('file \'' + f + '\'\n')
#     writer.flush()
# writer.close()
#
# cutvideo = "output/myout/cut.mp4"
# command = ('ffmpeg -f concat -i %s -c copy %s' % (filelist, cutvideo))
# output = subprocess.call(command, shell=True, stdout=None)