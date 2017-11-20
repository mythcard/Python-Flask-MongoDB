#!/usr/bin/env python
#from app import app
from flask import Flask,render_template, request, url_for, redirect, session
app = Flask(__name__)
app.config.from_object('config')
import mongoConnect
import Transaction
import DBConnect

"""
views.py defines the routes or page navigation more like a controller deciding on modelling and composing the response
contains 2 major pages
1. /addItem : This is the page where product catalog is displayed and items are added to cart for check out
2. /all_items_trans: This is the landing page where final bill is displayed

/index is a dummy page and has a link to the /addItem
"""

@app.route('/')
@app.route('/index')
def index():
    return render_template('startPage.html')

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    allItemsAdded = []
    all_products = []
    index_error = None
    if request.method == 'GET':
        """clear session and display all items in product catalog"""
        session.clear()
        productcur = DBConnect.getAllProduct()
        data = list(productcur)
        all_products = list()
        for row in data:
            all_products.append(row)


        return render_template('index.html', all_products=all_products)
    elif request.method == 'POST':
        allItemsAdded = []
        """ obtain lst through stored session variable"""
        allItemsAdded = session.get('sub_list', None)
        button_value = str(request.form['submit'])
        itemName = str(request.form['item'])

        """ perform 2 important functionalities
            1. Add item
            2. Delte Item
            List data structure used which is (allItemsAdded)
        """
        if(button_value == 'add'):
            if allItemsAdded is None:
                allItemsAdded = []
            if(DBConnect.checkItemExists(itemName)):
                allItemsAdded.append(itemName)
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


""" this is the final bill landing page where discounts are finalised"""
@app.route('/all_items_trans', methods =['GET'])
def all_items_trans():
    allItemsAdded = []
    allItemsAdded = session.get('sub_list', None)
    """ trans is the object for a transaction which takes all the item in the list and calculates the 
        bill with all discounts at once
    """
    trans = Transaction.Transaction()
    trans.addItem(allItemsAdded)
    """ this is where discount calculation starts
    1. BOGO
    2. CHMK
    3. addPriceDropFeatureItems to handle both APPL and APOM
    the objective of using one function is that this can be further simplified in terms of this function call where it is 
    elegantly written only once and is called with the help of some metadata through database
    """
    trans.addBOGOItems()

    if 'AP1' in allItemsAdded and 'OM1' in allItemsAdded:
        trans.addPriceDropFeatureItems('OM1', 'AP1', 1, 3.0, 'APOM')


    if 'AP1' in allItemsAdded and 'OM1' not in allItemsAdded:
        trans.addPriceDropFeatureItems('AP1', 'AP1', 3, 1.50, 'APPL')

    if 'AP1' not in allItemsAdded and 'OM1' in allItemsAdded:
        trans.addPriceDropFeatureItems('OM1', 'AP1', 1, 3.0, 'APOM')
    ## have to avoid stacking up here,  also as part of test check if the discount items present or not and how it behaves

    trans.addCHMKItems()

    lstOfItemsproductCode, lstOfItemsproductName, lstOfItemsproductPrice = trans.getListOfItems()
    return render_template('landingPage.html', lstOfItemsproductCode = lstOfItemsproductCode, lstOfItemsproductName= lstOfItemsproductName, lstOfItemsproductPrice = lstOfItemsproductPrice, totalPrice = trans.getTotalPrice())


if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')


