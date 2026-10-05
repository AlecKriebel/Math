import datetime, hashlib, json, pathlib
root=pathlib.Path(__file__).resolve().parent
rows=[]
specs=[
 ('hs1993','https://www.nber.org/system/files/working_papers/t0141/t0141.pdf','NBER Technical Working Paper 141, September 1993, 56 PDF pages, printed p26/PDF p28','download_hs1993'),
 ('lenzen2004','https://franklenzen.de/pdf/lenzen_scherzer_eccomas2004.pdf','ECCOMAS 2004, author-hosted proceedings paper, 21 PDF pages, Theorem 3.2 on printed/PDF p6','download_lenzen'),
 ('hansen2008','https://users.ssc.wisc.edu/~behansen/papers/et_08.pdf','Econometric Theory 24 (2008) 726–748, published paper, DOI 10.1017/S0266466608080304, 23 PDF pages, Theorem 3 on printed p731/PDF p6','download_hansen2008')]
for stem,url,version,capture in specs:
 p=root/'sources'/(stem+'.pdf'); data=p.read_bytes()
 assert data.startswith(b'%PDF-')
 record=json.loads((root/'process_evidence'/capture/'execution.json').read_text())
 assert record['exit_code']==0
 rows.append(dict(path=str(p.relative_to(root)),requested_url=url,version=version,
                  bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
                  response_headers='sources/'+stem+'.headers',download_capture='process_evidence/'+capture,
                  actual_download_pid=record['actual_child_pid'],retrieval_started_utc=record['started_utc'],
                  retrieval_finished_utc=record['finished_utc']))
result=dict(pinned_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sources=rows)
(root/'SOURCE_PINS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
