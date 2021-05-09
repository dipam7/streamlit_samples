# Object detection

In this demo, we see how changing nms affects the number of bboxes in the output of object detection. 

Learn more about [object detection](https://towardsdatascience.com/everything-about-fasterrcnn-6d758f5a6d79)

Learn more about [Streamlit](https://towardsdatascience.com/streamlit-use-data-apps-to-better-test-your-model-4a14dad235f5).

Directory tree:
```
obj_detection
      |______ predict.py   
      |______ images
      |______ csvs
      |______ streamlit_demo
                  |_______ app.py
```

The model was trained on [this dataset](https://www.kaggle.com/c/global-wheat-detection/data) and can be found [here](https://drive.google.com/drive/folders/10cq5c5HvRdab_qdEefW1Q2wC9RsOkXlG?usp=sharing). To try the demo yourself, download the model and move it under obj_detection/models/*.pth

Images should be under images. Csvs are used for training.

To run streamlit go to streamlit demo and run

```python
cd streamlit_demo
streamlit run app.py
```

Requirements:
```
torch == 1.5.0
torchvision == 0.6.0
```
