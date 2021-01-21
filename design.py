import configparser
import re

from PyQt5 import QtCore, QtWidgets

import my_widgets


class MyDesign(object):
    def __init__(self):
        self.flow_selected_sensors_label = dict()
        self.flow_sensors_label = dict()
        self.flow_grid_for_pipe = dict()
        self.flow_selected_sensors = dict()
        self.flow_sensors = dict()
        self.flow_pipes_tab = dict()

        self.pressure_selected_sensors_label = dict()
        self.pressure_sensors_label = dict()
        self.pressure_grid_for_pipe = dict()
        self.pressure_selected_sensors = dict()
        self.pressure_sensors = dict()
        self.pressure_pipes_tab = dict()

        self.main_widget = None
        self.main_layout = None
        self.right_layout = None
        self.load_configuration = None
        self.save_configuration = None
        self.start_loop = None
        self.settings_config_layout = None
        self.start_time_label = None
        self.end_time_label = None
        self.start_time = None
        self.end_time = None
        self.command_sequence = None
        self.distant_server = None
        self.read_folder_path = None
        self.read_skip = None
        self.read_buffer_size = None
        self.detect_window_size = None
        self.models_folder = None
        self.detect_models = None
        self.localize_models = None
        self.label_flag = None
        self.flag_debug = None
        self.flag_distant_server = None
        self.flag_distant_server_line_main = None
        self.flag_distant_server_line_reserving = None
        self.flag_use_gpu = None
        self.flag_wait_for_data = None
        self.flag_store_statistics_local = None
        self.flag_recreate_settings_config = None
        self.flag_create_subscription = None
        self.flag_crash_on_errors = None
        self.flag_create_subscription_line = None
        self.flag_kp_config = None
        self.flag_use_opc = None
        self.flag_kp_config_line = None
        self.flag_use_opc_line_host = None
        self.flag_main_config = None
        self.flag_use_opc_line_port = None
        self.flag_main_config_line = None
        self.tabs = None
        self.pipes_set = set()
        self.pressure = None
        self.flow = None
        self.flow_grid = None
        self.left_column_flag_layout = None
        self.right_column_flag_layout = None

    def setup_ui(self, main_window: QtWidgets.QWidget):
        main_window.setObjectName("main_window")
        main_window.resize(1920, 1600)

        self.main_widget = QtWidgets.QWidget(main_window)
        self.main_widget.setObjectName("main_widget")
        self.main_layout = QtWidgets.QGridLayout(self.main_widget)
        self.main_layout.setObjectName("main_layout")

        self.right_layout = QtWidgets.QGridLayout()
        self.right_layout.setObjectName("right_layout")

        self.distant_server = QtWidgets.QComboBox(self.main_widget)
        set_size_policy(self.distant_server, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.distant_server.setObjectName("distant_server")
        self.right_layout.addWidget(self.distant_server, 1, 0, 1, 1)
        self.distant_server.addItem("")
        self.distant_server.addItem("")
        self.distant_server.addItem("")

        self.load_configuration = QtWidgets.QPushButton(self.main_widget)
        self.load_configuration.setObjectName("load_configuration")
        self.right_layout.addWidget(self.load_configuration, 2, 0, 1, 1)

        self.save_configuration = QtWidgets.QPushButton(self.main_widget)
        self.save_configuration.setObjectName("save_configuration")
        self.right_layout.addWidget(self.save_configuration, 3, 0, 1, 1)

        self.start_loop = QtWidgets.QPushButton(self.main_widget)
        self.start_loop.setObjectName("start_loop")
        self.right_layout.addWidget(self.start_loop, 4, 0, 1, 1)

        self.settings_config_layout = QtWidgets.QGridLayout()
        self.settings_config_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.settings_config_layout.setObjectName("settings_config_layout")
        self.right_layout.addLayout(self.settings_config_layout, 0, 0, 1, 1)

        self.start_time_label = QtWidgets.QCheckBox(self.main_widget)
        set_size_policy(self.start_time_label, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.start_time_label.setObjectName("start_time_label")
        self.settings_config_layout.addWidget(self.start_time_label, 0, 0, 1, 1)

        self.end_time_label = QtWidgets.QLabel(self.main_widget)
        set_size_policy(self.end_time_label, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.end_time_label.setObjectName("end_time_label")
        self.settings_config_layout.addWidget(self.end_time_label, 0, 1, 1, 1)

        self.start_time = QtWidgets.QDateTimeEdit(self.main_widget)
        set_size_policy(self.start_time, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.start_time.setDateTime(QtCore.QDateTime(QtCore.QDate(2019, 1, 1), QtCore.QTime(0, 0, 0)))
        self.start_time.setObjectName("start_time")
        self.settings_config_layout.addWidget(self.start_time, 1, 0, 1, 1)

        self.end_time = QtWidgets.QDateTimeEdit(self.main_widget)
        set_size_policy(self.end_time, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.end_time.setDateTime(QtCore.QDateTime(QtCore.QDate(2019, 1, 1), QtCore.QTime(0, 0, 0)))
        self.end_time.setObjectName("end_time")
        self.settings_config_layout.addWidget(self.end_time, 1, 1, 1, 1)

        self.command_sequence = QtWidgets.QComboBox(self.main_widget)
        set_size_policy(self.command_sequence, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.command_sequence.setObjectName("command_sequence")
        self.settings_config_layout.addWidget(self.command_sequence, 2, 0, 1, 2)
        self.command_sequence.addItem("")
        self.command_sequence.addItem("")
        self.command_sequence.addItem("")
        self.command_sequence.addItem("")
        self.command_sequence.addItem("")

        self.read_skip = my_widgets.MyHidingQSpinBox(self.main_widget)
        set_size_policy(self.read_skip, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.read_skip.setObjectName("read_skip")
        self.settings_config_layout.addWidget(self.read_skip, 4, 0, 1, 1)
        self.read_skip.setMinimum(1)
        self.read_skip.setMaximum(1000)
        self.read_skip.setValue(10)

        self.read_buffer_size = my_widgets.MyHidingQTimeEdit(self.main_widget)
        set_size_policy(self.read_buffer_size, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.read_buffer_size.setObjectName("read_buffer_size")
        self.settings_config_layout.addWidget(self.read_buffer_size, 4, 1, 1, 1)

        self.detect_window_size = QtWidgets.QTimeEdit(self.main_widget)
        set_size_policy(self.detect_window_size, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.detect_window_size.setObjectName("detect_window_size")
        self.settings_config_layout.addWidget(self.detect_window_size, 5, 0, 1, 1)

        self.models_folder = my_widgets.MyFolderOpener(self.main_widget, "models/")
        set_size_policy(self.models_folder, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.models_folder.setObjectName("models_folder")
        self.settings_config_layout.addWidget(self.models_folder, 5, 1, 1, 1)

        self.detect_models = my_widgets.MyFilesOpener(self.main_widget, "rfc/state_of_the_art.mdl")
        set_size_policy(self.detect_models, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.detect_models.setObjectName("detect_models")
        self.settings_config_layout.addWidget(self.detect_models, 6, 0, 1, 1)

        self.localize_models = my_widgets.MyFilesOpener(self.main_widget, "comparator/state_of_the_art.mdl")
        set_size_policy(self.localize_models, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.localize_models.setObjectName("localize_models")
        self.settings_config_layout.addWidget(self.localize_models, 6, 1, 1, 1)

        self.label_flag = QtWidgets.QLabel(self.main_widget)
        set_size_policy(self.label_flag, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.label_flag.setObjectName("label_flag")
        self.settings_config_layout.addWidget(self.label_flag, 7, 0, 1, 2)

        self.left_column_flag_layout = QtWidgets.QVBoxLayout()
        self.left_column_flag_layout.setObjectName("left_column_flag_layout")
        self.settings_config_layout.addItem(self.left_column_flag_layout, 8, 0, 1, 1)

        self.right_column_flag_layout = QtWidgets.QVBoxLayout()
        self.right_column_flag_layout.setObjectName("right_column_flag_layout")
        self.settings_config_layout.addItem(self.right_column_flag_layout, 8, 1, 1, 1)

        self.flag_debug = QtWidgets.QCheckBox(self.main_widget)
        set_size_policy(self.flag_debug, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_debug.setObjectName("flag_debug")
        self.left_column_flag_layout.addWidget(self.flag_debug)

        self.flag_distant_server = QtWidgets.QCheckBox(self.main_widget)
        set_size_policy(self.flag_distant_server, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_distant_server.setObjectName("flag_distant_server")
        self.right_column_flag_layout.addWidget(self.flag_distant_server)

        self.flag_distant_server_line_main = my_widgets.MyHidingQLineEdit(self.main_widget)
        set_size_policy(self.flag_distant_server_line_main, QtWidgets.QSizePolicy.Minimum,
                        QtWidgets.QSizePolicy.Minimum)
        self.flag_distant_server_line_main.setObjectName("flag_distant_server_line_main")
        self.right_column_flag_layout.addWidget(self.flag_distant_server_line_main)

        self.flag_distant_server_line_reserving = my_widgets.MyHidingQLineEdit(self.main_widget)
        set_size_policy(self.flag_distant_server_line_reserving, QtWidgets.QSizePolicy.Minimum,
                        QtWidgets.QSizePolicy.Minimum)
        self.flag_distant_server_line_reserving.setObjectName("flag_distant_server_line_reserving")
        self.right_column_flag_layout.addWidget(self.flag_distant_server_line_reserving)

        self.read_folder_path = my_widgets.MyFolderOpener(self.main_widget, default_folder="",
                                                                     get_server_func=self.get_server)
        set_size_policy(self.read_folder_path, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.read_folder_path.setObjectName("read_folder_path")
        self.settings_config_layout.addWidget(self.read_folder_path, 3, 0, 1, 2)

        self.flag_use_gpu = QtWidgets.QCheckBox(self.main_widget)
        set_size_policy(self.flag_use_gpu, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_use_gpu.setObjectName("flag_use_gpu")
        self.left_column_flag_layout.addWidget(self.flag_use_gpu)

        self.flag_wait_for_data = QtWidgets.QCheckBox(self.main_widget)
        set_size_policy(self.flag_wait_for_data, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_wait_for_data.setObjectName("flag_wait_for_data")
        self.right_column_flag_layout.addWidget(self.flag_wait_for_data)

        self.flag_store_statistics_local = QtWidgets.QCheckBox(self.main_widget)
        set_size_policy(self.flag_store_statistics_local, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_store_statistics_local.setObjectName("flag_store_statistics_local")
        self.left_column_flag_layout.addWidget(self.flag_store_statistics_local)

        self.flag_recreate_settings_config = QtWidgets.QCheckBox(self.main_widget)
        set_size_policy(self.flag_recreate_settings_config,
                        QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_recreate_settings_config.setObjectName("flag_recreate_settings_config")
        self.right_column_flag_layout.addWidget(self.flag_recreate_settings_config)

        self.flag_create_subscription = QtWidgets.QCheckBox(self.main_widget)
        set_size_policy(self.flag_create_subscription, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_create_subscription.setObjectName("flag_create_subscription")
        self.left_column_flag_layout.addWidget(self.flag_create_subscription)

        self.flag_crash_on_errors = QtWidgets.QCheckBox(self.main_widget)
        set_size_policy(self.flag_crash_on_errors, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_crash_on_errors.setObjectName("flag_crash_on_errors")
        self.right_column_flag_layout.addWidget(self.flag_crash_on_errors)

        self.flag_create_subscription_line = QtWidgets.QLineEdit(self.main_widget)
        set_size_policy(self.flag_create_subscription_line, QtWidgets.QSizePolicy.Minimum,
                        QtWidgets.QSizePolicy.Minimum)
        self.flag_create_subscription_line.setObjectName("flag_create_subscription_line")
        self.left_column_flag_layout.addWidget(self.flag_create_subscription_line)

        self.flag_kp_config = QtWidgets.QCheckBox(self.main_widget)
        set_size_policy(self.flag_kp_config, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_kp_config.setObjectName("flag_kp_config")
        self.right_column_flag_layout.addWidget(self.flag_kp_config)

        self.flag_use_opc = QtWidgets.QCheckBox(self.main_widget)
        set_size_policy(self.flag_use_opc, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_use_opc.setObjectName("flag_use_opc")
        self.left_column_flag_layout.addWidget(self.flag_use_opc)

        self.flag_kp_config_line = my_widgets.MyConfigOpener(self.main_widget,
                                                                        default_conf="configs/KP.ini",
                                                                        get_server_func=self.get_server)
        set_size_policy(self.flag_kp_config_line, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_kp_config_line.setObjectName("flag_kp_config_line")
        self.right_column_flag_layout.addWidget(self.flag_kp_config_line)

        self.flag_use_opc_line_host = QtWidgets.QLineEdit(self.main_widget)
        set_size_policy(self.flag_use_opc_line_host, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_use_opc_line_host.setObjectName("flag_use_opc_line_host")
        self.left_column_flag_layout.addWidget(self.flag_use_opc_line_host)

        self.flag_main_config = QtWidgets.QCheckBox(self.main_widget)
        set_size_policy(self.flag_main_config, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_main_config.setObjectName("flag_main_config")
        self.right_column_flag_layout.addWidget(self.flag_main_config)

        self.flag_use_opc_line_port = QtWidgets.QLineEdit(self.main_widget)
        set_size_policy(self.flag_use_opc_line_port, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_use_opc_line_port.setObjectName("flag_use_opc_line_port")
        self.left_column_flag_layout.addWidget(self.flag_use_opc_line_port)

        self.flag_main_config_line = my_widgets.MyConfigOpener(self.main_widget,
                                                                          default_conf="configs/settings_config.ini",
                                                                          get_server_func=self.get_server)
        set_size_policy(self.flag_main_config_line, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.flag_main_config_line.setObjectName("flag_main_config_line")
        self.right_column_flag_layout.addWidget(self.flag_main_config_line)

        spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.left_column_flag_layout.addSpacerItem(spacer)
        self.right_column_flag_layout.addSpacerItem(spacer)

        self.tabs = QtWidgets.QTabWidget(self.main_widget)
        self.tabs.setObjectName("tabWidget")
        self.setup_flow()
        self.setup_pressure()
        self.main_layout.addWidget(self.tabs, 0, 0, 1, 1)
        self.main_layout.addLayout(self.right_layout, 0, 1, 1, 1)

        main_window.setCentralWidget(self.main_widget)

        self.translate_ui(main_window)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def setup_pressure(self):
        self.pressure = QtWidgets.QTabWidget(self.main_widget)
        self.pressure.setObjectName("pressure")
        sections, pipes_set = get_config("pressure")
        self.tabs.addTab(self.pressure, "")
        for pipe in sorted(self.pipes_set & pipes_set):
            self.pressure_sensors_label[pipe] = QtWidgets.QLabel(self.main_widget)
            self.pressure_selected_sensors_label[pipe] = QtWidgets.QLabel(self.main_widget)
            self.pressure_pipes_tab[pipe] = QtWidgets.QWidget(self.main_widget)
            self.pressure_pipes_tab[pipe].setObjectName("Pipe: " + pipe)
            self.pressure.addTab(self.pressure_pipes_tab[pipe], "")

            self.pressure_grid_for_pipe[pipe] = QtWidgets.QGridLayout(self.pressure_pipes_tab[pipe])

            self.pressure_grid_for_pipe[pipe].addWidget(self.pressure_sensors_label[pipe], 0, 0, 1, 1)
            self.pressure_grid_for_pipe[pipe].addWidget(self.pressure_selected_sensors_label[pipe], 0, 1, 1, 1)

            self.pressure_sensors[pipe] = my_widgets.MyDroppingTable(self.main_widget)
            self.pressure_sensors[pipe].setObjectName("t_pressure_" + pipe + "_sensors")
            self.pressure_grid_for_pipe[pipe].addWidget(self.pressure_sensors[pipe], 1, 0, 1, 1)

            self.pressure_selected_sensors[pipe] = my_widgets.MyDroppingTable(self.main_widget)
            self.pressure_selected_sensors[pipe].setObjectName("t_pressure_" + pipe + "_selected_sensors")
            self.pressure_grid_for_pipe[pipe].addWidget(self.pressure_selected_sensors[pipe], 1, 1, 1, 1)

            filtered_sections = list(sorted(get_config("measurement_%s.*_pressure" % pipe)[0],
                                            key=lambda x: float(x["km"]) if len(x["km"]) else 0))
            num_of_colums = 0
            columns = []
            for section in filtered_sections:
                if len(section) > num_of_colums:
                    num_of_colums = len(section)
                    columns = list(section.keys())

            self.pressure_sensors[pipe].setColumnCount(num_of_colums)
            self.pressure_sensors[pipe].setRowCount(len(filtered_sections))
            self.pressure_sensors[pipe].setHorizontalHeaderLabels(columns)

            self.pressure_selected_sensors[pipe].setColumnCount(num_of_colums)
            self.pressure_selected_sensors[pipe].setHorizontalHeaderLabels(columns)

            for row in range(len(filtered_sections)):
                for col, column in enumerate(columns):
                    if column in filtered_sections[row]:
                        cell = my_widgets.MyTableWidgetItem(filtered_sections[row][column])

                        cell.setFlags(
                            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
                        )

                        self.pressure_sensors[pipe].setItem(row, col, cell)
                self.pressure_sensors[pipe].hideRow(row)
            del filtered_sections

            self.pressure_sensors[pipe].doubleClicked.connect(self.pressure_sensors[pipe].double_clicked)
            self.pressure_selected_sensors[pipe].doubleClicked.connect(self.pressure_selected_sensors[pipe].
                                                                       double_clicked)

            self.pressure_sensors[pipe].resizeColumnsToContents()
            self.pressure_selected_sensors[pipe].resizeColumnsToContents()

            exec("self.t_pressure_" + pipe + "_sensors = self.pressure_sensors[pipe]")
            exec("self.t_pressure_" + pipe + "_selected_sensors = self.pressure_selected_sensors[pipe]")

    def setup_flow(self):
        self.flow = QtWidgets.QTabWidget(self.main_widget)
        self.flow.setObjectName("flow")
        self.tabs.addTab(self.flow, "")
        sections, self.pipes_set = get_config("flow")
        for pipe in sorted(self.pipes_set):
            self.flow_sensors_label[pipe] = QtWidgets.QLabel(self.main_widget)
            self.flow_selected_sensors_label[pipe] = QtWidgets.QLabel(self.main_widget)
            self.flow_pipes_tab[pipe] = QtWidgets.QWidget(self.main_widget)
            self.flow_pipes_tab[pipe].setObjectName("Pipe: " + pipe)
            self.flow.addTab(self.flow_pipes_tab[pipe], "")

            self.flow_grid_for_pipe[pipe] = QtWidgets.QGridLayout(self.flow_pipes_tab[pipe])

            self.flow_grid_for_pipe[pipe].addWidget(self.flow_sensors_label[pipe], 0, 0, 1, 1)
            self.flow_grid_for_pipe[pipe].addWidget(self.flow_selected_sensors_label[pipe], 0, 1, 1, 1)

            self.flow_sensors[pipe] = my_widgets.MyDroppingTable(self.main_widget)
            self.flow_sensors[pipe].setObjectName("t_flow_" + pipe + "_sensors")
            self.flow_grid_for_pipe[pipe].addWidget(self.flow_sensors[pipe], 1, 0, 1, 1)

            self.flow_selected_sensors[pipe] = my_widgets.MyDroppingTable(self.main_widget)
            self.flow_selected_sensors[pipe].setObjectName("t_flow_" + pipe + "_selected_sensors")
            self.flow_grid_for_pipe[pipe].addWidget(self.flow_selected_sensors[pipe], 1, 1, 1, 1)

            filtered_sections = list(sorted(get_config("measurement_%s.*_flow" % pipe)[0],
                                            key=lambda x: float(x["km"]) if len(x["km"]) else 0))
            num_of_colums = 0
            columns = []
            for section in filtered_sections:
                if len(section) > num_of_colums:
                    num_of_colums = len(section)
                    columns = list(section.keys())

            self.flow_sensors[pipe].setColumnCount(num_of_colums)
            self.flow_sensors[pipe].setRowCount(len(filtered_sections))
            self.flow_sensors[pipe].setHorizontalHeaderLabels(columns)

            self.flow_selected_sensors[pipe].setColumnCount(num_of_colums)
            self.flow_selected_sensors[pipe].setHorizontalHeaderLabels(columns)

            for row in range(len(filtered_sections)):
                for col, column in enumerate(columns):
                    if column in filtered_sections[row]:
                        cell = my_widgets.MyTableWidgetItem(filtered_sections[row][column])

                        cell.setFlags(
                            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
                        )

                        self.flow_sensors[pipe].setItem(row, col, cell)
            del filtered_sections

            self.flow_sensors[pipe].doubleClicked.connect(self.flow_sensors[pipe].double_clicked)
            self.flow_selected_sensors[pipe].doubleClicked.connect(self.flow_selected_sensors[pipe].double_clicked)

            self.flow_sensors[pipe].resizeColumnsToContents()
            self.flow_selected_sensors[pipe].resizeColumnsToContents()
            exec("self.t_flow_" + pipe + "_sensors = self.flow_sensors[pipe]")
            exec("self.t_flow_" + pipe + "_selected_sensors = self.flow_selected_sensors[pipe]")

    def get_server(self):
        return (lambda: "") if not self.flag_distant_server.isChecked() else self.flag_distant_server_line_main.text

    def translate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_time_label.setText(_translate("MainWindow", "Start time:"))
        self.end_time_label.setText(_translate("MainWindow", "End time:"))
        self.label_flag.setText(_translate("MainWindow", "Flags:"))
        self.start_time.setDisplayFormat(_translate("MainWindow", "yyyy.MM.dd HH:mm:ss"))
        self.end_time.setDisplayFormat(_translate("MainWindow", "yyyy.MM.dd HH:mm:ss"))
        self.models_folder.setText(_translate("MainWindow", "Models folder"))
        self.detect_models.setText(_translate("MainWindow", "Detect models open"))
        self.localize_models.setText(_translate("MainWindow", "Localize models open"))
        self.read_buffer_size.setDisplayFormat(_translate("MainWindow", "HH:mm:ss 'read buffer'"))
        self.detect_window_size.setDisplayFormat(_translate("MainWindow", "HH:mm:ss 'detect window'"))
        self.read_skip.setSuffix(_translate("MainWindow", " read skip"))
        self.flag_distant_server_line_main.setPlaceholderText(_translate("MainWindow", "Main server"))
        self.flag_distant_server_line_main.setText("//WIN-2MMDL7673AC")
        self.flag_distant_server_line_reserving.setPlaceholderText(_translate("MainWindow", "Reserving server"))
        self.read_folder_path.setText("Folder to read from")

        self.flag_debug.setText(_translate("MainWindow", "debug"))
        self.flag_use_gpu.setText(_translate("MainWindow", "use-gpu"))
        self.flag_store_statistics_local.setText(_translate("MainWindow", "store-statistics-local"))
        self.flag_create_subscription.setText(_translate("MainWindow", "create-subscription"))
        self.flag_kp_config.setText(_translate("MainWindow", "kp-config"))
        self.flag_kp_config_line.setText(_translate("MainWindow", "Select config"))
        self.flag_main_config.setText(_translate("MainWindow", "main-config"))
        self.flag_main_config_line.setText(_translate("MainWindow", "Select config"))
        self.flag_use_opc.setText(_translate("MainWindow", "use-opc"))

        self.flag_wait_for_data.setText(_translate("MainWindow", "wait-for-data"))
        self.flag_distant_server.setText(_translate("MainWindow", "distant-server"))
        self.flag_recreate_settings_config.setText(_translate("MainWindow", "recreate-settings-config"))
        self.flag_crash_on_errors.setText(_translate("MainWindow", "crash-on-errors"))

        self.flag_create_subscription_line.setText(_translate("MainWindow", "opc.tcp://localhost:30108"))
        self.flag_use_opc_line_host.setText(_translate("MainWindow", "172.20.14.1"))
        self.flag_use_opc_line_host.setInputMask("000.000.000.000")
        self.flag_use_opc_line_port.setText(_translate("MainWindow", "4842"))
        self.flag_use_opc_line_port.setInputMask("00000")

        self.load_configuration.setText(_translate("MainWindow", "Load configuration"))
        self.save_configuration.setText(_translate("MainWindow", "Save configuration"))
        self.start_loop.setText(_translate("MainWindow", "Start"))

        self.command_sequence.setItemText(0, _translate("MainWindow", "read-detect-localize-update-sleep"))
        self.command_sequence.setItemText(1, _translate("MainWindow", "detect-localize-update-sleep"))
        self.command_sequence.setItemText(2, _translate("MainWindow", "detect-update-sleep"))
        self.command_sequence.setItemText(3, _translate("MainWindow", "update-sleep"))
        self.command_sequence.setItemText(4, _translate("MainWindow", "sleep"))
        self.distant_server.setItemText(0, _translate("MainWindow", "server228"))
        self.distant_server.setItemText(1, _translate("MainWindow", "localhost"))
        self.distant_server.setItemText(2, _translate("MainWindow", "andrew"))

        self.tabs.setTabText(self.tabs.indexOf(self.flow), _translate("MainWindow", "Flow sensors"))
        self.tabs.setTabText(self.tabs.indexOf(self.pressure), _translate("MainWindow", "Pressure sensors"))

        for pipe in sorted(self.flow_sensors_label.keys()):
            self.flow_sensors_label[pipe].setText(_translate("MainWindow", "All flow sensors of pipe %s" % pipe))

        for pipe in sorted(self.flow_selected_sensors_label.keys()):
            self.flow_selected_sensors_label[pipe].setText(_translate("MainWindow",
                                                                      "All selected flow sensors of pipe %s" % pipe))

        for pipe in sorted(self.pressure_sensors_label.keys()):
            self.pressure_sensors_label[pipe].setText(_translate("MainWindow", "All pressure sensors of pipe %s" %
                                                                 pipe))

        for pipe in sorted(self.pressure_selected_sensors_label.keys()):
            self.pressure_selected_sensors_label[pipe].setText(_translate("MainWindow",
                                                                          "All selected pressure sensors of pipe %s" %
                                                                          pipe))

        for tab in sorted(self.flow_pipes_tab.keys()):
            self.flow.setTabText(self.flow.indexOf(self.flow_pipes_tab[tab]),
                                 _translate("MainWindow", self.flow_pipes_tab[tab].objectName()))

        for tab in sorted(self.pressure_pipes_tab.keys()):
            self.pressure.setTabText(self.pressure.indexOf(self.pressure_pipes_tab[tab]),
                                     _translate("MainWindow", self.pressure_pipes_tab[tab].objectName()))


def set_size_policy(widget, size1, size2):
    size_policy = QtWidgets.QSizePolicy(size1, size2)
    size_policy.setHorizontalStretch(0)
    size_policy.setVerticalStretch(0)
    size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
    widget.setSizePolicy(size_policy)
    return size_policy


def get_config(substr):
    from settings import KP_CONFIG_PATH
    ans = []
    pipes = set()
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(KP_CONFIG_PATH, encoding='utf-8')

    for section in config.sections():
        if len(re.findall(substr, section)):
            adding = config._sections[section].copy()
            adding.update({'section': section})
            adding.move_to_end('section', last=False)
            ans.append(adding)
            pipes.add(section.split("_")[1])
    return ans, pipes
