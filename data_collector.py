import pymysql
pymysql.install_as_MySQLdb()

import yfinance as yf
import pandas as pd
import numpy as np
from scipy import stats
import os
from fredapi import Fred

class YahooFinanceDataCollector:
    """Classe pour récupérer et traiter les données financières de Yahoo Finance."""

    def __init__(self, tickers, start_date, end_date, output_dir="financial_data"):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def download_data(self):
        """Télécharge les données depuis Yahoo Finance."""
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date)
        return data['Adj Close'] if 'Adj Close' in data.columns else data['Close']

    def handle_missing_values(self, df):
        """Remplit les valeurs manquantes en utilisant forward-fill uniquement."""
        return df.ffill().bfill()

    def remove_outliers(self, df):
        """Supprime les valeurs aberrantes avec le Z-score."""
        z_scores = np.abs(stats.zscore(df, nan_policy='omit'))
        df[z_scores > 3] = np.nan
        return self.handle_missing_values(df)

    def save_to_csv(self, df, filename="data_fonds.csv"):
        """Sauvegarde les données au format CSV."""
        filepath = os.path.join(self.output_dir, filename)
        df.to_csv(filepath)
        print(f"Données sauvegardées dans {filepath}")

    def run(self):
        """Exécute toutes les étapes du pipeline."""
        print("Téléchargement des données Yahoo Finance...")
        data = self.download_data()

        print("Traitement des valeurs manquantes...")
        data = self.handle_missing_values(data)

        print("Suppression des valeurs aberrantes...")
        data = self.remove_outliers(data)

        self.save_to_csv(data)

        return data


class FredDataCollector:
    """Classe pour récupérer les données macroéconomiques depuis FRED."""

    def __init__(self, api_key, start_date="2000-01-01", end_date="2024-12-31", output_dir="macro_data"):
        self.api_key = api_key
        self.start_date = start_date
        self.end_date = end_date
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.fred = Fred(api_key=self.api_key)

        self.fred_tickers = [
            'GDP', 'BSCICP03USM665S', 'WUIGLOBALWEIGHTAVG',
            'ECBDFR', 'IRLTLT01USM156N', 'IRLTLT01DEM156N','IRLTLT01EZM156N', 
            'IR3TIB01USM156N', 'CLVMEURSCAB1GQEA19', 'CPALTT01USM657N', 'CPALTT01FRM657N',
        ]

    def download_data(self):
        """Télécharge les données macroéconomiques depuis FRED."""
        data_frames = {}
        for ticker in self.fred_tickers:
            data = self.fred.get_series(ticker, self.start_date, self.end_date)
            data_frames[ticker] = data
        return pd.DataFrame(data_frames)

    def handle_missing_values(self, df):
        """Remplit les valeurs manquantes en utilisant forward-fill uniquement."""
        print("Avant traitement : ", df.isna().sum().sum(), "valeurs manquantes")
        df = df.ffill().bfill()
        print("Après traitement : ", df.isna().sum().sum(), "valeurs manquantes restantes")
        return df

    def remove_outliers(self, df):
        """Supprime les valeurs aberrantes avec le Z-score."""
        print("Avant suppression des outliers :", df.isna().sum().sum(), "valeurs manquantes")
        z_scores = np.abs(stats.zscore(df, nan_policy='omit'))
        df[z_scores > 3] = np.nan
        print("Après suppression des outliers :", df.isna().sum().sum(), "valeurs manquantes")
        return self.handle_missing_values(df)
    
    def save_to_csv(self, df, filename="data_macro.csv"):
        """Sauvegarde les données au format CSV."""
        filepath = os.path.join(self.output_dir, filename)
        df.to_csv(filepath)
        print(f"Données macroéconomiques sauvegardées dans {filepath}")

    def run(self):
        """Exécute toutes les étapes de récupération et sauvegarde des données."""
        print("Téléchargement des données FRED...")
        data = self.download_data()

        print("Vérification des données FRED :")
        print(data.head())  # Vérifie le contenu

        print("Traitement des valeurs manquantes...")
        data = self.handle_missing_values(data.copy())  # Copier le DataFrame

        print("Suppression des valeurs aberrantes...")
        data = self.remove_outliers(data.copy())  # Copier le DataFrame

        self.save_to_csv(data)
        return data
