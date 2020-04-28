# ProBind Tool

## Requirements
Install anaconda: [on windows](https://docs.anaconda.com/anaconda/install/windows/), [on mac](https://docs.anaconda.com/anaconda/install/mac-os/), [on linux](https://docs.anaconda.com/anaconda/install/linux/)

#### Linux
```
conda create -n probind python=3.6 pytorch torchvision matplotlib numpy seaborn 
conda activate probind
python3 -m pip install fbs PyQt5==5.9.2 --user
git clone git@github.com:pkiourti/probind.git
cd probind/Code/
export PYTHONPATH=$(pwd)
```

#### MacOS
```
conda create -n probind python=3.6
conda activate probind
python3 -m pip install pytorch 
python3 -m pip install torchvision
python3 -m pip matplotlib numpy seaborn
python3 -m pip install
python3 -m pip install fbs PyQt5==5.9.2
git clone git@github.com:pkiourti/probind.git
cd probind/Code/
export PYTHONPATH=$(pwd)
```
#### Windows
```
conda create -n probind python=3.6
conda activate probind
conda install -c pytorch pytorch
conda install -c pytorch torchvision
conda install -c conda-forge matplotlib numpy seaborn PyQt==5.9.2
python3 -m pip install fbs
Set the environmental variable PYTHONPATH to where probind/Code is.
git clone git@github.com:pkiourti/probind.git
```

## Run
Make sure that the PYTHONPATH is set to where probind/Code is as explained above.
```
cd probind/Code/gui
fbs run
```
