#!/usr/bin/python
#
# "she-bang" line is a directive to the web server: where to find python
# Name: Biken Maharjan
# filename: project.py
# Final Project
# ID: bm181354@bu.edu
# description: This python programming stimulates the basic digital guitar store where
# user can buy or sell their used/new guitars. They also have capability to track their
# packages.



import MySQLdb as db    # the mysql database API 
import time
import cgi
import cgitb; cgitb.enable()# web debugging package; always import it into your web apps
import random # random module from tracking number

# print out the HTTP headers right away, before we do any other statements
print "Content-Type: text/html"
print # blank line

################################################################################
def getConnectionAndCursor(): # done
    """

    This function will connect to the database and return the
    Connection and Cursor objects.
    """   
    ## NOTE: You will need to specify your connection to the database
    # Your username is your BU username and your password is the
    # first four numbers of your BUID.
    # For example, if your BUID is 'U123-45-6789',
    # your password is set to be '1234' (no quotes). 
    # change the db name to use your username, e.g. cs108_azs_miniFB
    conn = db.connect(host="localhost",
                  user="bm181354",
                  passwd="4951",
                  db="cs108_bm181354_project")

    cursor = conn.cursor()
    return conn, cursor

################################################################################
def doHTMLHead(title):
    '''
        Head of the HTML code. I've used this section to show the logo and link css file 
        with project.py
    '''
    
    # Html Code implementation
    # CSS linked by style.css
    print("""
    <html>
    <head>
    <title>%s</title>
    <link type ="text/css" rel="stylesheet" href="style.css">
    <body>
    <center>
    
    <header>Guitar Store</header>
    <div  class = "h"> <img src = "logo.png"> </div>
     <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br>
    
    
    
    <p>
    """ % (title))

################################################################################
def doHTMLTail():
    '''
        Tail part of the HTML section. I have modified attributes with help css.
    '''

    print("""
    <p>
  
    <footer>
    This page was generated at %s.<br>
    <a href="./project.py"> Return to main page.</a>
    </footer>
    </center>
    </body>
    </html>

    """ % time.ctime())

################################################################################
def debugFormData(form):
    """
    A helper function which will show us all of the form data that was
    sent to the server in the HTTP form.
    """
    
    print """
    <h2>DEBUGGING INFORMATION:</h2>
    <p>
    Here are the HTTP form fields:

    <table border=1>
        <tr>
            <th>key name</th>
            <th>value</th>
        </tr>
    """
    
    # form behaves like a python dict
    keyNames = form.keys()
    # note that there is no .values() method -- this is not an actual dict

    ## use a for loop to iterate all keys/values
    for key in keyNames:

        ## discover: do we have a list or a single MiniFieldStorage element?
        if type(form[key]) == list:

            # print out a list of values
            values = form.getlist(key)
            print """
        <tr>
            <td>%s</td>
            <td>%s</td>
        </tr>
            """ % (key, str(values))

        else:
            # print the MiniFieldStorage object's value
            value = form[key].value
            print """
        <tr>
            <td>%s</td>
            <td>%s</td>
        </tr>
            """ % (key, value)
        
    print """
    </table>
    <h3>End of HTTP form data.</h3>
    <hr>
    """

# Home page
################################################################################
def getAllItem():
    '''
        This method is used for getting all elements [Guitars' information] from the database,
        
    '''
    
    # connect to database
    conn, cursor = getConnectionAndCursor()
    
    # build SQL
    sql = """
        SELECT id, name, quantity,cost,link
        FROM item
        """
    
    # execute the query
    cursor.execute(sql)
    
    # get the data from the database:
    data = cursor.fetchall()
    
    # clean up
    conn.close()
    cursor.close()
    
    return data

################################################################################
def selling_form():
    
    '''
        
        If user decides he/she wants to sell rather than buy then this form will be prompted.
        User will input name,quantity,cost and link of the image. Form will store the input.
        
    '''
    
    print '''
        <fieldset>
        
        <legend>Selling</legend>
        <form>
        
        <table>
        
        <tr><th><label> Name:  </label></th>
        <th> <input type = "text" name="name" required pattern="[A-Za-z0-9\s]+" /><br></th>
        </tr>
        <tr>
        <th><label> Quantity:  </label></th>
        <th><input type = "text" name="quantity" required pattern="[0-9]+" /><br></th>
        </tr>
        <tr>
        <th><label>Cost:  </label></th>
        <th><input type = "text" name="cost" required pattern="[0-9]+"/><br></th>
        </tr>
        <tr>
        <th><label> link:  </label></th>
        <th><input type = "text" name="link" required "/><br></th>
        </tr>
        <tr>
        <th> </th>
        <th><input type="submit" name="sell_submit" value="submit"></th>
        </tr>
        
        </table>
        
        </form>
        
        </fieldset>
        '''

