# MiddleFingerprint

## Installation

Install docker and docker-compose

## Run
```shell
docker build -t firefox -f Dockerfile.ubuntu.firefox
docker run --net=host -e DISPLAY=$DISPLAY firefox

```

## Centos - Firefox
- [x] Work

FROM centos:7
RUN yum install -y firefox
RUN yum install -y libcanberra-gtk2
RUN yum install -y PackageKit-gtk3-module
CMD ["/usr/bin/firefox"]


## Misc
wget -qO- https://get.docker.com/ | sudo sh
dockerd-rootless-setuptool.sh install
docker
sudo usermod -aG docker $USER
x11docker 
curl -fsSL https://raw.githubusercontent.com/mviereck/x11docker/master/x11docker | sudo bash -s -- --update
x11docker
docker pull jess/tor-browser
docker image
x11docker --help
x11docker -I jess/tor-browser
docker image --help
docker image rm b197fdef08f0
docker pull jess/firefox
docker build -t Firefox -f Dockerfile.ubuntu.firefox
docker build -t firefox -f Dockerfile.ubuntu.firefox
docker run --net=host -e DISPLAY=:0 firefox
docker image rm firefox
docker run --rm -ti --net=host -e DISPLAY=:0 firefox
docker image rm 619d84389381
docker image ls -a
docker container ls
docker container ls all
docker container rm 7e59a52a04c3
docker container rm b204212a0b94
docker container ls a
docker container ls -a
docker image rm c838820dc6d7
docker image rm 85e28d16232b
docker image ls
docker build -t firefox -f Dockerfile.ubuntu.firefox .

