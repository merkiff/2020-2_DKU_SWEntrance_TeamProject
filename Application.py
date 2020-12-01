import sys
from PyQt5.QtWidgets import QApplication, QTextBrowser, QWidget, QPushButton, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QFileDialog
from YtDl import Download

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        '''UI 세팅'''
        #위젯 생성
        self.linkInput = QLineEdit(self)
        self.submitBtn = QPushButton('Submit', self)
        self.fileRoute = QTextBrowser(self)
        self.fileBtn = QPushButton('file...', self)
        self.mp3Btn = QPushButton('mp3', self)
        self.mp4Btn = QPushButton('mp4', self)   
        self.name = QTextBrowser(self)
        self.status = QLabel(self)
        #이벤트 연결
        self.linkInput.returnPressed.connect(self.inputURL)
        self.submitBtn.clicked.connect(self.inputURL)
        self.fileBtn.clicked.connect(self.setFileRoute)
        self.mp3Btn.clicked.connect(self.mp3Download)
        self.mp4Btn.clicked.connect(self.mp4Download)
        self.mp4Btn.clicked.connect(self.mp4Download)
        
        #레이아웃 생성, 기본 설정
        self.vbox = QVBoxLayout()
        self.InputBox = QHBoxLayout()
        self.fileRouteBox = QHBoxLayout()
        self.titleBox = QHBoxLayout()
        self.downloadbox = QHBoxLayout()
        self.setLayout(self.vbox)
        self.setWindowTitle('Youtube Download')
        self.setGeometry(300, 300, 400, 200)
        self.fileRoute.setMaximumHeight(60)
        self.name.setMaximumHeight(60)
        self.name.setMaximumWidth(195)
        self.show()

        #1: 주소 입력 박스
        self.InputBox.addWidget(QLabel('동영상 주소 입력:', self))
        self.InputBox.addWidget(self.linkInput)
        self.InputBox.addWidget(self.submitBtn)
        self.vbox.addLayout(self.InputBox)
        #2: 파일 경로 박스
        self.fileRouteBox.addWidget(QLabel('  다운로드 경로:  ', self))
        self.fileRouteBox.addWidget(self.fileRoute)
        self.fileRouteBox.addWidget(self.fileBtn)
        self.vbox.addLayout(self.fileRouteBox)
        #3: 영상 제목 박스
        self.titleBox.addWidget(QLabel('    영상 제목:      ', self))
        self.titleBox.addWidget(self.name)
        self.titleBox.addStretch(1)
        self.vbox.addLayout(self.titleBox)
        #4: 다운로드 버튼 박스
        self.downloadbox.addStretch(1)
        self.downloadbox.addWidget(self.mp3Btn)
        self.downloadbox.addWidget(self.mp4Btn)
        self.downloadbox.addStretch(1)
        self.vbox.addLayout(self.downloadbox)
        self.vbox.addWidget(self.status)
        #다운로드 버튼 비활성화
        self.btnStatusFalse()

    def btnStatusFalse(self):
        '''버튼 비활성화'''
        self.mp3Btn.setEnabled(False)
        self.mp4Btn.setEnabled(False)
        self.fileBtn.setEnabled(False)


    def inputURL(self):
        '''주소 입력 시 다운로드 모듈 실행,
        버튼 활성화'''
        self.btnStatusFalse()
        self.status.setText('')
        self.obj = Download(self.linkInput.text())
        self.name.setText(self.obj.getVideoName())
        self.fileRoute.setText(self.obj.parent_dir)
        self.fileBtn.setEnabled(True)
        self.mp3Btn.setEnabled(True)
        self.mp4Btn.setEnabled(True)

    def mp3Download(self):
        '''mp3 다운로드'''
        self.status.setText('downloading...')
        self.obj.downloadMp3()
        self.status.setText('complete!')
        
    def mp4Download(self):
        '''mp4 다운로드'''
        self.status.setText('downloading...')
        self.obj.downloadMp4()
        self.status.setText('complete!')

    def setFileRoute(self):
        '''파일 다운로드 경로 지정'''
        fname = QFileDialog.getExistingDirectory(self)
        self.obj.parent_dir = fname
        self.fileRoute.setText(self.obj.parent_dir)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())