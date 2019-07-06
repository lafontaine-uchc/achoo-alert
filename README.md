# Achoo Alert

Achoo Alert is a Dash based [web appliction](http://achooalert.site) for the visualization of predicted pollen counts for the Atlanta area. 

## Forecasting and Analysis

To recreate the pollen count forecasting and data analysis, the jupyter notebooks should be run in the following order:

* **atlanta_pollen_scraper.ipynb**
* **Data Processing & Feature Engineering.ipynb**
* Exploratory Analysis.ipynb
* **Fb_prophet.ipynb**
* Fb_prophet-weather.ipynb (Additional data file required, available [here](https://drive.google.com/open?id=159ELbaHdjkPE88BsWWv06W_YgOAUmRpc))

## Deploying Locally

If desired, it is possible to deploy the app locally using app.py, however it is necessary to run the bolded notebooks first in order to generate the pollen predictions data file. 
