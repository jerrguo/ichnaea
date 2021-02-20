in client, rtmpserver and api folders

```
npm install
```

GCP 
Create a new project
Go to API & Services
create OAuth2 credentials for web dev
whitelist domain http://localhost:3000
copy client id to client/.env

AWS
Create a bucket 
in glue.sh change bucket name to created bucket 



in client, rtmpserver and api folders

```
npm start
```
in root 
```
./glue.sh
```

Start a OBS Stream
Settings -> Stream
  Service: Custom
  Server: rtmp://localhost/live
  Stream Key: 1 

Start streaming
go to http://localhost:3000

create a stream 

watch stream

stop obs 

delete stream

vod should be in s3 bucket
