import streamlit as st
import requests

st.set_page_config(page_title="AI Video Generator", layout="centered")
st.title("🎬 Генератор видео через Runway ML")
st.markdown("**Сцены, стиль, масштаб — всё в твоих руках.**")

prompt = st.text_area("Описание сцены (Prompt):", "Inflatable Sherman tank in a foggy WW2 forest", height=150)
api_key = st.text_input("Runway API-ключ:", type="password")

st.subheader("Настройки генерации:")
num_frames = st.slider("Количество кадров:", min_value=8, max_value=64, value=24, step=8)
width = st.selectbox("Ширина (px):", [512, 576, 640, 768])
height = st.selectbox("Высота (px):", [512, 768, 1024])

if st.button("🚀 Сгенерировать видео") and prompt and api_key:
    st.info("Отправляю запрос к Runway ML...")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "stable-video-diffusion",
        "input": {
            "prompt": prompt,
            "num_frames": num_frames,
            "width": width,
            "height": height
        }
    }

    try:
        response = requests.post("https://api.runwayml.com/v1/generate", headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            video_url = result.get("video", "Не получено видео")
            st.success("Видео успешно сгенерировано!")
            st.video(video_url)
            st.markdown(f"[Скачать видео]({video_url})")
        else:
            st.error(f"Ошибка: {response.status_code} — {response.text}")
    except Exception as e:
        st.error(f"Сбой при генерации: {str(e)}")
