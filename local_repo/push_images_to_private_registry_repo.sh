#!/bin/bash
cd $CONTAINER_IMAGE_DIR
for filename in *.tgz; do
  echo "Loading docker image: $filename" 
  image_loaded=$(sudo docker load -i $filename)
  image_name_with_public_registry=$(echo $image_loaded | grep -oP "(?<=Loaded image: )[^\s]+(?=)")
 
  actual_image_name=$(echo "$image_name_with_public_registry" | awk -F/ '{print $3}' | awk -F: '{print $1}')
  echo "actual_image_name: $actual_image_name" 
  image_name_with_private_regsitry="localhost:5000/$actual_image_name" 
  echo "Docker tag with private_registry name: $image_name_with_private_regsitry" 
  sudo docker tag $image_name_with_public_registry $image_name_with_private_regsitry
  sudo docker push $image_name_with_private_regsitry
  echo " ---- exit ---- " 
done
