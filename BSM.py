import numpy as np
import pandas as pd
from scipy.stats import norm


class BSM:
    def __init__(self, spot: float, strike: float, maturity: int, interest_rate: float, volatility: float):
        self.spot = spot
        self.strike = strike
        self.maturity = maturity
        self.interest_rate = interest_rate
        self.volatility = volatility
        self._d1 = None
        self._d2 = None
        self.price = None
        self._compute_d1()

    @staticmethod
    def _compute_stochastic_integral(t: float, n: int):
        dt = t / n

        dw = np.random.randn(n) * np.sqrt(dt)
        w = np.cumsum(dw)
        return w

    def _compute_spot_price(self):
        s = self.spot * np.exp((self.interest_rate - self.volatility ** 2 / 2) + self.volatility * self._compute_stochastic_integral(self.maturity, 1000))
        return s

    def _compute_d1(self):
        self._d1 = (np.log(self.spot/self.strike) + self.maturity * (self.interest_rate + .5 * self.volatility**2)) / (self.volatility * np.sqrt(self.maturity))
        self._compute_d2()

    def _compute_d2(self):
        self._d2 = self._d1 - self.volatility * np.sqrt(self.maturity)

    def compute_option_price(self):
        call = self.spot * norm.cdf(self._d1) - self.strike * np.exp(-self.interest_rate * self.maturity) * norm.cdf(self._d2)
        put = self.strike * np.exp(-self.interest_rate * self.maturity) * norm.cdf(-self._d2) - self.spot * norm.cdf(-self._d1)
        return call, put

    def simulate_spot_price(self, N: int):
        """

        :param N:
        :return:
        """
        S = [self._compute_spot_price() for n in range(N)]
        return S
    