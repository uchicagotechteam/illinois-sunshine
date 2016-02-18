#Illinois Sunshine

## Check it out

[CartoDB Map](https://skotekal.cartodb.com/viz/9e6e0ad6-d44c-11e5-8ae0-0ecfd53eb7d3/map)

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

