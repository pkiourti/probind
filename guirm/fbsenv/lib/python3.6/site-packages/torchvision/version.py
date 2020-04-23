__version__ = '0.6.0'
git_version = '82fd1c85d7e42d93255ed01f763ca40d58f288e3'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
