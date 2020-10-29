from Google import Create_Service
from youtubeapifunctions import *
from tkinter import *
from tkinter import messagebox

CLIENT_SECRET_FILE = 'data_files/client_secret_1.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

picked_playlist = {'id': None, 'name': None}
playlists = get_all_playlists(service)

class Mainframe(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Youtube Playlist Manager')
        # start frame
        self.frame = PlaylistPicker(self)
        self.frame.grid()

    # changing frame
    def change(self, frame):
        self.frame = frame(self)
        self.frame.grid()


class PlaylistPicker(Frame):
    def __init__(self, master=None):
        # calling Frame __init__
        Frame.__init__(self, master)

        self.playlists_label = Label(text='Pick a Playlist to sort or clean: ', font="Arial 16 bold")
        self.playlists_label.grid(row=0, column=0)

        for index in range(len(playlists)):
            self.create_button(index + 1, 0, playlists[index]['name'])

    # creating buttons
    def create_button(self, x, y, text):
        tmp = Button(text=text, font="Arial 20 bold", command=lambda: self.save_picked_playlist(text))
        tmp.grid(row=x, column=y, pady=5)
        return tmp

    def save_picked_playlist(self, playlist_name):
        picked_playlist['name'] = playlist_name
        picked_playlist['id'] = playlists[[index for index in range(len(playlists)) if playlists[index]['name'] == picked_playlist['name']][0]]['id']
        if messagebox.askyesno(title='Choice', message='Do you want to clean the playlist first?'):
            messagebox.showinfo(title='Result', message=clean_playlist(service, picked_playlist))
        for widget in self.master.winfo_children():
            widget.grid_remove()
        self.master.change(SortingPicker)


class SortingPicker(Frame):
    def __init__(self, master=None):
        # calling Frame __init__
        Frame.__init__(self, master)

        self.playlists_label = Label(text='Sort the playlist \"' + picked_playlist['name'] + '\" by:', font="Arial 16 bold")
        self.playlists_label.grid(row=0, column=0)

        self.create_button(1, 0, 'Last Uploaded', sort_playlist_by_upload_time, True)
        self.create_button(2, 0, 'First Uploaded', sort_playlist_by_upload_time, False)
        self.create_button(3, 0, 'Last Added', sort_playlist_by_add_time, True)
        self.create_button(4, 0, 'First Added', sort_playlist_by_add_time, False)
        self.create_button(5, 0, 'Most Popular', sort_playlist_by_views, True)
        self.create_button(6, 0, 'Least Popular', sort_playlist_by_views, False)
        self.create_button(7, 0, 'Longest First', sort_playlist_by_video_duration, True)
        self.create_button(8, 0, 'Shortest First', sort_playlist_by_video_duration, False)
        self.create_button(9, 0, 'Alphabetical', sort_playlist_by_alphabet, True)
        self.create_button(10, 0, 'Reverse Alphabetical', sort_playlist_by_alphabet, False)

    # creating buttons
    def create_button(self, x, y, text, function, order):
        tmp = Button(text=text, font="Arial 20 bold", command=lambda: messagebox.showinfo(title='Result', message=function(service, picked_playlist, order)))
        tmp.grid(row=x, column=y, pady=5)
        return tmp


# starts mainframe if the main script is directly run
if __name__ == "__main__":
    app = Mainframe()
    app.mainloop()
