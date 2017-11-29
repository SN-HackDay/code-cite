import requests
import pandas
import time
from xml.etree import ElementTree

# Get API key from secrets folder
api_key_path = "../secrets/springer_fulltext_api_key.txt"
f = open(api_key_path, 'r')
api_key = f.readline()
api_base_url = "http://api.springer.com/xmldata/app"

def getQueryResult(query, base_url=api_base_url, key=api_key, timeout=None):
    # Construct API query URL
    url = "{}?q={}&api_key={}".format(base_url, query, key)
    response = requests.get(url, timeout=timeout)
    return response.content

def parseResultAsXml(result):
    return ElementTree.fromstring(result)

def countFromResultXml(xml):
    result = xml.find('result')
    count = result.find('total').text
    return int(count)

def countForQuery(query):
    return countFromResultXml(parseResultAsXml(getQueryResult(query)))

def records_by_term_and_year(search_terms, years):
    data = []
    for search_term in search_terms:
        for year in years:
            query = "{} year:{}".format(search_term, year)
            filteredCount = countForQuery(query)
            unfilteredCount = countForQuery("")
            row = {"term": search_term, "year": year,
                    "hits": filteredCount, "total": unfilteredCount}
            data.append(row)
    df = pandas.DataFrame(data)
    return df

def main():
    search_terms = ["github.com", "10.5281/zenodo"]
    years = range(2017, 2000, -1)
    df = records_by_term_and_year(search_terms, years)
    print(df)

if __name__ == "__main__":
    main()
