from tkinter import*
import os
from PIL import Image,ImageTk
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame                                           #to handle sound,for playing sound

window=Tk()
window.title("D.D Music")
window.geometry('900x420')
icon = PhotoImage(file='C:\\Users\\ACER\\Pictures\\iconmp.png')
window.iconphoto(True,icon)
window.config(background='#79a6c6')


title_label = Label(window, text="🎵 MP3 PLAYER 🎵", font=("Arial", 18, "bold"),
                    bg="#2c3e50", fg="white")
title_label.pack(pady=10)


song_name_label = Label(window, text="No song playing", font=("Arial", 10, "bold"), #Song name below the image
                        bg="#2c3e50", fg="white")
song_name_label.place(x=65,y=320)

#Now playing label
now_playing_label = Label(window, text="", font=("Arial", 10),
                          bg="#2c3e50", fg="#95a5a6")
now_playing_label.place(x=65,y=320)

#Song listbox with scrollbar
list_frame = Frame(window, bg="#2c3e50")
list_frame.place(x=300, y=90, width=400, height=250)
scrollbar = Scrollbar(list_frame)
scrollbar.pack(side=RIGHT, fill=Y)

song_listbox = Listbox(list_frame, font=("Arial", 11), bg="#34495e", fg="white",
                       selectbackground="#3498db", yscrollcommand=scrollbar.set,
                       height=12)
song_listbox.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=song_listbox.yview)



paths=["C:\\Users\\ACER\\Pictures\\pythonpro1.jpg","C:\\Users\\ACER\\Pictures\\pythonpro2.jpg",
       "C:\\Users\\ACER\\Pictures\\pythonpro3.jpg","C:\\Users\\ACER\\Pictures\\python4.jpg"]

images=[]
for path in paths:
    img = Image.open(path)
    img = img.resize((200, 200))
    images.append(ImageTk.PhotoImage(img))

index = 0
label = Label(window,text="Now playing",font=("Arial",16))

label.place(relx=0.045, rely=0.5, anchor="w")




def change_image():
    global index
    label.config(image=images[index])
    index = (index + 1) % len(images)
    window.after(10000, change_image)

change_image()


def play_selected_song():
    """Play the selected song from the list"""
    global current_song_index
    selection = song_listbox.curselection()

    if selection:
        current_song_index = selection[0]
        song_name = mp3_files[current_song_index]  # Name of the song
        file_path = os.path.join(folder, song_name)

        if os.path.exists(file_path):
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            song_name_label.config(text=song_name)
            now_playing_label.config(text="Now playing")
            play_pause_btn.config(text="⏸ Pause")
        else:
            print("File not found")


def toggle_play_pause():
    """Toggle between play and pause"""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        play_pause_btn.config(text="▶ Play")
    else:
        pygame.mixer.music.unpause()
        play_pause_btn.config(text="⏸ Pause")


def stop_music():
    """Stop the music"""
    pygame.mixer.music.stop()
    song_name_label.config(text="No song playing")
    now_playing_label.config(text="")
    play_pause_btn.config(text="▶ Play")


def next_song():
    """Play next song"""
    global current_song_index
    if current_song_index < len(mp3_files) - 1:
        current_song_index += 1
        song_listbox.selection_clear(0, END)
        song_listbox.selection_set(current_song_index)
        play_selected_song()


def previous_song():
    """Play previous song"""
    global current_song_index
    if current_song_index > 0:
        current_song_index -= 1
        song_listbox.selection_clear(0, END)
        song_listbox.selection_set(current_song_index)
        play_selected_song()


def set_volume(val):
    """Set volume"""
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

play_pause_btn = None
current_song_index = 0
folder = "Music"   # use real path

mp3_files=[]
def main():
    global mp3_files
    try:
        pygame.mixer.init()                             #It initializes the mixer module of Pygame,
                                                        #  which is responsible for handling audio (music and sound effects).
    except pygame.error as e:
        print("Audio initialization failed! ",e)
        return
    song_listbox.delete(0, END)
    mp3_files = []

    if not os.path.isdir(folder):
        print(f"Folder '{folder}' not found")
        return

    mp3_files= [file for file in os.listdir(folder) if file.endswith(".mp3")]

    song_listbox.delete(0, END)
    for song in mp3_files:
        song_listbox.insert(END, song)


    if not mp3_files:
        print("No .mp3 files found")


#Double-click to play
song_listbox.bind('<Double-Button-1>', lambda e: play_selected_song())

# Control buttons frame
control_frame = Frame(window,bg="#2c3e50")
control_frame.place(x=300,y=370)

# Buttons
prev_btn = Button(control_frame, text="⏮ Previous", command=previous_song,
                  font=("Arial", 10), bg="#3498db", fg="white", width=10)
prev_btn.grid(row=0, column=0, padx=5)

play_pause_btn = Button(control_frame, text="▶ Play", command=toggle_play_pause,
                            font=("Arial", 10), bg="#2ecc71", fg="white", width=10)
play_pause_btn.grid(row=0, column=1, padx=5)

stop_btn = Button(control_frame, text="⏹ Stop", command=stop_music,
                      font=("Arial", 10), bg="#e74c3c", fg="white", width=10)
stop_btn.grid(row=0, column=2, padx=5)

next_btn = Button(control_frame, text="Next ⏭", command=next_song,
                      font=("Arial", 10), bg="#3498db", fg="white", width=10)
next_btn.grid(row=0, column=3, padx=5)

# Volume control
volume_frame = Frame(window, bg="#79a6c6")
volume_frame.place(x=20,y=370)

volume_label = Label(volume_frame, text="🔊", font=("Arial", 30),
                         bg="#79a6c6", fg="white",bd=0,activebackground="#2c3e50",activeforeground="white")
volume_label.pack(side=LEFT, padx=(5,10))

volume_slider = Scale(volume_frame, from_=0, to=100, orient=HORIZONTAL,
                          command=set_volume, fg="white",
                          length=150, showvalue=0,sliderlength=12,bd=0,highlightthickness=0,troughcolor="#b0b0b0",bg="#79a6c6")
volume_slider.set(60)
volume_slider.pack(side=LEFT)


main()
window.mainloop()
