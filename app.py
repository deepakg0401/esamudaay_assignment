from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/order', methods=['POST'])
def add_message():
    content = request.get_json(force=True)
    # print(content)
    # print(content["order_items"])
    try:
        order_list=list(content["order_items"])
        item_total=0
        delivery_fee=0
        for mp in order_list:
            item_total+=mp["quantity"]*mp["price"]
        km_tmp=content["distance"]/1000
        if km_tmp>=0 and km_tmp<10:
            delivery_fee=50
        elif km_tmp>=10 and km_tmp<20:
            delivery_fee=100
        elif km_tmp>=20 and km_tmp<50:
            delivery_fee=500
        elif km_tmp>=50:
            delivery_fee=1000
        delivery_fee*=100
        total=item_total+delivery_fee
        try:
            if content["offer"]["offer_type"]=="DELIVERY":
                total-=delivery_fee
            elif content["offer"]["offer_type"]=="FLAT":
                discount=min(content["offer"]["offer_val"],total)
                total=total-discount
        except:
            pass 
    except:
        return jsonify({"message":"invalid input"})


    return jsonify({"order_total":total})
 

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
