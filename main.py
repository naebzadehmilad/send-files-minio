import argparse
import os
from minio import Minio

def minio_operations():
    parser = argparse.ArgumentParser(description='Connect to MinIO')
    parser.add_argument('-u', '--username', type=str, required=True, help='MinIO username')
    parser.add_argument('-p', '--password', type=str, required=True, help='MinIO password')
    parser.add_argument('-H', '--host', type=str, required=True, help='MinIO host')
    parser.add_argument('-P', '--port', type=int, default=9000, help='MinIO port (default: 9000)')
    parser.add_argument('-b', '--bucketname', type=str, required=True, help='Bucket name')
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory name')

    args = parser.parse_args()

    minio_client = Minio(f"{args.host}:{args.port}",
                         access_key=args.username,
                         secret_key=args.password,
                         secure=False)

    exists = minio_client.bucket_exists(args.bucketname)
    if not exists:
        try:
            minio_client.make_bucket(args.bucketname)
            print(f"Created bucket: {args.bucketname}")
        except Exception as e:
            print(f"Could not create bucket '{args.bucketname}': {e}")

    files = [f for f in os.listdir(args.directory) if os.path.isfile(os.path.join(args.directory, f))]
    for file_name in files:
        object_name = os.path.basename(file_name)
        try:
            minio_client.stat_object(args.bucketname, object_name)
            print(f"File '{object_name}' already exists in bucket '{args.bucketname}', skipping...")
        except Exception as e:
            try:
                file_path = os.path.join(args.directory, file_name)
                minio_client.fput_object(args.bucketname, object_name, file_path)
                print(f"Uploaded '{object_name}' to bucket '{args.bucketname}'")
            except Exception as upload_error:
                print(f"Could not upload '{object_name}': {upload_error}")

    try:
        bucket_list = minio_client.list_buckets()
        print("Connection established!")
        print("Available buckets:")
        for bucket in bucket_list:
            print(bucket.name)
    except Exception as e:
        print("Failed to establish connection:", e)

if __name__ == '__main__':
    minio_operations()
