import torch
from pytorch_forecasting import TemporalFusionTransformer
from pytorch_forecasting.metrics import SMAPE

from config import get_params
from data import dataloader

def eval_tft(args):
    best_tft = TemporalFusionTransformer.load_from_checkpoint(args.best_model_path)
    _, _, _, val_dataloader = dataloader()
    # calcualte mean absolute error on validation set
    actuals = torch.cat([y for x, y in iter(val_dataloader)])
    predictions = best_tft.predict(val_dataloader)
    print('MAE:', (actuals - predictions).abs().mean())

    # Looking at sample predictions directly
    raw_predictions, x = best_tft.predict(val_dataloader, mode="raw", return_x=True)
    for idx in range(5):  # plot 10 examples
        best_tft.plot_prediction(x, raw_predictions, idx=idx, add_loss_to_title=True).savefig('forecaster/plots/eval'+str(idx)+'.png')

    # Looking at the worst performers in terms of sMAPE
    predictions = best_tft.predict(val_dataloader)
    mean_losses = SMAPE(reduction="none")(predictions, actuals).mean(1)
    indices = mean_losses.argsort(descending=True)  # sort losses
    for idx in range(5):  # plot 10 examples
        best_tft.plot_prediction(x, raw_predictions, idx=indices[idx], add_loss_to_title=SMAPE()).savefig('forecaster/plots/worst'+str(idx)+'.png')


if __name__ == "__main__":
    args = get_params()
    eval_tft(args)