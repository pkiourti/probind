# ProBind Tool
ProBind has the ability to model the behavior of the binding of proteins. It can produce several models, one per protein. Each model is a Convolutional Neural Network that represents the binding behavior of one protein. The model accepts one or more DNA sequences of 300 b.p. each and their reverse complements as input. The output of the model is one binding value per DNA sequence. This output scalar value is between 0 and 1 and represents how well the protein that is modeled binds to the given DNA sequences.

## Requirements
Install anaconda: [on windows](https://docs.anaconda.com/anaconda/install/windows/), [on mac](https://docs.anaconda.com/anaconda/install/mac-os/), [on linux](https://docs.anaconda.com/anaconda/install/linux/)

#### Linux
```
conda create -n probind python=3.6 pytorch torchvision matplotlib numpy seaborn 
conda activate probind
python3 -m pip install fbs PyQt5==5.9.2 --user
git clone git@github.com:pkiourti/probind.git
cd probind/Final_Project_ProBind/Code
export PYTHONPATH=$(pwd)
```

#### MacOS
```
conda create -n probind python=3.6
conda activate probind
python3 -m pip install pytorch 
python3 -m pip install torchvision
python3 -m pip install matplotlib numpy seaborn
python3 -m pip install fbs PyQt5==5.9.2
git clone git@github.com:pkiourti/probind.git
cd probind/Final_Project_ProBind/Code/
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
Set the environmental variable PYTHONPATH to where probind/Final_Project_ProBind/Code is.
python3 -m pip install
git clone git@github.com:pkiourti/probind.git
```

## Run
Make sure that the PYTHONPATH is set to where probind/Code is as explained above.
```
cd probind/Final_Project_ProBind/Code/gui
fbs run
```
