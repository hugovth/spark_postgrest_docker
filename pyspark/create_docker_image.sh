
CONTAINER_URL="hugovth"
IMAGE_NAME=postrest
DEFAULT_TAG="latest"

#if [ $1 -ne "" ]; then
#    TAG=$DEFAULT_TAG
#else
#    TAG=$1
#fi

TAG=$DEFAULT_TAG

docker build -t $CONTAINER_URL/$IMAGE_NAME:$TAG .
docker push $CONTAINER_URL/$IMAGE_NAME:$TAG 

