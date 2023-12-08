from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class EpubFileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ファイル名")
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()

        self.label = QLabel(".epub", self)
        self.line_edit = QLineEdit(self)
        self.cancel_button = QPushButton("Cancel", self)
        self.ok_button = QPushButton("OK", self)

        layout2.addWidget(self.line_edit)
        layout2.addWidget(self.label)

        layout3.addWidget(self.cancel_button)
        layout3.addWidget(self.ok_button)

        layout1.addLayout(layout2)
        layout1.addLayout(layout3)

        self.setLayout(layout1)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def getText(self):
        return self.line_edit.text()
