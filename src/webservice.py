import datetime

from boto.gs import user
# from boto.gs import pin

from flask import *
import  pymysql
from sklearn.ensemble import RandomForestClassifier, IsolationForest

app=Flask(__name__)
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail
con=pymysql.connect(host="localhost",port=3306,user="root", passwd='',db="credit card fraud")
cmd=con.cursor()


@app.route('/login',methods=['post'])
def main():
    con = pymysql.connect(host="localhost", port=3306, user="root", passwd='', db="credit card fraud")
    cmd = con.cursor()
    uname=request.form['uname']
    passwd=request.form['psd']
    cmd.execute("SELECT * FROM `login` WHERE `user_name`='"+uname+"' AND `password`='"+passwd+"'")
    s=cmd.fetchone()
    id=s[0]
    if s is None:
        return jsonify({"result":"error"})
    elif s[3] == 'user':
        return jsonify({"result":"success","id":id})
    else:
        return jsonify({"result":"error"})


@app.route('/registration',methods=['post'])
def registration():
    fname=request.form['fname']
    lname=request.form['lname']
    gender=request.form['gender']
    email=request.form['email']
    phone=request.form['phone']
    uname=request.form['uname']
    password=request.form['password']
    hname=request.form['hname']
    post=request.form['post']
    place=request.form['place']
    pin=request.form['pin']
    dob=request.form['dob']
    qstn=request.form['qstn']
    ans=request.form['ans']

    cmd.execute("INSERT INTO `login` VALUES(NULL,'" + uname + "','" + password + "','user')")
    id = con.insert_id()
    cmd.execute("INSERT INTO `user` VALUES(NULL,'" + str(id) + "','" + fname + "','" + lname + "','" + dob + "','" + gender + "','" + hname + "','" + place + "','" + post + "','" + pin + "','" + email + "','" + phone + "')")
    cmd.execute("INSERT INTO `security_question` VALUES(NULL,'"+str(id)+"',CURDATE(),'"+qstn+"','"+ans+"')")
    con.commit()
    return jsonify({'task': 'success'})


@app.route('/feedback',methods=['post'])
def feedback():
    fdb = request.form['fbk']
    lid = request.form['lid']
    cmd.execute("INSERT INTO `feedback` VALUES(NULL,'"+str(lid)+"','"+fdb+"',CURDATE())")
    con.commit()
    return jsonify({'task': 'success'})



@app.route('/view_products',methods=['post'])
def view_products():
    con = pymysql.connect(host="localhost", port=3306, user="root", passwd='', db="credit card fraud")
    cmd = con.cursor()
    cmd.execute("SELECT `product`.* FROM `product` JOIN `stock` ON `stock`.`p_id`=`product`.`p_id`  AND NOT `stock`.`no_of_product`=0")
    row_headers = [x[0] for x in cmd.description]
    products = cmd.fetchall()
    json_data = []
    for product in products:
        json_data.append(dict(zip(row_headers, product)))
    return jsonify(json_data)

@app.route('/complaints',methods=['post'])
def complaints():
    comp = request.form['comp']
    lid = request.form['lid']
    pid = request.form['pid']
    cmd.execute("INSERT INTO `complaint` VALUES(NULL,'"+str(lid)+"','"+str(pid)+"','"+comp+"',CURDATE(),'pending')")
    con.commit()
    return jsonify({'task': 'success'})

@app.route('/view_comp_reply',methods=['post'])
def view_comp_reply():
    lid = request.form['lid']
    cmd.execute("SELECT `complaint`.*,`product`.`p_name` FROM `complaint` JOIN `product` ON `complaint`.`p_id`=`product`.`p_id` AND `complaint`.`u_id`='"+str(lid)+"'")
    row_headers = [x[0] for x in cmd.description]
    products = cmd.fetchall()
    json_data = []
    for product in products:
        json_data.append(dict(zip(row_headers, product)))
    return jsonify(json_data)

