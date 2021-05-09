import ast
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torchvision
import torchvision.transforms as T
from PIL import Image, ImageDraw

model_dir = Path('models')
img_dir = Path('images')
csv_dir = Path('csvs')

img_id = '006a994f7'
device = 'cpu'

def process_df(csv_path):
    df = pd.read_csv(csv_dir/csv_path)
    df['bbox'] = df['bbox'].apply(lambda x: ast.literal_eval(x))
    x = np.array(list(df['bbox']))

    for i,dim in enumerate(['x', 'y', 'w', 'h']):
        df[dim] = x[:,i]
    
    df.drop('bbox', axis = 1, inplace = True)
    return df

def process_image(img_id, df):
    im_name = str(img_dir/img_id) + '.jpg'
    img = Image.open(im_name).convert("RGB")
    img = T.ToTensor()(img)
    
    records = df[df['image_id'] == img_id]
        
    boxes = records[['x', 'y', 'w', 'h']].values
    boxes[:, 2] = boxes[:, 0] + boxes[:, 2]
    boxes[:, 3] = boxes[:, 1] + boxes[:, 3]
    boxes = torch.tensor(boxes, dtype=torch.int64)
    
    labels = torch.ones((records.shape[0],), dtype=torch.int64)
    
    
    target = {}
    target['boxes'] = boxes
    target['labels'] = labels
    
    return img, target

def get_prediction(img, nms_thresh = 0.3):
    img = [img.to(device)]
    outputs = model(img)

    boxes = outputs[0]['boxes'].data
    scores = outputs[0]['scores'].data
    labels = outputs[0]['labels'].data

    keep = torchvision.ops.nms(boxes, scores, nms_thresh)
    boxes = boxes[keep]
    scores = scores[keep]

    return boxes, scores

def plot_op(img, boxes, scores):
    im = (img.permute(1,2,0).detach().numpy() * 255).astype('uint8')
    vsample = Image.fromarray(im)

    draw = ImageDraw.Draw(vsample)
    for box in boxes:
        draw.rectangle(list(box), fill = None, outline = "red")
    return vsample

if __name__ == '__main__':
    df = process_df('train.csv')
    img, target = process_image(img_id, df)

    model = torch.load(model_dir/'model.pth', map_location=device)
    model.eval()
    boxes, scores = get_prediction(img)

    img = plot_op(img, boxes, scores)
    img.show()