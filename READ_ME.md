# Small Kubernetes Demo

This repo shows one very small workflow on Kubernetes. You build a Python container and run it as a **Job**. We use a browser‑only sandbox, so nothing is installed on your laptop.

---

## Why Kubernetes?

* **Runs containers for you** – tell it the desired state; it keeps that state true.
* **Easy scale‑out** – change *parallelism* from 1 to 10 and you get ten workers.
* **Self‑healing** – if a pod crashes, Kubernetes starts a new one.
* **Works anywhere** – the YAML you write here also runs on any managed cluster.

---

## Folder layout

```
Kubernetes_demo/
├── data-crunch/            # the actual app
│   ├── Dockerfile          # builds the Python image
│   ├── app.py              # simple data script (edit to taste)
│   └── requirements.txt    # Python deps
├── job.yaml                # Kubernetes Job spec
└── README.md               # this file
```

---

## Quick run (in Play‑With‑K8s)

```bash
# Clone the repo
git clone https://github.com/<you>/Kubernetes_demo.git
cd Kubernetes_demo

# Build the image in Docker
docker build -t data-crunch:0.1 ./data-crunch

# Copy that image into containerd so Kubernetes can use it
docker save data-crunch:0.1 | ctr -n k8s.io images import -

# Allow the control‑plane node to run pods (single‑node demo)
kubectl taint nodes --all node-role.kubernetes.io/control-plane-

# Apply the Job
kubectl apply -f job.yaml

# Watch it finish
kubectl get jobs
kubectl logs -l job-name=data-crunch-job
```

The output comes from **app.py** inside the container.

---

## How the Job works

```yaml
apiVersion: batch/v1
kind: Job
spec:
  completions: 1        # run once
  parallelism: 1        # set to >1 to shard work
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: crunch
        image: data-crunch:0.1
        command: ["python", "app.py"]
```

*The Job controller* creates one pod, waits until it exits, then marks the Job **Succeeded**. Add `ttlSecondsAfterFinished` to auto‑delete the pod later.

---

## Clean‑up

```bash
kubectl delete -f job.yaml   # remove the Job and pods
kind delete cluster          # if you used kind
# or just close the PWK tab – the sandbox wipes itself
```

---

## What to try next

* Change **parallelism** to 10 and split input files by index.
* Turn the script into a **CronJob** that runs hourly.
* Push the image to Docker Hub and deploy on a cloud cluster.
* Add Prometheus + Grafana for metrics.

---

*Last tested:* July 2025 in Play‑With‑Kubernetes (single‑node sandbox).
