import requests
from requests.auth import HTTPBasicAuth

LIST_JOBS_URL = 'https://harvest.greenhouse.io/v1/job_posts?per_page=500'
LIST_APPLICATIONS_FOR_JOB_URL = 'https://harvest.greenhouse.io/v1/applications?per_page=500&job_id={}'
LIST_CANDIDATES_FOR_JOB_URL = 'https://harvest.greenhouse.io/v1/candidates?per_page=500&job_id={}'
LIST_SCORECARDS_FOR_APPLICATION_URL = 'https://harvest.greenhouse.io/v1/applications/{}/scorecards'


class GreenhouseClient(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self._auth = HTTPBasicAuth(self.api_key, '')

    def get_api_result(self, url):
        response = requests.get(url, auth=self._auth)
        response.raise_for_status()
        return response.json()

    def list_jobs(self):
        return self.get_api_result(LIST_JOBS_URL)

    def get_candidates_for_job(self, job):
        job_id = job['job_id']
        return self.get_api_result(LIST_CANDIDATES_FOR_JOB_URL.format(job_id))

    def get_applications_for_job(self, job):
        job_id = job['job_id']
        return self.get_api_result(LIST_APPLICATIONS_FOR_JOB_URL.format(job_id))

    def get_scorecards_for_application(self, application):
        return self.get_api_result(LIST_SCORECARDS_FOR_APPLICATION_URL.format(application['id']))
