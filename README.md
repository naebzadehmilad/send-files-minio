# send-files-minio
send backup to minio 
The default port is 9000. To change the port, use -P

/usr/bin/python3 /opt/script/main.py -H 172.31.71.234 -u user -p password -b coredns  -d /opt/backup/core-dns

This sends the files existing in the destination directory to MinIO for the bucket 
If there is a duplicate file in the MinIO, its upload will be ignored 
