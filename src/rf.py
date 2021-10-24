from sklearn.ensemble import RandomForestClassifier
import pymysql
con = pymysql.connect(host="localhost", port=3306, user="root", passwd='', db="credit card fraud")
cmd = con.cursor()

cmd.execute("SELECT `transaction`.*,`bill`.`tot_amt`,DAYOFWEEK(`transaction`.`date`),HOUR(`time`)  FROM `transaction` JOIN `bill` ON `bill`.`bill_id`=`transaction`.`bill_id` ")
s=cmd.fetchall()
xtrain=[]
ytrain=[]
for i in s:
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

        xtrain.append([ i[2], i[3], time, int(i[8]), float(i[7])])
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
y_pred = clf.predict([xtrain[0]])
