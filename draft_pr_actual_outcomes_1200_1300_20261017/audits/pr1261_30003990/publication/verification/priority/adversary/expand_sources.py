"""Additional read-only public-primary requests for this audit."""
from pathlib import Path
import json
from concurrent.futures import ThreadPoolExecutor
from retrieve_sources import get

EXTRA = {
 'deklerk_laurent_2018_annealing': 'https://ir.cwi.nl/pub/28065/28065.pdf',
 'deklerk_laurent_1804_v2': 'https://arxiv.org/pdf/1804.05524v2',
 'totik_survey_2012_final': 'https://www.math.u-szeged.hu/pot/4madridpaper.pdf',
 'mastroianni_totik_2010': 'https://link.springer.com/content/pdf/10.1007/s00365-099-9047-1.pdf',
 'ivanov_totik_1990': 'https://link.springer.com/content/pdf/10.1007/BF01891406.pdf',
}
if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=5) as pool:
        records=list(pool.map(get,EXTRA.items()))
    Path(__file__).with_name('EXPANSION_RECEIPT.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))
