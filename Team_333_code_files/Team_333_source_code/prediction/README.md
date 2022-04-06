## CPU Utilisation Prediction using LSTM

### File Structure
- CPU Utilisation.csv : Dataset used for training
- model : model file trained in PyTorch
- prediction.py : Python file to get data from prometheus and transfer predictions to Google Sheets
- secrets.json : Credentials to upload to Google Sheets
- Train Model.ipynb: Code used to train the DL Model

### How to Run
```python3 prediction.py```

