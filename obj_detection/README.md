# Object detection

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
