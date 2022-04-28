from PySide6.QtCore import Slot, Qt, QAbstractTableModel, QModelIndex, QTimer
from MessageApiProvider import MessageApiProvider


class MessageTableModel(QAbstractTableModel):
    __update_timeout = 1_000
    __columns = ['date_send', 'from_id', 'message_text']

    def __init__(self, provider, parent=None):
        super().__init__(parent)
        self.__api: MessageApiProvider = provider
        self.__conversation = []
        self.__timer = QTimer(self)

        self.__timer.timeout.connect(self.update_model)

        self.__timer.start(self.__update_timeout)
        self.update_model()

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.__columns)

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.__conversation)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row, column = index.row(), index.column()
            if row < self.rowCount() and column < self.columnCount():
                return self.__get_display_data(row, column)

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        return self.__columns[section] \
                if orientation == Qt.Horizontal and role == Qt.DisplayRole \
                else None

    @Slot()
    def update_model(self):
        conversation = self.__api.get_conversation()
        if conversation != self.__conversation:
            self.beginResetModel()
            self.__conversation = conversation
            self.endResetModel()

    def __get_display_data(self, row: int, column: int) -> str:
        return self.__conversation[row][self.__columns[column]]
