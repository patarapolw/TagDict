import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from TagDict.excel import TagDict


def main():
    sys.argv += ['--style', 'fusion']
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.load("qml/main.qml")
    engine.quit.connect(app.quit)

    sys.exit(app.exec_())
