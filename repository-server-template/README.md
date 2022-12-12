# JDKM Repository Server Template

## Get started

```shell
sh -c "$(curl -fsSL https://raw.githubusercontent.com/swxfll/jjvmm/main/repository-server-template/install.sh)"
```

```shell
sudo docker build -f ./DockerFile -t  jdkm-repository-server-template:1.0.0 .
sudo docker run -id -p 9900:80 --name "jdkm-repository-server" jdkm-repository-server-template:1.0.0
```