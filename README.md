# cloud-team-19

docker build . -t cloud-team-19:v1


docker run --memory="1g" --cpus="1" --name converter-app -p 8080:8080 cloud-team-19:v1