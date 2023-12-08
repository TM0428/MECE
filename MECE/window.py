import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QDialog
from PyQt6.QtGui import QIcon, QAction
from typing import Final


class MainWindow(QMainWindow):
    title: Final[str] = "MECE"
    creator: Final[str] = "TM"
    app_dir: str

    def __init__(self):
        super().__init__()
        self.app_dir = os.getcwd()
        self.initUI()
        # ui = bodyUI(self)
        # self.setCentralWidget(ui)

    def initUI(self):
        # 設定
        self.setWindowTitle(self.title)  # ウィンドウのタイトル
        self.setGeometry(100, 100, 600, 600)  # ウィンドウの位置と大きさ
        self.statusBar().showMessage("Made by " + self.creator)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        helpMenu = mainMenu.addMenu("Help")
        # EPUBの解凍
        unepubbutton = QAction(QIcon("hoge.png"), "Epubの解凍", self)
        unepubbutton.setShortcut("Ctrl+R")
        unepubbutton.triggered.connect(self.epub_to_folder)
        # Epubの作成
        dirbutton = QAction(QIcon("hoge.png"), "Epubの作成", self)
        dirbutton.setShortcut("Ctrl+E")
        dirbutton.triggered.connect(self.folder_to_epub)
        # 終了ボタン
        exitButton = QAction(QIcon("public/icon/exit-24-32.png"), "Exit", self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("Exit application")
        exitButton.triggered.connect(QApplication.instance().quit)
        versionbutton = QAction("バージョン", self)
        versionbutton.triggered.connect(self.versiontab)
        fileMenu.addAction(dirbutton)
        fileMenu.addAction(unepubbutton)
        fileMenu.addAction(exitButton)
        helpMenu.addAction(versionbutton)

    def epub_to_folder(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Open file",
            self.app_dir,
            "Epubファイル(*.epub)",
            options=QFileDialog.Option.DontUseNativeDialog,
        )
        root, ext = os.path.splitext(fname[0])
        if fname[0] == "" or ext != ".epub":
            return
        dirname = os.path.dirname(fname[0])
        basename = os.path.basename(fname[0])
        bname, ext = os.path.splitext(basename)
        os.rename(fname[0], os.path.join(dirname, bname + ".zip"))
        from .util import unzip

        unzip(dirname + "/" + bname, dirname + "/" + bname + ".zip")
        os.remove(dirname + "/" + bname + ".zip")
        QMessageBox.question(self, "Message", "Epubを解凍しました")

    def folder_to_epub(self):
        from contents import EpubFileDialog

        fname = QFileDialog.getExistingDirectory(
            self,
            "Open file",
            self.app_dir,
            options=QFileDialog.Option.DontUseNativeDialog,
        )
        if fname == "":
            return
        pathname = os.path.basename(fname)
        dialog = EpubFileDialog(self)
        dialog.line_edit.setText(pathname)
        result = dialog.exec()
        if result == QDialog.DialogCode.Rejected:
            return
        elif result == QDialog.DialogCode.Accepted:
            t = dialog.getText()
        else:
            t = os.path.basename(fname)
        from .util import pack_epub

        pack_epub(fname, t + ".epub")
        QMessageBox.information(self, "Message", "Epubを作成しました")

    def versiontab(self):
        dialog = QMessageBox(parent=self)
        dialog.setWindowTitle("version")
        dialog.setText("0.0.0 alpha")
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.setWindowTitle("versions")
        dialog.exec()  # Stores the return value for the button pressed


def main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()
