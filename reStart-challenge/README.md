# AWS re/Start project

## Connection
   1. En la consola primero ingrese sus credenciales para AWS:  
  aws configure o vi ~/.aws/credentials
  
   2. Prueba la conexion con:  
        aws sts get-caller-identity
    
### Prepara las variables de entorno en Bash
    export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id) |
    export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key) |
    export AWS_REGION=$(aws configure get region)

## Part 1
1. Automatizador de subida de archivos a Amazon S3
Objetivo
Crear un script en Python que suba automáticamente archivos locales a un bucket.
Servicios involucrados
Amazon S3
boto3
Funcionalidad del proyecto
El script debe:
Subir un archivo
Listar archivos en el bucket
Descargar un archivo

2. Sistema automático de backups a S3
Objetivo
Crear un script que haga backup automático de una carpeta local hacia S3.
Servicios involucrados
Amazon S3
Funcionalidad
El programa debe:
Escanear una carpeta
Subir todos los archivos
Crear una carpeta con fecha
Ejemplo de estructura en S3:


3. Monitor de instancias EC2
Objetivo
Crear un script que liste y monitoree instancias EC2.
Servicios involucrados
Amazon EC2
Funcionalidad
El script debe mostrar:
Instance ID
Estado
Tipo de instancia
IP pública


4. Script para limpiar buckets S3 automáticamente
Objetivo
Crear un programa que detecte y elimine archivos antiguos.
Servicios
Amazon S3
Funcionalidad
El script debe:
listar objetos
detectar archivos > 30 días
eliminarlos

5. Sistema simple de alertas con CloudWatch
Objetivo
Crear métricas personalizadas desde Python.
Servicios
Amazon CloudWatch

6. Generador automático de usuarios IAM
Objetivo
Crear un script que cree usuarios IAM automáticamente.
Servicios
AWS Identity and Access Management
Funcionalidad
El script debe:
crear usuarios
asignar políticas
generar access keys

7. Inventario de recursos AWS
Objetivo
Crear un script que escanee tu cuenta AWS y genere un inventario.
Servicios
Amazon EC2
Amazon S3
AWS Lambda
Salida del programa
El script genera un archivo:
aws_inventory.json

## Part 2
8. Pipeline simple S3 → procesamiento
Servicios:
S3
Python
Flujo:
subir archivo
leer contenido
procesarlo (ej: contar líneas)
guardar resultado en otro bucket

9. Snapshot automático de volúmenes
Servicio: EC2 + EBS
Objetivo:
listar volúmenes
crear snapshot

10. Generador de reportes en S3
Objetivo:
combinar:
EC2 + S3
guardar reporte en JSON


