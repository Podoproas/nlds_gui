import os

from PyQt5 import QtWidgets, QtCore


class MyHidingQLineEdit(QtWidgets.QLineEdit):
    def __init__(self, main):
        super().__init__(main)

    def hide_special(self, dat_choice):
        if "read" not in dat_choice:
            self.hide()

    def show_special(self, dat_choice):
        if "read" in dat_choice:
            self.show()


class MyHidingQSpinBox(QtWidgets.QSpinBox):
    def __init__(self, main):
        super().__init__(main)

    def hide_special(self, dat_choice):
        if "read" not in dat_choice:
            self.hide()

    def show_special(self, dat_choice):
        if "read" in dat_choice:
            self.show()


class MyHidingQTimeEdit(QtWidgets.QTimeEdit):
    def __init__(self, main):
        super().__init__(main)

    def hide_special(self, dat_choice):
        if "read" not in dat_choice:
            self.hide()

    def show_special(self, dat_choice):
        if "read" in dat_choice:
            self.show()


class MyFilesOpener(QtWidgets.QPushButton):
    def __init__(self, main, default_filename=None):
        super().__init__(main)
        self.filenames = [default_filename]
        self.setToolTip(self.selected_files)

    def open_diag(self):
        filenames = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open file', "models")[0]
        if len(filenames) > 0:
            self.filenames = filenames
        self.setToolTip(self.selected_files)

    def get_str(self):
        return str(self.get_list())

    def get_list(self):
        return list(map(lambda x: os.path.join(os.path.split(os.path.split(x)[0])[1], os.path.split(x)[1]),
                        self.filenames))

    def set_from_str(self, value):
        self.filenames = eval(value)
        self.setToolTip(self.selected_files)

    @property
    def selected_files(self):
        return "\n".join(self.get_list())

    def hide_special(self, dat_choice):
        if "read" not in dat_choice:
            self.hide()

    def show_special(self, dat_choice):
        if "read" in dat_choice:
            self.show()


class MyFolderOpener(QtWidgets.QPushButton):
    def __init__(self, main, default_folder=None, get_server_func=None):
        super().__init__(main)
        self.folder_name = default_folder
        self.open = get_server_func
        self.setToolTip(self.get_str())

    def open_diag(self):
        folder_name = QtWidgets.QFileDialog.getExistingDirectory(self, "Select directory",
                                                                 "" if self.open is None else self.open()())
        if len(folder_name) > 0:
            self.folder_name = folder_name
        self.setToolTip(self.get_str())

    def get_str(self):
        return self.folder_name.replace("" if self.open is None else self.open()().lower(), "")

    def set_from_str(self, value):
        self.folder_name = value
        self.setToolTip(self.get_str())

    def hide_special(self, dat_choice):
        if "read" not in dat_choice:
            self.hide()

    def show_special(self, dat_choice):
        if "read" in dat_choice:
            self.show()


class MyConfigOpener(QtWidgets.QPushButton):
    def __init__(self, main, default_conf=None, get_server_func=None):
        super().__init__(main)
        self.folder_name = default_conf
        self.open = get_server_func
        self.setToolTip(self.get_str())

    def open_diag(self):
        folder_name = QtWidgets.QFileDialog.getOpenFileName(self, "Select directory",
                                                            "configs" if self.open is None else self.open()(),
                                                            "*.ini")[0]
        if len(folder_name) > 0:
            self.folder_name = folder_name
        self.setToolTip(self.get_str())

    def get_str(self):
        return self.folder_name.replace("" if self.open is None else self.open()().lower(), "")

    def set_from_str(self, value):
        self.folder_name = value
        self.setToolTip(self.get_str())

    def hide_special(self, dat_choice):
        if "read" not in dat_choice:
            self.hide()

    def show_special(self, dat_choice):
        if "read" in dat_choice:
            self.show()


