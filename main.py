'''
作者：yowayimono
日期：2023-05-19 20:21:29
最后编辑者：yowayimono
最后编辑时间：2023-05-20 13:52:43
描述：无
'''
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QLineEdit, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class VideoConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口属性
        self.setWindowTitle("视频工具")
        self.setGeometry(100, 100, 500, 300)

        # 创建标签
        self.input_label = QLabel("视频文件：", self)
        self.input_label.move(20, 20)
        self.input_label.setFont(QFont("Arial", 8))

        self.output_label = QLabel("保存路径：", self)
        self.output_label.move(20, 60)
        self.output_label.setFont(QFont("Arial", 8))

        self.output_name_label = QLabel("文件名：", self)
        self.output_name_label.move(20, 100)
        self.output_name_label.setFont(QFont("Arial", 8))

        # 创建用于输出文件名的文本框
        self.output_name_textbox = QLineEdit(self)
        self.output_name_textbox.move(90, 100)

        # 创建保存按钮
        self.save_button = QPushButton("保存", self)
        self.save_button.move(300, 100)
        self.save_button.setFont(QFont("Arial", 8, QFont.Bold))
        self.save_button.clicked.connect(self.save_output_file)

        # 创建用于选择输入文件和输出路径的按钮
        self.input_button = QPushButton("视频文件", self)
        self.input_button.move(300, 20)
        self.input_button.setFont(QFont("Arial", 8))
        self.input_button.clicked.connect(self.select_input_file)

        self.output_button = QPushButton("输出路径", self)
        self.output_button.move(300, 60)
        self.output_button.setFont(QFont("Arial", 8))
        self.output_button.clicked.connect(self.select_output_path)

        # 创建转换按钮
        self.convert_button = QPushButton("转换", self)
        self.convert_button.move(300, 140)
        self.convert_button.setFont(QFont("Arial", 8, QFont.Bold))
        self.convert_button.clicked.connect(self.convert_video)

        # 创建用于选择输出格式的组合框
        self.output_format_combobox = QComboBox(self)
        self.output_format_combobox.addItem("mp4")
        self.output_format_combobox.addItem("mp3")
        self.output_format_combobox.addItem("avi")
        self.output_format_combobox.addItem("flv")
        self.output_format_combobox.move(130, 60)

        # 初始化变量
        self.input_file = ""
        self.output_path = ""

    def select_input_file(self):
        # 打开文件对话框以选择输入文件
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("视频文件 (*.mp4 *.avi *.mkv *.flv)")
        if file_dialog.exec_():
            self.input_file = file_dialog.selectedFiles()[0]

    def select_output_path(self):
        # 打开文件对话框以选择输出路径
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        if file_dialog.exec_():
            self.output_path = file_dialog.selectedFiles()[0]

    def save_output_file(self):
        if not self.input_file or not self.output_path:
            return

        # 获取选择的输出格式和输出文件名
        output_format = self.output_format_combobox.currentText()
        output_name = self.output_name_textbox.text()

        if not output_name:
            output_name = "output"

        # 设置输出文件路径和用于 ffmpeg 转换的命令
        output_file = f"{self.output_path}/{output_name}.{output_format}"
        command = f"ffmpeg -i {self.input_file} -y {output_file}"

        try:
            # 使用 subprocess 运行 ffmpeg 命令
            subprocess.run(command, shell=True, check=True)
            print("转换成功！")
        except subprocess.CalledProcessError as e:
            print(f"转换失败：{e}")

    def convert_video(self):
        self.save_output_file()

# 创建应用程序和窗口
app = QApplication(sys.argv)
window = VideoConverterApp()
window.show()

# 运行应用程序
sys.exit(app.exec_())