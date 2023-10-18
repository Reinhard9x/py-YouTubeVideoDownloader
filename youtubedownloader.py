import os
from tkinter import *
from tkinter.ttk import *
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror
from tkinter import filedialog
import os


# start download


def download():
    link = entry.get()

    if link != '':
        try:
            def progress(stream, chunk, bytes_remaining):
                total_size = stream.filesize
                # video size name
                def size(total, factor=1024, suffix='B'):
                    # looping through the units
                    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                        if total < factor:
                            return f"{total:.2f}{unit}{suffix}"
                        total /= factor
                    # returning the formatted video size
                    return f"{total:.2f}Y{suffix}"

                formatted_size = size(total_size)
                bytes_downloaded = total_size - bytes_remaining
                percentage_completed = round(bytes_downloaded / total_size * 100)
                bar['value'] = percentage_completed
                percent.set(str(percentage_completed) + '%, File size:' + formatted_size)
                window.update()

            if only_audio.get() == 1:
                global file_type
                file_type = '.mp3'
                video = YouTube(link, on_progress_callback=progress)
                video.streams.get_audio_only().download()
                showinfo(title='Download Complete', message='The audio has been downloaded successfully.')
                percent.set('')
                bar['value'] = 0
                move(video.streams[0].title)
            else:
                file_type = '.mp4'
                video = YouTube(link, on_progress_callback=progress)
                video.streams.get_highest_resolution().download()
                showinfo(title='Download Complete', message='The video has been downloaded successfully.')
                percent.set('')
                bar['value'] = 0
                move(video.streams[0].title)
        except:
            showerror(title='Download Error', message='An error occurred while trying to ' 
                                                      'download the video\nThe following could '
                                                      'be the causes:\n->Invalid link\n->No internet connection\n'
                                                      'Make sure you have stable internet connection and the video link is valid.')
            percent.set('')
            bar['value'] = 0
    else:
        showerror(title='Link Missing!', message='You need to use a Youtube link.')


# delete link


def delete():
    entry.delete(0, END)

# choose where to download


def path():
    filename = filedialog.askdirectory()
    download_location.set(filename)

# move the file


def move(name):
    source = os.getcwd() + '\\' + name + '.mp4'
    print(source)
    print(download_location.get() + '/' + name + file_type)
    os.rename(source, download_location.get() + '/' + name + file_type)

# widow info
window = Tk()
window.title('Video Downloader')
window_height = 170
window_width = 700
window.resizable(False, False)
# center window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width/2)-(window_width/2))
y = int((screen_height/2)-(window_height/2))
window.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))
# icon
icon = PhotoImage(file='youtubelogo.png')
window.iconphoto(True, icon)

# functional part

bytes_downloaded = 0

label = Label(window,
              text='Insert the YouTube video link:',
              font=('Arial', 15, 'bold'))
label.place(x=0, y=0)

entry = Entry(window,
              width=50)
entry.place(x=295, y=3)

download_button = Button(window,
                         text='Download',
                         command=download)
download_button.place(x=0, y=100)

delete_button = Button(window,
                       text='Delete',
                       command=delete)
delete_button.place(x=615, y=2)

only_audio = IntVar()

check = Checkbutton(window,
                    text='Download only audio.',
                    variable=only_audio,
                    onvalue=1,
                    offvalue=0)
check.place(x=0, y=30)

bar = Progressbar(window,
                  orient=HORIZONTAL,
                  length=700)
bar.place(x=0, y=140)

percent = StringVar()

percent_val = Label(window,
                    textvariable=percent)
percent_val.place(x=350, y=120)

# where to download and file type

download_location = StringVar()

file_type = '.mp4'

location = Label(window,
                 textvariable=download_location,
                 width=60,
                 background='white')
location.place(x=0, y=65)

loc_button = Button(window,
                    text='Destination',
                    command=path)
loc_button.place(x=370, y=62)

window.mainloop()
