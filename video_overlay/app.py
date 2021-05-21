import streamlit as st
import subprocess
import tempfile
import time

import os
import base64

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href


def get_mapping_dict(od_x: int, od_y: int):
    overlay_mapping = {
        "top-right": f"main_w-(overlay_w+{od_x}):{od_y}",
        "top-left": f"{od_x}:{od_y}",
        "bottom-right": f"main_w-(overlay_w+{od_x}):main_h-(overlay_h+{od_y})",
        "bottom-left": f"{od_x}:main_h-(overlay_h+{od_y})",
    }
    return overlay_mapping

st.markdown("# Overlay one video over another")
st.markdown('A utility tool to create lectures using screen recording and a video of a person talking.')
st.markdown('Just choose a background and an overlay video and adjust parameters to place it where you like.')
st.markdown('Once the output is generated a download option will appear at the bottom.')

positions = ['top-right', 'top-left', 'bottom-right', 'bottom-left']

st.sidebar.title("Select options")
pos = st.sidebar.selectbox("Select position: ", positions)

h_label = "Horizontal distance of the overlayed video from left or right depending on placement"
v_label = "Vertical distance of the overlayed video from top or bottom depending on placement"

odist_x = st.sidebar.number_input(h_label, value = 50)
odist_y = st.sidebar.number_input(v_label, value = 50)

scale_x = st.sidebar.number_input("Width of overlayed video", value = 400)
scale_y = st.sidebar.number_input("height of overlayed video", value = -1)

back = st.file_uploader("Choose background video", type=["mp4", "mov"])
over = st.file_uploader("Choose overlay video", type=["mp4", "mov"])

if back is not None and over is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(back.read())
    tfile.write(over.read())

    time.sleep(10)
    os.system('ls video_overlay')

    bk = back.name
    ov = over.name

    op_vid = f"overlay_op.mp4"
    st.markdown(f'{bk} {ov}')
    overlay_dict = get_mapping_dict(odist_x, odist_y)
    cmd = f'ffmpeg -i {bk} -i {ov} -map 0:0 -map 1:1 -vf "movie={ov}, scale={scale_x}:{scale_y} [inner]; [in][inner] overlay={overlay_dict[pos]} [out]" {op_vid} -y'
    op = subprocess.check_output(cmd, shell=True)

    video_file = open(op_vid, 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)

    st.markdown(get_binary_file_downloader_html(f'{op_vid}', 'Video'), unsafe_allow_html=True)
