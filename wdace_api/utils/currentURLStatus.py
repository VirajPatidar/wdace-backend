import requests
from requests.structures import CaseInsensitiveDict

def currentURLStatus(url):

        httpMethod = 'GET'
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        r = requests.get(url, headers=headers)

        status_code = r.status_code
        status_text = r.reason
        content_length = len(r.content)
        time_taken = r.elapsed.total_seconds()
        content_type = r.headers['Content-Type']


        return {
            "httpMethod": httpMethod,
            "status_code": status_code,
            "status_text": status_text,
            "content_length": content_length,
            "time_taken": time_taken,
            "content_type": content_type,
        }