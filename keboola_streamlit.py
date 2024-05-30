import requests
from kbcstorage.client import Client
import streamlit as st
from streamlit.web.server.websocket_headers import _get_websocket_headers
import datetime
import os
import pandas as pd


class KeboolaStreamlit:
    def __init__(self, root_url, token, tmp_data_folder = 'tmp/'):
        self.client = Client(root_url, token)
        self.token = token
        self.root_url = root_url
        self.dev_mockup_headers = False
        self.client = False
        self.tmpDataFolder = tmp_data_folder

    def _get_headers(self):
        headers = _get_websocket_headers()
        if ('X-Kbc-User-Email' in headers):
            return headers
        elif (self.dev_mockup_headers != False):
            return self.dev_mockup_headers
        else:
            return []
             
    def _get_sapi_client(self):
        """Getter for SAPI clients

        Returns:
            Client: Sapi clients
        """
        if(self.client == False):
            self.client = Client(self.root_url, self.token)
        return self.client

    def set_dev_mockup_headers(self, headers):
        self.dev_mockup_headers = headers

    def auth_check(self, required_role_id):
        headers = self._get_headers()
        if ('X-Kbc-User-Email' in headers):
            st.sidebar.write(f"Logged in as user: {headers['X-Kbc-User-Email']}")
            st.sidebar.link_button('Logout', '/_proxy/sign_out')
            with st.sidebar.expander('Show more'):
                st.write(headers)
            if (required_role_id not in headers['X-Kbc-User-Roles']):
                st.error("You don't have priviledges to use this application")
                st.stop()
        else:
            st.write('Not using proxy')


    def create_event(self, jobId :int, data):
        headers = self._get_headers()
        url = f"{self.root_url}/v2/storage/events"
        st.write(url)
        requestHeaders = {
            'Content-Type': 'application/json',
            'X-StorageApi-Token': self.token
        }
        requestData = {
            'message': 'Streamlit app write event',
            'component': 'keboola.data-apps',
            'params': {
                "user": headers['X-Kbc-User-Email'],
                "time" : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "endpoint": '/v2/storage/tables/upload',
                "event_type": "keboola_data_app_write",
                "event_data": {"data":data},
                "event_application": headers['Origin'],
                "event_job_id": jobId
            }
        }
        response = requests.post(url, headers=requestHeaders, json=requestData)

        if response.status_code == 201:
            st.write('Event sent')
        else:
            st.write(f"Error: {response.status_code} - {response.text}")

    @st.cache_data(ttl=7200)
    def get_data(self, table_id: str):
        """Get table from Keboola Storage

        Args:
            table_id (str): id of table (e.g in-c.bucket.table)

        Returns:
            pd.DataFrame: Storage table as DataFrame
        """
        client = self._get_sapi_client()
        table_detail = self._get_sapi_client().tables.detail(table_id=table_id)
        table_path = f"tmp/{table_detail['name']}"
        self._get_sapi_client().tables.export_to_file(table_id=table_id, path_name=table_path)
        
        if(os.path.exists(table_path + '.csv')):
            os.remove(table_path + '.csv')
        os.rename(table_path, table_path + '.csv')
        df = pd.read_csv(table_path + '.csv')
        return df
