#  A set of scripts that provide examples about serving LLMs using vLLM deployed on Ray Serve.

### The scripts are based on the examples provided by the Anyscale team at <br> https://www.anyscale.com/blog/continuous-batching-llm-inference.

## Requirements.

- First you need to have a Kubernetes (K8s) cluster up and running.
- The K8s cluster must be equipped with NVIDIA GPUs with compute capabilities >= 7.0
- If you're using VMware Tanzu Kubernetes, you can check this documentation to learn <br> how to enable [GPUs on Tanzu Kubbernetes](https://docs.vmware.com/en/VMware-Tanzu-Kubernetes-Grid/1.6/vmware-tanzu-kubernetes-grid-16/GUID-tanzu-k8s-clusters-hardware.html).
- The AnyScale team provides comprehensive documentation about Ray Serve and how to deploy it K8s using Kuberay. Follow <br>
[Ray Serve](https://docs.ray.io/en/latest/serve/index.html) documentation to learn how to customize the vLLM service deployment on Ray Serve beyond the scope of this guide.


## Deploying a vLLM service on Ray Serve.
- Set `ClusterRoleBinding` to run a privileged set of workloads. This will prevent a Kuberay operator installation failure.<br>
```
kubectl create clusterrolebinding default-tkg-admin-privileged-binding --clusterrole=psp:vmware-system-privileged --group=system:authenticated
```
- Ensure you have [Helm installed](https://helm.sh/docs/intro/install/) in your env.
- Deploy Kuberay in your K8s cluster. More details at [KubeRay Operator install docs](https://github.com/ray-project/kuberay/blob/master/helm-chart/kuberay-operator/README.md)
````
# Add the Kuberay Helm repo
helm repo add kuberay https://ray-project.github.io/kuberay-helm/

# Install both CRDs and KubeRay operator v0.6.0.
helm install kuberay-operator kuberay/kuberay-operator --version 0.6.0

# Check the KubeRay operator Pod in `default` namespace
kubectl get pods

# NAME                                READY   STATUS    RESTARTS   AGE
# kuberay-operator-6fcbb94f64-mbfnr   1/1     Running   0          17s
````
- 