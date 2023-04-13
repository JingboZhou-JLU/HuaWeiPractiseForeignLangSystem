from pyAudioAnalysis import ShortTermFeatures as aSTF
from pyAudioAnalysis import MidTermFeatures as aMTF
from pyAudioAnalysis import audioBasicIO as aIO
import numpy as np
import os


class Audio:
    def __init__(self, path=None):
        self.path = path
        self.fs = None
        self.s = None
        self.short_term_feature = None
        self.mid_term_feature = None

    def set_path(self, path):
        """
        Set path for an audio file.
        :param path: path of an audio file
        :return: None
        """
        self.path = path

    def load_audio(self):
        """
        Load audio data from file, demanding format as ".wav".
        :return: sampling freq and signal as a numpy array
        """
        if self.path is None:
            raise ValueError("Audio path have not been set.")
        if not os.path.exists(self.path):
            raise FileNotFoundError
        if not self.path.endswith('.wav'):
            raise ValueError("Audio file needs a \".wav\" file.")
        self.fs, self.s = aIO.read_audio_file(self.path)
        return self.fs, self.s

    def get_duration(self):
        """
        Get duration of an audio data.
        :return: duration of an audio
        """
        return len(self.s) / float(self.fs)

    def short_term_feature_extraction(self, win=0.050, step=0.050):
        """
        Extract short-term features using non-overlapping windows.
        :param win: window length
        :param step: step length
        :return: short-term feature of an audio
        """
        self.short_term_feature = aSTF.feature_extraction(self.s, self.fs,
                                                          int(self.fs * win),
                                                          int(self.fs * step))
        return self.short_term_feature

    def mid_term_feature_extraction(self):
        """
        Extract middle-term features using non-overlapping windows.
        :return: middle-term feature of an audio
        """
        self.mid_term_feature = aMTF.mid_feature_extraction(self.s, self.fs,
                                                            1 * self.fs, 1 * self.fs,
                                                            0.05 * self.fs, 0.05 * self.fs)
        return self.mid_term_feature

    def feature_extraction(self, win=0.050, step=0.050):
        """
        Extract both short-term and middle-term features using non-overlapping windows.
        :param win: window length
        :param step: step length
        :return: short-term features and middle-term features
        """
        short_term_feature = self.short_term_feature(win, step)
        mid_term_feature = self.mid_term_feature()
        return short_term_feature, mid_term_feature


def similarity_ravel(a: Audio, b: Audio):
    """
    Calculate similarity between two audios with raveling feature matrix.
    :param a: one audio
    :param b: the other audio
    :return: similarity
    """
    a_feature, _ = a.short_term_feature_extraction()
    b_feature, _ = b.short_term_feature_extraction()
    d1 = np.array(a_feature).ravel()
    d2 = np.array(b_feature).ravel()
    return np.sum(d1 * d2) / (np.linalg.norm(d1) * np.linalg.norm(d2))


def similarity_mean(a: Audio, b: Audio):
    """
    Calculate similarity between two audios.
    Calculate the similarity of each feature,
    then treat the final similarity as the mean of these values above.
    :param a: one audio
    :param b: the other audio
    :return: similarity
    """
    a_feature, _ = a.short_term_feature_extraction()
    b_feature, _ = b.short_term_feature_extraction()
    m, _ = a_feature.shape()
    cos_sims = []
    for i in range(m):
        a_row_i = a_feature[i]
        b_row_i = b_feature[i]
        sim_row_i = np.sum(a_row_i * b_row_i) / (np.linalg.norm(a_row_i)
                                                 * np.linalg.norm(b_row_i))
        cos_sims.append(sim_row_i)
    return np.mean(cos_sims)
