import pandas as pd
from pytorch_forecasting import TemporalFusionTransformer

from .data import dataloader

def tft_pred():
    # load model
    best_model_path = 'lightning_logs/default/version_0/checkpoints/epoch=20.ckpt'
    best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)

    # Predict samples from validation dataset
    _, _, _, val_dataloader = dataloader()
    predictions = best_tft.predict(val_dataloader)

    data = {'month':[], 'item':[], 'value':[]}
    items = ['A', 'B', 'C', 'D', 'E']
    for month in range(6):
        for item_idx, item in enumerate(items):
            data['month'].append(month+1)
            data['item'].append(item)
            data['value'].append(predictions[item_idx][month].item())

    frame = pd.DataFrame(data)
    return frame