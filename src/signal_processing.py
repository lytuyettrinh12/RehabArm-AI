import numpy as np
from scipy.signal import butter, filtfilt

class SignalProcessor:
    """
    Digital Signal Processing (DSP) pipeline for sEMG filtering & feature extraction.
    """
    def __init__(self, sample_rate=100, lowcut=20.0, highcut=45.0):
        self.sample_rate = sample_rate
        self.lowcut = lowcut
        self.highcut = highcut

    def butter_bandpass(self, lowcut, highcut, fs, order=4):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def filter_semg(self, data):
        """
        Apply Bandpass Filter (20-45Hz for basic low-sample rate demo or 20-450Hz for high-rate)
        """
        if len(data) < 15: # Need enough points for filtfilt
            return data
        try:
            b, a = self.butter_bandpass(self.lowcut, self.highcut, self.sample_rate, order=2)
            y = filtfilt(b, a, data)
            return y
        except Exception:
            return data

    def extract_features(self, raw_window):
        """
        Extract sEMG time & frequency domain features for Machine Learning model:
        1. RMS (Root Mean Square)
        2. MAV (Mean Absolute Value)
        3. Variance
        4. Zero Crossing Rate (ZCR)
        5. Median Frequency (MF estimate)
        """
        signal = np.array(raw_window)
        if len(signal) == 0:
            return [0.0, 0.0, 0.0, 0.0, 0.0]

        filtered = self.filter_semg(signal)

        # Time-domain features
        rms = np.sqrt(np.mean(filtered**2))
        mav = np.mean(np.abs(filtered))
        var = np.var(filtered)
        
        # Zero crossings
        zero_crossings = np.where(np.diff(np.sign(filtered)))[0]
        zcr = len(zero_crossings) / float(len(filtered))

        # Median Frequency estimate via FFT
        fft_vals = np.abs(np.fft.rfft(filtered))
        fft_freqs = np.fft.rfftfreq(len(filtered), 1.0 / self.sample_rate)
        cumulative_power = np.cumsum(fft_vals)
        total_power = cumulative_power[-1] if len(cumulative_power) > 0 and cumulative_power[-1] > 0 else 1.0
        med_freq_idx = np.where(cumulative_power >= total_power / 2.0)[0]
        med_freq = fft_freqs[med_freq_idx[0]] if len(med_freq_idx) > 0 else 0.0

        return [rms, mav, var, zcr, med_freq]

def calculate_effort_score(rms_value, max_rms=2000.0):
    """
    Map RMS signal to Effort Percentage (0% - 100%)
    """
    effort = (rms_value / max_rms) * 100.0
    return float(np.clip(effort, 0.0, 100.0))
