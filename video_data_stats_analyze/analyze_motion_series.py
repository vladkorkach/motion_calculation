import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from config import frames_frequency, statistics_reports_folder


class DiscoverMotionData:
    """
    prototype of statistics counter class
    uses for analyze time series of move areas coefficients
    """
    def __init__(self, numpy_file_path, series, name="", save_data=False):
        if numpy_file_path is not None:
            self.movement_series = np.load(numpy_file_path)
        else:
            self.movement_series = series
        if len(self.movement_series) == 0:
            print("no data to analyze")
            exit()
        self.plot_name = name
        self.save_data = save_data
        self.statistics_values = ["median",
                                  "average_per_frame",
                                  "std",
                                  "variance"]
        self.ewma = self.pandas_ema(self.movement_series, frames_frequency)

    def data_to_plot(self):
        """
        Shows data on plot
        :param movement_series: list of areas timeseries
        :return: None
        """
        plt.plot(self.ewma)
        plt.ylabel('Frame areas of movement')

        if self.save_data:
            plt.savefig(os.path.join(statistics_reports_folder, "{}.png".format(self.plot_name)))

        plt.show()

    @staticmethod
    def pandas_ema(values, period):
        """
        uses for smoothing time series
        :param values: motion series from video
        :param period: period for EWMA smooth
        :return: series after EWMA applying
        """
        values = pd.Series(values)
        values = values.ewm(com=period).mean()

        return values

    def fill_values(self, movement_series):
        raw_data = {
            "names": self.statistics_values,
            "values": [round(np.median(movement_series), 6),
                       round(np.mean(movement_series), 6),
                       round(np.std(movement_series), 6),
                       round(np.var(movement_series), 6)]
        }

        return raw_data

    def count_statistic_values(self):
        """
        just try of simple statistics analysis movement areas as time series
        :param movement_series:
        :return: statistics info
        """
        # self.data_to_plot()
        raw_data = self.fill_values(self.movement_series)
        return raw_data
