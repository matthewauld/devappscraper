from devappscraper import *
import json

def main():
    x='https://app01.ottawa.ca/postingplans/searchResults.jsf?lang=en&newReq=yes&action=as&descriptionSearch=true&allWordsSearchValue=kanat&exactPhraseSearchValue=&oneOfWordsSearchValue=&streetNo=&streetName=&ward=&applicationType=&applicationNo='
    list = get_applist(x)
    for app in list['features']:
        if len(app['geometry']['coordinates'])is not 2:
            list['features'].remove(app)
    j = json.dumps(list)
    with open('sampleJSON.txt','w') as f:
        f.write(j)

if __name__ == '__main__':
    main()
