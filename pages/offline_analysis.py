import streamlit as st

from src2.navigation import navigation
from pages.do_anlysis import Analysis


class OfflineAnalysis:
    def __init__(self) -> None:

        self.files = self.upload_file()

    def upload_file(self):
        container = st.container(height=None, border=True)

        with container:
            files = st.file_uploader(
                label="Upload File(s)",
                label_visibility="visible",
                accept_multiple_files=True,
            )
        return files

    def display(self):

        if not self.files:
            return None

        do_analysis = Analysis(self.files, local=False)
        do_analysis.display()


navigation()

analysis = OfflineAnalysis()
analysis.display()
