"""Retrieve primary public sources. Downloaded bytes remain foreign evidence."""
import datetime, hashlib, json, pathlib, sys, urllib.error, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
FOREIGN=ROOT/'foreign_primary'
FOREIGN.mkdir(exist_ok=True)
sources=[
 ('bloom653.html','https://www.erdosproblems.com/653'),
 ('erdos_fishburn_attempt.pdf','https://users.renyi.hu/~p_erdos/1997-06.pdf'),
 ('erdos_favourites_attempt.pdf','https://users.renyi.hu/~p_erdos/1997-21.pdf'),
 ('szeged_ef_index.html','https://www.math.u-szeged.hu/~czedli/m/grafset/erdos-fishburn.html'),
 ('csizmadia_author_attempt.html','https://www.hofstra.edu/faculty/fac_profiles.cfm?id=1245&t=/Academics/Colleges/HCLAS/MATH/'),
 ('googlebooks_title_search.html','https://books.google.com/books?q=%22Intuitive+Geometry%22+%22Csizmadia%22')]
inventory=[]
for filename,url in sources:
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    row={'filename':filename,'requested_url':url,'started_utc':started,'ownership':'foreign_primary','proof_input':False}
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(request,timeout=30) as response:
            data=response.read()
            row.update(status=response.status,final_url=response.url,headers=dict(response.headers),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        (FOREIGN/filename).write_bytes(data)
        print(filename,row['status'],len(data),row['final_url'])
    except Exception as exc:
        row['error']=repr(exc)
        print(filename,repr(exc),file=sys.stderr)
    row['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    inventory.append(row)
(ROOT/'primary_fetch_inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