@app.route('/buy_items', methods=['post', 'get'])
def buy_items():
    bid =request.form['bid']
    pid=request.form['pid']
    lid=request.form['lid']
    qty=request.form['qty']
    cmd.execute("SELECT `price` FROM `product` WHERE `p_id`='"+str(pid)+"'")
    s=cmd.fetchone()
    print(s)
    cmd.execute("INSERT INTO `order_detiles` VALUES(NULL,'"+str(bid)+"','"+str(pid)+"','"+str(lid)+"',CURDATE(),'pending','pending','"+qty+"','"+str(s[0])+"')")
    cmd.execute("UPDATE `stock` SET `no_of_product`=`no_of_product`-'"+qty+"' WHERE `p_id`='"+str(pid)+"'")
    con.commit()
    return jsonify({'result': "success"})

@app.route('/add_to_cart', methods=['post', 'get'])
def add_to_cart():
    bid =request.form['bid']
    pid=request.form['pid']
    lid=request.form['lid']
    qty=request.form['qty']
    cmd.execute("SELECT `price` FROM `product` WHERE `p_id`='" + str(pid) + "'")
    s = cmd.fetchone()
    print(s)
    cmd.execute("INSERT INTO `order_detiles` VALUES(NULL,'"+str(bid)+"','"+str(pid)+"','"+str(lid)+"',CURDATE(),'pending','cart','"+qty+"','"+str(s[0])+"')")
    con.commit()
    return jsonify({'result': "success"})

@app.route('/bill', methods=['post', 'get'])
def bill():
    con = pymysql.connect(host="localhost", port=3306, user="root", passwd='', db="credit card fraud")
    cmd = con.cursor()
    lid =request.form['lid']
    bid=request.form['bid']

    cmd.execute("SELECT `product`.`price`,`order_detiles`.`quantity` FROM `order_detiles` JOIN `product` ON `order_detiles`.`prod_id`=`product`.`p_id` AND `order_detiles`.`bill_id`='"+str(bid)+"'")
    res=cmd.fetchall()
    print(res)
    tot=0
    for i in res:
        price=int(i[0])*int(i[1])
        tot=tot+price
    print(tot)
    cmd.execute("INSERT INTO `bill` VALUES(NULL,'"+str(lid)+"','"+str(tot)+"',CURDATE())")
    con.commit()
    return jsonify({'result': "success"})

