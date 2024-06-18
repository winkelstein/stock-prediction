from tinkoff.invest import CandleInterval, Client, MoneyValue
from tinkoff.invest.utils import now, quotation_to_decimal
from datetime import timedelta

from typing import List, Dict

import sys
import csv
import os

TOKEN = os.environ["TINKOFF_API_KEY"]


def parse_args(argv: List[str]) -> Dict[str, str]:
    result = {"figi": "BBG004730N88"}
    must_be_figi = False
    for arg in argv:
        if must_be_figi:
            result["figi"] = arg
            must_be_figi = False
        if arg == "--figi":
            must_be_figi = True

    return result


class Candle:
    def __init__(self, high, low, open_, close, volume, time):
        self.high = high
        self.low = low
        self.open_ = open_
        self.close = close
        self.volume = volume
        self.time = time

    def __str__(self) -> str:
        return f"high: {self.high}, low: {self.low}, open: {self.open_}, close: {self.close}, volume: {self.volume}, time: {self.time}"


def print_to_csv(file: str, candles: List[Candle]):
    with open(file, 'w', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=[
                                'Date', 'High', 'Low', 'Open', 'Close', 'Volume'])
        writer.writeheader()

        for candle in candles:
            writer.writerow({"Date": candle.time, "High": candle.high, "Low": candle.low,
                             "Open": candle.open_, "Close": candle.close, "Volume": candle.volume})


def main(argv: List[str]):
    conf = parse_args(argv)

    with Client(TOKEN) as client:
        candles = []
        for candle in client.get_all_candles(
            instrument_id=conf["figi"],
            from_=now() - timedelta(days=365),
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        ):
            high = quotation_to_decimal(candle.high)
            low = quotation_to_decimal(candle.low)
            open_ = quotation_to_decimal(candle.open)
            close = quotation_to_decimal(candle.close)

            candle = Candle(high, low, open_,
                            close, candle.volume, candle.time.timestamp())
            candles.append(candle)

        print_to_csv(conf["figi"] + ".csv", candles)


if __name__ == "__main__":
    main(sys.argv)
