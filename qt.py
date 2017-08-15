import sys
import threading
import PyQt5.QtCore as Qt
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtWebEngineWidgets as QtWeb

import cmd
import chart
import db

class StdoutRedirect(Qt.QObject):
    valueChanged = Qt.pyqtSignal('QString')

    def __init__(self, parent):
        super(StdoutRedirect, self).__init__()
        self.valueChanged.connect(parent.updateStatusBar)

    def write(self, string):
        string = string.rstrip()
        if len(string) > 0:
            self.valueChanged.emit(string)

    def flush(self):
        pass


class GUI(QtWidgets.QMainWindow):
    MAX_THREAD = 2

    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        central = QtWidgets.QWidget(self)
        self.svg = QtWeb.QWebEngineView(self)
        self.statusBar = QtWidgets.QStatusBar(self)
        self.btnlaunch = QtWidgets.QPushButton('Download and Save Result')
        self.btnStats = QtWidgets.QPushButton('Reload Stats')
        self.btnFlush = QtWidgets.QPushButton('Flush')

        self.btnlaunch.clicked.connect(self.launch)
        self.btnStats.clicked.connect(self.stats)
        self.btnFlush.clicked.connect(self.flush)
        self.svg.setContextMenuPolicy(Qt.Qt.NoContextMenu)
        self.svg.setContent(chart.makeChart(), mimeType='image/svg+xml')

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.btnlaunch)
        hbox.addWidget(self.btnStats)
        hbox.addWidget(self.btnFlush)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.svg)
        vbox.addLayout(hbox)

        central.setLayout(vbox)
        self.setCentralWidget(central)
        self.setStatusBar(self.statusBar)
        self.setWindowTitle('Youtube Watch Later Playlist Stats')
        sys.stdout = StdoutRedirect(self)
        self.show()

    def launch(self):
        if len(threading.enumerate()) < self.MAX_THREAD:
            self.thread = threading.Thread(target=cmd.main)
            self.thread.start()

    def stats(self):
        if len(threading.enumerate()) < self.MAX_THREAD:
            thread_target = self.svg.setContent(chart.makeChart(),
                                                mimeType='image/svg+xml')
            self.thread = threading.Thread(target=thread_target)
            self.thread.start()

    def flush(self):
        if len(threading.enumerate()) < self.MAX_THREAD:
            self.thread = threading.Thread(target=db.flush)
            self.thread.start()

    def updateStatusBar(self, string):
        self.statusBar.showMessage(string, 3000)


if __name__ == '__main__':
    gui = QtWidgets.QApplication(sys.argv)
    w = GUI()
    sys.exit(gui.exec_())
