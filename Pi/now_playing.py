from kivy.core.window import Window
import requests

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

song_title = ""
artist = ""
album = ""
playlist = ""

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
    try:
        res = requests.get("http://localhost:5050/artwork")
        if res.ok:
            with open("Pi/artwork.jpg", "wb") as f:
                f.write(res.content)
            print("Artwork saved as artwork.jpg")
        else:
            print("Error getting artwork:", res.status_code)
    except Exception as e:
        print("Exception:", e)

class MyApp(App):
    def build(self):
        outer_layout = BoxLayout(orientation='horizontal', padding=[70, 20, 20, 20], spacing=20)

        with outer_layout.canvas.before: # type: ignore
            Color(0.10, 0.11, 0.12, 1)
            self.rect = Rectangle(size=outer_layout.size, pos=outer_layout.pos)
        
        outer_layout.bind(size=self._update_rect, pos=self._update_rect) # type: ignore


        image_container = Widget(size_hint=(0.5, 1))

        with image_container.canvas: # type: ignore
            Color(1, 1, 1, 1)
            self.image_texture = CoreImage("Pi/artwork.jpg").texture
            self.rounded_image = RoundedRectangle(
                texture=self.image_texture,
                pos=image_container.pos,
                size=image_container.size,
                radius=[50]
            )

        image_container.bind(pos=self._update_rounded_image, size=self._update_rounded_image) # type: ignore
        outer_layout.add_widget(image_container)


        inner_layout = AnchorLayout(
            anchor_y='top',
            padding=[20, 100, 20, 0],
            size_hint=(0.5, 1)
        )

        
        song_artist_label_wrapper = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=[20, 0, 20, 0],
            size_hint_y=None,
        )

        self.songlabel = Label(
            text=f'[b]{song_title}[/b]',
            markup=True,
            font_size=70,
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
            font_size=60,
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
            spacing=20,
            padding=[20, 0, 20, 0],
            size_hint_y=None,
        )

        self.albumlabel = Label(
            text=album,
            font_size=52,
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

        self.playlistlabel = Label(
            text=playlist,
            font_size=52,
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
            spacing=200,
            size_hint_y=None
        )
        content_wrapper.bind(minimum_height=content_wrapper.setter('height')) # type: ignore

        content_wrapper.add_widget(song_artist_label_wrapper)
        content_wrapper.add_widget(album_playlist_label_wrapper)

        inner_layout.add_widget(content_wrapper)

        outer_layout.add_widget(inner_layout)

        return outer_layout
    
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


if __name__ == "__main__":
    get_song()
    get_artwork()
    print(song_title, artist, album, playlist)
    MyApp().run()