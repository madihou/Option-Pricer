import logging
from typing import Any
import numpy as np
from numpy import ndarray, dtype
from scipy.stats import norm

logger = logging.getLogger("BSM")
logging.basicConfig(level=logging.INFO)


class BSM:

    def __init__(self):
        self.spot = None
        self.strike = None
        self.maturity = None
        self.risk_free = None
        self.volatility = None
        self._d1 = None
        self._d2 = None
        self.price = None
        self.period = None
        self._initialized = False

    def initialize_bsm(self, spot: float, strike: float, maturity: float, risk_free_rate: float, volatility: float) -> None:
        """
        Initialize the Black-Sholes-Merton (BSM) model to compute European call/put option pricing.
        Args:
            spot (float): Current spot price (in $).
            strike (float): Strike price (i.e. exercise price) of the option (in $).
            maturity (float): Time to option expiration (in years).
            risk_free_rate (float): Annualized risk-free interest rate (e.g., .05 for 5%).
            volatility (float): Implied volatility of the underlying asset (e.g., .20 for 20%).
        Returns:
            None: Updates the internal attributes of the model.
        """
        logger.info("---------------------------------------------------------------------")
        logger.info(" Initialization of Black-Sholes-Merton model to compute option prices")
        logger.info("---------------------------------------------------------------------")
        logger.info(" Parameters :")
        logger.info(f"\n"
                    f"| Spot price: ${spot:.2f} |\n"
                    f"| Strike: ${strike:.2f} |\n"
                    f"| Maturity: {maturity} year(s) |\n"
                    f"| Risk-free rate: {risk_free_rate:.2%} |\n"
                    f"| Volatility: {volatility / 100:.2%} |"
                    )
        self.spot = spot
        self.strike = strike
        self.maturity = maturity
        self.risk_free = risk_free_rate
        self.volatility = volatility
        self._d1 = self._compute_d(self.spot, self.strike, self.risk_free, self.maturity, self.volatility)
        self._d2 = self._compute_d(self.spot, self.strike, self.risk_free, self.maturity, self.volatility,
                                   is_d1=False)
        self._initialized = True

    @staticmethod
    def _compute_stochastic_integral(dt, n: int) -> ndarray[Any, dtype[Any]]:
        """
        Simulate a stochastic integral using the Euler-Maruyama numerical method.
        Args:
            dt : Time period for the simulation.
            n (int): Number of time steps in the discretization.

        Return:
            np.ndarray: A 1D array of simulated values representing the stochastic process.
        """

        dw = np.random.randn(n+1) * np.sqrt(dt)
        w = np.cumsum(dw)
        return w

    def compute_spot_price(self, timescale: str, n: int):
        """

        """
        scale = {"Daily": 1/252, "Weekly": 1/52, "Year": 1}
        self.period = np.arange(n+1) * scale[timescale]
        dt = np.concat(([0], np.diff(self.period)))
        if not self._initialized:
            logger.error("Model not initialized. Please initialize a model with the required parameters.")
        else:
            self.price = self.spot * np.exp(
                (self.risk_free - .5 * self.volatility ** 2) * self.period + self.volatility * self._compute_stochastic_integral(
                    dt, n))

    def compute_option_price(self) -> tuple[float, float]:
        """
        Compute the prices of European call/put options using the Black-Scholes-Merton model.

        Returns:
            tuple[float, float]: Tuple containing:
                - Call option price (float)
                - Put option price (float)
        """
        if not self._initialized:
            logger.error("Model not initialized. Please initialize a model with the required parameters.")
        else:
            call = self.spot * norm.cdf(self._d1) - self.strike * np.exp(
                -self.risk_free * self.maturity) * norm.cdf(self._d2)
            put = self.strike * np.exp(-self.risk_free * self.maturity) * norm.cdf(
                -self._d2) - self.spot * norm.cdf(-self._d1)
            logger.info("---------------------------------------------------------------------")
            logger.info(" Result :")
            logger.info(
                f"| Call price: ${call:.2f} \n"
                f"| Put price: ${put:.2f} \n"
            )
            return call, put

    def simulate_spot_price(self, N: int):
        """

        :param N:
        :return:
        """
        S = [self._compute_spot_price() for n in range(N)]
        return S

    @staticmethod
    def _compute_d(s0: float | np.ndarray, K: float, r: float, T: float | np.ndarray, sigma: float, is_d1=True) -> float:
        """

        """
        d1 = (np.log(s0 / K) + (r + .5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        if is_d1:
            return d1
        else:
            return d1 - sigma * np.sqrt(T)

    def compute_bsm(self, s0: float, K: float, r: float, T: float, sigma: float, is_call=True) -> float:
        """

        """
        d1 = self._compute_d(s0, K, r, T, sigma)
        d2 = self._compute_d(s0, K, r, T, sigma, False)
        if is_call:
            return s0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            return K * np.exp(-r * T) * norm.cdf(-d2) - s0 * norm.cdf(-d1)

    def compute_greeks(self):
        pass

    def compute_delta(self, s0: float | np.ndarray, K: float, r: float, T: float | np.ndarray, sigma: float, is_call=True):
        d1 = self._compute_d(s0, K, self.maturity - T, r, sigma)
        if is_call:
            return norm.cdf(d1)
        else:
            return norm.cdf(d1) - 1

    def compute_gamma(self):
        pass

    def compute_theta(self):
        pass

    def compute_vega(self):
        pass

    def compute_rho(self):
        pass
