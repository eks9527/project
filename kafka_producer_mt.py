from confluent_kafka import Producer
import sys
# import time
# import pymongo
# from bson.codec_options import CodecOptions
# import pytz


def go_kafka_mt():
    import pymongo
    from bson.codec_options import CodecOptions
    import pytz
    import time

    client = pymongo.MongoClient("mongodb+srv://eks210017:eks210017@cluster0.yrvuu.mongodb.net/mydatabase?retryWrites=true&w=majority")
    options = CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Taipei'))
    db = client.get_default_database(codec_options=options)

    # items_green_tea = db.items.find_one({'item_name': 'GreenTea'}, {'_id': 0})
    # t_time_gt = items_green_tea['date'].strftime('%Y-%m-%d %H:%M:%S')
    # taiwan_time_gt = db.items.update_one({'item_name': "GreenTea"}, {'$set': {'taiwan_time': t_time_gt}})
    #
    # items_red_tea = db.items.find_one({'item_name': 'RedTea'}, {'_id': 0})
    # t_time_rt = items_red_tea['date'].strftime('%Y-%m-%d %H:%M:%S')
    # taiwan_time_rt = db.items.update_one({'item_name': "RedTea"}, {'$set': {'taiwan_time': t_time_rt}})

    items_milk_tea = db.items.find_one({'item_name': 'MilkTea'}, {'_id': 0})
    t_time_mt = items_milk_tea['date'].strftime('%Y-%m-%d %H:%M:%S')
    taiwan_time_mt = db.items.update_one({'item_name': "MilkTea"}, {'$set': {'taiwan_time': t_time_mt}})

    # print(items_coke['item_name'], items_coke['user_take'], items_coke['price'])
    # print(items_tea['item_name'], items_tea['user_take'], items_tea['price'])

    # 用來接收從Consumer instance發出的error訊息
    def error_cb(err):
        print('Error: %s' % err)


    props = {
        # Kafka集群在那裡? 10.1.0.87:9092
        'bootstrap.servers': '10.1.0.87:9092',  # <-- 置換成要連接的Kafka集群
        'error_cb': error_cb                    # 設定接收error訊息的callback函數
    }
    # 步驟2. 產生一個Kafka的Producer的實例
    producer = Producer(props)
    # 步驟3. 指定想要發佈訊息的topic名稱
    topicName_1 = 'items'
    topicName_2 = 'items2'
    topicName_3 = 'items3'
    msgCounter = 0
    try:
        # produce(topic, [value], [key], [partition], [on_delivery], [timestamp], [headers])
        # producer.produce(topicName_1, '{}  數量: {} 價格: {} date: {}'.format(items_green_tea['item_name'], items_green_tea['user_take'], items_green_tea['price'], items_green_tea['taiwan_time']), '商品')
        # producer.produce(topicName_2, '{}  數量: {} 價格: {} date: {}'.format(items_red_tea['item_name'], items_red_tea['user_take'], items_red_tea['price'], items_red_tea['taiwan_time']), '商品')
        producer.produce(topicName_3, '奶茶  數量: {} 價格: {} '.format(items_milk_tea['user_take'], items_milk_tea['price']), '商品3')
        producer.flush()
        # msgCounter += 2
        print('Send ' + ' messages to Kafka')
    except BufferError as e:
        # 錯誤處理
        sys.stderr.write('%% Local producer queue is full ({} messages awaiting delivery): try again\n'
                         .format(len(producer)))
    except Exception as e:
        print(e)
    # 步驟5. 確認所在Buffer的訊息都己經送出去給Kafka了
    producer.flush()
