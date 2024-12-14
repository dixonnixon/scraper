#!/usr/bin/env python 

from config import settings
import dataforseo_client
from dataforseo_client.models.content_analysis_category_trends_live_request_info import ContentAnalysisCategoryTrendsLiveRequestInfo
from dataforseo_client.models.content_analysis_category_trends_live_response_info import ContentAnalysisCategoryTrendsLiveResponseInfo
from dataforseo_client.rest import ApiException
from pprint import pprint



def start():
    print("Starting ...")
# Defining the host is optional and defaults to https://api.dataforseo.com
# See configuration.py for a list of all supported configuration parameters.
    configuration = dataforseo_client.Configuration(
        host = "https://api.dataforseo.com"
    )

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
    configuration = dataforseo_client.Configuration(
        username = settings.USER,
        password = settings.PASS
    )

# Enter a context with an instance of the API client
    with dataforseo_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
        api_instance = dataforseo_client.ContentAnalysisApi(api_client)
        content_analysis_category_trends_live_request_info = [dataforseo_client.ContentAnalysisCategoryTrendsLiveRequestInfo()] # List[ContentAnalysisCategoryTrendsLiveRequestInfo] |  (optional)

        try:
            api_response = api_instance.category_trends_live(content_analysis_category_trends_live_request_info=content_analysis_category_trends_live_request_info)
            print("The response of ContentAnalysisApi->category_trends_live:\n")
            pprint(api_response)
        except Exception as e:
            print("Exception when calling ContentAnalysisApi->category_trends_live: %s\n" % e)

#You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
#Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access



#if __name__ == '__main__':
    #print(settings)
    #client = RestClient(settings.USER, settings.PASS)
 #   start()
