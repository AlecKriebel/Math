from retrieve_sources import retrieve, ROOT
import json, concurrent.futures, datetime
ITEMS = [
 ('AM_latest','https://arxiv.org/pdf/1007.2454'),
 ('PP_v5','https://arxiv.org/pdf/1303.3708v5'),
 ('T_technical','https://egres.elte.hu/tr/egres-21-01.pdf'),
 ('HKT_technical','https://egres.elte.hu/tr/egres-15-10.pdf'),
 ('HKT_first','https://egres.elte.hu/tr/egres-15-10_July_2015.pdf'),
 ('MultiArrival2025','https://drops.dagstuhl.de/storage/00lipics/lipics-vol327-stacs2025/LIPIcs.STACS.2025.39/LIPIcs.STACS.2025.39.pdf'),
 ('Hoang_thesis_alt','https://www.research-collection.ethz.ch/bitstream/handle/20.500.11850/572947/1/thesis-hoang.pdf'),
 ('LDP_thesis','https://theses.hal.science/tel-04504876/document'),
 ('FL_author','https://lionellevine.github.io/coEulerian.pdf'),
 ('FL_journal','https://www.ams.org/journals/proc/2016-144-07/S0002-9939-2015-12952-3/S0002-9939-2015-12952-3.pdf'),
 ('HKT_journal','https://www.ams.org/journals/proc/2017-145-08/S0002-9939-2017-13498-3/S0002-9939-2017-13498-3.pdf'),
 ('Devil_latest','https://arxiv.org/pdf/2004.13104'),
 ('LO_latest','https://arxiv.org/pdf/2409.00763'),
]
if __name__ == '__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  rows=list(pool.map(retrieve,ITEMS))
 (ROOT/'SOURCE_RETRIEVAL_ADDITIONAL.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':rows},indent=2)+'\n')
 print(json.dumps([{k:v for k,v in r.items() if k in ('id','http_code','curl_exit','bytes','is_pdf','pdf_pages')} for r in rows]))