################################################################################
def addItem(name,quantity,cost,link):
    
    '''
       When selling/listing a guiter, user input values will be stored to the database
       with the help of this function.
    '''


    conn, cursor = getConnectionAndCursor()
    
    #for obtaining ID from the item database
    sql_one = '''SELECT max(id) FROM item'''
    cursor.execute(sql_one)
    # returns a tuple [id]
    rowcount = cursor.fetchone()

    # after obtaining id from database
    #SQL Query to insert guitar into the database
    sql = '''INSERT INTO item VALUES (%s,%s,%s,%s,%s)'''
    parameters = (int(rowcount[0]+1),name,quantity,cost,link)
    
    
    cursor.execute(sql,parameters)
    rowcount = cursor.rowcount
    cursor.close
    conn.commit()
    conn.close()
    
    return rowcount


################################################################################
def showAllItem(data):
    '''
        This method will utilized values from 'addItem()' and display it into the screen by embedding
        database values into the Html code.
    '''

   
    # list of guitar here!!
    # displays image and cost of the guitar in neat order
    
    print ''' <div class="content"> <ul>'''
    for row in data:

        # each iteration of this loop creates one row of output:
        (id,name,quantity,cost,link) = row
        

        print("""
            <li><img src = "%s" width ="200" height ="200"><br> <a href="?id=%s">%s</a>
            <br><br>
            Cost:$ %s
            </li>
            """ % (link,id, name,cost))
    print '''</ul></div>'''
    
    # Two option of the website: Buying and Selling will be displayed by this code
    
    print '''
           <div class="selling">
           <form>
           <table>
           <tr>
           <th> Mode: </th>
           <th><input type="submit" name="buying" value="Buy"></th>
           <th><input type="submit" name="selling" value="Sell"></th>
           </tr>
           </table>
           </form>
           </div>
          '''



################################################################################
def form_shipping(id,session,tracking):
    
    '''
        This method uses Html code to prompt user to input Different field for shipping address after 
        buying the guitars. 
        All of these field are mandatory. 
        Leaving it blank will not proceed it into the submit button action.
        
    '''
    
    # HTML code
    print'''
        <fieldset>
        
        <legend>Shipping Address</legend>
        <form>
        <table>
        
        <tr><th><label> First name:  </label></th>
           <th> <input type = "text" name="firstname" required pattern="[A-Za-z]+" /><br></th>
        </tr>
        <tr>
        <th><label> Last name:  </label></th>
            <th><input type = "text" name="lastname" required pattern="[A-Za-z]+" /><br></th>
        </tr>
        <tr>
        <th><label>Address:  </label></th>
            <th><input type = "text" name="address" required pattern="[A-Za-z0-9\s]+[A-Za-z0-9]+"/><br></th>
        </tr>
        <tr>
            <th><label> city:  </label></th>
            <th><input type = "text" name="city" required pattern="[A-Za-z]+"/><br></th>
         </tr>
            <th><label> state:  </label></th>
            <th><input type = "text" name="state" pattern="[A-Za-z]{2,2}"><br></th>
        <tr>
            <th><label> zip:  </label></th>
            <th><input type = "text" name="zip" pattern = "[0-9]{5,5}"><br></th>
        </tr>
        
        <tr>
            <th> </th>
            <input type="hidden" name="id" value="%s">
            <th><input type="submit" name="submit" value="submit"></th>
            <input type="hidden" name="session" value="%s">
            <input type="hidden" name="tracking" value="%s">
            
        </tr>
        
        </table>
            </form>
            
        </fieldset>
        ''' % (id,session,tracking)

################################################################################
def showItem(id,name,quantity,cost,link):

    '''
        This method takes in id,name,quantity,cost,link as an arguement and displays for 
        individual item in neat table when user clicks into a guitar from the buying page [main page].
        Also has Hidden field so that it can be later recorded in the database.
    '''
    
    # Html code  and also modified in CSS
    print ''' 
        
           <div class = "itemOne" >
           <h1>Name : %s <br><h1>
           <table>
           <tr>
           <th><img src= "%s" width = "300" height = "250"></th>
           <th>
           <b>Sale-Price: <i>$%s </i><br> <br></b>
           Available Quantity: <i>%s</i>
           <form>
           <label> Quantity <label><br>
           <input type="number" name="buyer_quantity" min="0" max="%s">
           
           <br>
           <input type="submit" name="addtocart" value="Add to cart">
           
           <input type="hidden" name="id" value="%s">
           <input type="hidden" name="name" value="%s">
           <input type="hidden" name="cost" value="%s">
           <input type="hidden" name="quantity" value="%s">
           <input type="hidden" name="link" value="%s">
           
           

           </form>
           </th><br>
           </tr>
           </table>
           </div>
           
          
        ''' % (name,link,cost,quantity,quantity,id,name,cost,quantity,link)
    
