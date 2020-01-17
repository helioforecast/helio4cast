# helio4cast
Codes for distributing and managing helio4cast results.

For the auroramaps, predstorm and helio4cast packages.


## Installation instructions:

Install python 3.7.6 with miniconda:

on Linux:

	  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
	  bash Miniconda3-latest-Linux-x86.sh

on MacOS:

	  curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
	  bash Miniconda3-latest-MacOSX-x86_64.sh


Create conda environment:

	  conda env create -f environment.yml

	  conda activate testenv

	  conda install cartopy==0.17.0

	  pip install -r requirements.txt
	  
go to a directory of your choice

	  git clone https://github.com/helioforecast/predstorm

	  git clone https://github.com/helioforecast/auroramaps

	  git clone https://github.com/helioforecast/helio4cast


run

	  python predstorm_l5.py --server
	  
	  python aurora.py --server --real

in the respective directories.

These programs are internally used to distribute the real time results:

   distribute_web.py
   distribute_tweet.py





## Dependencies summary:


environment.yml file:

name: testenv

dependencies:

  - python==3.7.6
  - astropy==4.0
  - matplotlib==3.1.2
  - numba==0.45.1
  - numpy==1.17.2
  - ipython==7.11.1
  - pip==19.3.1
  - scikit-learn==0.20.3
  - scikit-image==0.15.0
  - scipy==1.3.1
  - seaborn==0.9.0


requirements.txt file:

  - pillow==6.2.1
  - aacgmv2==2.6.0
  - heliosat==0.3.1
  - pysftp==0.2.8
  - tweepy==3.8.0
  - dropbox==9.4.0




## To update:

change  environment.yml and requirements.txt files

1. conda activate testenv

2. conda env update testenv --file environment.yml 

3. pip install -r requirements.txt















