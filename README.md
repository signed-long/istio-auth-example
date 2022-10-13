## Istio End-User Authentication Example

This project is a proof-of-concept using Istio's Ingress Gateway, and Authorization Policy resources in order to move authorization logic out of application code. 

The application consists of an authentication service and a test service. The test service has routes with `/private` and `/public` prefixes, only authenticated users should be able to access `/private` routes.

### Prereqs

- Install kubectl and point it to a kubernetes cluster (I did all testing on [minikube](https://minikube.sigs.k8s.io/docs/start/))
- Follow steps in the [istio getting started page](https://istio.io/latest/docs/setup/getting-started/) to install istio on your cluster and inject sidecar containers
- Install [helm](https://helm.sh/docs/intro/install/)
- Have a postgresql database server up and running, I used a [Digital Ocean managed postgres](https://docs.digitalocean.com/products/databases/postgresql/) instance
- Update values files in [config/](config/), and [k8s/secrets/secrets.yml](k8s/secrets/secrets.yml.example) to use this database
- [Configure cluster](https://dev.to/asizikov/using-github-container-registry-with-kubernetes-38fb) to be able to pull container images from github's container registry

### Deploying app to cluster:

#### Day 0

1. Apply secrets to cluster: `kubectl apply -g k8s/secrets/secrets.yml`
1. Apply istio manifests to cluster: `kubectl apply -f k8s/istio`
1. Deploy auth service: `helm install -f config/values.api_auth.yaml api-auth k8s/helm-charts/flaskapp`
1. Deploy test service: `helm install -f config/values.api_test.yaml api-test k8s/helm-charts/flaskapp`

#### Day N

1. Merge PR of any changes to [src/](src/) files, this will trigger a [CI build](.github/workflows) that runs tests and pushes the container image
1. Upgrade auth service: `helm upgrade -f config/values.api_auth.yaml api-auth k8s/helm-charts/flaskapp`
1. Upgrade test service: `helm upgrade -f config/values.api_test.yaml api-test k8s/helm-charts/flaskapp`

### Verify it's working:

- Follow the steps in the [istio docs](https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/) to expose the ingress gateway to external traffic.

```
$ curl $INGRESS_HOST:$INGRESS_PORT/public/hello
{
  "data": {},
  "http_response": {
    "message": "OK 200: Hello not authenticated",
    "status": 200
  }
}
```

```
$ curl $INGRESS_HOST:$INGRESS_PORT/private/hello
RBAC: access denied
```

```
$ curl -X POST $INGRESS_HOST:$INGRESS_PORT/auth/register \
	-d '{"email":"me@email.ca", "password":"super-strong-password"}' \
	--header 'Content-Type: application/json'
{
  "data": {},
  "http_response": {
    "message": "OK 201: Registration successful",
    "status": 201
  }
}
```

```
$ curl -X POST $INGRESS_HOST:$INGRESS_PORT/auth/login \
	-d '{"email":"me@email.ca", "password":"super-strong-password"}' \
	--header 'Content-Type: application/json'
{
  "data": {
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYzFmNGMyNi1lNWYxLTRhOWQtOTQ5Yi1kOGM2ZmE4ZDE4NzMiLCJleHAiOjE2NjU2NDgwMTAsImlzcyI6ImV4YW1wbGUuY29tIn0.UWpHFmCrOG-01tr42ElOGNEClflLrJqhSOdxbdsJXvZWW2kdGlkGNiBvLIu4cledJHzsrZpAh04R2Js3MqgPnJdKQKKcijinQmm-qOG0oecgqTFroImvvGS7g-4GwypGLauUp0tj23zUap-VeTs5m9xPA8k3CkY7w4wmTlA6H7YpYb7KRGMLO2ZpttH0gUJjLZGWF2BbnW4mpUYxVznAm55vub-_bqzwF_ENKAC1ylmFjVatVdV_YnEAlsktG1JvAik5yrhFuV_jpomRw-NYYWmMuH4To4TuCraRsemkGkdqvtMvTGJq-N0jjdWL-ndhuVxtsHFooPpyO5EjSeCQhc92Zv6Lav4y90ayK1RmeMW0WDB1Bc7JJoBrplKpHcJrCqHVst4ovbYxTWqJb_ALXjClJLKIubddqHiHYN_EFCZ-ZXZ0PtUvlNCXW6pUtYzZ5XeJzz_vYahMtNDOCFbSbzZqstT5utCmBOxV6zrD452TzfDj3_q_uEnsLMYe3cJ-"
  },
  "http_response": {
    "message": "OK 200: Authentication successful",
    "status": 200
  }
}
```

```
$ curl $INGRESS_HOST:$INGRESS_PORT/private/hello \
	--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYzFmNGMyNi1lNWYxLTRhOWQtOTQ5Yi1kOGM2ZmE4ZDE4NzMiLCJleHAiOjE2NjU2NDgwMTAsImlzcyI6ImV4YW1wbGUuY29tIn0.UWpHFmCrOG-01tr42ElOGNEClflLrJqhSOdxbdsJXvZWW2kdGlkGNiBvLIu4cledJHzsrZpAh04R2Js3MqgPnJdKQKKcijinQmm-qOG0oecgqTFroImvvGS7g-4GwypGLauUp0tj23zUap-VeTs5m9xPA8k3CkY7w4wmTlA6H7YpYb7KRGMLO2ZpttH0gUJjLZGWF2BbnW4mpUYxVznAm55vub-_bqzwF_ENKAC1ylmFjVatVdV_YnEAlsktG1JvAik5yrhFuV_jpomRw-NYYWmMuH4To4TuCraRsemkGkdqvtMvTGJq-N0jjdWL-ndhuVxtsHFooPpyO5EjSeCQhc92Zv6Lav4y90ayK1RmeMW0WDB1Bc7JJoBrplKpHcJrCqHVst4ovbYxTWqJb_ALXjClJLKIubddqHiHYN_EFCZ-ZXZ0PtUvlNCXW6pUtYzZ5XeJzz_vYahMtNDOCFbSbzZqstT5utCmBOxV6zrD452TzfDj3_q_uEnsLMYe3cJ-'
{
    "data": {},
    "http_response": {
        "message": "OK 200: Hello authenticated",
        "status": 200
    }
}
```
