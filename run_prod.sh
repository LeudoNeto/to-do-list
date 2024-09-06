kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/db-deployment.yaml
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/fastapi-deployment.yaml
kubectl apply -f k8s/db-service.yaml
kubectl apply -f k8s/redis-service.yaml
kubectl apply -f k8s/fastapi-service.yaml