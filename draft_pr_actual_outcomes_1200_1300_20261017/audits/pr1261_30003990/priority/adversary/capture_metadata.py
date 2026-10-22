"""Capture primary metadata pages already inspected through the web tool."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
from retrieve_web_bodies import fetch

URLS={
 'arxiv_1905_metadata':'https://arxiv.org/abs/1905.08142',
 'arxiv_2001_metadata':'https://arxiv.org/abs/2001.11289',
 'arxiv_1804_metadata':'https://arxiv.org/abs/1804.05524',
 'arxiv_2605_metadata':'https://arxiv.org/abs/2605.31496',
 'ems_owr_metadata':'https://ems.press/journals/owr/articles/16633',
 'siam_1603_metadata':'https://epubs.siam.org/doi/10.1137/16M1065264',
 'springer_1905_metadata':'https://link.springer.com/article/10.1007/s10107-020-01468-3',
 'springer_2001_metadata':'https://link.springer.com/article/10.1007/s10107-020-01586-y',
 'springer_overview_metadata':'https://link.springer.com/chapter/10.1007/978-981-95-1446-5_8',
 'cwi_worstcase_metadata':'https://ir.cwi.nl/pub/28994/',
}
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=8) as pool:records=list(pool.map(fetch,URLS.items()))
 Path(__file__).with_name('METADATA_RECEIPT.json').write_text(json.dumps(records,indent=2)+'\n')
 print(json.dumps(records,indent=2))
