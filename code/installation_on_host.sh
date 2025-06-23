sudo apt update
sudo apt install docker -y
sudo apt install docker.io -y # version 26.1.3-0ubuntu1~20.04.1

sudo usermod -aG docker $USER
newgrp docker
docker build -t my-image-name .

# Install dataset: VisDrone2019-SOT-train
# https://github.com/VisDrone/VisDrone-Dataset
# Links: "Task 3: Single-Object Tracking" - trainset_part1 & trainset_part2

docker run -it -v $HOME/DroTrack/results:/code/results my-image-name
