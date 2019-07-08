import os
import sys
from datetime import datetime, timedelta
from googleads import adwords

CLIENT_CUSTOMER_ID = sys.argv[1]
CLIENT_NAME = sys.argv[2]
REPORT_TYPE="FINAL_URL_REPORT"

# Specify where to download the file here.
PATH = './FINAL_URL_REPORT/'
YESTERDAY = datetime.strftime(datetime.now() - timedelta(days = 1),'%Y-%m-%d')
FILENAME = str(YESTERDAY)+'-'+CLIENT_NAME+'-'+REPORT_TYPE+'.csv'
filepath = os.path.join(PATH,FILENAME)

def main(client):
  # Initialize appropriate service.
  report_downloader = client.GetReportDownloader(version='v201809')

  report_query = (adwords.ReportQueryBuilder()
                  .Select('Date', 'AdGroupId', 'AdGroupName', 'CampaignId', 'CampaignName', 'EffectiveFinalUrl', 'Impressions', 'Cost', 'Clicks', 'Interactions', 'AveragePosition')
                  .From('FINAL_URL_REPORT')
                  .Where('AdGroupStatus').In('ENABLED', 'PAUSED')
                  .During('YESTERDAY')
                  .Build())

     
  # You can provide a file object to write the output to. For this
  # demonstration we use sys.stdout to write the report to the screen.
  with open(filepath, mode='wb') as handler:
    report_downloader.DownloadReportWithAwql(
        report_query, 'CSV', output=handler, skip_report_header=True,
        skip_column_header=False, skip_report_summary=True,
          include_zero_impressions=False, client_customer_id=CLIENT_CUSTOMER_ID)

if __name__ == '__main__':
  # Initialize client object. Set path of googleads.yaml here to use
  adwords_client = adwords.AdWordsClient.LoadFromStorage('googleads.yaml')

  main(adwords_client)
