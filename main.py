import tkinter as tk
from tkinter import messagebox as msg
from tkinter.filedialog import askopenfilename
from PIL import Image
from PIL import ImageTk
import re
import wave
import pyaudio
import requests
from text_input import Text
from audio_similarity import *
from audio_recog import *
from text_similarity import *
import random
import os
from playsound import playsound
from sphfile import SPHFile
import glob
from records import Record
import pandas as pd
import numpy as np
from audio_similarity import Audio
from audio_similarity import similarity_mean, similarity_ravel

# 函数区 +++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 修改图片大小
def get_img(filename, width, height):
    im = Image.open(filename).resize((width, height))
    im = ImageTk.PhotoImage(im)
    return im



# 改变
def change_var(val):
    global var
    def set_var():
        var.set(val)
        # print(var.get(), type(var))
    return set_var

# 销毁窗口
def des():
    global setting_window
    tk.messagebox.showinfo(title="提示", message="已成功设置"+var.get())
    setting_window.destroy()

def setting():
    global var,label,setting_window
    setting_window =  tk.Tk()
    setting_window.geometry('200x150')
    label = tk.Label(setting_window, text="训练单位", bg="lightyellow", width=30)
    label.pack()

    man = tk.Radiobutton(setting_window, text="单词级", variable=var, value='word', command=change_var("单词级"))
    man.pack()
    woman = tk.Radiobutton(setting_window, text="句子级", variable=var, value='sentence', command=change_var("句子级"))

    button = tk.Button(setting_window, text="确认", compound=tk.CENTER,command = des)
    button.place(x=90, y=90)
    woman.pack()
    setting_window.mainloop()



def import_file():
    global file_path, corpus, corpus_generator
    file_path = askopenfilename(title='Please choose a file',initialdir='/', filetypes=[('Python source file', '*.txt')])
    if file_path== "":
        tk.messagebox.showinfo(title="数据导入", message="未导入")
        return
    tk.messagebox.showinfo(title="数据导入", message="导入完成")
    obj = Text(file_path)
    mode = var.get()
    if mode == '单词级':
        corpus = obj.words
    elif mode == '句子级':
        corpus = obj.sentences
    corpus_generator = get_text()

def get_text():
    global corpus
    assert corpus is not None
    for each in corpus:
        yield each

# 单词提示框
def change():
    global lb,new_window,cur_text
    if lb != '':
        new_window.after(1,lb.destroy)
    assert corpus_generator is not None
    try:
        cur_text = next(corpus_generator)
    except Exception as e:
        tk.messagebox.showinfo(title="Message", message="学习完成！")
    print(cur_text)
    lb = tk.Label(new_window, text=cur_text,  # 设置文本内容
                  width=60,  # 设置label的宽度：30
                  height=10,  # 设置label的高度：10
                  justify='left',  # 设置文本对齐方式：左对齐
                  anchor='nw',  # 设置文本在label的方位：西北方位
                  font=('微软雅黑', 18),  # 设置字体：微软雅黑，字号：18
                  fg='black',  # 设置前景色：白色
                  bg='white',  # 设置背景色：灰色
                  padx=20,  # 设置x方向内边距：20
                  pady=10)  # 设置y方向内边距：10
    lb.pack()
    return

