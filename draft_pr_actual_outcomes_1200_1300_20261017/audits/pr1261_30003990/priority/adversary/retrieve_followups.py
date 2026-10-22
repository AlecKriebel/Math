"""Read-only follow-ups; retain failed version requests in earlier receipts."""
from pathlib import Path
import json
from concurrent.futures import ThreadPoolExecutor
from retrieve_sources import get

FOLLOWUPS = {
 'deklerk_laurent_1804_v1': 'https://arxiv.org/pdf/1804.05524v1',
 'mastroianni_totik_2010_corrected': 'https://link.springer.com/content/pdf/10.1007/s00365-009-9047-1.pdf',
 'kroo_2016': 'https://link.springer.com/content/pdf/10.1007/s10474-016-0593-2.pdf',
}
if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=3) as pool:
        records=list(pool.map(get,FOLLOWUPS.items()))
    Path(__file__).with_name('FOLLOWUP_RECEIPT.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))
