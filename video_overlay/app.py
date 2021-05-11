import streamlit as st
import subprocess

def get_mapping_dict(od_x: int, od_y: int):
    overlay_mapping = {
        "top-right": f"main_w-(overlay_w+{od_x}):{od_y}",
        "top-left": f"{od_x}:{od_y}",
        "bottom-right": f"main_w-(overlay_w+{od_x}):main_h-(overlay_h+{od_y})",
        "bottom-left": f"{od_x}:main_h-(overlay_h+{od_y})",
    }
    return overlay_mapping

positions = ['top-left', 'top-right', 'bottom-left', 'bottom-right']

st.sidebar.title("Select options")
pos = st.sidebar.selectbox("Select position: ", positions)

h_label = "Horizontal distance of the overlayed video from left or right depending on placement"
v_label = "Vertical distance of the overlayed video from top or bottom depending on placement"

odist_x = st.sidebar.number_input(h_label, value = 10)
odist_y = st.sidebar.number_input(v_label, value = 10)

scale_x = st.sidebar.number_input("Width of overlayed video", value = 400)
scale_y = st.sidebar.number_input("height of overlayed video", value = -1)

back = st.file_uploader("Choose background video", type=["mp4", "mov"])
over = st.file_uploader("Choose overlay video", type=["mp4", "mov"])

if back is not None and over is not None:
    bk = back.name
    ov = over.name
    op_vid = f"overlay_op.mp4"
    
    overlay_dict = get_mapping_dict(odist_x, odist_y)
    cmd = f'ffmpeg -i {bk} -i {ov} -map 0:0 -map 1:1 -vf "movie={ov}, scale={scale_x}:{scale_y} [inner]; [in][inner] overlay={overlay_dict[pos]} [out]" {op_vid} -y'
    op = subprocess.check_output(cmd, shell=True)
    video_file = open(op_vid, 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)