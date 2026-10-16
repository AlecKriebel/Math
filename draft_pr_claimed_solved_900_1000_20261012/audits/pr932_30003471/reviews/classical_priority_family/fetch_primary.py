#!/usr/bin/env python3
"""Bounded primary-source retrieval. Raw material remains private."""
import concurrent.futures, datetime, hashlib, json, pathlib, urllib.request
HERE=pathlib.Path(__file__).resolve().parent
PRIVATE=HERE/'private'/'sources'; PRIVATE.mkdir(parents=True,exist_ok=True)
SOURCES=[
 ('ak_v2','https://arxiv.org/pdf/1505.05263v2','pdf'),
 ('owr_ems','https://ems.press/content/serial-article-files/46683?nt=1','pdf'),
 ('owr_mfo','https://publications.mfo.de/bitstream/handle/mfo/3583/OWR_2017_19.pdf?isAllowed=y&sequence=1','pdf'),
 ('winter_metric_v2','https://arxiv.org/pdf/2302.14194v2','pdf'),
 ('winter_infinitesimal_v1','https://arxiv.org/pdf/2609.14645v1','pdf'),
 ('izmestiev_v3','https://arxiv.org/pdf/0704.0349v3','pdf'),
 ('mazzeo_montcouquiol_v3','https://arxiv.org/pdf/0908.2981v3','pdf'),
 ('schlenker_2000','https://link.springer.com/content/pdf/10.1007/PL00009509.pdf','pdf'),
 ('schlafli_souam','https://www.cambridge.org/core/services/aop-cambridge-core/content/view/6F3D10FABB1FF44B905FAE06FB3A747C/S0010437X03100048a.pdf/higher_schlafli_formulas_and_applications.pdf','pdf'),
 ('ak_metadata','https://arxiv.org/abs/1505.05263','html'),
 ('winter_metric_metadata','https://arxiv.org/abs/2302.14194','html'),
 ('winter_infinitesimal_metadata','https://arxiv.org/abs/2609.14645','html'),
 ('izmestiev_metadata','https://arxiv.org/abs/0704.0349','html'),
 ('mazzeo_metadata','https://arxiv.org/abs/0908.2981','html'),
 ('owr_metadata','https://ems.press/journals/owr/articles/15427','html'),
 ('winter_publisher','https://academic.oup.com/imrn/article/2024/9/7721/7480215','html'),
 ('winter_stoker_author','https://martinwintermath.github.io/pdf/publications/Stokers_conjecture.pdf','pdf'),
 ('winter_stoker_blog','https://kaguprasetya.com/wp-content/uploads/2026/09/stoker_s_conjecture-1.pdf','pdf'),
 ('winter_metric_published','https://wrap.warwick.ac.uk/id/eprint/182244/1/WRAP-rigidity-tensegrity-reconstruction-polytopes-under-metric-constraints-Winter-2023.pdf','pdf'),
 ('winter_author_home','https://martinwintermath.github.io/','html'),
 ('stoker_again_blog','https://kaguprasetya.com/2026/09/04/stoker-again/','html'),
 ('wxy_current_metadata','https://arxiv.org/abs/2606.30130','html'),
 ('bi_current_metadata','https://arxiv.org/abs/2608.06320','html'),
 ('winter_note_git_history','https://api.github.com/repos/martinwintermath/martinwintermath.github.io/commits?path=pdf/publications/Stokers_conjecture.pdf&per_page=10','json'),
 ('winter_crossref','https://api.crossref.org/works/10.1093/imrn/rnad298','json'),
 ('winter_stoker_git_766c313','https://raw.githubusercontent.com/martinwintermath/martinwintermath.github.io/766c313bc2187a5eafd5757dca43ffefc6a9ced6/pdf/publications/Stokers_conjecture.pdf','pdf'),
 ('bob_izm_alexandrov','https://www.numdam.org/item/10.5802/aif.2358.pdf','pdf'),
 ('rivin_lindsey_1998','https://www.jstor.org/stable/pdf/2589266.pdf','pdf'),
]
def fetch(item):
 key,url,ext=item
 row=dict(key=key,url=url,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 research-source-audit'}),timeout=45) as r:
   body=r.read(); row.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
  if ext=='pdf' and not body.startswith(b'%PDF'): raise ValueError('Response is not PDF')
  path=PRIVATE/(key+'.'+ext); path.write_bytes(body)
  row.update(bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),private_path=path.relative_to(HERE).as_posix(),ok=True)
 except Exception as e: row.update(ok=False,error=repr(e))
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(fetch,SOURCES))
(HERE/'SOURCE_PINS.json').write_text(json.dumps({'retrieval_only_not_acceptance':True,'sources':rows},indent=2)+'\n')
print(json.dumps(rows,indent=2))
