#!/bin/sh
function convert_all_to_mp4() {
  for file in ~/Downloads/ichnaea/*.flv ; do
    local bname=$(basename "$file" .flv)
    local mp4name="$bname.mp4"
    avconv -i "$file" -codec copy "$mp4name"
    # only s3 the file not the entire path
    # aws s3 cp "$mp4name" s3://cf-simple-s3-origin-cloudfrontfors3-778103269065/
    # rm "$file"
    # rm "$mp4name"
  done
}

while true
do
  find ~/Downloads -name "*.flv" -exec mv -i {} -t ~/Downloads/ichnaea \;
  mv ~/Downloads/ichnaea/1.flv ~/Downloads/ichnaea/$(date +"%FT%H%M").flv  
  convert_all_to_mp4  
  echo "done"
  sleep 15
done