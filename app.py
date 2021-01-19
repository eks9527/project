from flask import Flask, render_template
from flask_pymongo import PyMongo
# from kafka_producer_gt import *
# from kafka_producer_rt import *
# from kafka_producer_mt import *


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://eks210017:eks210017@cluster0.yrvuu.mongodb.net/mydatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)
total = 0


# 建立網頁首頁的回應方式
@app.route('/')
def index():
    return '<h1>Hello Wellcome!</h1>'

# 會員介面
# <name>: username
@app.route('/user/<name>')
def user_interface(name):
    users = mongo.db.users.find({"name" : name})
    items = mongo.db.items.find({}, {'_id':0})
    totals= total(name)
    return render_template('user.html', users=users, items=items, total=totals)

# 給會員介面 total用的
def total(name):
    total = 0
    users = mongo.db.users.find({"name" : name})
    items = mongo.db.items.find({}, {'_id':0})
    for user in users:
        for i in user['cart']:
            if i == 1:
                total = total + 1 * 10
                # print(total)
            if i == 2:
                total = total + 1 * 20
            if i is None:
                total = 0
    return total

# 更改 會員 的 in_stroe 的狀態
# <name>:username
# <status>: 0 or 1
@app.route('/user_in_or_out/<name>/<status>')
def status_of_store(name, status):
    users = mongo.db.users.update_one({'name':name}, {'$set':{'in_store':bool(int(status))}})
    return '<h1>User, in_store: {}!</h1>'.format(bool(int(status)))

# 把產品加入到會員的購物車
# <name>:username
# <item_id>:商品id
@app.route('/user/cart/plus/<name>/<item_id>')
def update_plus_cart(name, item_id):
    res = mongo.db.users.update_one({'name':name},{'$push':{'cart':int(item_id)}})
    return '<h1>Add product success!</h1>'

# 會員的購物車的產品減少
# <name>:username
# <item_id>:商品id
@app.route('/user/cart/delete/<name>/<item_id>')
def update_delete_cart(name, item_id):
    res = mongo.db.users.update_one({'name':name},{'$pop':{'cart':int(item_id)}})
    return '<h1>Delete product success!</h1>'

# 管理者的介面
@app.route('/manager')
def manager():
    users = mongo.db.users.find({"in_store": True})
    # items = mongo.db.items.find({}, {'_id':0})
    nums = mongo.db.items.aggregate([{'$count':'nums of product'}])
    return render_template('manager.html', nums=nums, users=users)

# 總共有多少個商品 (回傳數字)
@app.route('/how_many_products')
def get_num_items():
    nums = mongo.db.items.aggregate([{'$count':'num of item_id'}])
    return render_template('num_item.html', nums=nums)

# 刪除一個商品 'item_name': 'Coke'
@app.route('/delete_item')
def delete_item():
    de = mongo.db.items.delete_one({'item_name': 'Coke'})
    return '<h1>Delete item success!</h1>'
#
# 新增一個商品
@app.route('/add_item')
def add_item():
    list ={
        'item_id': 2503,
        'item_name': "Coke",
        'item_stock': 1,
        'price': 10
    }
    ad = mongo.db.items.insert_one(list)
    return '<h1>Add item success!</h1>'


@app.route('/<item_name>/take')
def item_name_take(item_name):
    thing_1 = mongo.db.items.update_one({'item_name': item_name},
                                   {'$inc': {'user_take': 1, 'price': 10},
                                    "$currentDate":{'date': True}})

    items_1 = mongo.db.items.find_one({'item_name': item_name}, {'_id': 0})
    return items_1

@app.route('/<item_name>/re')
def item_name_re(item_name):
    thing_2 = mongo.db.items.update_one({'item_name': item_name},
                                   {'$inc': {'user_take': -1, 'price': -10},
                                    "$currentDate":{'date': True}})

    items_2 = mongo.db.items.find_one({'item_name': item_name}, {'_id': 0})
    return items_2

# @app.route('/to_kafka/gt')
# def to_kafka_gt():
#     go_kafka_gt()
#     return "ok write to kafka gt"
#
# @app.route('/to_kafka/rt')
# def to_kafka_rt():
#     go_kafka_rt()
#     return "ok write to kafka rt"
#
# @app.route('/to_kafka/mt')
# def to_kafka_mt():
#     go_kafka_mt()
#     return "ok write to kafka mt"


# 啟動網站伺服器
app.run(host='0.0.0.0', debug=True, port=5002)
