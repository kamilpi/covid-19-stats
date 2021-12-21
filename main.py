
import requests
import logging
import os
from prometheus_client import Gauge
from prometheus_client import start_http_server
import time
import json

log_level = os.getenv('LOG_LEVEL', 'INFO')
http_request_timeout = os.getenv('HTTP_REQUEST_TIMEOUT', 10)
logging.basicConfig(format='%(asctime)s - %(message)s', level=log_level)

def getStats():
    pageUrl = "https://corona.lmao.ninja/v3/covid-19/countries?sort=country"
    rsMetrics = requests.get(pageUrl, timeout=http_request_timeout)

    if (rsMetrics.ok):
        return rsMetrics

    else:
        logging.error("%s" % rsMetrics)
        return False



cases = Gauge('covid19_cases', 'stats about covid-19', ['country'])
todayCases = Gauge('covid19_today_cases', 'stats about covid-19', ['country'])
deaths = Gauge('covid19_deaths', 'stats about covid-19', ['country'])
todayDeaths = Gauge('covid19_today_deaths', 'stats about covid-19', ['country'])
recovered = Gauge('covid19_recovered', 'stats about covid-19', ['country'])
active = Gauge('covid19_active', 'stats about covid-19', ['country'])
critical = Gauge('covid19_critical', 'stats about covid-19', ['country'])


def process_request():
    match = getStats().json()
    for singleObject in match:
        # logging.info(singleObject['country'])
        cases.labels(country='%s' % singleObject['country']).set(float(singleObject['cases']))
        todayCases.labels(country='%s' % singleObject['country']).set(float(singleObject['todayCases']))
        deaths.labels(country='%s' % singleObject['country']).set(float(singleObject['deaths']))
        todayDeaths.labels(country='%s' % singleObject['country']).set(float(singleObject['todayDeaths']))
        recovered.labels(country='%s' % singleObject['country']).set(float(singleObject['recovered']))
        active.labels(country='%s' % singleObject['country']).set(float(singleObject['active']))
        critical.labels(country='%s' % singleObject['country']).set(float(singleObject['critical']))

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    logging.info("Starting server...")
    while True:
        process_request()
        time.sleep(120)
