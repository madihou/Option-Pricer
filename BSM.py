import logging
import numpy as np
import pandas as pd
from scipy.stats import norm


class BSM:

    def __init__(self):
        self.spot = None
        self.strike = None
        self.maturity = None
        self.interest_rate = None
        self.volatility = None
        self._d1 = None
        self._d2 = None

    def initialize_bsm(self, spot: float, strike: float, maturity: int, interest_rate: float, volatility: float):
        """

        """
        self.spot = spot
        self.strike = strike
        self.maturity = maturity
        self.interest_rate = interest_rate
        self.volatility = volatility
        self._d1 = self._compute_d(self.spot, self.strike, self.interest_rate, self.maturity, self.volatility)
        self._d2 = self._compute_d(self.spot, self.strike, self.interest_rate, self.maturity, self.volatility, is_d1=False)


    @staticmethod
    def _compute_stochastic_integral(t: float, n: int):
        """

        """
        dt = t / n

        dw = np.random.randn(n) * np.sqrt(dt)
        w = np.cumsum(dw)
        return w

    def _compute_spot_price(self):
        """

        """
        s = self.spot * np.exp((self.interest_rate - self.volatility ** 2 / 2) + self.volatility * self._compute_stochastic_integral(self.maturity, 1000))
        return s

    def compute_option_price(self):
        """

        """
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

    @staticmethod
    def _compute_d(s0: float, K: float, r: float, T: int, sigma: float, is_d1=True):
        """

        """
        d1 = (np.log(s0 / K) + (r + .5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        if is_d1:
            return d1
        else:
            return d1 - sigma * np.sqrt(T)

    def compute_bsm(self, s0: float, K: float, r: float, T: int, sigma: float, is_call=True):
        """

        """
        d1 = self._compute_d(s0, K, r, T, sigma)
        d2 = self._compute_d(s0, K, r, T, sigma, False)
        if is_call:
            return s0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            return K * np.exp(-r * T) * norm.cdf(-d2) - s0 * norm.cdf(-d1)