# -*- coding: utf-8 -*-

#
# Created: Wed Jan 15 18:36:54 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import httplib, re
import thread

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(341, 303)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Python27/DLLs/py.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setModal(False)
        self.groupBox_1 = QtGui.QGroupBox(Dialog)
        self.groupBox_1.setGeometry(QtCore.QRect(20, 10, 141, 181))
        self.groupBox_1.setObjectName("groupBox_1")
        
        self.plainTextEdit_1 = QtGui.QPlainTextEdit(self.groupBox_1)
        self.plainTextEdit_1.setGeometry(QtCore.QRect(10, 20, 121, 151))
        self.plainTextEdit_1.setObjectName("plainTextEdit_1")
        
        
        self.lineEdit_1 = QtGui.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(20, 200, 141, 20))
        self.lineEdit_1.setObjectName("lineEdit_1")
        
        self.lineEdit_2 = QtGui.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 230, 141, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_3 = QtGui.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(180, 230, 141, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(180, 10, 141, 181))
        self.groupBox_2.setObjectName("groupBox_2")
        
        self.plainTextEdit_2 = QtGui.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(10, 20, 121, 151))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(20, 260, 171, 20))
        
        self.progressBar.setObjectName("progressBar")
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(250, 260, 73, 23))
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        #self.pushButton.setVisible(True)#hide
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.update_test)
        '''
        self.errorMessage = QtGui.QErrorMessage(Dialog)
        self.errorMessage.showMessage("If the box is unchecked, the message won't "
                "appear again.")
        '''
        self.MessageBox = QtGui.QMessageBox(Dialog)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "域名DNS批量修改工具", None))
        self.groupBox_1.setTitle(_translate("Dialog", "待修改域名", None))
        
        self.lineEdit_1.setText(_translate("Dialog", "123456", None))
        self.lineEdit_2.setText(_translate("Dialog", "f1g1ns1.dnspod.net", None))
        self.lineEdit_3.setText(_translate("Dialog", "f1g1ns2.dnspod.net", None))
        
        self.groupBox_2.setTitle(_translate("Dialog", "已修改域名", None))
        self.progressBar.setFormat(_translate("Dialog", "%p%", None))
        self.pushButton.setText(_translate("Dialog", "开始", None))

    def update_test(self, Dialog):
        self.pushButton.setEnabled(False)#disable
        self.plainTextEdit_2.clear()
        
        pas = self.lineEdit_1.text()
        ns1 = self.lineEdit_2.text()
        ns2 = self.lineEdit_3.text()
        if pas == '':
            self.MessageBox.setText(u"密码不能为空！")
            self.MessageBox.exec_()
        elif (ns1 == '') or (ns2 == ''):
            self.MessageBox.setText(u"DNS不能为空！")
            self.MessageBox.exec_()
        else:
            text = unicode(self.plainTextEdit_1.toPlainText()).strip()
            if text == '':
               self.MessageBox.setText(u"待修改域名不能为空！")
               self.MessageBox.exec_()
            else:
                name = text.split('\n')
                leng = len(name)
                i = 0
                while i < leng:
                    self.progressBar.setProperty("value", (i*100//leng))
                    #log = post_test(name[i], pas, ns1, ns2)
                    thread.start_new_thread(post_test, (self, name[i], pas, ns1, ns2))
                    i = i + 1
                self.progressBar.setProperty("value", 100)
        self.pushButton.setEnabled(True)#disable
        
def post_test(self, name, pas, ns1, ns2):
    url = 'https://access.enom.com/default.aspx?action=login'
    dat = 'sldtld={0}&DomainPassword={1}&Login.x=27&Login.y=11'.format(name, pas)
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn = httplib.HTTPSConnection('access.enom.com')
    conn.request('POST', url, dat, headers)
    httpres = conn.getresponse()
    if httpres.status == 302 :
        cookies = re.search('ShortBread=(.+?);', httpres.msg['Set-Cookie']).group(0)
        url = 'https://access.enom.com/domainmain.aspx?edit=updateDNS'
        dat = 'DNScount=2&UseNameserver=No&DNS1={0}&DNS2={1}&DNS3=&DNS4=&DNS5=&Save.x=17&Save.y=13'.format(ns1, ns2)
        headers = {"Content-type": "application/x-www-form-urlencoded","Cookie":cookies}
        conn = httplib.HTTPSConnection('access.enom.com')
        conn.request('POST', url, dat, headers)
        httpres = conn.getresponse()
        if httpres.status == 200 :
            html = httpres.read()
            dns1 = re.search('id="idDNS1" disabled value="(.+?)"', html).group(1)
            dns2 = re.search('id="idDNS2" disabled value="(.+?)"', html).group(1)
            if (dns1 == ns1 ) and (dns2 == ns2):
                log = ' ok'
            else:
                log = ' error'
        else:
            log = ' error'
    else:
        log = ' error'
    self.plainTextEdit_2.appendPlainText(_translate("Dialog", name+ log, None))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
