import requests
from kbcstorage.client import Client
import streamlit as st
from streamlit.web.server.websocket_headers import _get_websocket_headers
import datetime

class KeboolaStreamlit:
    def __init__(self, root_url, token):
        self.client = Client(root_url, token)
        self.token = token
        self.root_url = root_url
        self.dev_mockup_headers = False

    def _get_headers(self):
        headers = _get_websocket_headers()
        if ('X-Kbc-User-Email' in headers):
            return headers
        elif (self.dev_mockup_headers != False):
            return self.dev_mockup_headers
        else:
            return []
             
    
    def set_dev_mockup_headers(self, headers):
        self.dev_mockup_headers = headers

    def authCheck(self, required_role_id):
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


    def createEvent(self, jobId, data):
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
                "event_application": headers['X-Forwarded-Host'],
                "event_job_id": jobId
            }
        }
        response = requests.post(url, headers=requestHeaders, json=requestData)

        if response.status_code == 200:
            st.wirte('Event sent')
        else:
            st.write(f"Error: {response.status_code} - {response.text}")