#!/bin/bash

docker run --name beer -e SERVIDOR_REDSHIFT="data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com" \
-e DB_REDSHIFT="data-engineer-database" \
-e PUERTO_REDSHIFT=5439 \
-e USUARIO_REDSHIFT="usuario" \
-e CLAVE_REDSHIFT="contraseña" \
-it beer