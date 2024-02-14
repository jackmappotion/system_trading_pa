import numpy as np
import pandas as pd
from .._generator import PositionGenerator


class PriceBasedPositionGenerator(PositionGenerator):

    def get_raw_position(self, prices, time_size, position_size):
        positions = list()
        prices_li_arr = prices.apply(lambda x: [x]).values
        for idx in range(1, len(prices_li_arr) + 1):
            _prices_li_arr = prices_li_arr[max(0, idx - time_size) : idx]
            _raw_positions_arr = np.concatenate(_prices_li_arr)
            _positions = self._sample_positions(_raw_positions_arr, position_size)
            positions.append([_positions])
        position_df = pd.DataFrame(positions, columns=["positions"], index=prices.index)
        return position_df

    def get_raw_volume_position(self, prices, volumes, time_size, position_size):
        positions = list()
        prices_li_arr = prices.apply(lambda x: [x]).values
        volumes_arr = volumes.values
        for idx in range(1, len(prices_li_arr) + 1):
            _prices_li_arr = prices_li_arr[max(0, idx - time_size) : idx]

            _volume_arr = volumes_arr[max(0, idx - time_size) : idx]
            _normalized_volumes = (_volume_arr * position_size) / _volume_arr.sum()

            _raw_positions_arr = np.concatenate(
                _prices_li_arr * np.round(_normalized_volumes).astype(int)
            )
            _positions = self._sample_positions(_raw_positions_arr, position_size)
            positions.append([_positions])
        position_df = pd.DataFrame(positions, columns=["positions"], index=prices.index)
        return position_df

    def get_time_dependent_position(self, prices, time_size, position_size):
        positions = list()
        prices_li_arr = prices.apply(lambda x: [x]).values
        for idx in range(1, len(prices_li_arr) + 1):
            _prices_li_arr = prices_li_arr[max(0, idx - time_size) : idx]

            _time_arr = np.arange(1, len(_prices_li_arr) + 1)

            _raw_positions_arr = np.concatenate(_prices_li_arr * np.round(_time_arr).astype(int))
            _positions = self._sample_positions(_raw_positions_arr, position_size)
            positions.append([_positions])
        position_df = pd.DataFrame(positions, columns=["positions"], index=prices.index)
        return position_df

    def get_time_dependent_volume_position(self, prices, volumes, time_size, position_size):
        positions = list()
        prices_li_arr = prices.apply(lambda x: [x]).values
        volumes_arr = volumes.values
        for idx in range(1, len(prices_li_arr) + 1):
            _prices_li_arr = prices_li_arr[max(0, idx - time_size) : idx]

            _time_arr = np.arange(1, len(_prices_li_arr) + 1)

            _volume_arr = volumes_arr[max(0, idx - time_size) : idx]
            _normalized_volumes = (_volume_arr * position_size) / _volume_arr.sum()

            _weight_arr = _time_arr * _normalized_volumes

            _raw_positions_arr = np.concatenate(_prices_li_arr * np.round(_weight_arr).astype(int))

            _positions = self._sample_positions(_raw_positions_arr, position_size)
            positions.append([_positions])
        position_df = pd.DataFrame(positions, columns=["positions"], index=prices.index)
        return position_df
