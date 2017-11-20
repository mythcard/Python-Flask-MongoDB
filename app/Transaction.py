import DBConnect

class Item:

    def __init__(self, productCode, productName, productPrice):
       self.productCode = productCode
       self.productName = productName
       self.productPrice = productPrice

    def equals(self, obj):
        if( self.productName == obj.productName):
            return True
        else:
            return False


class Transaction:
    lstItm = None
    dict1 = dict()
    totalPrice = 0

    def __init__(self):
        self.lstItm = []
        dict1 = dict()
        totalPrice = 0



    def addItem(self,allItemsAdded):
        self.dict1 = dict()
        for pdCode in allItemsAdded:
            productCode, productName, productPrice = DBConnect.getItems(pdCode)
            #print("The details obtained here are: ", productCode, productName[0]['productName'], productPrice[0]['productPrice'])
            productName = productName[0]['productName']
            productPrice = productPrice[0]['productPrice']
            itm = Item(productCode, productName, productPrice)
            self.lstItm.append(itm)
            self.totalPrice += productPrice
            if productCode in self.dict1:
                self.dict1[productCode] += 1
            else:
                self.dict1[productCode] = 1
        print(self.dict1.viewitems())
        print(self.dict1.viewvalues())



    def checkLimit(self, itemName, n):
        if itemName not in self.dict1:
            return False
        if(self.dict1[itemName] >= n):
            return True
        else:
            return False

    """ needs a carefully crafted edge case check when buyLimit, getLimit  > 1 """
    def buyNgetNFree(self,buyLimit,buyItem, getLimit, getItem, limit):
        cnt = 0
        print("Here: ")
        if(self.checkLimit(buyItem, buyLimit)):
            print("Here: ")
            buyItemCount = self.dict1[buyItem]
            if(getItem in self.dict1):
                getItemCount = self.dict1[getItem]
            else:
                getItemCount = 0
            print("buyItem ",buyItem)
            print("getItem",getItem)
            """2 cases when items in question are same and when they are different"""
            if(buyItem == getItem):
                while(buyItemCount > 0):
                    buyItemCount-= buyLimit
                    if(buyItemCount>=getLimit ):
                        buyItemCount -= getLimit
                        cnt += getLimit
                    else:
                        if((getLimit - buyItemCount)> 0):
                            cnt += getLimit - buyItemCount
            else:
                while(buyItemCount > 0 and getItemCount > 0):
                    buyItemCount -= buyLimit
                    if (getItemCount >= getLimit):

                        getItemCount -= getLimit
                        cnt += getLimit
                    else:
                        if ((getLimit - getItemCount) > 0):
                            cnt += getLimit - getItemCount
        print("Cnt: ",cnt)
        """ handling unlimited and limit case"""
        if(limit == 0):
            return cnt
        elif(limit > 0 and limit > cnt):
            return 0
        elif(limit > 0 and cnt >= limit):
            return limit

    """ for BOGO """
    def addBOGOItems(self):
        limit = self.buyNgetNFree(1,'CF1', 1, 'CF1', 0)
        while(limit > 0):
            itm = Item('BOGO', 'BOGO', -11.23)
            self.lstItm.append(itm)
            self.totalPrice  = self.totalPrice -11.23
            if itm.productName in self.dict1:
                self.dict1[itm.productName] += 1
            else:
                self.dict1[itm.productName] = 1
            limit -= 1

    """ for CHMK """
    def addCHMKItems(self):
        limit = self.buyNgetNFree( 1, 'CH1', 1, 'MK1', 1)
        while (limit > 0):
            itm = Item('CHMK', 'CHMK', -4.75)
            self.lstItm.append(itm)
            self.totalPrice = self.totalPrice - 4.75
            if itm.productName in self.dict1:
                self.dict1[itm.productName] += 1
            else:
                self.dict1[itm.productName] = 1
            limit -= 1

    """for APPL and APOM, buy an item to its limit and find the price drop for all the items in its discount purview"""
    def addPriceDropFeatureItems(self, productCode, priceDropProductCode,  checkLimit, priceDrop, discountCode):
        if(self.checkLimit(productCode,checkLimit)):
            limit = self.dict1[priceDropProductCode]
        else:
            limit = 0
        while (limit > 0):
            itm = Item(discountCode, discountCode, -priceDrop )
            self.lstItm.append(itm)
            self.totalPrice = self.totalPrice - priceDrop
            if itm.productName in self.dict1:
                self.dict1[itm.productName] += 1
            else:
                self.dict1[itm.productName] = 1
            limit -= 1


    def getListOfItems(self):
        lstOfItemsproductCode = []
        lstOfItemsproductName = []
        lstOfItemsproductPrice = []
        for itm1 in self.lstItm:
            lstOfItemsproductCode.append(itm1.productCode)
            lstOfItemsproductName.append(itm1.productName)
            lstOfItemsproductPrice.append(itm1.productPrice)
        return lstOfItemsproductCode, lstOfItemsproductName, lstOfItemsproductPrice

    def getTotalPrice(self):
        return self.totalPrice



""" test cases for addition and deletion, dictionary construction"""
"""
trans = Transaction()

itm = Item("CH1", "Chai", 3.11)
trans.addItem(itm)
itm = Item("CH1", "Chai", 3.11)
trans.addItem(itm)

itm = Item("Mk1", "Milk", 4.75)
trans.addItem(itm)


itm = Item("CH1", "Chai", 3.11)
trans.addItem(itm)
itm = Item("CH1", "Chai", 3.11)
trans.addItem(itm)

itm = Item("Mk1", "Milk", 4.75)
trans.addItem(itm)

itm = Item("CF1", "Coffee", 11.23)
trans.addItem(itm)
itm = Item("CF1", "Coffee", 11.23)
trans.addItem(itm)
itm = Item("CF1", "Coffee", 11.23)
trans.addItem(itm)
itm = Item("CF1", "Coffee", 11.23)
trans.addItem(itm)
itm = Item("CF1", "Coffee", 11.23)
trans.addItem(itm)
itm = Item("CF1", "Coffee", 11.23)
trans.addItem(itm)


print(trans.lstItm[0].productCode)
print(trans.lstItm[1].productCode)
trans.deleteItem(Item("CH1","Chai",3.11))
print(trans.lstItm[0].productCode)



print(trans.dict1.viewkeys())
#print(trans.dict1['Chai'])

 test case to check the number of free for chai, basically testing CHMK 
 test case failure for Milk not present but BOGO applied
also test case failure when CHMK chai 4 milk 0, fixed by changing while clause for case 2 when items are different
 test case failure when chai 0 milk 2, failure in check limit for null keys
 test cases tried, coffee 3, coffee 4, milk 2 chai 4, milk 0 chai 4, chai 0 milk 2, coffee 6
cnt = trans.buyNgetNFree(1,'Chai', 1, 'Milk', 1)
print("Test case for CHMK: ",cnt)

cnt = trans.buyNgetNFree(1,'Coffee', 1, 'Coffee', 0)
print("Test case for BOGO: ",cnt)
print(trans.dict1['Coffee'])

"""






