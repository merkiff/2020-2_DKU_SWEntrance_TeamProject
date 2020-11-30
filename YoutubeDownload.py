from pytube import YouTube
import os.path
import ffmpeg

def downloadMp3():
    '''mp3 파일로 다운로드하는 함수'''
    #mp4형태지만 영상 없이 소리만 있는 파일 다운로드
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(parent_dir)

    src = stream.default_filename
    dst = stream.default_filename[0:-3] + 'mp3' #mp3로 변환된 파일명

    #mp4에서 mp3로 변환
    ffmpeg.input(os.path.join(parent_dir, src)).output(os.path.join(parent_dir, dst)).run()

    #변환되기 전 mp4파일 삭제
    os.remove(os.path.join(parent_dir, src))

    return dst #파일명만 리턴

def downloadMp4():
    '''mp4 파일로 다운로드하는 함수'''
    audio = downloadMp3()   #mp3파일 다운로드
    video = yt.streams.filter(adaptive=True, file_extension='mp4', fps = 30).first()
    print(video)
    video.download(parent_dir)  #mp4파일 다운로드

    #mp4로 해상도 높은 파일을 받으면 vcodec만 존재
    #->비디오에 소리를 입히려면 acodec 있는 파일 받아 FFmpeg로 병합
    inputAudio = ffmpeg.input(os.path.join(parent_dir, audio))
    inputVideo = ffmpeg.input(os.path.join(parent_dir, video.default_filename))

    #영상에 소리 입히기
    ffmpeg.output(inputAudio, inputVideo, os.path.join(parent_dir, "new.mp4"), vcodec='copy', acodec='aac').run(overwrite_output=True)

    #변환이 끝나 더 이상 필요 없는 mp3, mp4 파일 지우기
    os.remove(os.path.join(parent_dir, video.default_filename))
    os.remove(os.path.join(parent_dir, audio))

    #파일명 바꾸기
    os.rename(os.path.join(parent_dir, "new.mp4"), os.path.join(parent_dir, video.default_filename))

    return video.default_filename


print("유튜브 동영상 링크를 입력하세요>>", end = " ")
video = input()
yt = YouTube(video)
print(yt.title)

#다운로드 받을 디렉토리 지정
parent_dir = "C:\\Users\\32200542\\Desktop\\단국대\\1-2\\대학기초SW입문\\팀프로젝트\\projectTest"

print("mp3로 저장하려면 1, mp4로 저장하려면 2")
fileFormat = int(input())

if(fileFormat == 1):    #mp3 다운로드
    print("mp3로 다운로드합니다.")
    fileName = downloadMp3()
    print(f"{fileName}을 다운로드했습니다.")
else:   #mp4 다운로드
    print("mp4로 다운로드합니다.")
    fileName = downloadMp4()
    print(f"{fileName}을 다운로드했습니다.")