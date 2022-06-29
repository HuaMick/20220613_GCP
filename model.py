# pip install --upgrade google-cloud-storage
import datetime
from datetime import date
from urllib.request import Request
from google.cloud import storage
from google.oauth2 import service_account

import toml
import pickle

Info = {}
Info['AppName'] = '20220613'
Info['API_CAP'] = 10

Resources = {}
Resources['API'] = {}
Resources['GCP'] = {}
Resources['API']['AppName'] = []
Resources['API']['RequestDate'] = []
Resources['API']['Status'] = []
Resources['API']['Response'] = []
Resources['GCP']['AppName'] = []
Resources['GCP']['RequestDate'] = []
Resources['GCP']['RequestType'] = []
Resources['GCP']['Response'] = []

GCP = {}

VIEW_Model={}
VIEW_Model['ContactInfo'] = ("""

Author: Mick Hua
Linkedin: https://www.linkedin.com/in/mick-hua-3    53353a/
github: https://github.com/HuaMick/20220609

""")
VIEW_Model['OVERVIEWText0'] = ("""
This is a learning project to experiment with GCP Cloud Storage.
""")

VIEW_Model['STEP1Text0'] = ("""
The start button authenticates with GCP cloud using Streamlit's 
secrets manager. You need to add the GCP authentication json to 
the secrets input when you deploy in the .toml file format.
You also need to pass secrets when initating the client.
""")

VIEW_Model['STEP1Code0'] = ("""
credentials = service_account.Credentials.from_service_account_info(Secrets)
GCP['GCP_Client'] = storage.Client(credentials=credentials)
""")

VIEW_Model['STEP1Text1'] = ("""
Once authenticated we can inspect resources on GCP cloud storage.
If the app can find it will iniate a pull otherwise it will create
a blank one and push it. Once done we delete the button so it can't
be clicked again as we don't want trolls spamming pull requests.
""")

VIEW_Model['STEP2Text0'] = ("""
This button executes an API pull request from transport NSW.
Again we want to prevent trolls from spamming this, so we delete 
the button once we hit the max allowed. Every request is tracked
in resources, so we can detect the number of requests that have 
been initiated in the day and base the cap on that.
""")

from os.path import exists
#Secrets = (toml.load(".streamlit\secrets.toml"))['gcp_service_account']
#requests = pd.DataFrame({k:v for k,v in Resources['GCP'].items() if k in ['RequestDate', 'RequestType']})
def Model_Init(Secrets):
    global GCP
    credentials = service_account.Credentials.from_service_account_info(Secrets)
    GCP['GCP_Client'] = storage.Client(credentials=credentials)
    GCP['GCP_BucketName'] = '20220618-bucket'
    GCP['GCP_Bucket'] = GCP['GCP_Client'].bucket(GCP['GCP_BucketName'])

def Resources_Save(Resources):
    with open('Resources.pickle', 'wb') as handle:
        pickle.dump(Resources, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return Resources

def Resources_Load(Resources):
    if exists('Resources.pickle'):
        file = open("Resources.pickle",'rb')
        Resources = pickle.load(file)
    return Resources

def GCP_Push(GCP, Resources):
    Bucket = GCP['GCP_Bucket']
    Blob = Bucket.blob('Resources')

    Resources = Resources_Load(Resources)

    Resources['GCP']['AppName'].append(Info['AppName'])
    Resources['GCP']['RequestDate'].append(date.today())
    Resources['GCP']['RequestType'].append('PUSH')
    Resources['GCP']['Response'].append(Blob.__repr__())

    Resources = Resources_Save(Resources)

    Blob.upload_from_filename('Resources.pickle')
    return Resources

def GCP_Pull(GCP, Resources):
    Bucket = GCP['GCP_Bucket']
    Blob = Bucket.get_blob('Resources')

    Resources = pickle.loads(Blob.download_as_string())

    Resources['GCP']['AppName'].append(Info['AppName'])
    Resources['GCP']['RequestDate'].append(date.today())
    Resources['GCP']['RequestType'].append('PULL')
    Resources['GCP']['Response'].append(Blob.__repr__())

    Resources = Resources_Save(Resources)

    return Resources





# VIEW_Model['STEP1Text1'] = ("""
# API has request limits so we want to limit requestst to Once a Day
# """)