################################################################################
def fields(data,id_user):
    for row in data:
        (id,name,quantity,cost,link) = row
        # each iteration of this loop creates on row of output:
        # add link of the image
        if (int(id) == int(id_user)):
            return (id,name,quantity,cost,link)

################################################################################

def addtoCart(id,name,quantity,cost,link,buyer_quantity):
    '''
        Inserts data into the cart database until it has been checkout by the end user.
        Once checkout it will be emptied
        
    '''
    
    # connect to database
    conn, cursor = getConnectionAndCursor()
    parameters = (id,name,quantity,cost,link,buyer_quantity)
    
    # build SQL and insert the field
    sql = '''INSERT INTO cart VALUES(%s,%s,%s,%s,%s,%s) '''
    
    # execute the query
    cursor.execute(sql,parameters)
    # get the data from the database:
    rowcount = cursor.rowcount
    
    # clean up
    conn.commit()
    conn.close()
    
    cursor.close()
    return rowcount
    
################################################################################

def getAllcart():
    '''
        After inserting everything into cart, this method will get all the 
        elements of the carts. Done so that cart is updated everytime when 
        user continues shopping.
    '''
    
    # connect to database
    conn, cursor = getConnectionAndCursor()
    
    # build SQL
    sql = """
        SELECT id, name, quantity,cost,link,number
        FROM cart
        """
    # execute the query
    cursor.execute(sql)
    
    # get the data from the database:
    data = cursor.fetchall()
    
    # clean up
    conn.close()
    cursor.close()
    
    # return all the data (id, name, quantity,cost,link,number)
    return data

################################################################################
def costcalculation(data):
    '''
        Calculating the cost of all elements in cart.
    '''
    total_cost = 0
    for row in data:
        (id,name,quantity,cost,link,number) = row
        total_cost = ( cost * number )+ total_cost
    
    return total_cost    
################################################################################
def show_cart(data,total,session):
    
    '''
     This method will display the cart element in the web browser embedding HTML 
     and data variable obtained from 'getAllcart()'
     
    '''
    
    print ''' 
        <fieldset>
        <legend>Add to Cart</legend>
        <table>'''
    for row in data:
        (id,name,quantity,cost,link,number) = row
        print '''

           <tr>
           <td><img src= "%s" width = "100" height = "150"></td>
           <td><b>Name </b> : <i>%s</i><br></td>
           <td><b>     Sale Price:</b> <i>$ %s    </i><br> </td>
           <td><b>     Quantity:</b><i> %s </i></td><br>
           </tr>
              ''' % (link,name,cost,number)
    print '''
           <tr>
           <td></td><td></td><td></td>
           <td>Sub-Total: <i>$ %s </i></td>
           </tr>
           </table>''' %(total)
    
    
    # adding buttons [click to checkout] and [Continue shopping]
    # user will click one of these button to proceed into next process [Checking out or Still buying].
    
    print'''
        <form>
        <input type="hidden" name="quantity" value="%s">
        <input type="hidden" name="id" value="%s">
        <input type="hidden" name="number" value="%s">
        
        
        
        <input type="hidden" name="session" value="%s">
        
        <input type="submit" name="Checkout" value="Checkout">
        <input type="submit" name="Continueshopping" value="Continue shopping">
        <form>
        </fieldset>
         ''' % (quantity,id,number,session)
    
################################################################################
def empty_cart():
    '''
        After the session is over. The shopping cart database will be emptied for new customer.
        This method will helped to emptied the database.
    '''
    # connect to database
    conn, cursor = getConnectionAndCursor()
    
    # build SQL
    sql = '''DELETE FROM cart '''
    # execute the query
    cursor.execute(sql)
    # get the data from the database:
    rowcount = cursor.rowcount
    
    # clean up
    conn.commit()
    conn.close()
    cursor.close()
    
    return rowcount
################################################################################

