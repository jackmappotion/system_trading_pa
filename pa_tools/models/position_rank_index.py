import numpy as np
from typing import Union

Numeric = Union[int, float]


class PositionRankIndexModel:
    """
    0 : price is biggest in position
    1 : price is lowest in position
    """

    def calc(self, price: Numeric, positions: list):
        uppers = self._calc_uppers(price, positions)
        lowers = self._calc_lowers(price, positions)
        pri = round((uppers) / (uppers + lowers), 2)
        return pri

    @staticmethod
    def _calc_uppers(price: Numeric, positions: list):
        uppers = (np.array(positions) > price).sum()
        return uppers

    @staticmethod
    def _calc_lowers(price: Numeric, positions: list):
        lowers = (np.array(positions) < price).sum()
        return lowers
