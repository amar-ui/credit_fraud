import os

from flask import *
import  pymysql
import  random

from werkzeug.utils import secure_filename

app=Flask(__name__)
app.secret_key="gd"
con=pymysql.connect(host="localhost",port=3306,user="root", passwd='',db="credit card fraud")
cmd=con.cursor()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login1',methods=['post'])
def login1():
    uname=request.form['textfield']
    pswd=request.form['textfield2']
    cmd.execute("SELECT * FROM `login` WHERE `user_name`='"+uname+"' AND `password`='"+pswd+"'")
    s=cmd.fetchone()
    if s is None:
        return ''' <script>alert("Invalid user name or password");window.location="/"</script>'''
    elif s[3]=='admin':
        return ''' <script>alert("Login successful");window.location="/adminhome"</script>'''
    elif s[3]=='dealer':
        return ''' <script>alert("Login successful");window.location="/dealerhome"</script>'''
    else:
        return ''' <script>alert("Invalid");window.location="/"</script>'''







@app.route('/registration')
def registration():
    return render_template('registration form.html')

@app.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')

@app.route('/dealer_management')
def dealer_managment():
    cmd.execute("select * from dealer")
    s=cmd.fetchall()
    return render_template('dealer mngmnt.html',val=s)

@app.route('/dealer_edit')
def dealer_edit():
    id=request.args.get('id')
    session['did']=id
    cmd.execute("select * from dealer mngmnt where login_id='"+str(id)+"'")
    s = cmd.fetchone()
    return render_template('dealer_edit.html',val=s)

@app.route('/dealer_delete')
def dealer_delete():
    id = request.args.get('id')
    cmd.execute("delete from dealer where login_id='"+str(id)+"'" )
    con.commit()
    return '''<script>alert("delete successfully");window.location="/adminhome"</script>'''

@app.route('/dealer_update',methods=['post','get'])
def dealer_update():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    dob = request.form['textfield3']
    gender = request.form['radiobutton']
    place = request.form['textfield4']
    post = request.form['textfield5']
    pin = request.form['textfield6']
    email = request.form['textfield7']
    phone = request.form['textfield8']

    cmd.execute("UPDATE `dealer`SET `fname`='"+fname+"',`lname`='"+lname+"',`dob`='"+dob+"',`gender`='"+gender+"',`place`='"+place+"',`post`='"+post+"',`pin`='"+pin+"',`email`='"+email+"',`phone`='"+phone+"' WHERE `login_id`='"+str(session['did'])+"' ")
    con.commit()
    return '''<script>alert("update successfully");window.location="/adminhome"</script>'''



@app.route('/add_dealer',methods=['get'])
def add_dealer():
    return render_template('add_dealer.html')

@app.route('/add_dealer1',methods=['post','get'])
def add_dealer1():
    fname=request.form['textfield']
    lname=request.form['textfield2']
    dob=request.form['textfield3']
    gender=request.form['radiobutton']
    place=request.form['textfield4']
    post=request.form['textfield5']
    pin=request.form['textfield6']
    email=request.form['textfield7']
    phone=request.form['textfield8']
    uname=request.form['textfield9']
    psd=request.form['textfield10']
    cmd.execute("INSERT INTO `login` VALUES(NULL,'"+uname+"','"+psd+"','dealer')")
    lid=con.insert_id()
    cmd.execute("INSERT INTO `dealer` VALUES(NULL,'"+str(lid)+"','"+fname+"','"+lname+"','"+dob+"','"+gender+"','"+place+"','"+post+"','"+pin+"','"+email+"','"+phone+"')")
    con.commit()
    return '''<script>alert("registered successfully");window.location="/adminhome"</script>'''



@app.route('/view_user')
def view_user():
    cmd.execute("select * from user")
    s = cmd.fetchall()
    return render_template('view user.html',val=s)

@app.route('/generate_pin')
def generate_pin():
    id=request.args.get('id')
    session['uid']=id
    return render_template('Generate_pin.html')

