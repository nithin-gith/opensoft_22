# Installation Instructions

We will be using the following commands in sucesssion to set up all the required softwares and packages on our Azure Virtual Machine. The softwares and packages used are : 
- kubespray
- kubectl
- haproxy
- helm charts
- prometheus
- grafana


### Install Kubespray
Clone the [Kubespray Github Repo](https://github.com/kubernetes-sigs/kubespray)
```sh
git clone https://github.com/kubernetes-sigs/kubespray.git
```
We use Vagrant to install python dependencies for provisioning tasks. Check if Python and pip are installed:
```sh
python -V && pip -V
```
If this returns the version of the software, you're good to go. If not, download and install Python from here https://www.python.org/downloads/source/ Install the necessary requirements
```sh
sudo pip install -r requirements.txt
```
Take 3 machines Virtual Machines using a Public Cloud Service(or using any software like Vagrant and Virtual Box). Two of them are Master Nodes and the other is the worker Node. 

1. Edit the `hosts.yml` & `cluster.yml` file as per the requirement and IP requirements of the machine.
2. Run the playbook using Ansible
  ```ansible-playbook -i hosts.yml cluster.yml -u USERNAME -b```

### How to add services to the cluster
1. Dockerize the applications and push the images to dockerhub (eg: team333/orders)
2. Write the deployment and service yaml files (eg : flaskdeployment_orders.yml)
3. SSH into one of the master node and run the commands
```kubectl apply -f flaskdeployment_orders.yml```
4. Repeat the same process for other services like deliveries, SMS service.


# Instructions to setup a K8 cluster with 3 machines

### Install Kubesctl using native package management
Update the apt package index and install packages needed to use the Kubernetes apt repository:

```sh
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl
```
Download the Google Cloud public signing key:
```sh
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
```
Add the Kubernetes apt repository:
```sh
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```
Update apt package index with the new repository and install kubectl:
```sh
sudo apt-get update
sudo apt-get install -y kubectl
```

### Installation and setup instructions for HAProxy on public cloud
Update sources list  :  
```
sudo apt update
```
Installation for Linux machine: 
```
sudo apt install -y haproxy
```
Double check for installed version( Version should match what version??) : ```
```
haproxy -v
```
Configure HAProxy:
This is done by creating a configuration file /etc/haproxy/haproxy.cfg with the settings as mentioned in our haproxy.cfg file at our Github repo 


```sudo systemctl start haproxy.service```

1. Then copy the given cfg file `/etc/haproxy/haproxy.cfg` using the below command

```
sudo vi /etc/haproxy/haproxy.cfg
```
2.Then restart the haproxy service using the following commands
```sudo systemctl stop haproxy.service```
```sudo systemctl daemon-reload```
```sudo systemctl start haproxy.service```
3.Finally , check the status of haproxy service
```sudo systemctl status haproxy.status```

### Installing Prometheus and Grafana on the Kubernetes Clusters using Helm Charts 
Helm installation for Linux machine:
```
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```
Adding repositories
```
helm repo add prometheus-community
https://prometheus-community.github.io/helm-charts
helm repo add stable https://charts.helm.sh/stable
```
Updating Helm repositories:
```
helm repo update
```
Install Prometheus Kubernetes :
```
helm install prometheus prometheus-community/kube-prometheus-stack
```   
Run the port forward command :
```
kubectl port-forward deployment/prometheus-grafana 3000
```
All set. Now, you can open Grafana using the Grafana Dashboard link: 
http://52.172.14.72:3001/login and to log in use username admin and password prom-operator 

### Installation of Docker 
Before installing Docker engine for the first time, we  need to to set up Docker repository, then install and update docker from the repository
Update the apt package index and install packages to allow apt to use a repository over HTTPS:
	```
 $ sudo apt-get update 
	```
  ```
 $ sudo apt-get install \
   ca-certificates \
   curl \
   gnupg \
   lsb-release
  ```

Add docker’s official GPG key
```
 $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```



Use the following command to set up the stable repository. To add the nightlyor test repository, add the word nightly or test (or both) after the word stable in the commands below
```
$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```



Install Docker Engine :
Update the apt package index, and install the latest version of Docker Engine and containerd
```
 $ sudo apt-get update
 $ sudo apt-get install docker-ce docker-ce-cli containerd.io
```



### Installing Prometheus and Grafana using helm
Helm :
There are several different ways of deploying prometheus  in kubernetes cluster 
One way of doing that is to  put together all the  configuration files that  you need for all the parts,  so for each component of the prometheus monitoring stack basically you will  create those yaml files for prometheus stateful set , alert manager , grafana deployment , all the config maps and secrets that you  need etc then going ahead and execute them in the right order because of dependencies but this method of deployment is inefficient and requires lot of  effort but here’s an efficient way of doing the same using the helm charts to deploy Prometheus .

Installing Prometheus and grafana on the Kubernetes Clusters using helm charts 
Helm installation for Linux machine:
```
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -

sudo apt-get install apt-transport-https --yes

echo "deb https://baltocdn.com/helm/stable/debian/ all main" |      sudo tee /etc/apt/sources.list.d/helm-stable-debian.list

sudo apt-get update

sudo apt-get install helm
```
2)  Adding repositories
```
helm repo add prometheus-community
https://prometheus-community.github.io/helm-charts

helm repo add stable https://charts.helm.sh/stable
```

3)  Updating Helm repositories:
```
helm repo update
```
4)  Install Prometheus Kubernetes :
 ```
 helm install prometheus prometheus-community/kube-prometheus-stack
 ```
5)  Run the port forward command : 

```
kubectl port-forward deployment/prometheus-grafana 3000
```
6)  All set now you can open grafana using the Grafana dashboard link: http://52.172.14.72:3001/login and to log in use username `admin` and password `prom-operator` 

After this you can see the grafana dashboard and to observe the up and down time of the nodes running on your machine by clicking on dashboard and then on browse there you have to click on 
Node Exporter / Nodes  and here you can see the up and down times of your nodes.


