#Illinois Sunshine
Maps campaign finance data from [Illinois Sunshine](https://www.illinoissunshine.org/). We are looking to implement
more features such as filters, time sliders, etc.

##Leaflet & More Customization

[Leaflet](http://leafletjs.com/)

CartoDB has some limitations as it does not allow us to customize as much as we want. We will implement solutions in javascript and leaflet, which does all of the hard mapping work. We just have to do a little more of the lifting then when using CartoDB. For instance, now we can give leaflet the exact type of base map layer we want, the type of markers we want, the time slider, the heat visualization etc etc etc without being restricted to CSV files and other CartoDB requirements. 

I have gotten the committees to be mapped at this point. Thanks to CartoDB for their [free base map layer](https://cartodb.com/basemaps). 

To see this visualization:

```
cd .\leaflet\
python app.py
```

app.py uses flask and your machine to host the site. You can type in 127.0.0.1:5000 or whatever pops up in the python shell to see the map. 


Functionality can be expanded through [Leaflet plugins](http://leafletjs.com/plugins.html). Play with it!

Google/StackOverflow is your friend!

## Check it out

This map currently has the aggregate receipt amount and volume of receipts per year mapped for each committee. You can choose the year via the menu to the right. 
[CartoDB Map](https://skotekal.cartodb.com/viz/1c4aa0a4-d524-11e5-b8d9-0ea31932ec1d/map)

## Run

Fork this repository. Get url of repo from your own GitHub

```
git clone [your url here]
python dataPull.py
```

You should get a CSV file in /tmp/ called CommiteeData.csv
You can put this into CartoDB and play around with it.

## Alternative Visualization using D3-Flask
Make sure you have [pip installed](https://pip.pypa.io/en/stable/installing/).

Run the following commands:
 ```
pip install flask
pip install numpy
python app.py
 ```

 If everything worked properly, you should see a map of Illinois separated by county.