def shipping_info(id,firstname,tracking):
    
    '''
        This method helps to display tracking number of the package to the
        buyer and provides a short message for the customer.
        Hidden field passes the tracking info to other funciton which is later stored into 
        the databse
    '''
    
    #html code, also uses CSS.
    print"""
        <div class = "itemOne" >

         <center>
         <h3>Thank you</h3>
         <h4>Your Tracking Number is : %s </h4>
         Thank you to <b>%s </b>! <br>
         Every day we are looking forward of serving you.<br>
         Enjoy our products as we are on sale this coming month. <br>
         As our warmest appreciation for your loyalty and support; <br>
         Enjoy our surprises plus we offer more fun and exciting gifts.<br>
         </center>
         <form>
         <input type="submit" name="track" value="Track the Package">
         <input type="hidden" name="tracking" value="%s">
         <input type="hidden" name="id" value="%s">
         </form>
         
         </div>
         """ % (tracking,firstname,tracking,id)

################################################################################

def updateQuantity(id, quantity):
    
    '''
        This method is use to modified the quantity of the guitar.
    '''
    
    # SQL query
    conn, cursor = getConnectionAndCursor()
    sql = '''UPDATE item SET quantity = %s WHERE id = %s  '''
    
 
    
    parameters = (quantity,id,)
    cursor.execute(sql,parameters)
    rowcount = cursor.rowcount
    
    #clean up
    cursor.close
    conn.commit()
    conn.close()
   
    return rowcount


################################################################################
def tracking_form(id):
    
    '''
        This method provides a form where user can put in tracking number and check for the status of 
        the order.
    '''
    
    #Html code implementation
    
    print'''
        <fieldset>
        <legend>Tracking Package</legend>
        <form>
        <table>
        <tr><th><label> Tracking Number:  </label></th>
        <th> <input type = "text" name="tracking_number" required pattern="[A-Za-z0-9]+" /><br></th>
        </tr>
        <th></th> <th></th>
        <tr>
        <input type="hidden" name="id" value="%s">
        <th><input type="submit" name="disply_track" value="track"></th>
        </tr>
        </table>
        </form>
        </fieldset>
        ''' % (id)
################################################################################
def add_tracking(id,tracking,delivery,session):
    '''
       This method adds (id,tracking,delivery,session) into the database.
       This is helpful for tracking any packets bought from the website.
       it is similar to the UPS tracking number where user can input a tacking number
       and check the status.
       
    '''
    
    # connect to database
    conn, cursor = getConnectionAndCursor()
    parameters = (id,tracking,delivery,session)
    
    # build SQL
    sql = '''INSERT INTO trackinfo VALUES(%s,%s,%s,%s) '''
    # execute the query
    cursor.execute(sql,parameters)
    # get the data from the database:
    rowcount = cursor.rowcount
    
    # clean up
    conn.commit()
    conn.close()
    
    cursor.close()
    return rowcount
################################################################################

def make_tracking_info():
    '''
        randomly creates tracking number ranging from(10123120,1000000000000000000000)
    '''
    
    tracking = random.randrange(10123120,1000000000000000000000)
    return tracking


def make_session_id():
    '''
        randomly creates session number ranging from(120,100000)
    '''
    
    session = random.randrange(120,100000)
    return session

#===============================================================================
def info(session_id):
    '''
     This method gets the data field [trackinfo's] where session id is a matched.
    '''
    
    # connect to database
    conn, cursor = getConnectionAndCursor()
    
    # build SQL
    parameter = (session_id)
    sql = """
        SELECT * FROM trackinfo where session = %s
        """
    # execute the query
    cursor.execute(sql,parameter)
    
    # get the data from the database:
    data = cursor.fetchall()
    
    # clean up
    conn.close()
    cursor.close()
    
    return data
#===============================================================================
def info_about_tracking():
    '''
        This method gets the data field from trackinfo without caring about any constraints.
        All the values from the database is asked from this query.
        
    '''
    
    # connect to database
    conn, cursor = getConnectionAndCursor()
    
    # build SQL
   
    sql = """
        SELECT * FROM trackinfo
        """
    # execute the query
    cursor.execute(sql)
    
    # get the data from the database:
    data = cursor.fetchall()
    
    # clean up
    conn.close()
    cursor.close()
    
    return data
#===============================================================================
def tracking_with(data,track,imgs):
    '''
        This method displays tracking number, image of the item and status of delivery 
        to the user
    '''
    
    # Html code implementation
    print '''
        <fieldset>
        <legend>Tracking number</legend>
        <table>'''
    # gets the image from the tuple
    for img in imgs:
        (link,) = img
    # gets all the tracking number
    for row in data:
        (id,tracking,delivery,session) = row
        
        # if tracking number is mathed then proceed
        if (int(tracking) == int(track)):
            print '''
                <table>
            
                <tr>
                <td><img src= "%s" width = "100" height = "150"></td>
                <th> Tracking Number: <i>%s</i> </th>
                <th></th><th></th><th></th>
                <th> Delivery: %s</th>
                </tr>
            
                </table>
                ''' %(link,tracking,delivery)
    print '''</table></fieldset>'''


    # add buttons [click to checkout] and [Continue shopping]
