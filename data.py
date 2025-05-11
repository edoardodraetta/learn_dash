"""Data loading and processing"""
import pandas as pd


def load_data():
    """Load default data"""
    return pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')