import numpy as np
import scipy.stats as stat

import plotly.graph_objects as go

from src.calculation import (
    removedc_minus_mean,
    integrate_to_velocity,
    calculate_envelope_hilbert_transform,
)

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

        self.fs = fs  # in Hz

    def plot_timeseries_acceleration_remove_dc(self):

        y = []

        for data in self.Y:

            _data = removedc_minus_mean(data)

            y.append(_data)

        G = PlotlyGraph()

        G.add_line(
            self.X,
            y,
            label=self.labels,
            title="Acceleration",
            xlabel="Time [Second]",
            ylabel="Acceleration Amplitude [g]",
        )

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    def plot_timeseries_integrated_velocity(self):

        y = []

        for data in self.Y:

            vel = integrate_to_velocity(data, self.fs)

            y.append(vel)

        G = PlotlyGraph()

        G.add_line(
            self.X,
            y,
            label=self.labels,
            title="Velocity",
            xlabel="Time [Second]",
            ylabel="Velocity Amplitude [mm/s]",
        )

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    def plot_fft_acceleration(self, ref):

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

        if ref:
            add_box(G.fig, ref, max_v)

        G.add_line(
            x,
            y,
            label=self.labels,
            xlim=[5, 550],
            ylim=[0, max_v],
            title="Spectrum (Acceleration)",
            xlabel="Frequency [Hz]",
            ylabel="FFT Amplitude [g]",
        )

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    def plot_fft_velocity(self, ref):

        x = []
        y = []

        max_v = 0

        for data in self.Y:

            vel = integrate_to_velocity(data, self.fs)

            fft_x, fft_y = FA.calc_fft(vel, self.fs)

            y.append(fft_y)
            x.append(fft_x)

            _v = select_fft_range(fft_x, fft_y)
            if _v > max_v:
                max_v = _v

        G = PlotlyGraph()

        if ref:
            add_box(G.fig, ref, max_v)

        G.add_line(
            x,
            y,
            label=self.labels,
            xlim=[5, 550],
            ylim=[0, max_v],
            title="Spectrum (Velocity)",
            xlabel="Frequency [Hz]",
            ylabel="FFT Amplitude [mm/s]",
        )

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    def plot_envelope_fft_acceleration(self, ref):

        y = []
        x = []

        max_v = 0

        for data in self.Y:

            envelope = calculate_envelope_hilbert_transform(data)

            fft_x, fft_y = FA.calc_fft(envelope, self.fs)

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
            title="Envelope Spectrum (Acceleration)",
            xlabel="Frequency [Hz]",
            ylabel="FFT Amplitude [g]",
        )

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    def plot_envelope_fft_velocity(self, ref):

        y = []
        x = []

        max_v = 0

        for data in self.Y:

            vel = integrate_to_velocity(data, self.fs)

            envelope = calculate_envelope_hilbert_transform(vel)

            fft_x, fft_y = FA.calc_fft(envelope, self.fs)

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
            title="Envelope Spectrum (Velocity)",
            xlabel="Frequency [Hz]",
            ylabel="FFT Amplitude [mm/s]",
        )

        G.fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return G.fig

    def plot_statistic_acceleration(self):

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
                type="category",  # Prevent the auto-casting
            ),
            barmode="group",
        )

        return fig

    def plot_statistic_velocity(self):

        Y_rms = []
        Y_kurtosis = []

        for data in self.Y:

            vel = integrate_to_velocity(data, self.fs)

            rms = np.sqrt(np.mean(np.power(vel, 2)))
            kur = stat.kurtosis(vel)

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
                type="category",  # Prevent the auto-casting
            ),
            barmode="group",
        )

        return fig
