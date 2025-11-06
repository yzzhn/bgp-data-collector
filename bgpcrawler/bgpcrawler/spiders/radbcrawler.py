from pathlib import Path

import os
import scrapy
import pandas as pd


class QuotesSpider(scrapy.Spider):
    name = "radbcrawler"

    custom_settings = {
        'DOWNLOAD_DELAY': 1
        }

    def start_requests(self):
        asdf = pd.read_csv("../asrank/asnum_fromranking.csv", usecols=["asn"])
        as_list = sorted(asdf["asn"].tolist())

        #def chunks(lst, n):
        #    for i in range(0, len(lst), n):
        #        yield lst[i : i + n]

        #for chunk in chunks(as_list, 5000):
        for asnum in as_list[:65000]:
            url = f"https://www.radb.net/query?keywords=as{asnum}"
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={"asnum": asnum})

    def parse(self, response, asnum):
        # figure out folder based on ASN
        folder_int = int(asnum) // 5000
        folder_path = os.path.join(
            "../data/radb202511",
            f"asn_start{folder_int * 5000}",
        )
        os.makedirs(folder_path, exist_ok=True)

        filename = f"radb-{asnum}.html"
        fpath = os.path.join(folder_path, filename)

        # save raw HTML
        Path(fpath).write_bytes(response.body)
        self.log(f"Saved file {fpath}")

        # now also yield structured info so Scrapy can export it
        # you can extract more fields here if you need
        yield {
            "asn": asnum,
            "url": response.url,
            "saved_path": fpath,
        }
        
    
