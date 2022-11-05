# cloud-team-19

## Correr Contenedor de la base de datos en Docker

Construir la imagen ejecutando en la raiz del repositorio 'database' el comando:
```
docker build . -t database-convertion-tool:v1
```

Correr el contenedor ejecutando el comando:
```
docker run --name database-convertion-tool -e POSTGRES_USER=root -e POSTGRES_PASSWORD=admin123 -e POSTGRES_DB=convertion-tool -p 5432:5432 -d database-convertion-tool:v1
```

## Correr Contenedor de la app en Docker

Construir la imagen ejecutando en la raiz del repositorio 'convertion-tool' el comando:
```
docker build . -t convertion-tool:v1
```

Correr el contenedor ejecutando el comando:
```
docker run --memory="1g" --cpus="1" --name convertion-tool -p 8080:8080 convertion-tool:v1
```

## Correr Contenedor del proceso batch en Docker

Construir la imagen ejecutando en la raiz del repositorio 'batch_process' el comando:
```
docker build . -t batch-convertion-tool:v1
```

Correr el contenedor ejecutando el comando:
```
docker run --memory="1g" --cpus="1" --name batch-convertion-tool -p 8081:8081 batch-convertion-tool:v1
```

## Comprobar Funcionamiento

Ejecutar el CURL ping, el cual deberia responder "pong"
```
curl --location --request GET 'localhost:8080/ping'
```