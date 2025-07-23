from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable')



from kivy.core.window import Window
import requests
import shutil
import os


# Set 5:3 aspect ratio
Window.size = (800, 480)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.stencilview import StencilView
from kivy.uix.widget import Widget
from kivy.core.image import Image as CoreImage
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.clock import Clock

song_title = ""
artist = ""
album = ""
playlist = ""
path_to_artwork = ""

IP_ADRESS = "" # Set to the ip adress of the host (the device running music_server.py)
PORT = "5050" # Set to the port the server is runnning at (5050 is default)
PATH_TO_APPLEMUSICCONTROLLER = ""

def get_song():
    global song_title, artist, album, playlist
    try:
        response = requests.get("http://"+IP_ADRESS+":"+PORT+"/nowplaying")
        if response.ok:
            data = response.json()
            print("Song:", data.get('title'))
            print("Artist:", data.get('artist'))
            print("Album:", data.get('album'))
            print("Playlist:", data.get('playlist'))
            song_title = data.get('title')
            artist = data.get('artist')
            album = data.get('album')
            playlist = data.get('playlist')
        else:
            print("Error:", response.status_code)
    except Exception as e:
        print("Exception get song:", e)


def get_artwork():
    global path_to_artwork
    try:
        shutil.rmtree(PATH_TO_APPLEMUSICCONTROLLER+"/Pi/Song Art")
        os.mkdir(PATH_TO_APPLEMUSICCONTROLLER+"/Pi/Song Art")
        res = requests.get("http://"+IP_ADRESS+":"+PORT+"/artwork")
        if res.ok:
            with open(PATH_TO_APPLEMUSICCONTROLLER+f"/Pi/Song Art/artwork_{song_title.replace(' ', '')}.jpg", "wb") as f:
                f.write(res.content)
            path_to_artwork = PATH_TO_APPLEMUSICCONTROLLER+f"/Pi/Song Art/artwork_{song_title.replace(' ', '')}.jpg"
            print(path_to_artwork)
        else:
            print("Error getting artwork:", res.status_code)
    except Exception as e:
        print("Exception get artwork:", e)

