# Bring your function as k8s operator

I always felt, writing infrastructure/platform is never ending & complex tasks which goes on and on, just like - "calling
plumber in your house :-)"

On the major concerns in creating infrastructure as code and how it get tangled with 
internal of the platform like k8s, aws. There has to be nice separation/abstraction. Kubernetes operator provides nice 
decoupling from k8s and helps in creating your business specific k8s artifacts. I will demonstration building operator 
by writing plain old simple logic in programing language of your choice. In this blog, I will use python.

Creating k8s operator can be quiet challenging. MetaController provides nice abstraction and framework for developing 
k8s operator. This helps engineers to concentrate on writing business logic for k8s operator. I this blog, I will 
demonstrate creating webhook using OpenFaas, hence removes to complication around setting up code on k8s to build the 
operator. This leads to development methodology called "Function As Service". That is,as engineer, it's only required to business logic.

**This take to simplicity which I terms - "just bring your function to create a k8s operator"** 

This open's opportunities to create cloud agnostic infrastructure (operator) and marry with engineering need, for example, 
- machine learning model training operator (sagemeker, kubeflow etc)
- machine learning model serving operator (sagemeker, kubeflow etc)
- maching learning model hyper parameter tuning operator (sagemeker, kubeflow etc)
- .. more ..

## Pre-requisites 

Following installation are required to create MetaController based k8s operator.

### Install k8s
````
brew install k3d
````

### Install helm3
````
brew install helm
````

### Install MetaController
````
kubectl create namespace metacontroller
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/metacontroller/master/manifests/metacontroller-rbac.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/metacontroller/master/manifests/metacontroller.yaml
````

### Install OpenFaas

- Create namespaces for openaas

````
kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml
````

- Add helm
````
helm repo add openfaas https://openfaas.github.io/faas-netes/
````

- Deploy OpenFaas helm chart

````
helm repo update \
 && helm upgrade openfaas --install openfaas/openfaas \
    --namespace openfaas  \
    --set functionNamespace=openfaas-fn \
    --set generateBasicAuth=true \
    --set openfaasPRO=false --set serviceType=LoadBalancer --set ingress.enabled=true
````

- Install OpenFaas CLI

````
brew install faas-cli
````

-- Setup cli

````
PASSWORD=$(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode) && \
echo "OpenFaaS admin password: $PASSWORD"
echo $(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode)
````

-- Setup OpenFaas UI

````
export OPENFAAS_URL=http://127.0.0.1:8080
kubectl port-forward -n openfaas svc/gateway 8080:8080 &
````

Hit the OpenFaas UI using below url:
````
http://localhost:8080/ui
````

## K8s operator

Let's create a simple k8s operator HelloWorld using OpenFaas based webhook

Following are key objects:

1. crd (crd.yaml) : This file create custom resource definition - 'KIND'
2. controller (controller.yaml): This files link crd with OpenFaas based webhook to be called with crd
3. handler.py: The python file which contains business logic of creating required k8s objects

````
kubectl create -f crd.yaml
kubectl create -f controller.yaml
faas-cli up -f openfaas-webhook.yml
kubectl apply -f busybox-operator.yaml
````

Check the pods creation using following:
````
  kubectl get pods -n <namespace>
````

Check the pods created and also the logs.




