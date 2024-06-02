import sqlite3
import telebot
from telebot import types
import webbrowser
import ccxt
import pandas as pd
import numpy as np
import ta
import time
import logging
from scalping_infrasct import get_graph_about_coin_to_user


# Настройки скальпинга
api_key = "9xOQgHJV6SMhLkK2TN"
api_secret = "BbbCsx1piBH27J1sShdCnfhXYFJjG6nnFZoE"
timeframe = "1s"  # Интервал в 1 минуту
risk_per_trade = 0.01  # 1% от баланса
profit_target = 0.002  # 0.2%
stop_loss = 0.001  # 0.1%

# Подключение к Bybit
exchange = ccxt.bybit(
    {"apiKey": api_key, "secret": api_secret, "enableRateLimit": True}
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Функция получения данных о ценах
def fetch_data(symbol, timeframe, limit=100):
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(
        bars, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


# Применение технических индикаторов
def apply_technical_indicators(df):
    df["rsi"] = ta.momentum.rsi(df["close"], window=14)
    df["sma_50"] = ta.trend.sma_indicator(df["close"], window=50)
    df["sma_200"] = ta.trend.sma_indicator(df["close"], window=200)
    return df


# Стратегия скальпинга
def scalping_strategy(df):
    buy_signal = (df["rsi"].iloc[-1] < 30) and (
        df["sma_50"].iloc[-1] > df["sma_200"].iloc[-1]
    )
    sell_signal = (df["rsi"].iloc[-1] > 70) and (
        df["sma_50"].iloc[-1] < df["sma_200"].iloc[-1]
    )
    return buy_signal, sell_signal


# Основной цикл скальпинга для получения рекомендаций
def start_scalping(symbol):
    while True:
        try:
            df = fetch_data(symbol, timeframe)
            df = apply_technical_indicators(df)
            buy_signal, sell_signal = scalping_strategy(df)

            if buy_signal:
                logger.info(f"Buy signal for {symbol}")
                return f"Buy signal for {symbol} at {df['close'].iloc[-1]}"
            elif sell_signal:
                logger.info(f"Sell signal for {symbol}")
                return f"Sell signal for {symbol} at {df['close'].iloc[-1]}"

            time.sleep(60)  # Ожидание следующей минуты
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(60)