class MyApp(App):
    
    def build(self):

        outer_layout = BoxLayout(orientation='horizontal', padding=[dp(70), dp(20), dp(0), dp(20)], spacing=dp(20))

        with outer_layout.canvas.before: # type: ignore
            Color(0.10, 0.11, 0.12, 1)
            self.rect = Rectangle(size=outer_layout.size, pos=outer_layout.pos)
        
        outer_layout.bind(size=self._update_rect, pos=self._update_rect) # type: ignore


        self.image_container = Widget(size_hint=(0.5, 1))

        with self.image_container.canvas: # type: ignore
            Color(1, 1, 1, 1)
            self.image_texture = CoreImage(path_to_artwork).texture
            self.rounded_image = RoundedRectangle(
                texture=self.image_texture,
                pos=self.image_container.pos,
                size=self.image_container.size,
            )

        self.image_container.bind(pos=self._update_rounded_image, size=self._update_rounded_image) # type: ignore
        outer_layout.add_widget(self.image_container)


        inner_layout = AnchorLayout(
            anchor_y='top',
            padding=[dp(20), dp(30), dp(0), dp(0)],
            size_hint=(0.5, 1)
        )

        
        song_artist_label_wrapper = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=[dp(20), dp(0), dp(0), dp(0)],
            size_hint_y=None,
        )

        self.songlabel = Label(
            text=f'[b]{song_title}[/b]',
            markup=True,
            font_size=dp(40),
            color=(0.98, 0.98, 0.96, 1),
            halign='left',
            valign='middle',
            size_hint_y=None
        )
        self.songlabel.bind( # type: ignore
            width=lambda instance, value: setattr(instance, 'text_size', (value, None)),
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        
        song_artist_label_wrapper.add_widget(self.songlabel)

        self.artistlabel = Label(
            text=artist,
            font_size=dp(30),
            color=(0.63, 0.63, 0.63, 1),
            halign='left',
            valign='middle',
            size_hint_y=None
        )
        self.artistlabel.bind( # type: ignore
            width=lambda instance, value: setattr(instance, 'text_size', (value, None)),
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        song_artist_label_wrapper.add_widget(self.artistlabel)
        song_artist_label_wrapper.bind( # type: ignore
                    minimum_height=song_artist_label_wrapper.setter('height') # type: ignore
                )




        album_playlist_label_wrapper = BoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=[dp(20), dp(0), dp(0), dp(0)],
            size_hint_y=None,
        )

        self.albumlabel = Label(
            text=album,
            font_size=dp(25),
            color=(0.63, 0.63, 0.63, 1),
            halign='left',
            valign='middle',
            size_hint_y=None
        )
        self.albumlabel.bind( # type: ignore
            width=lambda instance, value: setattr(instance, 'text_size', (value, None)),
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        album_playlist_label_wrapper.add_widget(self.albumlabel)


        if playlist and not playlist == "Library":
            self.playlistlabel = Label(
                text=playlist,
                font_size=dp(25),
                color=(0.63, 0.63, 0.63, 1),
                halign='left',
                valign='middle',
                size_hint_y=None
            )
            self.playlistlabel.bind( # type: ignore
                width=lambda instance, value: setattr(instance, 'text_size', (value, None)),
                texture_size=lambda instance, value: setattr(instance, 'height', value[1])
            )
            album_playlist_label_wrapper.add_widget(self.playlistlabel)


        content_wrapper = BoxLayout(
            orientation='vertical',
            spacing=dp(0),
            padding=[0, 0, 0, dp(30)],
        )
        content_wrapper.bind(minimum_height=content_wrapper.setter('height')) # type: ignore

        content_wrapper.add_widget(song_artist_label_wrapper)
        content_wrapper.add_widget(album_playlist_label_wrapper)
        
        button_anchor = AnchorLayout(
            anchor_x='center',
            anchor_y='bottom',
            padding=[0, 0, 0, dp(25)]
        )

        self.button_wrapper = BoxLayout(
            orientation="horizontal",
            spacing=dp(10)
        )

        self.previous_button = Button(
            size_hint=(None, None),
            size=(dp(65), dp(65)),
            background_normal=PATH_TO_APPLEMUSICCONTROLLER+'/Pi/Assets/previous.png',
            background_down=PATH_TO_APPLEMUSICCONTROLLER+'/Pi/Assets/previous.png',
            border=(0, 0, 0, 0)
        )
        
        self.play_pause_button = Button(
            size_hint=(None, None),
            size=(dp(70), dp(70)),
            background_normal=PATH_TO_APPLEMUSICCONTROLLER+'/Pi/Assets/play_pause.png',
            background_down=PATH_TO_APPLEMUSICCONTROLLER+'/Pi/Assets/play_pause.png',
            border=(0, 0, 0, 0)
        )

        self.next_button = Button(
            size_hint=(None, None),
            size=(dp(65), dp(65)),
            background_normal=PATH_TO_APPLEMUSICCONTROLLER+'/Pi/Assets/next.png',
            background_down=PATH_TO_APPLEMUSICCONTROLLER+'/Pi/Assets/next.png',
            border=(0, 0, 0, 0)
        )


        def previous_song(instance):
            requests.get("http://"+IP_ADRESS+":"+PORT+"/previous")
            self.update_song_info()
        
        def next_song(instance):
            requests.get("http://"+IP_ADRESS+":"+PORT+"/next")
            self.update_song_info()


        def toggle_play_pause(instance):
            requests.get("http://"+IP_ADRESS+":"+PORT+"/playpause")
                

        self.play_pause_button.bind(on_release=toggle_play_pause) # type: ignore
        self.previous_button.bind(on_release=previous_song) # type: ignore
        self.next_button.bind(on_release=next_song) # type: ignore

        self.button_wrapper.add_widget(self.previous_button)
        self.button_wrapper.add_widget(self.play_pause_button)
        self.button_wrapper.add_widget(self.next_button)

        button_anchor.add_widget(self.button_wrapper)

        content_wrapper.add_widget(button_anchor)

        inner_layout.add_widget(content_wrapper)

        outer_layout.add_widget(inner_layout)

        self.update_song_info()
        Clock.schedule_interval(lambda dt: self.update_song_info(), 1)  # every 2 seconds
        return outer_layout
    
    
    def update_song_info(self):
            global song_title, artist, album, playlist
            old_song = song_title
            get_song()
            if old_song == song_title: return
            self.songlabel.text = f"[b]{song_title}[/b]"
            self.artistlabel.text = artist
            self.albumlabel.text = album
            

            if hasattr(self, 'playlistlabel') and self.playlistlabel:
                self.playlistlabel.text = playlist if (playlist and playlist != "Library") else ""
            
            get_artwork()
            self.image_texture = CoreImage(path_to_artwork, nocache=True).texture
            self.rounded_image.texture = self.image_texture
            self._update_rounded_image(self.image_container, None)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    
    def _update_rounded_image(self, instance, value):
        container_width, container_height = instance.size
        container_x, container_y = instance.pos

        tex_width = self.image_texture.width # type: ignore
        tex_height = self.image_texture.height # type: ignore
        tex_aspect = tex_width / tex_height
        container_aspect = container_width / container_height

        if tex_aspect > container_aspect:
            new_width = container_width
            new_height = container_width / tex_aspect
        else:
            new_height = container_height
            new_width = container_height * tex_aspect

        new_x = container_x + (container_width - new_width) / 2
        new_y = container_y + (container_height - new_height) / 2

        self.rounded_image.pos = (new_x, new_y)
        self.rounded_image.size = (new_width, new_height)
        self.rounded_image.radius = [min(new_width, new_height) * 0.1]
    
    



if __name__ == "__main__":
    get_song()
    get_artwork()
    print(song_title, artist, album, playlist)
    MyApp().run()




