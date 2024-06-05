import io
import streamlit as st
from pytube import YouTube, Playlist

st.title("Descargador de Audio de YouTube")

option = st.radio("Selecciona una opción:", ("Video individual", "Lista de reproducción"))

if option == "Video individual":
    yt_url = st.text_input("Ingresa el enlace del video de YouTube:")

    def descargar_audio(url):
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        buffer = io.BytesIO()
        audio.stream_to_buffer(buffer)
        buffer.seek(0)  # Mover el puntero al inicio del búfer
        return buffer.getvalue(), yt.title + ".mp3"

    if yt_url:
        file_bytes, filename = descargar_audio(yt_url)
        st.download_button(
            label="Descargar Audio",
            data=file_bytes,
            file_name=filename,
            mime="audio/mpeg"
        )

elif option == "Lista de reproducción":
    playlist_url = st.text_input("Ingresa el enlace de la lista de reproducción de YouTube:")

    if playlist_url:
        playlist = Playlist(playlist_url)
        for video in playlist.videos:
            audio = video.streams.filter(only_audio=True).first()
            buffer = io.BytesIO()
            audio.stream_to_buffer(buffer)
            buffer.seek(0)  # Mover el puntero al inicio del búfer
            file_bytes = buffer.getvalue()
            filename = video.title + ".mp3"
            st.download_button(
                label=f"Descargar {filename}",
                data=file_bytes,
                file_name=filename,
                mime="audio/mpeg"
            )