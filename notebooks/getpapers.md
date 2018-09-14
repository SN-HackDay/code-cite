
# Step 1: find the papers that contain the term of interest

We use ContentMine's [getpapers](https://github.com/ContentMine/getpapers) tool to identify papers for a particular term.
This is step one of the full pipeline to analyse the open access literature for software citation and other practises, as developed by the code-cite team at Collaborations Workshop 2018, building on work done at the Springer Nature hack day 2017.

## a. Setup your local environment

You can run getpapers without local installation using this Docker image:

```
docker run softwaresaved/getpapers --version
```

On linux and mac you will probably need to prepend this with `sudo`. This should return the current getpapers version number:

```
0.4.17
```

If you prefer to run locally, please follow these steps:

* Open the terminal
* [Install npm](https://github.com/blahah/installing-node-tools) if you do not already have it.
* Install getpapers
```
npm install --global getpapers
```
* Check it is installed
```
getpapers --version
```
should return the installed version number. We're using v0.4.17.

## b. Understanding getpapers

Full documentation is at: https://github.com/ContentMine/getpapers

For this process, here's some useful info.

Sample code:
```
# local install:

getpapers --query 'query' -o output
```

With docker you will need to specify a local directory which maps to the docker directory where the data will be downloaded, like so:

```
docker run -v <local_data_dir>:<docker_dir> softwaresaved/getpapers --query 'query' -o <docker_dir>
```

Further explanation is given in the getpapers [docker repo](://github.com/softwaresaved/getpapers).

query = your search term. The search query language is dependent on the API being called. By default, this is europePMC, and notes on the queries possible are at
output = name of directory that your output will be printed to. Without specifying further, this will be JSON with paper metadata and abstract.

Append -x to the sample code to download the full-text article XMLs into the output directory.
Include -n (before -o) to just return a number of results instead of downloading the paper data.

Search directory: getpapers will search europePMC by default, which accesses all the open biomedical literature so is a comprehensive directory to choose for biomedical sciences. Other APIs ContentMine can search are IEEE, ArXiv and CrossRef. To search other repositories, see .....
*P.S. we'd love to see this pipeline extended to other APIs.*

## b. Decide your query term

The query term you use should retrieve the right results. Take a look through some of the literature to understand which common elements will make a good search query.

In this example, we search for GitHub URLs using the term 'github.com' since we are looking to identify github urls. Searching for 'github' alone retrieves 12,823 papers from europePMC using getpapers; whilst searching for 'github.com' retrieves 11,377 so is a more refined search and likely excludes individual mentions of GitHub that are not external links, as well as incuding github.io links which are more likely to be landing pages than software repositories.

Other queries to try:
* Zenodo - '/zenodo.' may be a good common string to identify zenodo DOIs. Source: [Kirstie Whitaker](https://github.com/SN-HackDay/code-cite/issues/3)
* Figshare

## c. Run getpapers to find number of results for your query

Set <local_data_dir> to be a directory of your choice on your local machine where any downloaded data will be stored.

Sample code:
```

# local install

getpapers --query 'query' -n -o <local_data_dir>

# docker container

docker run -v <local_data_dir>:<docker_dir> softwaresaved/getpapers --query 'query' -o <docker_dir>

```

For github.com mentions:
```

# local install

getpapers --query 'github.com' -n -o <local_data_dir>

# docker container

docker run -v <local_data_dir>:<docker_dir> softwaresaved/getpapers --query 'github.com' -n -o <docker_dir>
```
returns
```
info: Searching using eupmc API
info: Running in no-execute mode, so nothing will be downloaded
info: Found 11377 open access results
```

## d. Run getpapers to download matching article data in xml
Sample code:
```
# local install

getpapers --query 'query' -o output -x

# docker container

docker run -v <local_data_dir>:<docker_dir> softwaresaved/getpapers --query 'query' -o <docker_dir> -x
```
Appending -x here specifies that the articles should be downloaded in xml. The default without -x is to return the article JSON with article metadata and abstract but not full-text. Note this will also be returned in addition to the xml download.

Before running this command, check you are in the right directory for this project (e.g. /code-cite/<query-term> if you have cloned from this project's Github). This next step will create a directory called 'data' that will include all the full-text articles in XML.

For github.com articles:
```
# local install

getpapers --query 'github.com' -o data -x

# docker container

docker run -v <local_data_dir>:<docker_dir> softwaresaved/getpapers --query 'github.com' -o <docker_dir> -x
```
Returns:
```
info: Done collecting results
info: Duplicate records found: 11374 unique results identified
info: Saving result metadata
info: Full EUPMC result metadata written to eupmc_results.json
info: Individual EUPMC result metadata records written
info: Extracting fulltext HTML URL list (may not be available for all articles)
info: Fulltext HTML URL list written to eupmc_fulltext_html_urls.txt
...<warnings about articles for which no XML found>
info: Got XML URLs for 11310 out of 11374 results
info: Downloading fulltext XML files
Downloading files [===============] 100% (11310/11310) [181.1s elapsed, eta 0.0]
info: All downloads succeeded!
```
Note some articles may not have associated XMLs if they are missing a PMCID or are not open access.

Note also the time it takes to download these files: for >11,000 XMLs, it took 3 minutes on a standard laptop (MacBook Air) and excellent internet connection (81.40 Mbps by speedtest directly after this command was run).

## e. Check the outputs and structure of these data.

We expect in our chosen parent directory:
- [x] Full EUPMC result metadata written to eupmc_results.json [!large!]
- [x] Fulltext HTML URL list written to eupmc_fulltext_html_urls.txt
- [x] XML article data in subfolders

The subfolders we find in <local_data_dir> are:

* /10.1101 - contains more subfolders, each named by doi extension (e.g. 003905 for doi: 10.1101/003905). These subfolders contain one file: 'eupmc_result.json' which is the article metadata including abstract for that DOI. These are the DOIs without a PMC or full-text.
* many subfolders called /PMC{numerics} - each of these folders is for a single article, identified by their PMCID. The folder contains the 'eupmc_result.json' and 'fulltext.xml'.

## f. Go to step two

In step two, we will use a Jupyter notebook to extract the GitHub URLs from the full-texts, and transform the resulting data into a usable structure for interpretation and visualisation via the downstream steps.
