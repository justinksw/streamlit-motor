import numpy as np
import pywt
import scipy.stats as stat
from scipy.signal import hilbert, welch

import plotly.graph_objects as go

from kswutils_plotly.plotly_graph import PlotlyGraph
from kswutils_signal.frequency_analysis import FrequencyAnalysis as FA


def select_fft_range(fft_x, fft_y):
    fft_range = (5, 550)

    lo = 0
    up = 0
    for x in fft_x:
        if x <= fft_range[0]:
            lo += 1

        if x >= fft_range[1]:
            up += 1

    fft_x = fft_x[lo:-up]
    fft_y = fft_y[lo:-up]

    return fft_y.max()


def add_box(fig, ref, y_max, y_min=0):
    class BBox:
        def __init__(self, x, w=3) -> None:
            self.w = w
            self.h = y_max

            # Starting point, bottom-left point of the box
            self.x = x

    if ref["Show RPM"]:
        bb = BBox(ref["RPM"])
        name = "RPM"
        fcolor = "gray"

    elif ref["Show BPFI"]:
        bb = BBox(ref["BPFI"])
        name = "BPFI"
        fcolor = "#e377c2"

    elif ref["Show BPFO"]:
        bb = BBox(ref["BPFO"])
        name = "BPFO"
        fcolor = "#7f7f7f"

    elif ref["Show BSF"]:
        bb = BBox(ref["BSF"])
        name = "BSF"
        fcolor = "#bcbd22"

    elif ref["Show FTF"]:
        bb = BBox(ref["FTF"])
        name = "FTF"
        fcolor = "#17becf"

    else:
        return None

    fig.add_trace(
        go.Scatter(
            x=[
                bb.x - bb.w // 2,
                bb.x - bb.w // 2,
                bb.x + bb.w // 2,
                bb.x + bb.w // 2,
                bb.x - bb.w // 2,
            ],
            y=[y_min, bb.h, bb.h, y_min, y_min],
            fill="toself",
            mode="none",
            name=name,
            fillcolor=fcolor,
        ),
    )

    if ref["Show FTF"]:
        return None

    else:

        fig.add_trace(
            go.Scatter(
                x=[
                    bb.x * 2 - bb.w // 2,
                    bb.x * 2 - bb.w // 2,
                    bb.x * 2 + bb.w // 2,
                    bb.x * 2 + bb.w // 2,
                    bb.x * 2 - bb.w // 2,
                ],
                y=[y_min, bb.h, bb.h, y_min, y_min],
                fill="toself",
                mode="none",
                name=name,
                fillcolor=fcolor,
            ),
        )

        fig.add_trace(
            go.Scatter(
                x=[
                    bb.x * 3 - bb.w // 2,
                    bb.x * 3 - bb.w // 2,
                    bb.x * 3 + bb.w // 2,
                    bb.x * 3 + bb.w // 2,
                    bb.x * 3 - bb.w // 2,
                ],
                y=[y_min, bb.h, bb.h, y_min, y_min],
                fill="toself",
                mode="none",
                name=name,
                fillcolor=fcolor,
            ),
        )