@app.route('/generate_pin1',methods=['get','post'])
def generate_pin1():
    cardno = request.form['cardno']
    bal = request.form['bal']
    edate = request.form['date2']
    ifsc = request.form['ifsc']
    pin=random.randint(1111,9999)
    cmd.execute("SELECT * FROM `pin` WHERE `user_id`='"+str(session['uid'])+"'")
    s=cmd.fetchone()
    if s is None:
        cmd.execute("INSERT INTO `pin` VALUES(NULL,'" + str(session['uid']) + "','" + cardno + "','" + edate + "','" + str(pin) + "',CURDATE(),'"+bal+"','"+ifsc+"')")
        cmd.execute("UPDATE `login` SET `user_type`='user' WHERE`login_id`='"+str(session['uid'])+"'")
        con.commit()
        return '''<script> alert("Success"); window.location="view_user"</script>'''
    else:
        return '''<script> alert("PIN already generated"); window.location="view_user"</script>'''
@app.route('/fake')
def fake():
    cmd.execute("SELECT `transaction`.*,`product`.`p_name`,`bill`.`tot_amt`,`user`.`fname`,`user`.`lname`  FROM  `product` JOIN `order_detiles` ON `order_detiles`.`prod_id`=`product`.`p_id` JOIN `user` ON `user`.`login_id`=`order_detiles`.`user_id` JOIN `bill` ON `user`.`login_id`=`bill`.user_id JOIN `transaction` ON `transaction`.`bill_id`=`bill`.`bill_id` AND `transaction`.`finished`='fake' GROUP BY `transaction`.`transaction_id`")
    s = cmd.fetchall()
    return render_template('view fake.html',val=s)
@app.route('/feedback')
def feedback():
    cmd.execute("SELECT `feedback`.*,`user`.`fname`,`user`.`lname`,`user`.`login_id` FROM `user` JOIN `feedback` ON `feedback`.`u_id`=`user`.`login_id`")
    s = cmd.fetchall()
    return render_template('view feedback.html',val=s)

@app.route('/dealerhome')
def dealerhome():
    return render_template('dealerhome.html')

@app.route('/product_view')
def product_view():
    cmd.execute("SELECT `product`.*,`stock`.`no_of_product` FROM `product` JOIN `stock` ON `product`.`p_id`=`stock`.`p_id`")
    s=cmd.fetchall()
    return render_template('View_products.html',val=s)



@app.route('/product_add_manage')
def product_add_manage():
    return render_template('product add and manage.html')

@app.route('/product_add_manage1',methods=['get','post'])
def product_add_manage1():
    prod=request.form['textfield']
    details=request.form['textfield3']
    price=request.form['textfield2']
    qty=request.form['textfield4']
    img=request.files['filefield']
    fname=secure_filename(img.filename)
    img.save(os.path.join('./static/product/',fname))
    cmd.execute("INSERT INTO `product` VALUES(NULL,'"+prod+"','"+price+"','"+details+"','"+str(fname)+"')")
    pid=con.insert_id()
    cmd.execute("INSERT INTO `stock` VALUES(NULL,'"+str(pid)+"','"+qty+"')")
    con.commit()
    return '''<script> alert("Success"); window.location="dealerhome"</script>'''

@app.route('/product_edit')
def product_edit():
    id=request.args.get('id')
    session['pid']=id
    cmd.execute("SELECT * FROM `product` WHERE `p_id`='"+str(id)+"'")
    s=cmd.fetchone()
    return render_template('product_edit.html',val=s)

@app.route('/product_edit1',methods=['get','post'])
def product_edit1():
    prod=request.form['textfield']
    details=request.form['textfield3']
    price=request.form['textfield2']
    cmd.execute("UPDATE `product` SET `p_name`='"+prod+"',`price`='"+price+"',`details`='"+details+"' WHERE `p_id`='"+str(session['pid'])+"'")
    con.commit()
    return '''<script> alert("Success"); window.location="product_view"</script>'''

@app.route('/change_image')
def change_image():
    id=request.args.get('id')
    session['pid']=id
    return render_template('change_image.html')

