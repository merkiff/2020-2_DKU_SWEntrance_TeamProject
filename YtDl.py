from pytube import YouTube  #유튜브영상을 다운로드하기 위한 모듈
import os.path              #경로를 설정하기 위한 모듈
import ffmpeg               #미디어를 변환하기 위한 모듈
from getpass import getuser #기본 경로를 다운로드 폴더로 지정하기 위한 모듈

class Download:
    '''
    파일을 변환하기 위해선 ffmpeg란 프로그램을 별도로 설치해 컴퓨터 환경변수 설정을 마쳐야 함.
    '''
    def __init__(self, link):
        #link 인자는 gui에서 입력된 값을 받을 때 사용
        #컴퓨터 이용자명을 받아서 다운로드폴더를 기본폴더로 지정
        self.parent_dir = f"C:\\Users\\{getuser()}\\Downloads"
        self.yt = YouTube(link)

    def getVideoName(self):
        '''(GUI버전) 비디오 이름을 내보내는 함수'''
        name = self.yt.title
        return name

    def downloadMp3(self):
        '''mp3 파일로 다운로드하는 함수'''
        #mp4형태지만 영상 없이 소리만 있는 파일 다운로드
        stream = self.yt.streams.filter(only_audio=True).first()
        stream.download(self.parent_dir)

        src = stream.default_filename   #mp4로 다운받은 영상제목(파일명과 같음)
        dst = stream.default_filename[0:-3] + 'mp3' #mp3로 변환된 파일명

        #mp4에서 mp3로 변환
        ffmpeg.input(os.path.join(self.parent_dir, src)).output(os.path.join(self.parent_dir, dst)).run(overwrite_output=True)

        #변환되기 전 mp4파일 삭제
        os.remove(os.path.join(self.parent_dir, src))

        return dst #저장한 파일명 리턴

    def downloadMp4(self):
        '''mp4 파일로 다운로드하는 함수'''
        audio = self.downloadMp3()   #mp3파일 다운로드
        video = self.yt.streams.filter(adaptive=True, file_extension='mp4', fps = 30).first()
        print(video)
        video.download(self.parent_dir)  #mp4파일 다운로드

        #mp4로 해상도 높은 파일을 받으면 vcodec만 존재
        #->비디오에 소리를 입히려면 acodec 있는 파일 받아 FFmpeg로 병합
        #->downloadMp3로 mp3파일을 받고 오디오 소스로 사용
        inputAudio = ffmpeg.input(os.path.join(self.parent_dir, audio))
        inputVideo = ffmpeg.input(os.path.join(self.parent_dir, video.default_filename))

        #영상에 소리 입혀 "new.mp4"파일로 내보내기
        ffmpeg.output(inputAudio, inputVideo, os.path.join(self.parent_dir, "new.mp4"), vcodec='copy', acodec='aac').run(overwrite_output=True)

        #변환이 끝나 더 이상 필요 없는 mp3, mp4 파일 지우기
        os.remove(os.path.join(self.parent_dir, video.default_filename))
        os.remove(os.path.join(self.parent_dir, audio))

        #"new.mp4"를 영상 제목으로 바꾸기
        os.rename(os.path.join(self.parent_dir, "new.mp4"), os.path.join(self.parent_dir, video.default_filename))

        return video.default_filename   #저장한 파일명 리턴
