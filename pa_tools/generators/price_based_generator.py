import numpy as np
import pandas as pd
from .._generator import PositionGenerator


class PriceBasedPositionGenerator(PositionGenerator):

    def _get_raw_position(self, position_li_df, idx, time_size, position_size):
        _position_li_df = position_li_df.iloc[max(0, idx - time_size) : idx]
        _positions_arr = np.concatenate(_position_li_df.values)
        _positions = self._sample_positions(_positions_arr, position_size)
        return _positions

    def get_raw_position(self, prices, time_size, position_size):
        position_li_df = prices.apply(lambda x: [x]).rename("price")
        idx = len(position_li_df)
        _position = self._get_raw_position(position_li_df, idx, time_size, position_size)
        return _position

    def get_raw_position_df(self, prices, time_size, position_size):
        positions = list()
        position_li_df = prices.apply(lambda x: [x])
        for idx in range(1, len(position_li_df) + 1):
            _positions = self._get_raw_position(position_li_df, idx, time_size, position_size)
            positions.append([_positions])
        position_df = pd.DataFrame(positions, columns=["positions"], index=prices.index)
        return position_df

    def _get_raw_volume_position(self, pv_df, idx, time_size, position_size):
        _pv_df = pv_df.iloc[max(0, idx - time_size) : idx, :].copy()
        _pv_df["noramlized_volume"] = _pv_df["volume"].apply(
            lambda x: round((x * position_size) / _pv_df["volume"].sum())
        )
        _pv_df["position"] = _pv_df["price"].apply(lambda x: [x]) * _pv_df[
            "noramlized_volume"
        ].astype(int)
        _positions_arr = np.concatenate(_pv_df["position"].values)
        _positions = self._sample_positions(_positions_arr, position_size)
        return _positions

    def get_raw_volume_position(self, prices, volumes, time_size, position_size):
        pv_df = pd.concat([prices.rename("price"), volumes.rename("volume")], axis=1)
        idx = len(pv_df)
        _positions = self._get_raw_volume_position(pv_df, idx, time_size, position_size)
        return _positions

    def get_raw_volume_position_df(self, prices, volumes, time_size, position_size):
        positions = list()
        pv_df = pd.concat([prices.rename("price"), volumes.rename("volume")], axis=1)
        for idx in range(1, len(pv_df) + 1):
            _positions = self._get_raw_volume_position(pv_df, idx, time_size, position_size)
            positions.append([_positions])
        position_df = pd.DataFrame(positions, columns=["positions"], index=prices.index)
        return position_df

    def _get_time_dependent_position(self, position_li_df, idx, time_size, position_size):
        _position_li_df = position_li_df.iloc[max(0, idx - time_size) : idx, :].copy()
        _position_li_df["time"] = list(range(1, len(_position_li_df) + 1))
        _position_li_df["position"] = _position_li_df["price"] * _position_li_df["time"].astype(int)
        _positions_arr = np.concatenate(_position_li_df["position"].values)
        _positions = self._sample_positions(_positions_arr, position_size)
        return _positions

    def get_time_dependent_position(self, prices, time_size, position_size):
        position_li_df = prices.apply(lambda x: [x]).rename("price").to_frame()
        idx = len(position_li_df)
        _positions = self._get_time_dependent_position(
            position_li_df, idx, time_size, position_size
        )
        return _positions

    def get_time_dependent_position_df(self, prices, time_size, position_size):
        positions = list()
        position_li_df = prices.apply(lambda x: [x]).rename("price").to_frame()
        for idx in range(1, len(position_li_df) + 1):
            _positions = self._get_time_dependent_position(
                position_li_df, idx, time_size, position_size
            )
            positions.append([_positions])
        position_df = pd.DataFrame(positions, columns=["positions"], index=prices.index)
        return position_df

    def _get_time_dependent_volume_position(self, pv_df, idx, time_size, position_size):
        _pv_df = pv_df.iloc[max(0, idx - time_size) : idx, :].copy()
        _pv_df["time"] = list(range(1, len(_pv_df) + 1))
        _pv_df["normalized_volume"] = _pv_df["volume"] / _pv_df["volume"].sum()
        _pv_df["weight"] = _pv_df["time"] * _pv_df["normalized_volume"]
        _pv_df["normalized_weight"] = _pv_df["weight"].apply(
            lambda x: round((x * position_size) / _pv_df["weight"].sum())
        )
        _pv_df["position"] = _pv_df["price"].apply(lambda x: [x]) * _pv_df[
            "normalized_weight"
        ].astype(int)
        _positions_arr = np.concatenate(_pv_df["position"].values)
        _positions = self._sample_positions(_positions_arr, position_size)
        return _positions

    def get_time_dependent_volume_position(self, prices, volumes, time_size, position_size):
        pv_df = pd.concat([prices.rename("price"), volumes.rename("volume")], axis=1)
        idx = len(pv_df)
        _positions = self._get_time_dependent_volume_position(pv_df, idx, time_size, position_size)
        return _positions

    def get_time_dependent_volume_position_df(self, prices, volumes, time_size, position_size):
        positions = list()
        pv_df = pd.concat([prices.rename("price"), volumes.rename("volume")], axis=1)
        for idx in range(1, len(pv_df) + 1):
            _positions = self._get_time_dependent_volume_position(
                pv_df, idx, time_size, position_size
            )
            positions.append([_positions])
        position_df = pd.DataFrame(positions, columns=["positions"], index=prices.index)
        return position_df
