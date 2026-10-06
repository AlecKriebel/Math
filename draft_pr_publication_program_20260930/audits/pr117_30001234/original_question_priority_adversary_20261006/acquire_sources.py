#!/usr/bin/env python3
"""Read-only, bounded acquisition of public primary sources and citation metadata."""
import datetime, hashlib, json, os, pathlib, subprocess, sys, time, urllib.request

D = pathlib.Path(__file__).resolve().parent
PRIVATE = D / 'private_sources'
PRIVATE.mkdir(exist_ok=True)
J = {'schema': 'pr117-original-question-primary-acquisition/v1', 'pid': os.getpid(),
     'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'events': [], 'new_proof_turns': 0, 'read_only_external': True}

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def ck(b, msg):
    if not b:
        raise ValueError(msg)

def emit():
    (D / 'ACQUISITION_PROCESS_JOURNAL.json').write_text(json.dumps(J, indent=2, sort_keys=True)+'\n')

def pin(path):
    body = path.read_bytes()
    return {'relative_path': str(path.relative_to(D)), 'bytes': len(body),
            'sha256': hashlib.sha256(body).hexdigest()}

local = D.parent / 'primary_source_scope_adversary_20261006' / 'private_sources'
sources = [
 ('owr21_2009.pdf', 'https://ems.press/content/serial-article-files/46224', 'ee3b3e545a5d613abbb63e51a4d4c15224db017ae5d54887803b824ae076450b'),
 ('shibuta_takagi_0810.1278v3.pdf', 'https://arxiv.org/pdf/0810.1278v3', 'abfd9f905c80f82a9253874f82fd8161f4740bb3270d3fd740b6a79fa2cdbfa7'),
 ('laclair_2304.13299v2.pdf', 'https://arxiv.org/pdf/2304.13299v2', None),
]
for name, url, expected in sources:
    origin=local/name
    body=origin.read_bytes()
    ck(body.startswith(b'%PDF'), 'Local source is not PDF: '+name)
    actual=hashlib.sha256(body).hexdigest()
    if expected:
        ck(actual == expected, 'Local source digest mismatch: '+name)
    dest=PRIVATE/name
    if dest.exists():
        ck(dest.read_bytes() == body, 'Existing source bytes conflict: '+name)
    else:
        dest.write_bytes(body)
    J['events'].append({'utc': stamp(), 'action': 'authenticated_local_read_only_copy',
                        'origin': str(origin), 'public_url': url, **pin(dest)})
    emit()

requests=[
 ('shibuta_takagi_0810.1278v1.pdf', 'https://arxiv.org/pdf/0810.1278v1', 'pdf'),
 ('shibuta_takagi_0810.1278v2.pdf', 'https://arxiv.org/pdf/0810.1278v2', 'pdf'),
 ('arxiv_0810.1278.html', 'https://arxiv.org/abs/0810.1278', 'html'),
 ('takagi_papers.html', 'https://www.ms.u-tokyo.ac.jp/~stakagi/academic/papers.htm', 'html'),
 ('openalex_shibuta_takagi.json', 'https://api.openalex.org/works/doi:10.1007/s00229-009-0270-7', 'json'),
 ('semantic_scholar_shibuta_takagi.json', 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/s00229-009-0270-7?fields=title,year,publicationDate,citationCount,citations.title,citations.year,citations.externalIds,citations.url,citations.openAccessPdf', 'json'),
]
for name,url,kind in requests:
    ev={'utc':stamp(),'action':'public_GET','url':url,'destination':'private_sources/'+name,'kind':kind}
    J['events'].append(ev); emit()
    try:
        req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (research priority audit)'} )
        with urllib.request.urlopen(req, timeout=40) as response:
            body=response.read(10_000_001)
            ev['http_status']=response.status; ev['final_url']=response.url
        ck(len(body)<=10_000_000, 'Public body exceeds bounded limit')
        if kind=='pdf': ck(body.startswith(b'%PDF'), 'Not an actual PDF body')
        if kind=='json': json.loads(body)
        dest=PRIVATE/name
        if dest.exists(): ck(dest.read_bytes()==body, 'Existing source differs')
        else: dest.write_bytes(body)
        ev.update(pin(dest)); ev['status']='retrieved_and_pinned'
    except Exception as e:
        ev['status']='unavailable'; ev['error_type']=type(e).__name__; ev['error']=str(e)
    emit()

for path in sorted(PRIVATE.glob('*.pdf')):
    out=path.with_suffix('.txt')
    argv=['/opt/homebrew/bin/pdftotext','-layout',str(path),str(out)]
    ev={'utc':stamp(),'action':'pdftotext','argv':argv}
    J['events'].append(ev); emit()
    res=subprocess.run(argv, capture_output=True, timeout=40, env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'})
    ev['returncode']=res.returncode; ev['stderr_bytes']=len(res.stderr)
    ck(res.returncode==0 and len(res.stderr)==0, 'PDF extraction failed')
    ev.update(pin(out)); ev['status']='extracted_private_text'; emit()

J['finished_utc']=stamp(); J['status']='complete_with_explicit_access_limits'; emit()
print(json.dumps({'pid':os.getpid(),'status':J['status'],'events':len(J['events']),
                  'successful_sources':[e['destination'] for e in J['events'] if e.get('status')=='retrieved_and_pinned'],
                  'unavailable':[{'url':e['url'],'error':e.get('error')} for e in J['events'] if e.get('status')=='unavailable']}, sort_keys=True))
