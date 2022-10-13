## Istio End-User Authentication Example

This project is a proof-of-concept using Istio's Ingress Gateway, and Authorization Policy resources used to move authorization logic out of application code for a simple microservice applciation running on kubernetes.

### Prereqs

- Install kubectl and point it to a kubernetes cluster (I did all testing on [minikube](https://minikube.sigs.k8s.io/docs/start/))
- Follow steps in the [istio getting started page](https://istio.io/latest/docs/setup/getting-started/) to install istio on your cluster and inject sidecar containers
- Install [helm](https://helm.sh/docs/intro/install/)
- Have a postgresql database server up and running, I used a [Digital Ocean managed postgres](https://docs.digitalocean.com/products/databases/postgresql/) instance
- Update values files in [config/](config/), and [k8s/secrets/secrets.yml](k8s/secrets/secrets.yml.example) to use this database
- [Configure cluster](https://dev.to/asizikov/using-github-container-registry-with-kubernetes-38fb) to be able to pull container images from github's container registry

### Deploying app to cluster:

1. Merge PR of any changes to [src/](src/) files, this will trigger a [CI build](.github/workflows) that runs tests and pushes the container image
1. Apply secrets to cluster: `kubectl apply -g k8s/secrets/secrets.yml`
1. Deploy auth service: `helm install -f config/values.api_auth.yaml api-auth k8s/helm-charts/flaskapp`
1. Deploy test service: `helm install -f config/values.api_test.yaml api-test k8s/helm-charts/flaskapp`

### Verify it's working:
