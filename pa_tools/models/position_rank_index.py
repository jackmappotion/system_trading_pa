import numpy as np


class PositionRankIndexModel:
    def calc(self, price, positions):
        uppers = self._calc_uppers(price, positions)
        lowers = self._calc_lowers(price, positions)
        pri = round((uppers) / (uppers + lowers), 2)
        return pri

    @staticmethod
    def _calc_uppers(price, positions):
        uppers = (np.array(positions) > price).sum()
        return uppers

    @staticmethod
    def _calc_lowers(price, positions):
        lowers = (np.array(positions) < price).sum()
        return lowers