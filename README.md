# helio4cast
Codes for distributing and managing helio4cast results

for auroramaps, predstorm and helio4cast packages


1. install python 3.7.6 with miniconda

2. conda env create  f environment.yml

3. conda activate testenv

4. conda install -c conda-forge cartopy==0.17.0

5. pip install -r requirements.txt

6. git clone https://github.com/helioforecast/predstorm

7. git clone https://github.com/helioforecast/auroramaps

8. git clone https://github.com/helioforecast/helio4cast


environment.yml
name: testenv
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

requirements.txt
aacgmv2==2.6.0
heliosat==0.3.1
pysftp==0.2.9
tweepy==3.8.0
dropbox==9.4.0



To update:

change  environment.yml and requirements.txt files

1. conda activate testenv

2. conda env update testenv --file environment.yml 

3. pip install -r requirements.txt















