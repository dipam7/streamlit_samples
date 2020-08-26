# import streamlit as st
# from PIL import Image, ImageDraw
# import torchvision.transforms as T
# import torchvision
# import torch

# st.write("# Wheat detection")

# st.set_option('deprecation.showfileUploaderEncoding', False)
# uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "png"])
# if uploaded_file is not None:
#     img = Image.open(uploaded_file).convert("RGB")
#     imageLocation = st.empty()
#     imageLocation.image(img, use_column_width=True)

#     img = T.ToTensor()(img)
#     model = torch.load('../models/model.pth', map_location = 'cpu')
#     model.eval()
#     output = get_prediction(model, img)
#     boxes,scores = post_process(output, nms_thresh = nms)
#     img = plot_op(img, boxes, scores)
#     imageLocation.image(img, use_column_width=True)
















import streamlit as st
from PIL import Image, ImageDraw
import torchvision.transforms as T
import torchvision
import torch

device = 'cpu'

def get_prediction(model, img):
    img = [img.to(device)]
    outputs = model(img)
    return outputs[0]

@st.cache
def post_process(outputs, nms_thresh = 0.3):
    boxes = outputs['boxes'].data
    scores = outputs['scores'].data
    labels = outputs['labels'].data

    keep = torchvision.ops.nms(boxes, scores, nms_thresh)
    boxes = boxes[keep]
    scores = scores[keep]

    return boxes, scores

def plot_op(img, boxes, scores):
    im = (img.permute(1,2,0).detach().numpy() * 255).astype('uint8')
    vsample = Image.fromarray(im)
    draw = ImageDraw.Draw(vsample)
    for box in boxes:
        draw.rectangle(list(box), fill = None, outline = "red", width = 3)
    return vsample

st.write("# Wheat detection")
st.set_option('deprecation.showfileUploaderEncoding', False)
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "png"])
if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    imageLocation = st.empty()
    imageLocation.image(img, use_column_width=True)

    img = T.ToTensor()(img)
    model = torch.load('../models/model.pth', map_location = 'cpu')
    model.eval()
    output = get_prediction(model, img)

    nms = st.sidebar.slider('nms', 0.0, 1.0, 0.1)
    boxes,scores = post_process(output, nms_thresh = nms)

    img = plot_op(img, boxes, scores)
    imageLocation.image(img, use_column_width=True)