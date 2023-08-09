#  A set of scripts that provide examples about serving LLMs using vLLM deployed on Ray Serve.

### The scripts are based on the examples provided by the Anyscale team at <br> https://www.anyscale.com/blog/continuous-batching-llm-inference.

## Requirements.

- First you need to have a Kubernetes (K8s) cluster up and running.
- The K8s cluster must be equipped with NVIDIA GPUs with compute capabilities >= 7.0
- If you're using VMware Tanzu Kubernetes, you can check this documentation to learn <br> how to enable [GPUs on Tanzu Kubbernetes](https://docs.vmware.com/en/VMware-Tanzu-Kubernetes-Grid/1.6/vmware-tanzu-kubernetes-grid-16/GUID-tanzu-k8s-clusters-hardware.html).
- The AnyScale team provides comprehensive documentation about Ray Serve and how to deploy it K8s using Kuberay. Follow  the [Ray Serve](https://docs.ray.io/en/latest/serve/index.html) 
documentation to learn how to customize the vLLM service deployment on Ray Serve beyond the scope of this guide.


## Deploying a vLLM service on Ray Serve.
- Set `ClusterRoleBinding` to run a privileged set of workloads. This will prevent a Kuberay operator installation failure.<br>
```
kubectl create clusterrolebinding default-tkg-admin-privileged-binding --clusterrole=psp:vmware-system-privileged --group=system:authenticated
```
- Ensure you have [Helm installed](https://helm.sh/docs/intro/install/) in your env.
- Deploy Kuberay in your K8s cluster. More details at [KubeRay Operator install docs](https://github.com/ray-project/kuberay/blob/master/helm-chart/kuberay-operator/README.md)
````
# Add the Kuberay Helm repo.
helm repo add kuberay https://ray-project.github.io/kuberay-helm/

# Install both CRDs and KubeRay operator v0.6.0.
helm install kuberay-operator kuberay/kuberay-operator --version 0.6.0

# Check the KubeRay operator pod in the `default` namespace.
kubectl get pods

# NAME                                READY   STATUS    RESTARTS   AGE
# kuberay-operator-6fcbb94f64-mbfnr   1/1     Running   0          17s
````
- Pull the Ray Serve manifest from GitHub and apply it.
````
# Pull the ray-service.vllm.yaml manifest (from this repo) from the raw URL 
wget -L https://raw.githubusercontent.com/vecorro/vllm_examples/main/ray-service.vllm.yaml

# Create a Ray Serve cluster using the manifest

kubectl apply -f ray-service.vllm.yaml

# The Ray cluster starts to create the head and worker pods

kubectl get pods

# NAME                                           READY   STATUS              RESTARTS   AGE
# kuberay-operator-6b68b5b49d-tvgpg              1/1     Running             0          40h
# vllm-raycluster-ksl9p-head-9q6dx               0/1     ContainerCreating   0          1s
# vllm-raycluster-ksl9p-worker-gpu-group-xnxck   0/1     Init:0/1            0          1s

# After several minutes, the Ray cluster should be up and running

kubectl get pods

# NAME                                           READY   STATUS    RESTARTS   AGE
# kuberay-operator-6b68b5b49d-tvgpg              1/1     Running   0          40h
# vllm-raycluster-ksl9p-head-9q6dx               1/1     Running   0          14s
# vllm-raycluster-ksl9p-worker-gpu-group-xnxck   1/1     Running   0          14s

# The vLLM service will get exposed as a LoadBalancer. In the next example
# the vLLM API service gets exposed over http://172.29.214.16:8000. That is the URL you
# need to use to make prompt completion requests.

kubectl get svc

# NAME                             TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)                                                                                       AGE
# kuberay-operator                 ClusterIP      10.108.37.47    <none>          8080/TCP                                                                                      2d14h
# vllm-raycluster-vphmv-head-svc   LoadBalancer   10.110.93.143   172.29.214.16   10001:30859/TCP,8265:30939/TCP,52365:32230/TCP,6379:31806/TCP,8080:31088/TCP,8000:31758/TCP   18m
````

- The `ray-service.vllm.yaml` manifest has a section that defines the vLLM service deployment:
````
spec:
  serviceUnhealthySecondThreshold: 3600 # Config for the health check threshold for service. Default value is 60.
  deploymentUnhealthySecondThreshold: 3600 # Config for the health check threshold for deployments. Default value is 60.
  serveConfigV2: |
    applications:
      - name: vllm
        import_path: vllm_falcon_7b:deployment
        runtime_env:
          working_dir: "https://github.com/vecorro/vllm_examples/archive/refs/heads/main.zip"
          pip: ["vllm==0.1.3"]
````
- Here some remarks about the service definition:
    - We increased `serviceUnhealthySecondThreshold` and `deploymentUnhealthySecondThreshold` to give Ray sufficient time
  to install vLLM on a virtual working environment. vLLM can cate between >15 minutes to install.
    - `working_dir`is set to the URL of the compressed version of this Github repo. Ray will use this URL to pull the Python code<br>
  that implements the vLLM service.
    - We use vLLM 0.1.3 to create the Ray working env.
    - `import_path` is set to the proper `module:object` for Ray Serve to get the service definition. In this case <br>
  the `module` is the `vllm_falcon_7b.py` Python script and `deployment` is a `serve.deployment.bind()`<br>
  object type defined inside that script.