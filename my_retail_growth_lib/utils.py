import json, os, re
import ipykernel
import requests
from requests.compat import urljoin
from notebook.notebookapp import list_running_servers

def get_notebook_fullname():
    """
    Return the full path of the jupyter notebook.
    @see https://github.com/jupyter/notebook/issues/1000#issuecomment-359875246
    """
    kernel_id = re.search('kernel-(.*).json',
                          ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()
    for ss in servers:
        response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                params={'token': ss.get('token', '')})
        for nn in json.loads(response.text):
            if not isinstance(nn, str) and nn['kernel']['id'] == kernel_id:
                relative_path = nn['notebook']['path']
                return os.path.realpath(os.path.join(ss['notebook_dir'], relative_path))


#/////////////////////////////////////////////////////////////////////////////////////































































