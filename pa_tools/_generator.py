from random import choices
from abc import ABC, abstractmethod
import numpy as np


class PositionGenerator(ABC):
    @abstractmethod
    def get_raw_position():
        pass

    @abstractmethod
    def get_raw_volume_position():
        pass

    @abstractmethod
    def get_time_dependent_position():
        pass

    @abstractmethod
    def get_time_dependent_volume_position():
        pass

    @staticmethod
    def _calc_time_weight_arr(series):
        time_weight_arr = np.arange(1, len(series) + 1)
        return time_weight_arr

    @staticmethod
    def _sample_positions(raw_positions, position_size):
        positions = choices(raw_positions, k=position_size)
        return positions
