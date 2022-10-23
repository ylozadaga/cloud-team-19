# cloud-team-19

## Correr Contenedor en Docker

Construir la imagen ejecutando en la raiz del repositorio el comando:
```
docker build . -t cloud-team-19:v1
```

Correr el contenedor ejecutando el comando:
```
docker run --memory="1g" --cpus="1" --name converter-app -p 8080:8080 cloud-team-19:v1
```

## Comprobar Funcionamiento

Ejecutar el CURL ping, el cual deberia responder "pong"
```
curl --location --request GET 'localhost:8080/ping'
```