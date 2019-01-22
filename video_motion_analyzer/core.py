import os
import cv2
import numpy as np
from config import undetected_strange_frames_folder
from video_motion_analyzer.video_meta_getter import VideoObjectHandler
from video_data_stats_analyze.analyze_motion_series import DiscoverMotionData
from video_data_stats_analyze.core import VideoStatsDto


class VideoDispather:
    """
    core class for handling video
    """
    def __init__(self, file_path, play_video):
        self.file_path = file_path
        self.name = os.path.splitext(os.path.basename(file_path))[0]
        self.video_statistics = VideoStatsDto()
        self.video_object = VideoObjectHandler(file_path)

        if self.video_object.type != 0:
            self.time_treshold = 1
            if self.video_object.fps < 30:
                self.time_treshold = 1000
        else:
            self.time_treshold = 1000

        self.play_video = play_video
        self.base_frame = None
        self.zero = True
        self.frames_len = 0
        self.frames_with_motion = 0
        self.motion_areas = 0
        self.movement_status = "stay"
        # todo use for quantify motion
        self.critical_motion_value = 0.03
        self.movement_area_series = []

        self.temporary_movement_area_series = []
        self.temporary_motion_areas = 0

    @property
    def color_status_mapper(self):
        return {
            "stay": (0, 0, 255),
            "move": (255, 0, 0),
            "active_move": (0, 255, 0)
        }

    def diff_img(self, t0, t1, t2):
        """
        Finds differences between frames
        :param t0: 'basic' frame
        :param t1: prev frame
        :param t2: current frame
        :return:
        """
        # a = self.fgbg.apply(t0)
        d1 = cv2.absdiff(t2, t1)
        d2 = cv2.absdiff(t1, t0)
        d3 = cv2.absdiff(t0, t2)
        return cv2.bitwise_and(d1, d2, d3)

    def deeper_diff(self, t0, t1, t2):
        delta_plus = cv2.absdiff(t1, t0)
        delta_0 = cv2.absdiff(t2, t0)
        delta_minus = cv2.absdiff(t1, t2)
        dbp = cv2.adaptiveThreshold(delta_plus, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        dbm = cv2.adaptiveThreshold(delta_minus, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        db0 = cv2.adaptiveThreshold(delta_0, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        tmp = cv2.bitwise_and(dbp, dbm)

        return cv2.bitwise_and(tmp, cv2.bitwise_not(db0))

    def save_prev_moves_coords(self):
        pass

    def launch(self):
        raise NotImplementedError

    def debug_frame_saver(self, frame, thresh, frame_delta=None, gray=None):
        """
        uses for saving frames without movement detection
        :param gray:
        :param frame:
        :param thresh:
        :param frame_delta:
        :return: None
        """
        filename = os.path.join(undetected_strange_frames_folder, "frame-{}.png".format(self.frames_len))
        cv2.imwrite(filename, frame)

        filename_thresh = os.path.join(undetected_strange_frames_folder, "thresh-frame-{}.png".format(self.frames_len))
        cv2.imwrite(filename_thresh, thresh)

        if gray is not None:
            filename_gray = os.path.join(undetected_strange_frames_folder, "gray-frame-{}.png".format(self.frames_len))
            cv2.imwrite(filename_gray, gray)

        if frame_delta is not None:
            filename_frame_delta = os.path.join(undetected_strange_frames_folder,
                                                "frame_delta-frame-{}.png".format(self.frames_len))
            cv2.imwrite(filename_frame_delta, frame_delta)

    def calculate_segment_data(self, plot=False, final=False):
        """
        uses for calculating motion based on window size
        :return:
        """
        tmp = {}
        if not final:
            movement_series = np.array(self.temporary_movement_area_series)
        else:
            movement_series = np.array(self.movement_area_series)

        d = DiscoverMotionData(numpy_file_path=None, series=movement_series, name="")
        if plot:
            d.data_to_plot()
        additional_data = d.count_statistic_values()

        tmp["clip_segment_time"] = round(self.video_object.video_timestamp / self.time_treshold, 0)
        tmp["segment_frame"] = self.video_object.current_frame
        tmp["segment_motion"] = self.temporary_motion_areas

        if not final:
            for i, item in enumerate(additional_data["names"]):
                tmp[item] = additional_data["values"][i]

            self.video_statistics.values.append(tmp)
        else:
            print("final")

    def prepare_motion_values_to_analyze(self, plot=False):
        """
        some basic dispatcher.
        :return:None
        """
        self.launch()

        self.calculate_segment_data(plot, final=True)

        self.video_statistics.duration_total = round(self.video_object.video_timestamp / self.time_treshold, 0)
        self.video_statistics.frames_total = round(self.video_object.total_frames, 0)
        self.video_statistics.total = self.motion_areas

        self.video_object.data.release()
        cv2.destroyAllWindows()
        return self.video_statistics