class MyDroppingTable(QtWidgets.QTableWidget):

    def __init__(self, main):
        super().__init__(main)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSortingEnabled(True)
        self.neighbour = None
        self.filtering_tables = []
        self.segments = []

    def connect_neighbour(self, neighbour):
        self.neighbour = neighbour

    def connect_filter(self, filter_table):
        self.filtering_tables.append(filter_table)

    def double_clicked(self):
        this_row = {}
        row = self.currentRow()
        for col in range(self.columnCount()):
            column_name = self.horizontalHeaderItem(col).text()
            if self.item(row, col) is not None:
                item_string = self.item(row, col).text()
                this_row[column_name] = item_string
        self.neighbour.set(this_row)
        self.removeRow(row)
        self.resizeColumnsToContents()
        if len(self.filtering_tables) > 0:
            self.recalc_segs()
            self.filter()

    def set(self, row):
        self.setSortingEnabled(False)
        row_number = self.rowCount()
        sort_ind = 0
        self.insertRow(row_number)
        for col in range(self.columnCount()):
            column_name = self.horizontalHeaderItem(col).text()
            if column_name == "km":
                sort_ind = col
            if column_name in row:
                cell = MyTableWidgetItem(row[column_name])
                cell.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
                )
                self.setItem(row_number, col, cell)
        self.resizeColumnsToContents()
        self.sortByColumn(sort_ind, 0)
        self.setSortingEnabled(True)
        if len(self.filtering_tables) > 0:
            self.recalc_segs()
            self.filter()

    def recalc_segs(self):
        self.segments = []
        range_km_ind = 0
        for col in range(self.columnCount()):
            if self.horizontalHeaderItem(col).text() == "km":
                range_km_ind = col

        for row in range(self.rowCount()):
            cur_km = float(self.item(row, range_km_ind).text())
            next_km = self.item(row + 1, range_km_ind)
            if next_km is not None:
                self.segments.append((cur_km, float(next_km.text())))

    def is_in_seg(self, value):
        for seg in self.segments:
            if seg[0] <= value <= seg[1]:
                return True
        return False

    def filter(self):
        for cur_filtering in self.filtering_tables:
            range_km_ind = 0
            for col in range(cur_filtering.columnCount()):
                if cur_filtering.horizontalHeaderItem(col).text() == "km":
                    range_km_ind = col

            for row in range(cur_filtering.rowCount()):
                text = cur_filtering.item(row, range_km_ind).text()
                if self.is_in_seg(float(text) if len(text) else 0):
                    cur_filtering.showRow(row)
                    cur_filtering.resizeColumnsToContents()
                else:
                    cur_filtering.hideRow(row)
                    cur_filtering.resizeColumnsToContents()

    def get_str(self):
        ans = {"columnNames": [self.horizontalHeaderItem(col).text() for col in range(self.columnCount())]}
        rows = []
        for row in range(self.rowCount()):
            cur_row = {"isHidden": self.isRowHidden(row), "rowNumber": row}
            row_data = {}
            for col in range(self.columnCount()):
                row_data[self.horizontalHeaderItem(col).text()] = self.item(row, col).text()
            cur_row["data"] = row_data
            rows.append(cur_row)
        ans['rows'] = rows
        return str(ans)

    def set_from_str(self, str_value: str):
        ans = eval(str_value)
        num_of_cols = len(ans["columnNames"])
        num_of_rows = len(ans["rows"])
        self.clear()
        self.setColumnCount(num_of_cols)
        self.setRowCount(num_of_rows)
        self.setHorizontalHeaderLabels(ans["columnNames"])
        for row_elem in ans["rows"]:
            row = row_elem["rowNumber"]
            is_hidden = row_elem["isHidden"]
            for col_name in row_elem["data"].keys():
                cell = MyTableWidgetItem(row_elem["data"][col_name])

                cell.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
                )
                self.setItem(row, ans["columnNames"].index(col_name), cell)
            if is_hidden:
                self.hideRow(row)
            else:
                self.showRow(row)
        self.resizeColumnsToContents()


class MyTableWidgetItem(QtWidgets.QTableWidgetItem):
    def __init__(self, text):
        super().__init__(text)

    def __eq__(self, other):
        try:
            return float(self.text()) == float(other.text())
        except Exception:
            return self.text() == other.text()

    def __ne__(self, other):
        try:
            return float(self.text()) != float(other.text())
        except Exception:
            return self.text() != other.text()

    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except Exception:
            return self.text() < other.text()

    def __le__(self, other):
        try:
            return float(self.text()) <= float(other.text())
        except Exception:
            return self.text() <= other.text()

    def __gt__(self, other):
        try:
            return float(self.text()) > float(other.text())
        except Exception:
            return self.text() > other.text()

    def __ge__(self, other):
        try:
            return float(self.text()) >= float(other.text())
        except Exception:
            return self.text() >= other.text()
