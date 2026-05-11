#!/usr/bin/env bash

set -euo pipefail

echo "Deleting existing cluster (if any)..."
minikube delete || true

echo "Starting 3-node Minikube cluster..."
minikube start \
  --nodes 3 \
  --driver=docker

echo "Applying node labels..."

kubectl label node minikube workload=app --overwrite

kubectl label node minikube-m02 workload=db --overwrite

kubectl label node minikube-m03 workload=infra --overwrite

echo "Cluster status:"
kubectl get nodes

echo "Waiting for nodes to be ready..."
kubectl wait --for=condition=Ready nodes --all --timeout=120s

echo "Node labels:"
kubectl get nodes --show-labels