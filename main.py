from flask import Flask, render_template, request
import pandas as pd

import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
import seaborn as sns


app = Flask(__name__)

data = pd.DataFrame()

@app.route('/')
def index():
    data = {}
    return render_template('index.html', data=data)

@app.route('/upload', methods=['POST'])
def upload():
    global data
    data = None
    uploaded_file = request.files['csvFile']
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        data['ClimberName'] = 'uploadedCSV'
        
    else:
        url = request.form["profileURL"]
        if request.form["profileURL"][-1] != "/":
            url = url + "/"
        url = url + "tick-export"
        data = pd.read_csv(url)
        
        data['ClimberName'] = url[url.find('/',37)+1:url.rfind('/')]

    this_year = data[(data['Date'] >= '2023-01-01')]
    routes = this_year.Route.nunique()
    locations = this_year.Location.nunique()
    max_crag = "Not enough data :("
    if (locations > 0 ):
        max_crag = this_year.groupby(['Location'])['Location'].count().idxmax()
    
    max_type = "Not enough data :("
    max_route = "Not enough data :("
    if (routes > 0):
        max_type = this_year.groupby(['Route Type'])['Route Type'].count().idxmax()
        max_route = this_year['Route'][this_year['Your Stars'].idxmax()]
        number_days = this_year['Date'].nunique()
        avg_ticklength = this_year['Notes'].str.len().mean()


        data['Just this Year'] = (data['Date'] >= '2023-01-01')
        data['TickLength'] = data['Notes'].str.len().values


        plt.figure()
        sns.violinplot(data=data,x="ClimberName", y="TickLength", hue="Just this Year",split=True, inner="quart")

        # Save the plot to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

         # Embed the plot in the HTML template
        plot_url = base64.b64encode(img.getvalue()).decode()
    
    
    return render_template('data.html', routes=routes, locations=locations, max_crag=max_crag, max_type=max_type, max_route=max_route,number_days=number_days,avg_ticklength=avg_ticklength,plot_url=plot_url)


@app.route('/compareUS', methods=['POST'])
def compareUS():
    global data
    data2 = None
    uploaded_file = request.files['csvFile2']
    if uploaded_file:
        data2 = pd.read_csv(uploaded_file)
        data2['ClimberName'] = 'uploadedCSV'
        
    else:
        url = request.form["profileURL2"]
        if request.form["profileURL2"][-1] != "/":
            url = url + "/"
        url = url + "tick-export"
        data2 = pd.read_csv(url)
        
        data2['ClimberName'] = url[url.find('/',37)+1:url.rfind('/')]

    this_year2 = data2[(data2['Date'] >= '2023-01-01')]
    routes2 = this_year2.Route.nunique()
    locations2 = this_year2.Location.nunique()
    max_crag2 = "Not enough data :("
    if (locations2 > 0 ):
        max_crag2 = this_year2.groupby(['Location'])['Location'].count().idxmax()
    
    max_type2 = "Not enough data :("
    max_route2 = "Not enough data :("
    if (routes2 > 0):
        max_type2 = this_year2.groupby(['Route Type'])['Route Type'].count().idxmax()
        max_route2 = this_year2['Route'][this_year2['Your Stars'].idxmax()]
        number_days2 = this_year2['Date'].nunique()
        avg_ticklength2 = this_year2['Notes'].str.len().mean()


        data2['Just this Year'] = (data2['Date'] >= '2023-01-01')
        data2['TickLength'] = data2['Notes'].str.len().values

        #Now concatenate the new data
        data = pd.concat([data,data2])

        plt.figure()
        sns.violinplot(data=data,x="ClimberName", y="TickLength", hue="Just this Year",split=True, inner="quart")

        # Save the plot to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

         # Embed the plot in the HTML template
        plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('data.html', routes=routes2, locations=locations2, max_crag=max_crag2, max_type=max_type2, max_route=max_route2,number_days=number_days2,avg_ticklength=avg_ticklength2,plot_url=plot_url)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
