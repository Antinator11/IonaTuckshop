from flask import Flask, render_template, session, request, redirect, url_for
from DatabaseManager import OrderingManager, ItemManager, UserManager, User, Item, GetTableHeaders, EndpointManager
from flask_login import login_manager, login_required, login_user, logout_user

app = Flask(__name__)

# Init all managers
# OrderMan = OrderingManager()
UserMan = UserManager()
ItemMan = ItemManager()

print(ItemMan)
loginman = login_manager.LoginManager()
loginman.init_app(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


## THIS CRAP IS USELESS TO THE ASSIGNMENT

@app.route('/')
def Landing():
    return render_template('index.html')


@app.route('/login')
def LoginPage():
    return render_template('signin.html')


@app.route('/menu/<search>')
@login_required
def Menu(search:Item):
    if search != 'NULL':
        return render_template('items.html', items=search)
    else:
        return render_template('items.html', items=ItemMan.Items)


@app.route('/loginredirect', methods=['POST'])
def Login():
    if request.method == "POST":
        EnteredP = request.form['Password']
        EnteredU = request.form['Username']
        if UserMan.FindUser(EnteredU) != False:
            NewUser = UserMan.LoadUser(EnteredU)
            if UserMan.LoginUser(NewUser, EnteredP) == True:
                login_user(NewUser)  # Authenticate the use with Flask
                UserMan.CurrentUser = NewUser  # Autheticate the user with the  manager
                return redirect(url_for('Menu', search='NULL'))
            else:
                return redirect(url_for('Landing'))
        else:
            return redirect(url_for('Landing'))
    else:
        return redirect(url_for('Landing'))


@app.route('/userlogout')
def LogoutUser():
    logout_user()
    return redirect(url_for('Landing'))


@app.route('/searchmenu', methods=['POST', 'GET'])
def SearchMenu():
    if request.method == 'POST':
        query = request.form['Search']
        ItemMan.SearchItems(query)
        return redirect(url_for('Menu', search=ItemMan.SearchItems(query)))
    else:
        return redirect(url_for('Menu', search='NULL'))


## -- Flask Endpoints -- ##

# Return the entire order table in JSON format to '/orderdata'
# :return render_template -> 'endpoints.html' with a data payload
@app.route('/orderdata')
def GetOrderData():
    return render_template('endpoints.html', json=EndpointManager.ConvertData(EndpointManager.GetOrderData(), "Orders"))


# Return the entire items entity in JSON format to '/itemdata'
# :return render_template -> 'endpoints.html' with a data payload
@app.route('/itemdata')
def GetItemData():
    return render_template('endpoints.html', json=EndpointManager.ConvertData(EndpointManager.GetAllItems(), 'Items'))


# Return the entire extra order info entity in JSON format to '/extraorderinfo'
# :return render_template -> 'endpoints.html' with a data payload
@app.route('/extraorderinfo')
def GetExtraOrderInfo():
    return render_template('endpoints.html',
                           json=EndpointManager.ConvertData(EndpointManager.GetExtraOrderInfo(), 'AdditionalOrderInfo'))


# Return the processed data from the databases in JSON format
# :return  render_template -> 'endpoints.html' with a data payload
@app.route('/processedata')
def GetProcessed():
    return render_template('endpoints.html',
                           json=EndpointManager.ConvertProcessedData(EndpointManager.ConstructProcessedData()))






# doing some stuff

@app.route('/test')
def Test():
    return render_template('endpoints.html', json=EndpointManager.LoadData())


# Check to see if the user is still valid
@loginman.user_loader
def load_user(user_id):
    return UserMan.LoadUserFromID(user_id)


if __name__ == '__main__':
    app.run()



