# stock-prediction

## Installation

```bash
pip install -r requirements.txt
```

## dataloader.py

dataloader.py is a script that can download 1-hour interval stock prices for one year.
You need to specify `TINKOFF_API_KEY` from Tinkoff broker API to use that script. Use script like this:

```
python dataloder.py --figi BBG004730N88
```

Here you can convert ticker to FIGI: https://usdrur.ru/ti/get-figi

## LSTM

LSTM neural network using Pytorch.
