#  A set of scripts that provide examples about serving LLMs using vLLM deployed on Ray Serve.

### The scripts are based on the examples provided by the Anyscale team at <br> https://www.anyscale.com/blog/continuous-batching-llm-inference.

## Requirements.

- First you need to have a Kubernetes (K8s) cluster up and running.
- The K8s cluster must be equipped with NVIDIA GPUs with compute capabilities >= 7.0
- If you're using VMware Tanzu Kubernetes, you can check this documentation to learn <br> how to enable [GPUs on Tanzu Kubbernetes](https://docs.vmware.com/en/VMware-Tanzu-Kubernetes-Grid/1.6/vmware-tanzu-kubernetes-grid-16/GUID-tanzu-k8s-clusters-hardware.html).

## Deploying a vLLM service on Ray Serve.
- The AnyScale team provides comprehensive documentation about Ray Serve and how to deploy it <br>
 K8s using Kuberay. Proceed to this link to learn more about [Ray Serve](https://docs.ray.io/en/latest/serve/index.html). Follow that documentation to <br>
understand how to customize the vLLM service deployment on Ry Serve beyond the scope of this guide.
- Ensure you have [Helm installed](https://helm.sh/docs/intro/install/) in your env.
- 
- Deploy Kuberay in your K8s cluster.
