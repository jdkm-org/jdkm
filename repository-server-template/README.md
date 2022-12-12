# 

```shell
sudo docker build -f ./DockerFile -t  jdkm-repository-server-template:1.0.0 .
sudo docker run -id -p 9900:80 --name "jdkm-repository-server" jdkm-repository-server-template:1.0.0
```