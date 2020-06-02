import sys

from flask import Flask, render_template, request, redirect, Response
#from flask import Bundle, Evironment

import random, json

app = Flask(__name__)

# js = Bundel('search.js',output = 'gen/main.js')

# assets = Environment(app)

# assets.register('main_js', js)

def dataJson(vcpuRange):
    datatmp = {}
    i = 0
    vcpu = 0
    tmppricePerUnit = 0
    
    with open('index.json') as json_file:
        data = json.load(json_file)
        
        for item in data['products']:
            tmppricePerUnit = None
            vcpu = data['products'][item]['attributes'].get('vcpu')
            if(data['terms']['OnDemand'].get(item)):
                for item1 in data['terms']['OnDemand'][item]:
                    datatmp1 = data['terms']['OnDemand'][item][item1]['priceDimensions']
                    for item2 in datatmp1:
                        tmppricePerUnit = data['terms']['OnDemand'][item][item1]['priceDimensions'][item2].get('pricePerUnit')
                    # if tmppricePerUnit:
                    #     print(tmppricePerUnit)
            if vcpu:
                if vcpuRange == 0:
                    datatmp[item] = data['products'][item]['attributes']
                elif (int(vcpu)== int(vcpuRange)):
                    datatmp[item] = data['products'][item]['attributes']
                if(datatmp.get(item)):
                    datatmp[item]['priceDimensions'] = tmppricePerUnit
    return datatmp
    

@app.route('/')
def output():
	# serve index template
    to_send = dataJson(0)
    return render_template('index.html', to_send = to_send)


@app.route('/', methods = ["POST","GET"])
def handle_data():
    if request.method == "POST":
        result = request.form['projectFilepath']
        getData = result
        print (getData)
        to_send = dataJson(getData)
        return render_template('index.html', to_send = to_send)
    else:
        return render_template('index.html') 


if __name__ == '__main__':
	# run!
	app.run(debug=True)