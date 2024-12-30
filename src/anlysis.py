import streamlit as st

from src.components import Static
from src.plots import Plots


class Analysis:
    def __init__(self):
        pass

    @staticmethod
    def write_metrics(motor_name, sensor_id, motor_condition, day_diff, rms):
        container = st.container(height=None, border=True)
        with container:
            col1, col2, col3, col4, col5 = st.columns(5)

            col1.metric(label="Motor", value=f"{motor_name}")
            col2.metric(label="Sensor", value=f"{sensor_id}")
            col3.metric(label="Condition", value=motor_condition)
            col4.metric(label="Since last inspection", value=f"{day_diff} day(s)")
            col5.metric(label="RMS [mm/s]", value=f"{rms}")

        return None

    @staticmethod
    def gauge_indicator(ai_score, rms):
        container = st.container(height=None, border=True)
        with container:
            col1, col2 = st.columns([6, 6], vertical_alignment="top", gap="medium")

            static = Static()

            with col1:
                static.gauge_chart_ai(value=ai_score)
            with col2:
                static.gauge_chart_rms(value=rms)

        return None

    @staticmethod
    def plot_charts(x, y, labels, fs=1600):

        plot = Plots(x, y, labels, fs)

        # == ROW == #

        container = st.container(border=True)
        with container:
            st.subheader("Temporal Analysis")

            col1, col2 = st.columns(2, gap="medium")

            with col1:
                if st.session_state["data_type"] == "Acceleration":
                    st.plotly_chart(plot.plot_fft_iftt())

                elif st.session_state["data_type"] == "Velocity":
                    st.plotly_chart(plot.plot_velocity())

            with col2:
                if st.session_state["data_type"] == "Acceleration":
                    st.plotly_chart(plot.plot_statistic())

                elif st.session_state["data_type"] == "Velocity":
                    st.plotly_chart(plot.plot_statistic_velocity())

        # == ROW == #

        ref = {
            "Show RPM": 0,
            "Show BPFI": 0,
            "Show BPFO": 0,
            "Show BSF": 0,
            "Show FTF": 0,
            "RPM": 0,
            "BPFI": 0,
            "BPFO": 0,
            "BSF": 0,
            "FTF": 0,
        }

        # == ROW == #

        st.write("")

        container = st.container(border=True)
        with container:

            st.subheader("Spectral Analysis")

            # ================================== #
            container = st.container(border=True)
            with container:

                st.markdown("##### Visualize characteristic frequencies")

                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    ref["RPM"] = int(st.text_input("Rotation Speed (RPM)", "1488")) / 60
                    ref["Show RPM"] = st.checkbox("Show RPM")

                with col2:
                    ref["BPFI"] = (
                        float(st.text_input("BPFI (Inner Race)", "5.0020")) * ref["RPM"]
                    )
                    ref["Show BPFI"] = st.checkbox("Show BPFI")

                with col3:
                    ref["BPFO"] = (
                        float(st.text_input("BPFO (Outer Race)", "2.9980")) * ref["RPM"]
                    )
                    ref["Show BPFO"] = st.checkbox("Show BPFO")

                with col4:
                    ref["BSF"] = (
                        float(st.text_input("BSF (Ball Spin)", "1.8710")) * ref["RPM"]
                    )
                    ref["Show BSF"] = st.checkbox("Show BSF")

                with col5:
                    ref["FTF"] = (
                        float(st.text_input("FTF (Cage)", "0.3750")) * ref["RPM"]
                    )
                    ref["Show FTF"] = st.checkbox("Show FTF")

            # ================================== #

            col1, col2 = st.columns(2, gap="medium")
            with col1:
                st.plotly_chart(plot.plot_fft(ref))
            with col2:
                st.plotly_chart(plot.plot_envelope_fft(ref))

        # == ROW == #

        # container = st.container(border=True)
        # with container:

        #     col1, col2 = st.columns(2, gap="medium")
        #     with col1:
        #         st.plotly_chart(plot.plot_envelope_fft_with_wavelet_denosing(ref))
        #     with col2:
        #         st.write("")
        #         # st.plotly_chart(plot.plot_envelope_fft_with_filter(ref))
        #         # st.plotly_chart(plot.plot_envelope_fft_with_denoising_filter(ref))

        #         st.plotly_chart(plot.plot_fft_iftt())

        return None
