#!/usr/bin/env python3
"""Read-only HTTP acquisition: bodies stay under this review's ignored private/."""
import concurrent.futures, datetime, hashlib, json, pathlib, sys, urllib.error, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
SOURCES={
 'current_math':'https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf',
 'archive_math':'https://web.archive.org/web/20261002014549id_/https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf',
 'notebook_v48':'https://arxiv.org/pdf/1401.0300v48',
 'sipacheva_v1':'https://arxiv.org/pdf/1612.04878v1',
 'arxiv_history':'https://arxiv.org/abs/1401.0300',
 'official_repository':'https://kourovkanotebookorg.wordpress.com/repository/',
 'wayback_cdx':'https://web.archive.org/cdx/search/cdx?url=kourovkanotebookorg.wordpress.com%2Fwp-content%2Fuploads%2F2026%2F09%2Fkourovka-mathematics.pdf&output=json&filter=statuscode%3A200&filter=mimetype%3Aapplication%2Fpdf&collapse=digest',
 'wayback_timemap':'https://web.archive.org/web/timemap/link/https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf'
}
def fetch(key):
 url=SOURCES[key]; started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 req=urllib.request.Request(url,headers={'User-Agent':'Independent-source-audit/1.0'})
 row={'key':key,'url':url,'started_utc':started}
 try:
  response=urllib.request.urlopen(req,timeout=45)
 except urllib.error.HTTPError as err:
  response=err
 except Exception as err:
  row.update(error=repr(err),completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()); return row
 with response:
  body=response.read(); path=ROOT/'private'/(key+'.body'); path.write_bytes(body)
  row.update(status=response.status,final_url=response.geturl(),headers=dict(response.headers.items()),bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),body=str(path.relative_to(ROOT)),completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 return row
if __name__=='__main__':
 keys=sys.argv[1:] or list(SOURCES)
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  rows=list(pool.map(fetch,keys))
 for row in rows:
  (ROOT/(row['key']+'.receipt.json')).write_text(json.dumps(row,indent=2)+'\n')
  print(json.dumps(row))
