#Illinois Sunshine
Maps campaign finance data from [Illinois Sunshine](https://www.illinoissunshine.org/). We are looking to implement
more features such as filters, time sliders, etc.

## Check it out

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

