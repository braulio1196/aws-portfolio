import boto3
import os 
from botocore.exceptions import NoCredentialsError, ClientError

def connect_s3():
    # Create a cleint to connect to S3
    return boto3.client(
        's3'
        , aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        , aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        , region_name = os.getenv('AWS_REGION')
    )

def upload_file(s3_name: str = None):
    print("\n--- 1.- Subir Archivo -------------")
#First select file 
    local_path = input("Nombre del Archivo: ").strip()
    local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), local_path) 
    if not os.path.exists(local_path):
        print(f"[ERROR] El Archivo '{local_path}' no existe.")
        return

    s3 = connect_s3()

#Listamos los Buckets
    try:
        response = s3.list_buckets()
        buckets  = [b['Name'] for b in response.get('Buckets', [])]
 
        if buckets:
            print("\n  Buckets Disponibles:")
            for i, name in enumerate(buckets, 1):
                print(f"    {i}. {name}")
        else:
            print("\n  [INFO] Sin Buckets.")
    except (NoCredentialsError, ClientError) as e:
        print(f"[ERROR] Could not retrieve buckets: {e}")
        return
    
    bucket     = input("Nombre del Bucket (existente o nuevo para crear): ").strip()
    
#Creamos Bucket si no existe  
    if bucket not in buckets:
        confirm = input(f"  Bucket '{bucket}' no existe. Quiere crearlo? (y/n): ").strip().lower()
        if confirm == 'y':
            try:
                region = os.getenv('AWS_REGION', 'us-east-1')
                if region == 'us-east-1':
                    s3.create_bucket(Bucket=bucket)
                else:
                    s3.create_bucket(
                        Bucket=bucket,
                        CreateBucketConfiguration={'LocationConstraint': region}
                    )
                print(f"[OK] Bucket '{bucket}' created successfully.")
            except ClientError as e:
                print(f"[ERROR] Could not create bucket: {e}")
                return
        else:
            print("Upload cancelled.")
            return    

    #s3_name    = input("Nombre del Archivo en S3 (en blanco para default): ").strip()
    s3_name    = s3_name or os.path.basename(local_path)

 
    try:
        s3.upload_file(local_path, bucket, s3_name)
        print(f"[OK] '{local_path}' uploaded to s3://{bucket}/{s3_name}")
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
    except ClientError as e:
        print(f"[ERROR] {e}")    

       
def list_files():
    print("\n--- 2.- Listar Objetos ------------")

    s3 = connect_s3()
#Listamos los Buckets
    try:
        response = s3.list_buckets()
        buckets  = [b['Name'] for b in response.get('Buckets', [])]
 
        if buckets:
            print("\n  Buckets Disponibles:")
            for i, name in enumerate(buckets, 1):
                print(f"    {i}. {name}")
        else:
            print("\n  [INFO] Sin Buckets.")
    except (NoCredentialsError, ClientError) as e:
        print(f"[ERROR] Could not retrieve buckets: {e}")
        return
    
#Escribimos el Bucket a listar
    bucket = input("Nombre del Bucket: ").strip()
    #prefix = input("Si quieres filtrar por carpeta (en blanco para todos): ").strip()
    prefix = ''
 
    try:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        contents = response.get('Contents', [])
 
        if not contents:
            print(f"[INFO] No hay archivos en '{bucket}'.")
            return
 
        print(f"\nArchivos en s3://{bucket}/{prefix}")
        print("-" * 50)
        for obj in contents:
            name = obj['Key']
            size = obj['Size']
            date = obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S')
            print(f"  {name:<40} {size:>10} bytes  {date}")
        print("-" * 50)
        print(f"Total: {len(contents)} archivo(s)\n")
 
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
    except ClientError as e:
        print(f"[ERROR] {e}")   
  
    
def download_file():
    print("\n--- 3.- Descargar Archivo ---------")


    s3 = connect_s3()
#Listamos los Buckets
    try:
        response = s3.list_buckets()
        buckets  = [b['Name'] for b in response.get('Buckets', [])]
 
        if buckets:
            print("\n  Buckets Disponibles:")
            for i, name in enumerate(buckets, 1):
                print(f"    {i}. {name}")
        else:
            print("\n  [INFO] Sin Buckets.")
    except (NoCredentialsError, ClientError) as e:
        print(f"[ERROR] Could not retrieve buckets: {e}")
        return

#escribimos los datos para descargar el archivo
    bucket          = input("Nombre del Bucket ").strip()
    s3_name         = input("Archivo a Descargar: ").strip()
    destination     = input("Ruta del archivo (o en blanco para usar la default): ").strip()
    destination     = destination or os.path.basename(s3_name)
 
    try:
        s3.download_file(bucket, s3_name, destination)
        print(f"[OK] 's3://{bucket}/{s3_name}' downloaded to '{destination}'")
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"[ERROR] File '{s3_name}' does not exist in the bucket.")
        else:
            print(f"[ERROR] {e}")   
    
def show_menu():
    print("-----S3 File Manager-----")
    print(" 1. Subir Archivo")
    print(" 2. Listar objetos del Bucket")
    print(" 3. Descargar archivo")
    print(" 4. Exit")
    
if __name__ == "__main__":
    actions = {
        "1": upload_file,
        "2": list_files,
        "3": download_file,
    }
 
    while True:
        show_menu()
        choice = input("Selecciona una opcion (1-4): ").strip()
 
        if choice == "4":
            print("Cerrando...")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("[ERROR] Opcioin invalida, ingrese 1, 2, 3, o 4.")    