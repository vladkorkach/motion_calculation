import numpy as np
from datetime import timedelta

from config import window_size
import matplotlib.pyplot as plt
from cycler import cycler

from database_actions.query_builder import get_clips_and_motions
from video_data_stats_analyze.analyze_motion_series import DiscoverMotionData
from video_data_stats_analyze.core import VideoStatsDto


def show_final_motions_data(d, d1):
    """
    Just show plot with ewma data for comparing videos stats
    :param d: object - result of prepare_data_for_intervals() motions from first period
    :param d1: object - result of prepare_data_for_intervals() motions from second period
    :return: None
    """
    videos_averages = []
    videos_stds = []
    for v in d['values']:
        videos_averages.append(v["average_per_frame"])
        videos_stds.append(v["std"])
    # print("=======")
    videos_averages1 = []
    videos_stds1 = []
    for v in d1['values']:
        videos_averages1.append(v["average_per_frame"])
        videos_stds1.append(v["std"])

    f, ax = plt.subplots()
    ax.set_prop_cycle(cycler('color', ['red', 'orange', 'blue', "green"]))

    plt.plot(DiscoverMotionData.pandas_ema(np.array(videos_averages), window_size), 'o')
    plt.plot(DiscoverMotionData.pandas_ema(np.array(videos_stds), window_size), 'o')

    plt.plot(DiscoverMotionData.pandas_ema(np.array(videos_averages1), window_size), 'o')
    plt.plot(DiscoverMotionData.pandas_ema(np.array(videos_stds1), window_size), 'o')

    plt.legend(["first video averages", "first video stds", "second video averages", "second video stds"])
    plt.show()


def prepare_data_for_intervals(start_time, end_time, cam_id, name=""):
    """
    returns motions stats from selected period
    :param start_time: datetime
    :param end_time: datetime
    :param cam_id: integer
    :param name: string
    :return: dict
    """
    data = get_clips_and_motions(start_time, end_time, cam_id)
    if data is None:
        return False
    interval_wrapper = {"name": name, "total_duration": 0, "total": 0, "frames_total": 0, "end_time": end_time,
                        "values": [], "empty": 0}

    time_frame = 0
    if data.returns_rows and data.rowcount > 0:
        prev = None
        for k, d in enumerate(data):
            tmp = VideoStatsDto()
            tmp.unserialize(d["motion_values"])

            if tmp.start_time == "":
                continue

            e_time = tmp.start_time + timedelta(seconds=tmp.duration_total)

            if prev:
                interval_len = int((tmp.start_time - prev).total_seconds())
                if interval_len > 1:
                    skipped_intervals = round(interval_len / 59)
                    print(k)
                    print("no data for {} minutes".format(skipped_intervals))
                    print("=======")

                    for a in range(round(skipped_intervals * 60 / window_size)):
                        time_frame += window_size
                        interval_wrapper["values"].append({
                            "clip_segment_time": time_frame,
                            "average_per_frame": 0,
                            "std": 0,
                        })
                    interval_wrapper["empty"] += round(skipped_intervals * 60 / window_size)
                else:
                    interval_wrapper["total"] += tmp.total
                    interval_wrapper["total_duration"] += tmp.duration_total
                    interval_wrapper["frames_total"] += tmp.frames_total

                    for item in tmp.values:
                        time_frame += window_size
                        interval_wrapper["values"].append({
                            "clip_segment_time": time_frame,
                            "average_per_frame": item["average_per_frame"],
                            "std": item["std"]
                        })
            else:
                interval_wrapper["start_time"] = tmp.start_time
            prev = e_time

    return interval_wrapper
