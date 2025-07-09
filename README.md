# Small Kubernetes Demo

This repo shows one very small workflow on Kubernetes, **run entirely in the free browser sandbox at [labs.play-with-k8s.com](https://labs.play-with-k8s.com)**.  You build a Python container and run it as a **Job**; no software is installed on your own machine.

---

## Why Kubernetes?

* **Runs containers for you** – you declare the desired state; it keeps that state true.
* **Easy scale‑out** – change *parallelism* from 1 to 10 and you get ten workers.
* **Self‑healing** – if a pod crashes, Kubernetes restarts it.
* **Works anywhere** – the YAML you write here also runs on any managed cluster.

---

## Folder layout

```
Kubernetes_demo/
├── data-crunch/            # the actual app
│   ├── Dockerfile          # builds the Python image
│   ├── app.py              # simple data script (edit to taste)
│   └── requirements.txt    # Python deps
├── job.yaml                # Kubernetes Job spec (root copy)
└── README.md               # this file
```

---

## Quick run (Play‑With‑K8s)

### 0  Open the sandbox

1. Visit **[https://labs.play-with-k8s.com](https://labs.play-with-k8s.com)**.
2. Sign in with GitHub and click **+ Add New Instance**. You’ll get a shell prompt that looks like `node1 ~]$`.

### 1  Clone this repo

```bash
git clone https://github.com/<your‑user>/Kubernetes_demo.git
cd Kubernetes_demo
```

### 2  Build the container image

```bash
docker build -t data-crunch:0.1 ./data-crunch
```

### 3  Make the image visible to Kubernetes (sandbox uses containerd)

```bash
docker save data-crunch:0.1 | ctr -n k8s.io images import -
```

### 4  Allow the single node to run pods

```bash
kubectl taint nodes --all node-role.kubernetes.io/control-plane-
```

### 5  Apply the Job

```bash
kubectl apply -f job.yaml
```

### 6  Watch it finish

```bash
kubectl get jobs
POD=$(kubectl get pods -l job-name=data-crunch-job -o jsonpath='{.items[0].metadata.name}')
kubectl logs "$POD"
```

You should see the output from **app.py**.

---

## How the Job works

```yaml
apiVersion: batch/v1
kind: Job
spec:
  completions: 1        # run once
  parallelism: 1        # set to >1 to shard work
  ttlSecondsAfterFinished: 300   # clean up pods after 5 min
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: crunch
        image: data-crunch:0.1
        imagePullPolicy: IfNotPresent   # use local copy
        command: ["python", "app.py"]
```

The Job controller creates one pod, waits until it exits, then marks the Job **Succeeded**.

---

## Clean‑up

```bash
kubectl delete -f job.yaml   # remove the Job and pods
# or simply close the PWK tab – the sandbox wipes itself in a few hours
```

---

## What to try next

* Change **parallelism** to 10 and split input files by index.
* Turn the script into a **CronJob** that runs hourly.
* Push the image to Docker Hub and deploy on a cloud cluster.
* Add Prometheus + Grafana for metrics.

---

*Last tested:* July 2025 in Play‑With‑Kubernetes (single‑node sandbox).
