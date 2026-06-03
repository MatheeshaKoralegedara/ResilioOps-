
# 📊  Monitoring Stack Setup

This component manages the cluster monitoring infrastructure using **Prometheus** (metrics collection) and **Grafana** (visualization).

## 🛠️ Setup Instructions

### 1. Prerequisites
Ensure Helm is installed locally on WSL. If not installed, use the official script:

curl -fsSL -o get_helm.sh [https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3](https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3)
chmod 700 get_helm.sh
./get_helm.sh


### 2. Deployment

Create a dedicated isolation zone for monitoring and deploy the community stack:


# Create namespace
kubectl create namespace monitoring

# Add community Helm charts
helm repo add prometheus-community [https://prometheus-community.github.io/helm-charts](https://prometheus-community.github.io/helm-charts)
helm repo update

# Install the stack
helm install kube-stack prometheus-community/kube-prometheus-stack --namespace monitoring


### 3. Verification

Verify all monitoring pods are healthy and running:


kubectl get pods -n monitoring



---

## 🖥️ Accessing the Dashboards (WSL Port-Forward)

Because this cluster runs locally on `kind` within WSL, you must proxy traffic to access the web user interfaces from your Windows host browser.

### Grafana Access

1. **Retrieve the auto-generated admin password:**

kubectl get secret --namespace monitoring kube-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo



* Default Username: `admin`


2. **Establish the port-forward tunnel:**

kubectl port-forward -n monitoring svc/kube-stack-grafana 3000:80




3. **Access via Browser:** Open `http://localhost:3000` on your Windows machine.

---

## 📈 Key Metrics Traced

* **Cluster Resource Metrics:** Pod/Node CPU and Memory Utilization.
* **Health States:** Pod restarts, CrashLoopBackOffs, and deployment replica counts.




