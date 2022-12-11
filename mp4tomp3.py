# -*- coding: gbk -*-


from moviepy.editor import VideoFileClip,AudioFileClip,afx
import tkinter
from tkinter.filedialog import *
from tkinter import messagebox
root = tkinter.Tk()
root.geometry('300x200+600+400')
files = tkinter.StringVar()
saves = tkinter.StringVar()
def file_path(path):
    path_ = askopenfilename()
    path.set(path_)
def save_path(path):
    path_ = asksaveasfilename()
    path.set(path_)
def main(file_paths,save_paths):
    try:
        video = VideoFileClip(file_paths)
    except:
        messagebox.showerror('错误!','读取文件出错')
    try:
        audio = video.audio
        if '.mp3' not in save_paths:save_paths+='.mp3'
        audio.write_audiofile(save_paths)
        messagebox.showinfo('完成！','成功提取MP3文件')
    except:
        messagebox.showerror('错误!', '提取音乐出错')
tkinter.Button(root,text='选择视频文件',
               font=('宋体',15),bg='#33ff99',command=lambda :file_path(files)).place(x=0,y=0)
tkinter.Button(root,text='存储路径',font=('宋体',15),bg='#33ff99',
               command=lambda :save_path(saves)).place(x=200,y=0)
tkinter.Button(root,text='转换',font=('宋体',20),bg='#FFFF00',fg='red',command=lambda :main(files.get(),saves.get())).place(x=100,y=100)
root.mainloop()

