from PySide6.QtCore import Slot

from PySide6.QtSql import QSqlDatabase, QSqlTableModel

from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QTableView,
    QLabel, QWidget, QPushButton,
    QFileDialog, QLineEdit
)
from UserApiProvider import UserApiProvider
from UserTableModel import UserTableModel
from QTConversation import ConversationWindow


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Desktop application')
        self._conv_window = None
        self.__label = QLabel('Users', self)

        self.__model = None
        self.__view = QTableView(self)

        model = UserTableModel(UserApiProvider('http://localhost:8081'), self)
        self.__view.setModel(model)

        model.update_model()

        self._sender_label = QLabel('Sender name', self)
        self._sender_edit = QLineEdit(self)
        self._sender_edit.setText("Alice")

        self._receiver_label = QLabel('Receiver name', self)
        self._receiver_edit = QLineEdit(self)
        self._receiver_edit.setText("Bob")

        self._conversation_button = QPushButton("Go to conversation", self)
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.__label)

        layout = QVBoxLayout()
        layout.addLayout(horizontal_layout)
        layout.addWidget(self.__view)
        layout.addWidget(self._sender_label)
        layout.addWidget(self._sender_edit)
        layout.addWidget(self._receiver_label)
        layout.addWidget(self._receiver_edit)
        layout.addWidget(self._conversation_button)

        self.setLayout(layout)
        sender_name = self._sender_edit.text()
        receiver_name = self._receiver_edit.text()

        self._conversation_button.clicked.connect(self.__open_conversation)

    @Slot()
    def __open_conversation(self):
        sender_name = self._sender_edit.text()
        receiver_name = self._receiver_edit.text()
        self.conv_window = ConversationWindow(sender_name=sender_name, receiver_name=receiver_name)
        self.conv_window.show()


