import mysql.connector
import datetime
import sys
import time
from PyQt5 import QtCore, QtWidgets, uic

mydb = mysql.connector.connect(host="localhost", user="smoke", password="hellomoto", database="car", autocommit=True)
mycursor = mydb.cursor()

mycursor.execute("DROP TABLE IF EXISTS slot")
mycursor.execute("DROP TABLE IF EXISTS duration")
mycursor.execute("DROP TABLE IF EXISTS entry")
mycursor.execute("DROP TABLE IF EXISTS exits")
mycursor.execute("DROP TABLE IF EXISTS cost")

mycursor.execute("CREATE TABLE slot(carNumber VARCHAR(15), slot int)")
mycursor.execute("CREATE TABLE entry(carNumber VARCHAR(15), entry VARCHAR(40))")
mycursor.execute("CREATE TABLE exits(carNumber VARCHAR(15), exit1 VARCHAR(40))")
mycursor.execute("CREATE TABLE duration(carNumber VARCHAR(15), durationInSec int)")
mycursor.execute("CREATE TABLE cost(carNumber VARCHAR(15), cost int)")

slots = [False for _ in range(16)]


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("front.ui", self)
        self.ENTRYBUTTON.released.connect(self.xd)
        self.EXITBUTTON.released.connect(self.exit)
        self.Active.setStyleSheet("background-color: #FF0B00")  # red
        self.Active.setStyleSheet("background-color: #40FF50")  # green

    def xd(self):
        carNumber = self.lineEdit.text()
        mycursor.execute("SELECT carNumber FROM slot")
        f = list(mycursor.fetchall())
        if any(carNumber in s for s in f):
            print("a")
            self.label_2.setText("Duplicate")
        else:
            self.bla()

    def bla(self):
        carNumber = self.lineEdit.text()
        print(len(carNumber))
        if len(carNumber) == 0:
            self.blank()
            exit()
        else:
            self.entry()

    def entry(self):
        try:
            carNumber = self.lineEdit.text()
            print(len(carNumber))
            if len(carNumber) == 0:
                self.blank()
                exit()

            self.lineEdit.clear()
            print(carNumber)
            slotNO = int(slots.index(False))

            slots[slotNO] = True
            slotNO = slotNO + 1
            print(slotNO)

            entry_time = datetime.datetime.now()
            print(type(entry_time))

            mycursor.execute("INSERT INTO slot (carNumber, slot) VALUES(%s,%s)", (carNumber, slotNO))
            mycursor.execute("INSERT INTO entry (carNumber, entry) VALUES(%s,%s)", (carNumber, entry_time))
            mycursor.execute("INSERT INTO exits (carNumber) VALUES(%s)", (carNumber,))
            mycursor.execute("INSERT INTO duration (carNumber) VALUES(%s)", (carNumber,))
            mycursor.execute("INSERT INTO cost (carNumber) VALUES(%s)", (carNumber,))

            self.label_2.setText("Slot: {:,}".format(int(slotNO)))

            if slots[0] == True:
                self.s1.setStyleSheet("background-color: #FF0B00")
            
            if slots[1] == True:
                self.s2.setStyleSheet("background-color: #FF0B00")
            
            if slots[2] == True:
                self.s3.setStyleSheet("background-color: #FF0B00")
            
            if slots[3] == True:
                self.s4.setStyleSheet("background-color: #FF0B00")
            
            if slots[4] == True:
                self.s5.setStyleSheet("background-color: #FF0B00")
            
            if slots[5] == True:
                self.s6.setStyleSheet("background-color: #FF0B00")
            
            if slots[6] == True:
                self.s7.setStyleSheet("background-color: #FF0B00")
            
            if slots[7] == True:
                self.s8.setStyleSheet("background-color: #FF0B00")
            
            if slots[8] == True:
                self.s9.setStyleSheet("background-color: #FF0B00")
            
            if slots[9] == True:
                self.s10.setStyleSheet("background-color: #FF0B00")
            
            if slots[10] == True:
                self.s11.setStyleSheet("background-color: #FF0B00")
            
            if slots[11] == True:
                self.s12.setStyleSheet("background-color: #FF0B00")
            
            if slots[12] == True:
                self.s13.setStyleSheet("background-color: #FF0B00")
            
            if slots[13] == True:
                self.s14.setStyleSheet("background-color: #FF0B00")
            
            if slots[14] == True:
                self.s15.setStyleSheet("background-color: #FF0B00")
            
            if slots[15] == True:
                self.s16.setStyleSheet("background-color: #FF0B00")

            # Rest of the conditions for slots[1] to slots[15]

        except Exception as e:
            print(e)
            self.label_2.setText("Invalid")

    def blank(self):
        print("in")
        self.label_2.setText("Empty")
        time.sleep(5)

    def exit(self):
        try:
            carNumber = self.lineEdit.text()
            self.lineEdit.clear()
            print(carNumber)

            exit_time = datetime.datetime.now()

            mycursor.execute("SELECT slot FROM slot WHERE carNumber = %s", (carNumber,))
            slotNO = int(re.sub("[^0-9]", "", str(mycursor.fetchone())))
            print(slotNO)

            slots[slotNO - 1] = False

            mycursor.execute("UPDATE exits SET exit1 = %s WHERE carNumber = %s", (exit_time, carNumber))

            mycursor.execute("SELECT entry FROM entry WHERE carNumber = %s", (carNumber,))
            entry_time = str(mycursor.fetchone())
            entry_time = re.sub('[,)(/\']', '', str(mycursor.fetchone()))
            e = datetime.datetime.fromisoformat(entry_time)

            duration = int((exit_time - e).total_seconds())
            print(duration)

            cost = int(10 * duration)
            print(cost)
            if cost > 150:
                cost = 150
            self.label_2.setText("Cost: Rs." + str(cost))

            mycursor.execute("UPDATE duration SET durationInSec = %s WHERE carNumber = %s", (duration, carNumber))
            mycursor.execute("UPDATE cost SET cost = %s WHERE carNumber = %s", (cost, carNumber))

            if slots[0] == False:
                self.s1.setStyleSheet("background-color: #40FF50")
        
            if slots[1] == False:
                self.s2.setStyleSheet("background-color: #40FF50")
        
            if slots[2] == False:
                self.s3.setStyleSheet("background-color: #40FF50")
        
            if slots[3] == False:
                self.s4.setStyleSheet("background-color: #40FF50")
            
            if slots[4] == False:
                self.s5.setStyleSheet("background-color: #40FF50")
        
            if slots[5] == False:
                self.s6.setStyleSheet("background-color: #40FF50")
        
            if slots[6] == False:
                self.s7.setStyleSheet("background-color: #40FF50")
        
            if slots[7] == False:
                self.s8.setStyleSheet("background-color: #40FF50")
        
            if slots[8] == False:
                self.s9.setStyleSheet("background-color: #40FF50")
        
            if slots[9] == False:
                self.s10.setStyleSheet("background-color: #40FF50")
        
            if slots[10] == False:
                self.s11.setStyleSheet("background-color: #40FF50")
        
            if slots[11] == False:
                self.s12.setStyleSheet("background-color: #40FF50")
        
            if slots[12] == False:
                self.s13.setStyleSheet("background-color: #40FF50")
        
            if slots[13] == False:
                self.s14.setStyleSheet("background-color: #40FF50")
        
            if slots[14] == False:
                self.s15.setStyleSheet("background-color: #40FF50")
        
            if slots[15] == False:
                self.s16.setStyleSheet("background-color: #40FF50")
        # Rest of the conditions for slots[1] to slots[15]

        except Exception as e:
            print(e)
            self.label_2.setText("Invalid Entry")



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
