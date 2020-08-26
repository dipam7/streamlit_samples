# streamlit_samples
Samples of streamlit apps that I've built

Python version 3.8.5

**Installation**

```
pip install streamlit
```

### [Object detection](https://github.com/dipam7/streamlit_samples/tree/master/obj_detection)

Directory tree:
```
obj_detection
      |______ predict.py   
      |______ images
      |______ csvs
      |______ streamlit_demo
                  |_______ app.py
```

To run object detection manually, run

```
python predict.py
```

Image should be in images and model should be under obj_detection/models/*.pth. Csvs are used for training.

To run streamlit go to streamlit demo and run

```
streamlit run app.py
```

![](https://github.com/dipam7/streamlit_samples/blob/master/obj_detection/streamlit_demo/screenshots/streamlit_demo.gif)
