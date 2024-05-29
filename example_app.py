import streamlit as st
from keboola_streamlit import KeboolaStreamlit

#Required ROLE id
REQUIRED_ROLE_ID = st.secrets['REQUIRED_ROLE_ID']
STORAGE_API_TOKEN = st.secrets['STORAGE_API_TOKEN']
KEBOOLA_HOSTNAME = st.secrets['KEBOOLA_HOSTNAME']

kst = KeboolaStreamlit(KEBOOLA_HOSTNAME, STORAGE_API_TOKEN)

kst.set_dev_mockup_headers({
    'X-Kbc-User-Email': 'user@dev.com',
    'X-Kbc-User-Roles': ['123', '11111111-2222-3333-4444-1234567890', 'abc'],
    'X-Forwarded-Host': 'https://mock-server/non-existing-app'
})

kst.auth_check(REQUIRED_ROLE_ID)
if st.button('create event'):
    kst.create_event(123, {'data':'of_event'})
