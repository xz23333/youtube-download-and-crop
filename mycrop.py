import pickle, os, subprocess


id = '-7TMJtnhiPM'
video = ' D:\\0xz\\code\\TalkingHead-1KH\\data\\-7TMJtnhiPM.mp4'

file = pickle.load(open('./output/pywork/' + id + '/tracks.pckl', 'rb'))
count = 1
os.makedirs('output/myout/' + id)
print(len(file))

for f in file:
    frames = f['track']['frame']
    start = (frames[0]) / 25
    end = (frames[-1] + 1) / 25
    print(end-start, 'sec')
    output = 'output/myout/' + id + '/' + str(count).zfill(3) + '.mp4'
    command = ("ffmpeg -y -i %s -ss %.3f -to %.3f %s" % (video, start, end, output))
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