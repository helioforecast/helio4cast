# helio4cast
Codes for distributing and managing helio4cast results

for auroramaps and predstorm

Python 3.7.6 miniconda
conda env create  -f environment.yml
conda activate envtest3
conda install -c conda-forge cartopy  **(add 0.17.0)
conda install scikit-image  (add version)
pip install -r requirements.txt



(maybe try pip install sunpy? problems when both in conda or not?)=


name: envtest3
dependencies:
  - astropy==4.0
  - matplotlib==3.1.1
  - numba==0.45.1
  - numpy==1.17.2
  - ipython==7.11.1
  - pip==19.3.1
  - scikit-learn==0.20.3
  - scikit-image==0.15.0
  - scipy==1.3.1
  - seaborn==0.9.0



aacgmv2==2.6.0
heliosat==0.3.1
pysftp==0.2.9
tweepy==3.8.0
dropbox==9.4.0






---------

>> conda env create --prefix ./envtest -f environment.yml 



>> conda env create --prefix ./envreal -f environment.yml 

logout, check which python, which pip

>> conda activate /path_to_env/envtest

>> conda install  pip

>> pip install -r requirements.txt

>> conda install -c conda-forge cartopy


cd envtest
>> git clone https://github.com/helioforecast/predstorm
>> git clone https://github.com/helioforecast/auroramaps
>> git clone https://github.com/helioforecast/helio4castset 

to update
conda env update --prefix ./realtest --file environment.yml 
pip install***? -r requirements.txt























helio4cast runs in a conda environment 

tested on linux 

install python anaconda or miniconda

use files environment .yml and requirements.txt in this repo, put in the directory below the conda environment; the conda environment is called realtest and is created in a folder in the current directory



then install all repositories:



go to predstorm and auroramaps and do
pip install . 
in each.

see also
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#create-env-file-manually


to update
conda env update --prefix ./realtest --file environment.yml 
pip install -r requirements.txt