################################################################################
def image(id):

    '''
        
        This method gets the link[image source] of the item by combining [JOIN] two database
        [item and trackinfo]  and comparing item.id with traackinfo.id
        
    '''
    
    # connect to database
    conn, cursor = getConnectionAndCursor()
    
    # build SQL
    # id is obtained from
    parameter = (id)
    sql = """
        SELECT link FROM item JOIN trackinfo WHERE item.id = %s
        """
    # execute the query
    cursor.execute(sql,parameter)
    
    # get the data from the database:
    data = cursor.fetchall()
    
    # clean up
    conn.close()
    cursor.close()
    
    return data

################################################################################
if __name__ == "__main__":

    # get form field data
    form = cgi.FieldStorage()
    #debugFormData(form)
    doHTMLHead("Project")
    
    # displays the tracking number status by JOINs two different database. This methods will show image,
    # tracking number and status of the delivery by combining different databases.
    if 'disply_track' in form:
        
        tracking_number = form['tracking_number'].value
        id = form['id'].value
        data = info_about_tracking()
        img = image(id)
        tracking_with(data,tracking_number,img)
    
    
    #Asks for the tracking number
    elif 'track' in form:
        id = form['id'].value
        tracking_form(id)
    
    # This will generate random package tracking number of the items
    # and check for any error in the from. If found then prompt the user
    # to fill it properly
    elif 'submit' in form:
        
        tracking = make_tracking_info()
        session = make_session_id()
        id = form['id'].value
        # choose between [Shipped,Delivered,Out for Delivery]
        detail = ['Shipped', 'Delivered', 'Out for Delivery']
        add_tracking(id,tracking,random.choice(detail),session)
        
        # checking if any of the submitted form field is empty
        try:
            firstname = form['firstname'].value
            lastname = form['lastname'].value
            address = form['address'].value
            city = form['city'].value
            state = form['state'].value
            zip = form['zip'].value
            session = form['session'].value
            shipping_info(id,firstname,tracking)
        
        # if anykind of error occur then prompt user to refill the form
        except KeyError:
            print "<strong> Please Fill Up The Form Properly. </strong>"
            form_shipping(id,session,tracking)

    # if user wants to check out then provide the user the address form
    # where he/she will input the correct address. all of these field are mandatory
    elif 'Checkout' in form:

        session = form['session'].value
        id = form['id'].value
        #tracking = form['tracking'].value
        form_shipping(id,session,1212)
        empty_cart()
    
    
    # if user wants to shop instead of checkout then show him the main page where he can pick
    # another guitar
    elif 'Continueshopping' in form:
        
        data = getAllItem()
        showAllItem(data)

    # gets the hidden fields and passes it into database and modifies the quantity of the guitar
    elif 'addtocart' in form:
        
        # hidden field of the item that has been added to the cart
        id = form['id'].value
        name = form['name'].value
        cost = form['cost'].value
        quantity = form['quantity'].value
        buyer_quantity = form['buyer_quantity'].value
        link = form['link'].value
        
        # add new element into the cart
        addtoCart(id,name,quantity,cost,link,buyer_quantity)
        session = make_session_id()
  
        # get the element from the cart
        data = getAllcart()
        total = costcalculation(data)
        
        # show the cart to the end user
        show_cart(data,total,session)
        
        # update the quantity
        new_quantity = int(quantity) - int(buyer_quantity)
        updateQuantity(id,new_quantity)
            


    # obtaining the hidden data fields and store/list it into the database
    # so that other user can buy it
    elif 'sell_submit' in form:
        
       name = form['name'].value
       cost = form['cost'].value
       quantity = form['quantity'].value
       link = form['link'].value
       
       addItem(name,quantity,cost,link)
       data = getAllItem()
       showAllItem(data)

    # prompts a selling form that asks about name,quantity,image link, cost of the guitar
    elif 'selling' in form:
        selling_form()

    # when user press into the item
    elif 'id' in form:
        
        id = form['id'].value
        data = getAllItem()
        (id,name,quantity,cost,link) = fields(data,id)
        showItem(id,name,quantity,cost,link)

    # displays all the items from the database into neat manner [Home page]
    else:
        data = getAllItem()
        showAllItem(data) # welcome screen

    doHTMLTail()




