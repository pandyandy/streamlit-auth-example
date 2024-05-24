import streamlit as st
from kbcstorage.client import Client
from streamlit.web.server.websocket_headers import _get_websocket_headers
import requests

websocket_headers = _get_websocket_headers()

#Required ROLE id
REQUIRED_ROLE_ID = '30e3f1fb-5028-4c1c-9a98-ebaf8b668898'
LOGOUT_URL = 'https://630064.hub.europe-west3.gcp.keboola.com/_proxy/sign_out'
STORAGE_API_TOKEN = '336-45296-1e8hNxLoXBVpVdui1pAG0zJPADbj63dPoiHtlooI'


if('X-Kbc-User-Email' in websocket_headers):
    st.write('Using proxy')
    st.write('Logged in as user:' + websocket_headers['X-Kbc-User-Email'])
    st.link_button('Logout', LOGOUT_URL)
    if(REQUIRED_ROLE_ID not in websocket_headers):
        st.error("You don't have priviledges to use this applicaiton")
        st.stop()

else:
    st.write('Not using proxy')


with st.expander("Headers:"):
    st.write(websocket_headers)


client = Client('https://connection.europe-west3.gcp.keboola.com/', STORAGE_API_TOKEN)

def sendWriteData(tableId, data):
    #client.tables.load(table_id=tableId,)
    return 0


def createEvent(jobId, user, data):
    url = 'https://connection.europe-west3.gcp.keboola.com/v2/storage/events'
    headers = {
        'Content-Type': 'application/json',
        'X-StorageApi-Token': '336-45296-1e8hNxLoXBVpVdui1pAG0zJPADbj63dPoiHtlooI'
    }
    data = {
        'Message': 'Streamlit app write event',
        'component': 'keboola.data-apps',
        'type': 'info'
    }
    






