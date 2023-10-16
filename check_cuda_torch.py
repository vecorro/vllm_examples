import torch

cuda_available = torch.cuda.is_available()
print(f"Pytorch CUDA available: {cuda_available}")

print(f" CUDA device count: {torch.cuda.device_count()}")

print(f"CUDA dev name: {torch.cuda.get_device_name(0)}")