@app.route('/view_cart_details',methods=['get','post'])
def view_cart_details():
    lid=request.form['lid']
    cmd.execute("SELECT `product`.`p_name`,`product`.`price`,`product`.`details`,`product`.`image`,`order_detiles`.*,`product`.`p_id` FROM `order_detiles` JOIN `product` ON `order_detiles`.`prod_id`=`product`.`p_id` AND `order_detiles`.`booking_satus`='cart' AND `order_detiles`.`user_id`='"+str(lid)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    print(results)
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/remove', methods=['post', 'get'])
def remove():
    oid =request.form['oid']
    pid=request.form['pid']
    cmd.execute("DELETE FROM `order_detiles` WHERE `ord_id`='"+str(oid)+"' AND `prod_id`='"+str(pid)+"'")
    con.commit()
    return jsonify({'result': "success"})

@app.route('/addtocart2', methods=['post', 'get'])
def addtoCart2():
    oid =request.form['oid']
    pid = request.form['pid']
    qty=request.form['qty']
    cmd.execute("UPDATE `order_detiles` SET `booking_satus`='pending' WHERE `ord_id`='"+str(oid)+"'")
    cmd.execute("UPDATE `stock` SET `no_of_product`=`no_of_product`-'"+qty+"' WHERE `p_id`='"+str(pid)+"'")
    con.commit()
    return jsonify({'result': "success"})

@app.route('/my_orders',methods=['GET','POST'])
def my_orders():
    lid=request.form['lid']
    cmd.execute("SELECT `product`.`p_name`,`product`.`image`,`order_detiles`.`quantity`,`order_detiles`.`booking_satus`,`order_detiles`.`del_date`,`bill`.`tot_amt` FROM `bill` JOIN `user` ON `user`.`login_id`=`bill`.`user_id` JOIN `order_detiles` ON `order_detiles`.`bill_id`=`bill`.`bill_id` JOIN `product` ON `product`.`p_id` = `order_detiles`.`prod_id` AND `order_detiles`.`user_id`='"+str(lid)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        row = []
        for r in result:
            row.append(str(r))
        json_data.append(dict(zip(row_headers, row)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/billid', methods=['post', 'get'])
def billid():

     cmd.execute("SELECT `bill_id` FROM `bill`")
     s=cmd.fetchone()
     if s is None:
         bill_id=1
         print("bill======================", bill_id)
         return jsonify(bill_id)
     else:
         cmd.execute("SELECT max(`bill_id`)+1 as bill_id FROM `bill`")
         row_headers = [x[0] for x in cmd.description]
         results = cmd.fetchall()
         print("id",results[0])
         json_data = []
         for result in results:
             json_data.append(dict(zip(row_headers, result)))
         con.commit()
         print("bill======================",json_data)
         return jsonify(json_data)

@app.route('/transaction', methods=['post', 'get'])
def pay():
        # from django.db import transaction
        con = pymysql.connect(host="localhost", port=3306, user="root", passwd='', db="credit card fraud")
        cmd = con.cursor()
        bid = request.form['bid']
        # print("bid",bid)
        lid = request.form['lid']
        lat = request.form['lati']
        lon = request.form['longi']
        # bnk = request.POST['bnk']
        ifsc = request.form['ifsc']
        # cvv = request.form['ccv']
        # amt = request.POST['amt']
        # pin = request.POST['pin']
        exp = request.form['exp']
        ano = request.form['crd']

        try:
            print(lat, lon)
            if lat == '':
                lat = 11.35678
                lon = 75.3456

            print(lid, "===========")
            cmd.execute("SELECT * FROM `pin` WHERE `user_id`='"+str(lid)+"' AND `card_no`='"+ano+"' AND `expiry_date`='"+exp+"' AND `ifsc_code`='"+ifsc+"'")
            print("SELECT * FROM `pin` WHERE `user_id`='"+str(lid)+"' AND `card_no`='"+ano+"' AND `expiry_date`='"+exp+"' AND `ifsc_code`='"+ifsc+"'")
            bnkob = cmd.fetchone()
            print("gf",bnkob)
            bal=bnkob[6]
            print("bal",bal)
            cmd.execute("SELECT SUM(`amount`) FROM `order_detiles` WHERE `bill_id`='"+str(bid)+"'")
            amt = cmd.fetchone()
            total=amt[0]
            print("amt",amt)
            # print("tot",tot)
            if bnkob is not None:
                tot = bal- total

                cmd.execute("SELECT `transaction`.*,`bill`.`tot_amt`  FROM `transaction` JOIN `bill` ON `bill`.`bill_id`=`transaction`.`bill_id` AND `transaction`.`finished`='success' and `bill`.`user_id`="+str(lid))
                res=cmd.fetchall()
                cmd.execute(
                    "SELECT `transaction`.*,`bill`.`tot_amt`  FROM `transaction` JOIN `bill` ON `bill`.`bill_id`=`transaction`.`bill_id` AND `transaction`.`finished`='fake' and `bill`.`user_id`=" + str(
                        lid))
                res1 = cmd.fetchall()

                cmd.execute("SELECT `transaction`.*,`bill`.`tot_amt`,DAYOFWEEK(`transaction`.`date`),HOUR(`time`)  FROM `transaction` JOIN `bill` ON `bill`.`bill_id`=`transaction`.`bill_id` AND `bill`.`user_id`='"+str(lid)+"'")
                tobs = cmd.fetchall()
                # cmd.execute("SELECT `transaction`.*,`bill`.`tot_amt`  FROM `transaction` JOIN `bill` ON `bill`.`bill_id`=`transaction`.`bill_id` AND `bill`.`user_id`='"+str(lid)+"'")
                # tobs1=cmd.fetchone()
                # print("tob1s", tobs1)
                print("tobs",tobs)

                if len(res) >4 and len(res1>4):
                    from sklearn.ensemble import RandomForestClassifier

                    xtrain = []
                    ytrain = []
                    for i in tobs:
                        if i[6] == "success":
                            time = 0
                            if int(i[9]) < 6:
                                time = 0
                            elif int(i[9]) < 12:
                                time = 20
                            elif int(i[9]) < 18:
                                time = 30
                            else:
                                time = 40

                            xtrain.append([i[2], i[3], time, int(i[8]), float(i[7])])
                            ytrain.append(1)
                        else:
                            time = 0
                            if int(i[9]) < 6:
                                time = 0
                            elif int(i[9]) < 12:
                                time = 20
                            elif int(i[9]) < 18:
                                time = 30
                            else:
                                time = 40

                            xtrain.append([i[2], i[3], time, int(i[8]), float(i[7])])
                            ytrain.append(0)
                    clf = RandomForestClassifier(n_estimators=100)

                    # Training the model on the training dataset
                    # fit function is used to train the model using the training sets as parameters
                    clf.fit(xtrain, ytrain)

                    # performing predictions on the test dataset
                    cmd.execute("SELECT DAYOFWEEK(CURDATE()),HOUR(CURTIME())")
                    s = cmd.fetchone()
                    time = 0
                    if int(s[1]) < 6:
                        time = 0
                    elif int(s[1]) < 12:
                        time = 20
                    elif int(s[1]) < 18:
                        time = 30
                    else:
                        time = 40
                    reslat=[]
                    reslat.append([ lat, lon, time, int(s[0]), total])

                    y_pred = clf.predict(reslat)

                    if y_pred[0] == 1:
                        cmd.execute(
                            "INSERT INTO `transaction` VALUES(NULL,'" + str(bid) + "','" + str(lat) + "','" + str(
                                lon) + "',CURDATE(),CURTIME(),'success')")
                        cmd.execute("UPDATE `pin` SET `balance`=`balance`-'" + str(tot) + "' WHERE `user_id`='" + str(
                            lid) + "'")
                        con.commit()
                        print("jgaif")
                        data = {"result": "ok"}
                        r = json.dumps(data)
                        print("r", r)
                        return jsonify({"result": "success"})
                    else:

                        data = {"result": "fake"}
                        r = json.dumps(data)
                        cmd.execute("INSERT INTO `transaction` VALUES(NULL,'" + str(
                            bid) + "','" + lat + "','" + lon + "',CURDATE(),CURTIME(),'fake')")
                        con.commit()
                        cmd.execute("SELECT email FROM `user` WHERE `login_id`='" + str(lid) + "'")
                        s1 = cmd.fetchone()
                        print(s1)
                        email = s1[0]
                        try:
                            gmail = smtplib.SMTP('smtp.gmail.com', 587)
                            gmail.ehlo()
                            gmail.starttls()
                            gmail.login('frauddetection1234@gmail.com', 'fraud@1234')
                        except Exception as e:
                            print("Couldn't setup email!!" + str(e))
                        msg = MIMEText("FAKE TRANSACTION DETECTED : -transaction amount is" + str(tot))
                        print(msg)
                        msg['Subject'] = 'credit card'
                        msg['To'] = email
                        msg['From'] = 'frauddetection1234@gmail.com'
                        try:
                            gmail.send_message(msg)
                        except Exception as e:
                            print("COULDN'T SEND EMAIL", str(e))
                        con.commit()
                        return jsonify({"result": "error"})
                else:

                    reslat = []
                    reslong = []
                    resamount = []
                    if bnkob is not None:

                        for i in tobs:
                            print("i",i[2])
                            print("f")

                            if i[6] =="success":
                                time=0
                                if int(i[9])<6:
                                    time=0
                                elif int(i[9])<12:
                                    time=20
                                elif int(i[9]) < 18:
                                    time=30
                                else:
                                    time=40

                                reslat.append(["0", i[2], i[3],time,int(i[8]),float(i[7])])
                                reslong.append(["0", i[3]])
                                resamount.append(["0", i[7]])
                                print("hello")
                        cmd.execute("SELECT DAYOFWEEK(CURDATE()),HOUR(CURTIME())")
                        s=cmd.fetchone()
                        time = 0
                        if int(s[1]) < 6:
                            time = 0
                        elif int(s[1]) < 12:
                            time = 20
                        elif int(s[1]) < 18:
                            time = 30
                        else:
                            time = 40
                        reslat.append(["0", lat, lon,time,int(s[0]),total])

                        print("reslat",reslat)

                        resloc = outlier(reslat)
                        print("Amount")
                        resmt = outlier(resamount)
                        resll = resloc[len(resloc) - 1]
                        print("resl1",resll)
                        if resll != -1:
                            cmd.execute("INSERT INTO `transaction` VALUES(NULL,'" + str(bid) + "','" + str(lat) + "','" + str(lon) + "',CURDATE(),CURTIME(),'success')")
                            cmd.execute("UPDATE `pin` SET `balance`=`balance`-'" + str(tot) + "' WHERE `user_id`='" + str(lid) + "'")
                            con.commit()
                            print("jgaif")
                            data = {"result": "ok"}
                            r = json.dumps(data)
                            print("r",r)
                            return jsonify({"result": "success"})
                        else:

                            data = {"result": "fake"}
                            r = json.dumps(data)
                            cmd.execute("INSERT INTO `transaction` VALUES(NULL,'" + str(bid) + "','" + lat + "','" + lon + "',CURDATE(),CURTIME(),'fake')")
                            con.commit()
                            cmd.execute("SELECT email FROM `user` WHERE `login_id`='" + str(lid) + "'")
                            s1 = cmd.fetchone()
                            print(s1)
                            email = s1[0]
                            try:
                                gmail = smtplib.SMTP('smtp.gmail.com', 587)
                                gmail.ehlo()
                                gmail.starttls()
                                gmail.login('frauddetection1234@gmail.com', 'fraud@1234')
                            except Exception as e:
                                print("Couldn't setup email!!" + str(e))
                            msg = MIMEText("FAKE TRANSACTION DETECTED : -transaction amount is" + tot)
                            print(msg)
                            msg['Subject'] = 'credit card'
                            msg['To'] = email
                            msg['From'] = 'frauddetection1234@gmail.com'
                            try:
                                gmail.send_message(msg)
                            except Exception as e:
                                print("COULDN'T SEND EMAIL", str(e))
                            con.commit()
                            return jsonify({"result":"error"})
                    else:
                        data = {"result": "ok"}
                        r = json.dumps(data)
                        return jsonify({"result": "fake"})
        except:

            data = {"result": "ok"}
            r = json.dumps(data)
            cmd.execute("SELECT email FROM `user` WHERE `login_id`='" + str(lid) + "'")
            s1 = cmd.fetchone()
            print(s1)
            email = s1[0]
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)
                gmail.ehlo()
                gmail.starttls()
                gmail.login('frauddetection1234@gmail.com', 'fraud@1234')
            except Exception as e:
                print("Couldn't setup email!!" + str(e))
            msg = MIMEText("FAKE TRANSACTION DETECTED : -transaction amount is" + str(tot))
            print(msg)
            msg['Subject'] = 'credit card'
            msg['To'] = email
            msg['From'] = 'frauddetection1234@gmail.com'
            try:
                gmail.send_message(msg)
            except Exception as e:
                print("COULDN'T SEND EMAIL", str(e))
            con.commit()
            return jsonify({"result": "error"})

# @app.route('/transaction', methods=['post', 'get'])
# def transaction():ra
#     bid =request.form['bid']
#     lid =request.form['lid']
#     lati=request.form['lati']
#     longi=request.form['longi']
#     cmd.execute("SELECT `tot_amt` FROM `bill` WHERE `bill_id`='"+str(bid)+"'")
#     tot=cmd.fetchone()
#     cmd.execute("INSERT INTO `transaction` VALUES(NULL,'"+str(bid)+"','"+lati+"','"+longi+"',CURDATE(),CURTIME(),'finished')")
#     cmd.execute("UPDATE `pin` SET `balance`=`balance`-'"+str(tot)+"' WHERE `user_id`='"+str(lid)+"'")
#     con.commit()
#     return jsonify({'result': "success"})

@app.route('/t_history',methods=['GET','POST'])
def t_history():
    lid=request.form['lid']
    cmd.execute("SELECT `transaction`.*,`product`.`p_name`,`bill`.`tot_amt`  FROM `product` JOIN `order_detiles` ON `order_detiles`.`prod_id`=`product`.`p_id` JOIN `bill` ON `bill`.`bill_id`=`order_detiles`.`bill_id` JOIN `transaction` ON `transaction`.`bill_id`=`bill`.`bill_id` AND `bill`.`user_id`='"+str(lid)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        row = []
        for r in result:
            row.append(str(r))
        json_data.append(dict(zip(row_headers, row)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/ac_details',methods=['GET','POST'])
def ac_details():
    lid=request.form['lid']
    cmd.execute("SELECT pin.*,`user`.* FROM `pin` JOIN `user` ON `user`.`login_id`=`pin`.`user_id` WHERE `pin`.`user_id`='"+str(lid)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        row = []
        for r in result:
            row.append(str(r))
        json_data.append(dict(zip(row_headers, row)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/sec_qstn',methods=['GET','POST'])
def sec_qstn():
    lid=request.form['lid']
    cmd.execute("SELECT * FROM `security_question` WHERE `user_id`='"+str(lid)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        row = []
        for r in result:
            row.append(str(r))
        json_data.append(dict(zip(row_headers, row)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/answer',methods=['GET','POST'])
def answer():
    print(request.form)
    bid=request.form['bid']
    lati=request.form['lati']
    longi=request.form['longi']
    lid=request.form['lid']
    print(lati)
    ans=request.form['ans']
    print(longi)

    cmd.execute("SELECT * FROM `security_question` WHERE `user_id`='"+str(lid)+"' AND `answer`='"+ans+"'")
    results = cmd.fetchone()
    print(results)
    if results is not None:
       cmd.execute("SELECT SUM(`amount`) FROM `order_detiles` WHERE `bill_id`='"+str(bid)+"'")
       s1=cmd.fetchone()
       cmd.execute("UPDATE `pin` SET `balance`=`balance`='"+str(s1[0])+"' WHERE `user_id`='"+str(lid)+"'")
       cmd.execute("INSERT INTO `transaction` VALUES(NULL,'"+str(bid)+"','"+lati+"','"+longi+"',CURDATE(),CURTIME(),'success')")
       con.commit()
       return jsonify({"task": "success"})
    else:
        cmd.execute("INSERT INTO `transaction` VALUES(NULL,'"+str(bid)+"','"+lati+"','"+longi+"',CURDATE(),CURTIME(),'fake')")
        con.commit()
        return jsonify({"task":"failed"})



def outlier(res):
    print("outlier")
    ano = []

    print(res)

    model = IsolationForest(n_estimators=50, max_samples='auto', contamination=float(0.1), max_features=1.0)
    model.fit(res)

    ano.append(model.predict(res))
    print(ano)
    anomaly = []
    idvalue = 0
    for ij in ano:
        print(ij)
    res=[]
    for index, value in enumerate(ij, start=1):
        # print(list((index, value)))  # print(k)
        res.append(value)
    print(res)
    return res

if  __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)