import configparser
import os
import sys

from PyQt5 import QtWidgets, QtGui, QtCore

import my_widgets
from design import MyDesign

QtCore.QCoreApplication.setOrganizationName("Vira Realtime")
QtCore.QCoreApplication.setOrganizationDomain("rlt.ru")
QtCore.QCoreApplication.setApplicationName("NLDS")


class MyApp(QtWidgets.QMainWindow, MyDesign):
    def __init__(self):
        super().__init__()
        self.setup_ui(self)
        self.connect_all()
        self.setWindowTitle("NLDS auto-testing")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.gui_restore(last=True)
        self.loaded_config = None
        self.flags = []

    def connect_all(self):
        self.read_folder_path.clicked.connect(self.read_folder_path.open_diag)
        self.models_folder.clicked.connect(self.models_folder.open_diag)
        self.detect_models.clicked.connect(self.detect_models.open_diag)
        self.localize_models.clicked.connect(self.localize_models.open_diag)
        self.flag_kp_config_line.clicked.connect(self.flag_kp_config_line.open_diag)
        self.flag_main_config_line.clicked.connect(self.flag_main_config_line.open_diag)
        self.command_sequence.currentTextChanged['QString'].connect(self.read_folder_path.hide_special)
        self.command_sequence.currentTextChanged['QString'].connect(self.read_folder_path.show_special)
        self.command_sequence.currentTextChanged['QString'].connect(self.read_buffer_size.hide_special)
        self.command_sequence.currentTextChanged['QString'].connect(self.read_buffer_size.show_special)
        self.command_sequence.currentTextChanged['QString'].connect(self.read_skip.hide_special)
        self.command_sequence.currentTextChanged['QString'].connect(self.read_skip.show_special)
        self.start_time_label.toggled['bool'].connect(self.start_time.setHidden)
        self.start_time_label.toggled['bool'].connect(self.start_time.setVisible)
        self.start_time.setHidden(True)
        self.start_time_label.toggled['bool'].connect(self.end_time.setHidden)
        self.start_time_label.toggled['bool'].connect(self.end_time.setVisible)
        self.end_time.setHidden(True)
        self.start_time_label.toggled['bool'].connect(self.end_time_label.setHidden)
        self.start_time_label.toggled['bool'].connect(self.end_time_label.setVisible)
        self.end_time_label.setHidden(True)
        self.flag_distant_server.toggled['bool'].connect(self.flag_distant_server_line_main.setHidden)
        self.flag_distant_server.toggled['bool'].connect(self.flag_distant_server_line_main.setVisible)
        self.flag_distant_server_line_main.setHidden(True)
        self.flag_distant_server.toggled['bool'].connect(self.flag_distant_server_line_reserving.setHidden)
        self.flag_distant_server.toggled['bool'].connect(self.flag_distant_server_line_reserving.setVisible)
        self.flag_distant_server_line_reserving.setHidden(True)
        self.flag_use_opc.toggled['bool'].connect(self.flag_use_opc_line_host.setHidden)
        self.flag_use_opc.toggled['bool'].connect(self.flag_use_opc_line_host.setVisible)
        self.flag_use_opc_line_host.setHidden(True)
        self.flag_use_opc.toggled['bool'].connect(self.flag_use_opc_line_port.setHidden)
        self.flag_use_opc.toggled['bool'].connect(self.flag_use_opc_line_port.setVisible)
        self.flag_use_opc_line_port.setHidden(True)
        self.flag_kp_config.toggled['bool'].connect(self.flag_kp_config_line.setHidden)
        self.flag_kp_config.toggled['bool'].connect(self.flag_kp_config_line.setVisible)
        self.flag_kp_config_line.setHidden(True)
        self.flag_main_config.toggled['bool'].connect(self.flag_main_config_line.setHidden)
        self.flag_main_config.toggled['bool'].connect(self.flag_main_config_line.setVisible)
        self.flag_main_config_line.setHidden(True)
        self.flag_create_subscription.toggled['bool'].connect(self.flag_create_subscription_line.setHidden)
        self.flag_create_subscription.toggled['bool'].connect(self.flag_create_subscription_line.setVisible)
        self.flag_create_subscription_line.setHidden(True)
        self.load_configuration.clicked.connect(self.gui_restore)
        self.save_configuration.clicked.connect(self.gui_save)

        for pipe in self.flow_sensors.keys():
            self.flow_sensors[pipe].connect_neighbour(self.flow_selected_sensors[pipe])
            self.flow_selected_sensors[pipe].connect_neighbour(self.flow_sensors[pipe])
            try:
                self.flow_selected_sensors[pipe].connect_filter(self.pressure_sensors[pipe])
                self.flow_selected_sensors[pipe].connect_filter(self.pressure_selected_sensors[pipe])
            except KeyError:
                pass

        for pipe in self.pressure_sensors.keys():
            self.pressure_sensors[pipe].connect_neighbour(self.pressure_selected_sensors[pipe])
            self.pressure_selected_sensors[pipe].connect_neighbour(self.pressure_sensors[pipe])

        self.start_loop.clicked.connect(self.collect_data_and_start)

    @staticmethod
    def get_handled_type():
        return (QtWidgets.QComboBox, QtWidgets.QLineEdit, QtWidgets.QCheckBox, QtWidgets.QRadioButton,
                QtWidgets.QSpinBox, QtWidgets.QSlider, QtWidgets.QListWidget, QtWidgets.QGroupBox,
                QtWidgets.QDateTimeEdit, my_widgets.MyFilesOpener, my_widgets.MyFolderOpener,
                my_widgets.MyConfigOpener, my_widgets.MyDroppingTable)

    def is_handled_type(self, widget):
        return any(isinstance(widget, t) for t in self.get_handled_type())

    def gui_save(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Create or reload file',
                                                         os.path.join("configs", "gui"), "*.ini")[0]
        if len(filename) == 0:
            return
        if os.path.split(filename)[1] in ["KP.ini", "settings_config.ini"]:
            QtWidgets.QErrorMessage(self).showMessage("Requested name is invalid.")
            return
        settings = QtCore.QSettings(os.path.join("configs", "gui", filename), QtCore.QSettings.IniFormat)

        for name, obj in self.__dict__.items():
            if not self.is_handled_type(obj):
                continue

            name = obj.objectName()
            value = None
            if isinstance(obj, QtWidgets.QComboBox):
                value = obj.currentText()

            if isinstance(obj, QtWidgets.QLineEdit):
                value = obj.text()

            if isinstance(obj, QtWidgets.QCheckBox):
                value = obj.isChecked()

            if isinstance(obj, QtWidgets.QGroupBox):
                value = obj.isChecked()

            if isinstance(obj, QtWidgets.QRadioButton):
                value = obj.isChecked()

            if isinstance(obj, QtWidgets.QSpinBox):
                value = obj.value()

            if isinstance(obj, QtWidgets.QSlider):
                value = obj.value()

            if isinstance(obj, QtWidgets.QDateTimeEdit):
                value = obj.dateTime()

            if isinstance(obj, my_widgets.MyFilesOpener):
                value = obj.get_str()

            if isinstance(obj, my_widgets.MyFolderOpener):
                value = obj.get_str()

            if isinstance(obj, my_widgets.MyConfigOpener):
                value = obj.get_str()

            if isinstance(obj, my_widgets.MyDroppingTable):
                value = obj.get_str()

            if isinstance(obj, QtWidgets.QListWidget):
                settings.beginWriteArray(name)
                for i in range(obj.count()):
                    settings.setArrayIndex(i)
                    settings.setValue(name, obj.item(i).text())
                settings.endArray()
            elif value is not None:
                settings.setValue(name, value)
        settings.sync()

    def gui_restore(self, last=False):
        from distutils.util import strtobool
        if not last:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Create or reload file',
                                                             os.path.join("configs", "gui"), "*.ini")[0]
            if len(filename) == 0:
                return
            if os.path.split(filename)[1] in ["KP.ini", "settings_config.ini"]:
                QtWidgets.QErrorMessage(self).showMessage("Requested name is invalid.")
                return
            settings = QtCore.QSettings(os.path.join("configs", "gui", filename), QtCore.QSettings.IniFormat)
        else:
            import glob
            try:
                settings = QtCore.QSettings(
                    max(glob.glob(os.path.join("configs", "gui", "*.ini")), key=os.path.getctime),
                    QtCore.QSettings.IniFormat)
            except ValueError:
                return

        for name, obj in sorted(self.__dict__.items(), key=lambda x: x[0], reverse=True):
            if not self.is_handled_type(obj):
                continue

            name = obj.objectName()
            value = None
            if not isinstance(obj, QtWidgets.QListWidget):
                value = settings.value(name)
                if value is None:
                    continue

            if isinstance(obj, QtWidgets.QComboBox):
                index = obj.findText(value)  # get the corresponding index for specified string in combobox

                if index == -1:  # add to list if not found
                    obj.insertItems(0, [value])
                    index = obj.findText(value)
                    obj.setCurrentIndex(index)
                else:
                    obj.setCurrentIndex(index)  # preselect a combobox value by index

            if isinstance(obj, QtWidgets.QLineEdit):
                obj.setText(value)

            if isinstance(obj, QtWidgets.QCheckBox):
                obj.setChecked(strtobool(value))

            if isinstance(obj, QtWidgets.QGroupBox):
                obj.setChecked(strtobool(value))

            if isinstance(obj, QtWidgets.QRadioButton):
                obj.setChecked(strtobool(value))

            if isinstance(obj, QtWidgets.QSlider):
                obj.setValue(int(value))

            if isinstance(obj, QtWidgets.QSpinBox):
                obj.setValue(int(value))

            if isinstance(obj, QtWidgets.QDateTimeEdit):
                obj.setDateTime(value)

            if isinstance(obj, my_widgets.MyFilesOpener):
                obj.set_from_str(value)

            if isinstance(obj, my_widgets.MyFolderOpener):
                obj.set_from_str(value)

            if isinstance(obj, my_widgets.MyConfigOpener):
                obj.set_from_str(value)

            if isinstance(obj, my_widgets.MyDroppingTable):
                obj.set_from_str(value)

            if isinstance(obj, QtWidgets.QListWidget):
                size = settings.beginReadArray(name)
                for i in range(size):
                    settings.setArrayIndex(i)
                    value = settings.value(name)
                    if value is not None:
                        obj.addItem(value)
                settings.endArray()
        settings.sync()

    def collect_data_and_start(self):
        from settings import KP_CONFIG_PATH, MAIN_CONFIG_PATH
        config = configparser.ConfigParser()
        config.read([KP_CONFIG_PATH, MAIN_CONFIG_PATH], encoding="utf-8")
        config.set("Paths", "models_folder", self.models_folder.get_str())
        config.set("Paths", "dir_for_logs", "")
        config.set("Paths", "dir_with_input_files", self.read_folder_path.get_str())

        config.set("General", "read_skip", str(self.read_skip.value()))
        config.set("General", "remove_files", "False")
        config.set("General", "detect_models", self.detect_models.get_str())
        config.set("General", "use_start_time", "True")
        config.set("General", "localize_models", self.localize_models.get_str())
        config.set("General", "command_sequence", str(self.command_sequence.currentText().split("-")))
        if self.start_time_label.isChecked():
            config.set("DateTime", "start_time_dt", self.start_time.dateTime().toString("yyyy-MM-dd hh:mm:ss") + "+0000")
            config.set("DateTime", "end_time_dt", self.end_time.dateTime().toString("yyyy-MM-dd hh:mm:ss") + "+0000")
        else:
            config.set("DateTime", "start_time_dt", "")
            config.set("DateTime", "end_time_dt", "")

        config.set("DateTime", "buffer_size_td", self.read_buffer_size.time().toString("00:hh:mm:ss"))
        config.set("DateTime", "adjust_start_time_td", "00:00:00:00")
        config.set("DateTime", "detect_window_size_td", self.detect_window_size.time().toString("00:hh:mm:ss"))

        config.set("Server", "host", "'" + self.flag_use_opc_line_host.text().replace(" ", "") + "'")
        config.set("Server", "port", self.flag_use_opc_line_port.text())

        for section in config.sections():
            if "pressure" in section:
                pipe = section.split("_")[1]
                table = getattr(self, "t_pressure_" + pipe + "_selected_sensors")
                section_ind = 0
                for col in range(table.columnCount()):
                    if table.horizontalHeaderItem(col).text() == "section":
                        section_ind = col
                        break
                use = False
                for row in range(table.rowCount()):
                    if table.item(row, section_ind).text() == section and not table.isRowHidden(row):
                        use = True
                        break
                config.set(section, "use", str(use))
            elif "flow" in section:
                pipe = section.split("_")[1]
                table = getattr(self, "t_flow_" + pipe + "_selected_sensors")
                section_ind = 0
                for col in range(table.columnCount()):
                    if table.horizontalHeaderItem(col).text() == "section":
                        section_ind = col
                        break
                use = False
                for row in range(table.rowCount()):
                    if table.item(row, section_ind).text() == section and not table.isRowHidden(row):
                        use = True
                        break
                config.set(section, "use", str(use))

        self.loaded_config = config

        for checkbox in self.main_widget.findChildren(QtWidgets.QCheckBox, QtCore.QRegExp(r'flag_.*')):
            if checkbox.isChecked():
                _string = "--" + checkbox.text()
                try:
                    _string += "=" + self.main_widget.findChild(my_widgets.MyConfigOpener,
                                                                checkbox.objectName() + "_line").get_str()
                except AttributeError:
                    pass

                try:
                    _string += "=" + self.main_widget.findChild(QtWidgets.QLineEdit,
                                                                checkbox.objectName() + "_line").text()
                except AttributeError:
                    pass

                self.flags.append(_string)
        self.flags.append("--main-server=" + self.main_widget.findChild(
            QtWidgets.QLineEdit,
            "flag_distant_server_line_main").text().replace("\\", "").replace("/", ""))
        self.flags.append("--reserving-server=" + self.main_widget.findChild(
            QtWidgets.QLineEdit,
            "flag_distant_server_line_reserving").text().replace("\\", "").replace("/", ""))
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = MyApp()
    win.show()
    app.exec()
    print(win.loaded_config)
    print(win.flags)
    if win.loaded_config or len(win.flags) > 0:
        sys.argv[1:] = win.flags
        import loop
        import cli
        cli.parse_args()
        loop.loop(indirect=win.loaded_config)
