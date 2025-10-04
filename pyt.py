import torch
print(torch.__version__)
print(torch.backends.mps.is_available())  # should be True if MPS works
print(torch.backends.mps.is_built())      # checks if PyTorch was built with MPS support
x = torch.ones(5, device="mps")
print(x)
