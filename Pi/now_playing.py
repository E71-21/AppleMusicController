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
from kivy.metrics import dp, sp

song_title = ""
artist = ""
album = ""
playlist = ""
path_to_artwork = ""

def get_song():
    global song_title, artist, album, playlist
    try:
        response = requests.get("http://localhost:5050/nowplaying")
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
        print("Exception:", e)


def get_artwork():
    global path_to_artwork
    try:
        shutil.rmtree("Pi/Song Art")
        os.mkdir("Pi/Song Art")
        res = requests.get("http://localhost:5050/artwork")
        if res.ok:
            with open(f"Pi/Song Art/artwork_{song_title.replace(' ', '')}.jpg", "wb") as f:
                f.write(res.content)
            path_to_artwork = f"Pi/Song Art/artwork_{song_title.replace(' ', '')}.jpg"
            print(path_to_artwork)
        else:
            print("Error getting artwork:", res.status_code)
    except Exception as e:
        print("Exception:", e)

class MyApp(App):
    
    def build(self):

        outer_layout = BoxLayout(orientation='horizontal', padding=[dp(70), dp(20), dp(20), dp(20)], spacing=dp(20))

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
            padding=[dp(20), dp(100), dp(20), dp(0)],
            size_hint=(0.5, 1)
        )

        
        song_artist_label_wrapper = BoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=[dp(20), dp(0), dp(20), dp(0)],
            size_hint_y=None,
        )

        self.songlabel = Label(
            text=f'[b]{song_title}[/b]',
            markup=True,
            font_size=dp(70),
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
            font_size=dp(60),
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
            padding=[dp(20), dp(0), dp(20), dp(0)],
            size_hint_y=None,
        )

        self.albumlabel = Label(
            text=album,
            font_size=dp(52),
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
                font_size=dp(52),
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
            spacing=dp(130),
            padding=[0, 0, 0, dp(30)],
        )
        content_wrapper.bind(minimum_height=content_wrapper.setter('height')) # type: ignore

        content_wrapper.add_widget(song_artist_label_wrapper)
        content_wrapper.add_widget(album_playlist_label_wrapper)
        
        button_anchor = AnchorLayout(
            anchor_x='center',
            anchor_y='bottom',
            padding=[0, 0, 0, dp(80)]
        )

        self.button_wrapper = BoxLayout(
            orientation="horizontal",
            spacing=dp(20)
        )

        self.previous_button = Button(
            size_hint=(None, None),
            size=(dp(120), dp(120)),
            background_normal='Pi/Assets/previous.png',
            background_down='Pi/Assets/previous.png',
            border=(0, 0, 0, 0)
        )
        
        self.play_pause_button = Button(
            size_hint=(None, None),
            size=(dp(120), dp(120)),
            background_normal='Pi/Assets/pause.png',
            background_down='Pi/Assets/pause.png',
            border=(0, 0, 0, 0)
        )

        self.next_button = Button(
            size_hint=(None, None),
            size=(dp(120), dp(120)),
            background_normal='Pi/Assets/next.png',
            background_down='Pi/Assets/next.png',
            border=(0, 0, 0, 0)
        )


        def previous_song(instance):
            requests.get("http://localhost:5050/previous")
            self.update_song_info()
        
        def next_song(instance):
            requests.get("http://localhost:5050/next")
            self.update_song_info()

        self.is_playing = True

        def toggle_play_pause(instance):
            self.is_playing = not self.is_playing
            if self.is_playing:
                self.play_pause_button.background_normal = 'Pi/Assets/pause.png'
                self.play_pause_button.background_down = 'Pi/Assets/pause.png'
                requests.get("http://localhost:5050/playpause")
                print("Playing music...")
            else:
                self.play_pause_button.background_normal = 'Pi/Assets/play.png'
                self.play_pause_button.background_down = 'Pi/Assets/play.png'
                requests.get("http://localhost:5050/playpause")
                print("Paused music...")

        self.play_pause_button.bind(on_press=toggle_play_pause) # type: ignore
        self.previous_button.bind(on_press=previous_song) # type: ignore
        self.next_button.bind(on_press=next_song) # type: ignore

        self.button_wrapper.add_widget(self.previous_button)
        self.button_wrapper.add_widget(self.play_pause_button)
        self.button_wrapper.add_widget(self.next_button)

        button_anchor.add_widget(self.button_wrapper)

        content_wrapper.add_widget(button_anchor)

        inner_layout.add_widget(content_wrapper)

        outer_layout.add_widget(inner_layout)

        self.update_song_info()
        return outer_layout
    
    
    def update_song_info(self):
            global song_title, artist, album, playlist
            get_song()
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


