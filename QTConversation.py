from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QTableView,
    QLabel, QWidget, QPushButton,
    QLineEdit,
)
from MessageApiProvider import MessageApiProvider
from MessageTableModel import MessageTableModel


class ConversationWindow(QWidget):
    def __init__(self, parent=None, sender_name="Alice", receiver_name="Bob"):
        super().__init__(parent)
        self.setWindowTitle('Desktop application')
        self._conv_window = None
        self.__label = QLabel('Users', self)

        self.__model = MessageTableModel(MessageApiProvider('http://localhost:8081', sender_name, receiver_name), self)
        self.__view = QTableView(self)

        #model = MessageTableModel(MessageApiProvider('http://localhost:8081', sender_name, receiver_name), self)
        self.__api = MessageApiProvider('http://localhost:8081', sender_name, receiver_name)
        self.__view.setModel(self.__model)

        self.__model.update_model()

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.__label)

        self._message_edit = QLineEdit(self)
        self._message_button = QPushButton("Send message", self)

        layout = QVBoxLayout()
        layout.addLayout(horizontal_layout)
        layout.addWidget(self.__view)
        layout.addWidget(self._message_edit)
        layout.addWidget(self._message_button)

        self.setLayout(layout)
        self._message_button.clicked.connect(self.__send_message)


    @Slot()
    def __send_message(self):
        print("Button cliked!")
        message_text = self._message_edit.text()
        data = {'message': message_text}
        print(data)
        self.__api.add_message(data)