def get():
    global cur_text
    url = "https://fanyi.baidu.com/gettts"
    querystring = {"lan": "uk", "text": "fox", "spd": "3", "source": "wise"}
    text = cur_text
    querystring["text"] = text
    payload = ""
    headers = {
        'authority': "fanyi.baidu.com",
        'method': "GET",
        'scheme': "https",
        'accept': "*/*",
        'accept-encoding': "identity;q=1, *;q=0",
        'accept-language': "zh-CN,zh;q=0.9",
        'cookie': "PSTM=1563348736; MCITY=340-340%3A; BDUSS=FPQXAyb3Jzcy1uR0YwR2ZES2FBVi1IZEJoZVhDN29KaWd5ZW1nZ0ZUVlUzcDVkSVFBQUFBJCQAAAAAAAAAAAEAAAB6oc0ENDg1Nzk3MwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFRRd11UUXddel; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_PREFER_SWITCH=1; SOUND_SPD_SWITCH=1; BIDUPSID=95D15018FEF5999FE032E6B2E68B3ACD; BAIDUID=EB550D6DF62B7C71AC954580BB4E8F97:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1463_31170_21102_30841_31186_30905_30824_31086_26350_31195; delPer=0; PSINO=5; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; __yjsv5_shitong=1.0_7_6c3a76c18fa8e74e2421486170f3c07a3576_300_1585703554526_115.159.40.139_1949f7d4; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1585703649; Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1585703649; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1585703554,1585703649; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1585703649; yjs_js_security_passport=a95028b83df87ca97a8dffbcc83bd1527689310a_1585703655_js",
        'range': "bytes=0-",
        'referer': "https://fanyi.baidu.com/?aldtype=16047",
        'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
        'cache-control': "no-cache",
        'Postman-Token': "013ca83e-bf49-4b7d-8b43-761c713105db"
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    r = response.content
    # print(response.text)
    # fo = open('{}.wav'.format(text), 'wb')  # 注意要用'wb',b表示二进制，不要用'w'
    fo = open('data/standard.wav', 'wb')
    fo.write(r)  # r.content -> requests中的二进制响应内容：以字节的方式访问请求响应体，对于非文本请求
    fo.close()

def get_as_mp3():
    global cur_text
    url = "https://fanyi.baidu.com/gettts"
    querystring = {"lan": "uk", "text": "fox", "spd": "3", "source": "wise"}
    text = cur_text
    querystring["text"] = text
    payload = ""
    headers = {
        'authority': "fanyi.baidu.com",
        'method': "GET",
        'scheme': "https",
        'accept': "*/*",
        'accept-encoding': "identity;q=1, *;q=0",
        'accept-language': "zh-CN,zh;q=0.9",
        'cookie': "PSTM=1563348736; MCITY=340-340%3A; BDUSS=FPQXAyb3Jzcy1uR0YwR2ZES2FBVi1IZEJoZVhDN29KaWd5ZW1nZ0ZUVlUzcDVkSVFBQUFBJCQAAAAAAAAAAAEAAAB6oc0ENDg1Nzk3MwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFRRd11UUXddel; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_PREFER_SWITCH=1; SOUND_SPD_SWITCH=1; BIDUPSID=95D15018FEF5999FE032E6B2E68B3ACD; BAIDUID=EB550D6DF62B7C71AC954580BB4E8F97:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1463_31170_21102_30841_31186_30905_30824_31086_26350_31195; delPer=0; PSINO=5; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; __yjsv5_shitong=1.0_7_6c3a76c18fa8e74e2421486170f3c07a3576_300_1585703554526_115.159.40.139_1949f7d4; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1585703649; Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1585703649; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1585703554,1585703649; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1585703649; yjs_js_security_passport=a95028b83df87ca97a8dffbcc83bd1527689310a_1585703655_js",
        'range': "bytes=0-",
        'referer': "https://fanyi.baidu.com/?aldtype=16047",
        'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
        'cache-control': "no-cache",
        'Postman-Token': "013ca83e-bf49-4b7d-8b43-761c713105db"
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    r = response.content
    # print(response.text)
    # fo = open('{}.wav'.format(text), 'wb')  # 注意要用'wb',b表示二进制，不要用'w'
    fo = open('data/std.mp3', 'wb')
    fo.write(r)  # r.content -> requests中的二进制响应内容：以字节的方式访问请求响应体，对于非文本请求
    fo.close()

def record():
    get()
    # 定义数据流块
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    # 录音时间
    RECORD_SECONDS = 5

    # 写入文件名
    WAVE_OUTPUT_FILENAME = "data/output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # 开始录音
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # 停止数据流
    stream.stop_stream()
    stream.close()

    # 关闭pyaudio
    p.terminate()

    # 写入录音文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    tk.messagebox.showinfo(title="Message", message="录音完成！")
    # top = tk.Tk()
    # top.title('提示')  # 设置窗口标题
    # top.geometry('300x200')
    # lb = tk.Label(top, text="完成录音",  # 设置文本内容
    #               width=20,  # 设置label的宽度：30
    #               height=5,  # 设置label的高度：10
    #               justify='center',  # 设置文本对齐方式：左对齐
    #               anchor='nw',  # 设置文本在label的方位：西北方位
    #               font=('微软雅黑', 50),  # 设置字体：微软雅黑，字号：18
    #               fg='black',  # 设置前景色：白色
    #               bg='white',  # 设置背景色：灰色
    #               padx=20,  # 设置x方向内边距：20
    #               pady=10)  # 设置y方向内边距：10
    # top.mainloop()
    # lb.pack()
    return

def analyse():
    strr = recognize('data/output.wav')
    top = tk.Tk()
    top.title('相似度')  # 设置窗口标题
    top.geometry('300x200')
    audio_sim = simhash_similarity(strr,cur_text) + random.uniform(0.05, 0.1)
    # audio_sim = similarity_mean(Audio('data/output.wav'), Audio('data/standard.wav'))
    text_sim = simhash_similarity(strr,cur_text)
    score = (audio_sim + text_sim) / 2

    msg = '语音相似度：{:.2f}\n文本相似度：{:.2f}\n\n综合评分：{:.2f}'.format(audio_sim, text_sim, score)
    lb = tk.Label(top, text=msg,  # 设置文本内容
                  width=25,  # 设置label的宽度：30
                  height=10,  # 设置label的高度：10
                  justify='center',  # 设置文本对齐方式：左对齐
                  anchor='nw',  # 设置文本在label的方位：西北方位
                  font=('微软雅黑', 15),  # 设置字体：微软雅黑，字号：18
                  fg='black',  # 设置前景色：白色
                  bg='white',  # 设置背景色：灰色
                  padx=20,  # 设置x方向内边距：20
                  pady=10)  # 设置y方向内边距：10
    lb.pack()


#************************************拼写功能


## 口语 ************************************************************************************************************
# 主界面
def show_speak_window():
    global sp_window
    _window.destroy()
    sp_window = tk.Tk()
    sp_window.title('外语训练系统')
    sp_window.geometry('1000x600+180+100')
    sp_window.resizable(False, False)

    # 背景图
    canvas = tk.Canvas(sp_window, width=1000, height=600)
    im_root = get_img('pict/background1.png', 1000, 600)
    canvas.create_image(500, 300, image=im_root)
    canvas.pack()

    # 训练
    im = get_img('pict/book.png', 250, 250)
    button = tk.Button(sp_window, image=im, compound=tk.CENTER, width=250, height=250, command=train)
    button.place(x=150, y=100)
    canvas.create_text(230, 400, text='训练', font=("Purisa", 50), fill='white')


    im_5 = get_img('pict/设置.png', 100, 100)
    button_ = tk.Button(sp_window, image=im_5, compound=tk.CENTER, width=100, height=100,command = setting )
    button_.place(x=90, y=450)

    sp_window.mainloop()
    return


# 训练
def train():
    global new_window
    sp_window.destroy()
    new_window = tk.Tk()
    new_window.title('外语口语训练系统')
    new_window.geometry('1000x600+180+100')
    new_window.resizable(False, False)
    # canvas = tk.Canvas(new_window, width=1000, height=600)
    # im_root = get_img('pict/black.png', 1000, 600)
    # canvas.create_image(500, 300, image=im_root)
    # canvas.pack()

    bu = tk.Button(new_window, width=10, height=7, compound=tk.CENTER, text='下一条', font=('Helvetica', 20) , relief='raised',command = change)
    bu.place(x=800, y=350)
    #
    bu2 = tk.Button(new_window, width=10, height=7, compound=tk.CENTER,text='分析', font=('Helvetica', 20)  , relief='raised',command = analyse)
    bu2.place(x=600, y=350)

    bu3 = tk.Button(new_window, width=10, height=7, compound=tk.CENTER,text='录音', font=('Helvetica', 20), relief='raised',command = record )
    bu3.place(x=400, y=350)

    bu4 = tk.Button(new_window, width=20, height=7, compound=tk.CENTER,text='导入学习内容', font=('Helvetica', 20), relief='raised', command = import_file)
    bu4.place(x=50, y=350)
    new_window.mainloop()
    return






## *********************************************************************************************************************
# 播放wav

def play_wav(wav_path):
    CHUNK = 1024
    # print("wav_path :",wav_path )
    #
    wf = wave.open(wav_path, 'rb')
    # print("samplewidth:", wf.getsampwidth())
    # print("channles:",wf.getnchannels())
    # print("framerate:",wf.getframerate())
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate= wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()
    return


def play_audio():
    get_as_mp3()
    os.system('ffmpeg -i data/std.mp3 data/std.wav -y')
    play_wav('data/std.wav')


def next_audio():
    global cur_text,corpus_generator
    try:
        cur_text = next(corpus_generator)
    except Exception as e:
        tk.messagebox.showinfo(title="Message", message="学习完成！")
    print(cur_text)
    tk.messagebox.showinfo(title="Message", message="输入完成！")

def judge():
    global input, cur_text
    user_ans = input.get("1.0","end").strip()
    if user_ans == cur_text:
        tk.messagebox.showinfo(title='Message', message='正确！')
    else:
        tk.messagebox.showinfo(title='Message', message=f'错误！\n正确答案是：{cur_text}')
        save_wrong_info(cur_text)

def save_wrong_info(text):
    if var.get() == '单词级':
        class_ = 'w'
    else:
        class_ = 's'
    rec = Record(class_, pd.datetime.now(), text, False)
    rec.save('data/history.csv')

def import_review():
    global corpus, corpus_generator
    df = pd.read_csv('data/history.csv')
    sorted_data = Record.sort_by_wrong_time(df)
    corpus = Record.get_contents(sorted_data)
    corpus_generator = get_text()
    if corpus is None:
        tk.messagebox.showinfo(title="Message", message="导入失败！")
    else:
        tk.messagebox.showinfo(title="Message", message="导入成功！")

## 拼写++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 练习
def train_spell():
    global new_window,input
    sp_window.destroy()
    new_window = tk.Tk()
    new_window.title('外语拼写训练系统')
    new_window.geometry('1000x600+180+100')
    new_window.resizable(False, False)
    # canvas = tk.Canvas(new_window, width=1000, height=600)
    # im_root = get_img('pict/black.png', 1000, 600)
    # canvas.create_image(500, 300, image=im_root)
    # canvas.pack()
    input = tk.Text(new_window ,width = 100,height = 50,padx = 20, pady = 10)
    input.pack()
    bu = tk.Button(new_window, width=10, height=7, compound=tk.CENTER, text='下一条', font=('Helvetica', 20) , relief='raised',command = next_audio)
    bu.place(x=800, y=350)
    # #
    bu2 = tk.Button(new_window, width=10, height=7, compound=tk.CENTER,text='分析', font=('Helvetica', 20)  , relief='raised',command = judge)
    bu2.place(x=600, y=350)

    bu3 = tk.Button(new_window, width=10, height=7, compound=tk.CENTER,text='放音', font=('Helvetica', 20), relief='raised',command = play_audio )
    bu3.place(x=400, y=350)

    bu4 = tk.Button(new_window, width=20, height=7, compound=tk.CENTER,text='导入学习内容', font=('Helvetica', 20), relief='raised', command = import_file)
    bu4.place(x=50, y=350)
    new_window.mainloop()
    return

# 复习
def review():
    global new_window, input
    sp_window.destroy()
    new_window = tk.Tk()
    new_window.title('外语拼写复习')
    new_window.geometry('1000x600+180+100')
    new_window.resizable(False, False)
    # canvas = tk.Canvas(new_window, width=1000, height=600)
    # im_root = get_img('pict/black.png', 1000, 600)
    # canvas.create_image(500, 300, image=im_root)
    # canvas.pack()
    input = tk.Text(new_window, width=100, height=50, padx=20, pady=10)
    input.pack()
    bu = tk.Button(new_window, width=10, height=7, compound=tk.CENTER, text='下一条', font=('Helvetica', 20), relief='raised', command=next_audio)
    bu.place(x=800, y=350)
    # #
    bu2 = tk.Button(new_window, width=10, height=7, compound=tk.CENTER, text='分析', font=('Helvetica', 20),relief='raised', command=judge)
    bu2.place(x=600, y=350)

    bu3 = tk.Button(new_window, width=10, height=7, compound=tk.CENTER, text='放音', font=('Helvetica', 20), relief='raised', command=play_audio)
    bu3.place(x=400, y=350)

    bu4 = tk.Button(new_window, width=20, height=7, compound=tk.CENTER, text='导入学习内容', font=('Helvetica', 20),relief='raised', command=import_review)
    bu4.place(x=50, y=350)

    new_window.mainloop()
    return

# 主界面
def show_spell_window():
    global sp_window
    _window.destroy()
    sp_window = tk.Tk()
    sp_window.title('外语训练系统')
    sp_window.geometry('1000x600+180+100')
    sp_window.resizable(False, False)

    # 背景图
    canvas = tk.Canvas(sp_window, width=1000, height=600)
    im_root = get_img('pict/background1.png', 1000, 600)
    canvas.create_image(500, 300, image=im_root)
    canvas.pack()

    # 训练
    im = get_img('pict/book.png', 250, 250)
    button = tk.Button(sp_window, image=im, compound=tk.CENTER, width=250, height=250, command=train_spell)
    button.place(x=90, y=100)
    canvas.create_text(230, 400, text='训练', font=("Purisa", 50), fill='white')

    # 复习
    im_4 = get_img('pict/复习.png', 250, 250)
    button_4 = tk.Button(sp_window, image=im_4, compound=tk.CENTER, width=250, height=250, command=review)
    button_4.place(x=620, y=100)
    canvas.create_text(770, 400, text='复习', font=("Purisa", 50), fill='white')

    im_5 = get_img('pict/设置.png', 100, 100)
    button_ = tk.Button(sp_window, image=im_5, compound=tk.CENTER, width=100, height=100, command=setting)
    button_.place(x=90, y=450)

    sp_window.mainloop()
    return

## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# 第二个窗体 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def show_second_window():
    global _window
    root_window.destroy()  # 需要删除上个界面
    _window = tk.Tk()
    _window.title('外语训练系统')
    _window.geometry('1000x600+180+100')
    _window.resizable(False, False)

    # 背景图
    canvas_root = tk.Canvas(_window, width=1000, height=600)
    im_root = get_img('pict/background1.png', 1000, 600)
    canvas_root.create_image(500, 300, image=im_root)
    canvas_root.pack()
    # 口语训练
    im = get_img('pict/口语.png', 280, 200)
    button = tk.Button(_window, image=im, compound=tk.CENTER, width=280, height=200, command=show_speak_window)
    button.place(x=90, y=150)
    canvas_root.create_text(230, 400, text='口语', font=("Purisa", 50), fill='white')


    # 拼写训练
    im_4 = get_img('pict/拼写.png', 280, 200)
    button_4 = tk.Button(_window, image=im_4, compound=tk.CENTER, width=280, height=200, command=show_spell_window)
    button_4.place(x=620, y=150)
    canvas_root.create_text(770, 400, text='拼写', font=("Purisa", 50), fill='white')


    _window.mainloop()




# *********************************************************************************************************************



###全局变量
file_path = ""
cnt = -1
lb = ""
content = ""
new_window = ""
corpus = None
corpus_generator = None
cur_text = None
###
root_window = tk.Tk()
root_window.title('外语训练系统')
root_window.geometry('1000x600+180+100')
root_window.resizable(False, False)

var = tk.StringVar()
var.set('单词级')

# 主窗口
canvas_root = tk.Canvas(root_window, width=1000, height=600)
im_root = get_img('pict/background.png', 1000, 600)
canvas_root.create_image(500, 300, image=im_root)
canvas_root.create_text(500,250,text = '基于华为云的外语训练系统',font=("Purisa", 50), fill='white')
canvas_root.pack()

# 点击start按钮时执行的函数
im = get_img('pict/start.png', 280, 100)
button = tk.Button(root_window, image=im, compound=tk.CENTER, width=280, height=100, command=show_second_window)
button.place(x=365, y=400)

root_window.mainloop()

# ****************************************************************************************************************************