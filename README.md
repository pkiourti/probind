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
#### For using a model (through the `Run model` button) we accept the following DNA representations:
- 2 DNA strings in the text boxes
- Load 2 separate DNA sequences:
	- saved as 2 separate .npy arrays:
	 shape of numpy array: (1, 4, num_base_pairs) 
	 with num_base_pairs > 300
	 (This corresponds to the one-hot vector representation)
	- saved as 1 .csv file: 
	A,C,T,G,A,T,C,G,T,A, …  
	C,T,A,G,T,A,G,C,A,T, … 
	- saved as 1 .txt file:
	A C T G A T C G T A … 
	C T A G T A G C A C … 

#### Test our tool by choosing the data inside the test_data folder: probind/Final_Project_ProBind/Code/test_data. Choose:
- dna.csv **or**
- dna.txt **or**
- **both** dna1.npy, dna2.npy **or**
- copy and paste in the text boxes the 2 strings inside the separate files dna1, dna2
