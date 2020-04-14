# Python Crawler with Tor

## How to use

1.  Edit source.csv
2.  Edit config.json, the format of the file is

<pre>
"column_name": {
    ... beautiful soup selector
}
</pre>

Please refer to [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

3.  Run the Tor setup script

Running this project via docker using volume

`docker run -it -v <source_dir>:<container_dir> ubuntu:18.04 bash`

Example:

`docker run -it -v C:\Users\aaqid\Documents\tor-crawler:/home/tor-crawler ubuntu:18.04 bash`

then run `cd home/tor-crawler && sh setup.sh`

4.  Run the python script via `python3 crawler.py` Or run it in background via `chmod +x crawler.py && nohup python3 crawler.py > crawl.log &`

**The output will be generated as output.csv**

Please check and run the default example for more details

## Tor network via setup.sh
To enable anonymous crawling, we will use Tor network. The process of setting up the network is simplified using bash setup script.

## crawler.py
This is the main file for the crawler to work. It will read the input file (consists of url data to be crawled) and crawl each row then write it in new csv file. You can terminate `crawler.py` anytime and it will resume the process in the next run by comparing the input file and output file length.

References:
`https://gist.github.com/DusanMadar/8d11026b7ce0bce6a67f7dd87b999f6b`

