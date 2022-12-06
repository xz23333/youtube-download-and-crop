datapath='./data'

files=$(ls $datapath)

echo $files

for video in $files
do
  echo Start processing $video =====
  python run_pipeline.py --videofile $datapath/$video --reference $video[:-4]
  python
done