class Plots:
    def __init__(self, x, y, labels, fs):

        self.X = x
        self.Y = y
        self.labels = labels

        # Local analysis: files: directories
        # Online analysis: files: streamlit upload file objects

        # datafiles = [MotorJsonFile(i, local) for i in files]

        self.fs = fs  # in Hz

        # self.X = []
        # self.Y = []
        # self.label = []

        # for m in datafiles:

        #     data = m.get_data()
        #     self.Y.append(data)

        #     _t = np.linspace(0, len(data), len(data)) / self.fs
        #     self.X.append(_t)

        #     self.label.append(m.get_file_name())

    def plot_raw_data(self):

        G = PlotlyGraph()

        G.add_line(
            self.X,
            self.Y,
            label=self.labels,
            title="Raw Data",
            xlabel="Time [Second]",
            ylabel="Acceleration Amplitude [g]",
        )

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    def plot_envelope(self):

        y = []

        for data in self.Y:

            analytic_signal = hilbert(data)
            amplitude_envelope = np.abs(analytic_signal)

            y.append(amplitude_envelope)

        G = PlotlyGraph()

        G.add_line(
            self.X,
            y,
            label=self.labels,
            title="Envelope",
            xlabel="Time [Second]",
            ylabel="Acceleration Amplitude [g]",
        )

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    def plot_fft(self, ref):

        x = []
        y = []

        max_v = 0

        for data in self.Y:

            fft_x, fft_y = FA.calc_fft(data, self.fs)

            y.append(fft_y)
            x.append(fft_x)

            _v = select_fft_range(fft_x, fft_y)
            if _v > max_v:
                max_v = _v

        G = PlotlyGraph()

        add_box(G.fig, ref, max_v)

        G.add_line(
            x,
            y,
            label=self.labels,
            xlim=[5, 550],
            ylim=[0, max_v],
            title="Spectrum (Raw Data)",
            xlabel="Frequency [Hz]",
            ylabel="FFT Amplitude [g]",
        )

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    def plot_envelope_fft(self, ref):

        y = []
        x = []

        max_v = 0

        for data in self.Y:

            analytic_signal = hilbert(data)
            amplitude_envelope = np.abs(analytic_signal)

            fft_x, fft_y = FA.calc_fft(amplitude_envelope, self.fs)

            y.append(fft_y)
            x.append(fft_x)

            _v = select_fft_range(fft_x, fft_y)
            if _v > max_v:
                max_v = _v

        G = PlotlyGraph()

        add_box(G.fig, ref, max_v)

        G.add_line(
            x,
            y,
            label=self.labels,
            xlim=[5, 550],
            ylim=[0, max_v],
            title="Spectrum (Envelope)",
            xlabel="Frequency [Hz]",
            ylabel="FFT Amplitude [g]",
        )

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    #

    def plot_envelope_fft_with_filter(self, ref):

        y = []
        x = []

        max_v = 0

        for data in self.Y:

            data = FA.bandpass_filter(data, lowcut=10, highcut=500, fs=self.fs, order=3)

            analytic_signal = hilbert(data)
            amplitude_envelope = np.abs(analytic_signal)

            fft_x, fft_y = FA.calc_fft(amplitude_envelope, self.fs)

            y.append(fft_y)
            x.append(fft_x)

            _v = select_fft_range(fft_x, fft_y)
            if _v > max_v:
                max_v = _v

        G = PlotlyGraph()

        add_box(G.fig, ref, max_v)

        G.add_line(
            x,
            y,
            label=self.labels,
            xlim=[5, 550],
            ylim=[0, max_v],
            title="Envelope Spectrum + Band Pass Filter",
            xlabel="Frequency [Hz]",
            ylabel="FFT Amplitude [g]",
        )

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    #

    def plot_envelope_fft_with_wavelet_denosing(self, ref):

        y = []
        x = []

        max_v = 0

        for data in self.Y:

            # Perform a multi-level wavelet decomposition
            coeffs = pywt.wavedec(data, "db1", level=4)

            # Set a threshold to nullify smaller coefficients (assumed to be noise)
            threshold = 0.5
            coeffs_thresholded = [
                pywt.threshold(c, threshold, mode="soft") for c in coeffs
            ]

            # Reconstruct the signal from the thresholded coefficients
            data = pywt.waverec(coeffs_thresholded, "db1")

            analytic_signal = hilbert(data)
            amplitude_envelope = np.abs(analytic_signal)

            fft_x, fft_y = FA.calc_fft(amplitude_envelope, self.fs)

            y.append(fft_y)
            x.append(fft_x)

            _v = select_fft_range(fft_x, fft_y)
            if _v > max_v:
                max_v = _v

        G = PlotlyGraph()

        add_box(G.fig, ref, max_v)

        G.add_line(
            x,
            y,
            label=self.labels,
            xlim=[5, 550],
            ylim=[0, max_v],
            title="Envelope Spectrum + Wavelet Transform Denoising",
            xlabel="Frequency [Hz]",
            ylabel="FFT Amplitude [g]",
        )

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    #

    def plot_envelope_fft_with_denoising_filter(self, ref):

        y = []
        x = []

        max_v = 0

        for data in self.Y:

            # Perform a multi-level wavelet decomposition
            coeffs = pywt.wavedec(data, "db1", level=4)
            # Set a threshold to nullify smaller coefficients (assumed to be noise)
            threshold = 0.5
            coeffs_thresholded = [
                pywt.threshold(c, threshold, mode="soft") for c in coeffs
            ]
            # Reconstruct the signal from the thresholded coefficients
            data = pywt.waverec(coeffs_thresholded, "db1")

            #
            data = FA.bandpass_filter(data, lowcut=10, highcut=600, fs=self.fs, order=3)

            analytic_signal = hilbert(data)
            amplitude_envelope = np.abs(analytic_signal)

            fft_x, fft_y = FA.calc_fft(amplitude_envelope, self.fs)

            y.append(fft_y)
            x.append(fft_x)

            _v = select_fft_range(fft_x, fft_y)
            if _v > max_v:
                max_v = _v

        G = PlotlyGraph()

        add_box(G.fig, ref, max_v)

        G.add_line(
            x,
            y,
            label=self.labels,
            xlim=[5, 550],
            ylim=[0, max_v],
            title="Envelope Spectrum + Denoising + Filter",
            xlabel="Frequency [Hz]",
            ylabel="FFT Amplitude [g]",
        )

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    #

    def plot_envelope_psd(self, ref):

        y = []
        x = []

        max_v = 1

        for data in self.Y:

            analytic_signal = hilbert(data)
            amplitude_envelope = np.abs(analytic_signal)

            f, Pxx_den = welch(amplitude_envelope, self.fs, nperseg=self.fs // 2)

            y.append(Pxx_den)
            x.append(f)

        G = PlotlyGraph()

        add_box(G.fig, ref, max_v, y_min=1e-9)

        G.add_line(
            x,
            y,
            label=self.labels,
            xlim=[0, 550],
            # ylim=[1e-9, 1],
            title="Power Spectrum Density (PSD) (Envelope)",
            xlabel="Frequency [Hz]",
            ylabel="Amplitude [g**2/Hz]",
        )

        G.fig.update_yaxes(type="log", range=[-9, 0])

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    def plot_statistic(self):

        Y_rms = []
        Y_kurtosis = []

        for data in self.Y:

            rms = np.sqrt(np.mean(np.power(data, 2)))
            kur = stat.kurtosis(data)

            Y_rms.append(rms)
            Y_kurtosis.append(kur)

        fig = go.Figure(
            data=[
                go.Bar(name="RMS", x=self.labels, y=Y_rms),
                go.Bar(name="Kurtosis", x=self.labels, y=Y_kurtosis),
            ]
        )
        # Change the bar mode
        fig.update_layout(
            title=dict(
                text="Statistic",
                font=dict(size=18),
            ),
            yaxis_title=dict(
                text="Amplitude",
                font=dict(
                    size=16,
                ),
            ),
            xaxis=dict(
                tickfont=dict(
                    size=16,
                ),
            ),
            barmode="group",
        )

        return fig
