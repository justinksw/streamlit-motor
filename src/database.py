import pandas as pd

import streamlit as st


class Database:
    def __init__(self) -> None:
        self.conn = st.connection("mysql", type="sql")

    def get_data(self, label):
        """ 
        Args:
            label (string): f"SELECT data, label FROM lub WHERE label='{label}'"

        Returns:
            pd.DataFrame: Selected table from database
        """

        query = f"SELECT data, label FROM lub WHERE label='{label}'"
        table = self.conn.query(query, ttl=0)
        df = pd.DataFrame(table)

        return df
