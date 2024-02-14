import numpy as np
import pandas as pd
from .._generator import PositionGenerator


class HighLowBasedPositionGenerator(PositionGenerator):
    """
    High / Low based Position Generator
    position : normal_distribution(
        mean : (high + low) / 2
        var  : (high - low) / 6
    )
    """
    def get_raw_position(self, highs, lows, time_size, position_size):
        positions = list()
        highs_lows = pd.concat([highs.rename("high"), lows.rename("low")], axis=1)
        prices_li_arr = highs_lows.apply(
            lambda x: self._get_high_low_samples(x["high"], x["low"], 1), axis=1
        ).values
        for idx in range(1, len(prices_li_arr) + 1):
            _prices_li_arr = prices_li_arr[max(0, idx - time_size) : idx]
            _raw_positions_arr = np.concatenate(_prices_li_arr)
            _positions = self._sample_positions(_raw_positions_arr, position_size)
            positions.append([_positions])
        position_df = pd.DataFrame(positions, columns=["positions"], index=highs.index)
        return position_df

    def get_raw_volume_position(self, highs, lows, volumes, time_size, position_size):
        positions = list()
        highs_lows = pd.concat([highs.rename("high"), lows.rename("low")], axis=1)
        volumes_arr = volumes.values
        for idx in range(1, len(highs_lows) + 1):
            _high_lows = highs_lows.iloc[max(0, idx - time_size) : idx, :]
            _volume_arr = volumes_arr[max(0, idx - time_size) : idx]
            _normalized_volumes = (_volume_arr * position_size) / _volume_arr.sum()
            _high_lows.loc[:, ["volume"]] = np.round(_normalized_volumes).astype(int)

            _raw_positions = _high_lows.apply(
                lambda x: self._get_high_low_samples(x["high"], x["low"], x["volume"]), axis=1
            )
            _raw_positions_arr = np.concatenate(_raw_positions.values)
            _positions = self._sample_positions(_raw_positions_arr, position_size)
            positions.append([_positions])
        position_df = pd.DataFrame(positions, columns=["positions"], index=highs.index)
        return position_df

    def get_time_dependent_position(self, highs, lows, time_size, position_size):
        positions = list()
        highs_lows = pd.concat([highs.rename("high"), lows.rename("low")], axis=1)
        for idx in range(1, len(highs_lows) + 1):
            _high_lows = highs_lows.iloc[max(0, idx - time_size) : idx, :]
            _time_arr = np.arange(1, len(_high_lows) + 1)

            _high_lows.loc[:, ["time"]] = np.round(_time_arr).astype(int)
            _raw_positions = _high_lows.apply(
                lambda x: self._get_high_low_samples(x["high"], x["low"], x["time"]), axis=1
            )
            _raw_positions_arr = np.concatenate(_raw_positions.values)
            _positions = self._sample_positions(_raw_positions_arr, position_size)
            positions.append([_positions])
        position_df = pd.DataFrame(positions, columns=["positions"], index=highs.index)
        return position_df

    def get_time_dependent_volume_position(self, highs, lows, volumes, time_size, position_size):
        positions = list()
        highs_lows = pd.concat([highs.rename("high"), lows.rename("low")], axis=1)
        volumes_arr = volumes.values
        for idx in range(1, len(highs_lows) + 1):
            _high_lows = highs_lows.iloc[max(0, idx - time_size) : idx, :]

            _volume_arr = volumes_arr[max(0, idx - time_size) : idx]
            _normalized_volumes_arr = ((_volume_arr * position_size) / _volume_arr.sum())

            _time_arr = np.arange(1, len(_high_lows) + 1)

            _weights = _normalized_volumes_arr * _time_arr
            _high_lows.loc[:,["weight"]] = np.round(_weights).astype(int)

            _raw_positions = _high_lows.apply(
                lambda x: self._get_high_low_samples(x["high"], x["low"], x["weight"]), axis=1
            )
            _raw_positions_arr = np.concatenate(_raw_positions.values)
            _positions = self._sample_positions(_raw_positions_arr, position_size)
            positions.append([_positions])
        position_df = pd.DataFrame(positions, columns=["positions"], index=highs.index)
        return position_df

    @staticmethod
    def _get_high_low_samples(high, low, n):
        mean = (high + low) / 2
        var = (high - low) / 6
        samples = np.random.normal(loc=mean, scale=var, size=n).tolist()
        return samples
