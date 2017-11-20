#!/usr/bin/env python
#from app import app
from flask import Flask,render_template, request, url_for, redirect, session
app = Flask(__name__)
app.config.from_object('config')
import mongoConnect
import Transaction
import DBConnect





@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    allItemsAdded = []
    all_products = []
    index_error = None
    if request.method == 'GET':
        session.clear()
        productcur = DBConnect.getAllProduct()
        data = list(productcur)
        all_products = list()
        for row in data:
            all_products.append(row)


        return render_template('index.html', all_products=all_products)
    elif request.method == 'POST':
        allItemsAdded = []
        allItemsAdded = session.get('sub_list', None)
        button_value = str(request.form['submit'])
        itemName = str(request.form['item'])


        if(button_value == 'add'):
            if allItemsAdded is None:
                allItemsAdded = []
            if(DBConnect.checkItemExists(itemName)):
                allItemsAdded.append(itemName)
                print("Here what the fuck exists :'(")
            else:
                return "Sorry, Item cannot be added as it does not exist in our catalog. Please Enter the product code as mentioned in the catalof to swiftly add the item to your basket!"

        elif(button_value == 'delete'):
            ## check DB catalog and delete
            allItemsAdded.remove(itemName)

        productcur = DBConnect.getAllProduct()
        data = list(productcur)
        all_products = list()
        for row in data:
            all_products.append(row)


        session['sub_list'] = allItemsAdded
        return render_template('index.html', all_products=all_products, lstOfItems = allItemsAdded)

@app.route('/all_items_trans', methods =['GET'])
def all_items_trans():
    allItemsAdded = []
    allItemsAdded = session.get('sub_list', None)
    trans = Transaction.Transaction()
    trans.addItem(allItemsAdded)
    trans.addBOGOItems()
    trans.addPriceDropFeatureItems('AP1','AP1',3,1.50,'APPL')
    ## have to avoid stacking up here,  also as part of test check if the discount items present or not and how it behaves
    trans.addPriceDropFeatureItems('OM1', 'AP1',1, 3.0, 'APOM')
    trans.addCHMKItems()
    lstOfItemsproductCode, lstOfItemsproductName, lstOfItemsproductPrice = trans.getListOfItems()
    return render_template('landingPage.html', lstOfItemsproductCode = lstOfItemsproductCode, lstOfItemsproductName= lstOfItemsproductName, lstOfItemsproductPrice = lstOfItemsproductPrice, totalPrice = trans.getTotalPrice())


if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')


