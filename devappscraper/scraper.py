from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pprint
import re
import time
import datetime


def get_applications(app_url,url,delay):
    """ Gets all applications for a given search result page
    Param
    ------
    app_url : str
        The url template for a single app, so you only need to
        append the code:

    url : str
        The URL of the search page. Note, will iterate though all pagenated pages

    """
    result = []
    page = 1

    while True :

        search_page = get_url(url+'&page='+str(page))
        html = BeautifulSoup(search_page,'html.parser')
        links = html.find_all('a','app_applicationlink')
        for id in links:
            appid = get_appid(id.get('href'))
            link = app_url + appid
            app = parse_application(link)
            app['appid'] = appid
            result.append(app)
            time.sleep(delay)

        # check to see if there is a "next" button for pages. If there isn't this is the last page.
        if html.find('a',string='Next >>') is not None:
            page += 1
        else:
            break
    return result


def get_url(url):
    """Returns content from a response object. Raises RequestException and details code on fail. """

    with closing(get(url, stream=True)) as response:
        if response.status_code != 200:
            raise RequestException("url {} returned a reponse code of {}".format(url,response.status_code))
        return response.content

def parse_application(url):
    """Takes a url to an development application, returns a dictonary of data listed in desired_values"""

    result = {'Supporting Documents':[]}
    response = get_url(url)
    html = BeautifulSoup(response,'html.parser')
    app = html.find('div','box')
    data = [x for x in app.contents if x != '\n']
    # values we want to extract

    desired_values = ['Application #',"Date Received","Address","Ward","Application","Review Status","Description","Name","Phone","Status Date"]
    for entry in data:
        label = entry.find('div', 'label')

        if label is not None:
             label = label.string.replace('\r','').replace('\n','').replace('\t','').replace(':','')

        if label is not None and label in desired_values:
            detail = entry.find('div','appDetailValue')
            # Deal with fields that require special parsing
            # Address
            if label == "Address":
                detail = []
                addr = entry.find_all('a')
                for a in addr:
                    detail.append(a.string)
                result[label]=detail
            elif label == 'Date Received':
                detail = detail.string.replace('\r','').replace('\n','').replace('\t','').replace('\xa0',' ')
                detail = re.sub("\s\s+", " ", detail)
                detail = datetime.datetime.strptime(detail,'%B %d, %Y')
                result[label] = detail


            # Ward
            elif label == 'Ward':
                detail = detail.string.replace('\r','').replace('\n','').replace('\t','').replace('\xa0',' ')
                detail = re.sub("\s\s+", " ", detail)
                detail = detail.split(' - ')
                result['ward_num'] = ""
                result['ward_name'] = ""
                result['councillor'] = ""
                try:
                    result['ward_num'] = detail[0].split(' ')[1]
                    result['ward_name'] = detail[1]
                    result['councillor'] = detail[2]
                except IndexError as e:
                    print("Error parsing Ward Field: {}".format(e))
            # Status Date
            elif label == "Status Date":
                detail = detail.string.replace('\r','').replace('\n','').replace('\t','').replace('\xa0',' ')
                detail = re.sub("\s\s+", " ", detail)
                date = datetime.datetime.strptime(detail,'%B %d, %Y')
            elif label == 'Review Status':
                detail = detail.string.replace('\r','').replace('\n','').replace('\t','').replace('\xa0',' ')
                detail = re.sub("\s\s+", " ", detail)
                status = detail
            # All other fields
            elif detail is not None and detail.string is not None:
                detail=detail.string.replace('\r','').replace('\n','').replace('\t','').replace('\xa0',' ').strip()

                result[label]=detail

    supporting = app.find_all(find_supporting_docs)
    for x in supporting:
        result['Supporting Documents'].append(x.get('href'))

    #Insert status

    result['status'] = {"type":status,"date":date}
    return result





def get_appid(data):
    '''Returns the appid from a url'''
    return data.split('__')[1]

def find_supporting_docs(tag):
    '''Find all supporing doc tags in a document'''
    return tag.has_attr('id') and 'main:content:supportingDocLink' in tag['id']



#x= parse_application('https://app01.ottawa.ca/postingplans/appDetails.jsf?lang=en&appId=__A1K4I5')