@app.route('/change_image1',methods=['get','post'])
def change_image1():
    img = request.files['filefield']
    fname = secure_filename(img.filename)
    img.save(os.path.join('./static/product/', fname))
    cmd.execute("UPDATE `product` SET `image`='"+str(fname)+"' WHERE `p_id`='"+str(session['pid'])+"'")
    con.commit()
    return '''<script> alert("Success"); window.location="product_view"</script>'''


@app.route('/product_delete')
def product_delete():
    id = request.args.get('id')
    cmd.execute("DELETE FROM `product` WHERE `p_id`='"+str(id)+"'")
    cmd.execute("DELETE FROM `stock` WHERE `p_id`='"+str(id)+"'")
    con.commit()
    return '''<script> alert("Success"); window.location="product_view"</script>'''

@app.route('/stock_view')
def stock_view():
    cmd.execute("SELECT `product`.*,`stock`.`no_of_product` FROM `product` JOIN `stock` ON `product`.`p_id`=`stock`.`p_id`")
    s=cmd.fetchall()
    return render_template('View_stock.html',val=s)

@app.route('/stock_updation')
def stock_updation():
    cmd.execute("SELECT * FROM `product`")
    s=cmd.fetchall()
    return render_template('stock updation.html',val=s)

@app.route('/stock_updation1',methods=['get','post'])
def stock_updation1():
    pid=request.form['select']
    qty=request.form['textfield3']
    cmd.execute("UPDATE `stock` SET `no_of_product`='"+qty+"' WHERE `p_id`='"+str(pid)+"'")
    con.commit()
    return '''<script> alert("Success");window.location="stock_updation"</script>'''

@app.route('/view_order')
def view_order():
    cmd.execute("SELECT `user`.*,`product`.`p_name`,`order_detiles`.`quantity`,`bill`.`tot_amt`,`bill`.`date`,`order_detiles`.`ord_id` FROM `bill` JOIN `user` ON `bill`.`user_id`=`user`.`login_id` JOIN `order_detiles` ON `order_detiles`.`user_id`=`user`.`login_id` JOIN `product` ON `order_detiles`.`prod_id`=`product`.`p_id` AND `order_detiles`.`booking_satus`='pending' GROUP BY order_detiles.ord_id")
    s=cmd.fetchall()
    return render_template('view order accept and reject.html',val=s)

@app.route('/accept')
def accept():
    id=request.args.get('id')
    session['oid']=id
    print('id',id)
    return render_template("set_delivery_date.html")

@app.route('/accept1',methods=['get','post'])
def accept1():
    date=request.form['date2']
    cmd.execute("UPDATE `order_detiles` SET `booking_satus`='accepted',`del_date`='"+date+"' WHERE `ord_id`='"+str(session['oid'])+"'")
    con.commit()
    return '''<script> alert("Accepted"); window.location="view_order"</script>'''

@app.route('/reject',methods=['get','post'])
def reject():
    id = request.args.get('id')
    cmd.execute("UPDATE `order_detiles` SET `booking_satus`='rejected' WHERE `ord_id`='"+str(id)+"'")
    con.commit()
    return '''<script> alert("Rejected"); window.location="view_order"</script>'''


@app.route('/complaint_reply')
def complaint_reply():
    cmd.execute("SELECT `product`.`p_name`,`user`.`fname`,`user`.`fname`,`complaint`.* FROM `complaint` JOIN `user` ON `user`.`login_id`=`complaint`.`u_id` JOIN `product` ON `product`.`p_id`=`complaint`.`p_id` AND `complaint`.`reply`='pending'")
    s=cmd.fetchall()
    return render_template('view complaint send replay.html',val=s)

@app.route('/reply')
def reply():
    id=request.args.get('id')
    session['cid']=id
    return render_template("reply.html")

@app.route('/reply1',methods=['get','post'])
def reply1():
    reply=request.form['rep']
    cmd.execute("UPDATE `complaint` SET `reply`='"+reply+"' WHERE `cmp_id`='"+str(session['cid'])+"'")
    con.commit()
    return '''<script> alert("Success"); window.location="complaint_reply"</script>'''














if __name__ == '__main__':
    app.run(debug=True)