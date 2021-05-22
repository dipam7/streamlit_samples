import base64
import codecs
import subprocess

import streamlit as st
import streamlit.components.v1 as components


# deprecated, not usable for larger files
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}">Download {file_label}</a>'
    return href


def download_button(html_file):
    calc_file = codecs.open(html_file, 'r')
    page = calc_file.read()
    components.html(html=page, height=50)


def get_mapping_dict(od_x: int, od_y: int):
    overlay_mapping = {
        "top-right": f"main_w-(overlay_w+{od_x}):{od_y}",
        "top-left": f"{od_x}:{od_y}",
        "bottom-right": f"main_w-(overlay_w+{od_x}):main_h-(overlay_h+{od_y})",
        "bottom-left": f"{od_x}:main_h-(overlay_h+{od_y})",
    }
    return overlay_mapping


st.markdown("""
    # Overlay one video over another
    A utility tool to create lectures using screen recording and a video of a person talking.<br>
    Just choose a background and an overlay video and adjust parameters to place it where you like.<br>
    Once the output is generated a download option will appear at the bottom.
    """,
    unsafe_allow_html=True)

positions = ['top-right', 'top-left', 'bottom-right', 'bottom-left']

st.sidebar.title("Select options")
pos = st.sidebar.selectbox("Select position: ", positions)

h_label = "Horizontal distance of the overlayed video from left or right depending on placement"
v_label = "Vertical distance of the overlayed video from top or bottom depending on placement"

odist_x = st.sidebar.number_input(h_label, value=50)
odist_y = st.sidebar.number_input(v_label, value=50)

scale_x = st.sidebar.number_input("Width of overlayed video", value=400)
scale_y = st.sidebar.number_input("height of overlayed video", value=-1)

back = st.file_uploader("Choose background video", type=["mp4", "mov"])
over = st.file_uploader("Choose overlay video", type=["mp4", "mov"])

if back is not None and over is not None:
    bk = back.name
    ov = over.name
    with open(bk, mode='wb') as f:
        f.write(back.read())
    with open(ov, mode='wb') as f:
        f.write(over.read())

    st.markdown(f"""
    ### Files
    - {bk}
    - {ov}
    """,
    unsafe_allow_html=True)

    op_vid = "overlay_op.mp4"
    overlay_dict = get_mapping_dict(odist_x, odist_y)

    if st.button('Run overlay merge process'):
        with st.spinner('Wait for ffmpeg to process...'):
            cmd = f'ffmpeg -i {bk} -i {ov} -map 0:0 -map 1:1 -vf "movie={ov}, scale={scale_x}:{scale_y} [inner]; [in][inner] overlay={overlay_dict[pos]} [out]" {op_vid} -y'
            op = subprocess.check_output(cmd, shell=True)

            st.video(op_vid)
            st.balloons()
            download_button('videodownload.html')
            # st.markdown(get_binary_file_downloader_html(op_vid, 'Video'), unsafe_allow_html=True)