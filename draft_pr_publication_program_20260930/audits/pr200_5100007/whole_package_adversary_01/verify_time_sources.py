from pathlib import Path
import urllib.request,json,datetime,hashlib
root=Path(__file__).resolve().parent
sources=[('datacite','https://api.datacite.org/dois/10.5281/zenodo.23093258'),('zenodo','https://zenodo.org/api/records/23093258'),('github','https://api.github.com/repos/AlecKriebel/Math/pulls/200')]
results=[]
for kind,url in sources:
    row={'kind':kind,'url':url,'checked_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'Independent-Publication-Audit/1.0','Accept':'application/json'})
        with urllib.request.urlopen(request,timeout=20) as r:
            data=r.read(1024*1024+1)
            if len(data)>1024*1024:raise RuntimeError('small-response byte ceiling exceeded')
            row['http_status']=r.status
        obj=json.loads(data);row['response_sha256']=hashlib.sha256(data).hexdigest()
        if kind=='datacite':
            a=obj['data']['attributes'];row['observed']={k:a.get(k) for k in ['doi','created','registered','published','state','titles','url','version']}
        elif kind=='zenodo':
            row['observed']={k:obj.get(k) for k in ['id','created','updated','revision_id','doi']}
            row['observed']['metadata']={k:obj['metadata'].get(k) for k in ['title','publication_date','version','creators']}
            row['observed']['files']=[{'key':f.get('key'),'size':f.get('size'),'checksum':f.get('checksum')} for f in obj.get('files',[])]
        else:
            row['observed']={k:obj.get(k) for k in ['number','created_at','html_url','state']}
            row['observed']['head_sha_current']=obj.get('head',{}).get('sha')
            row['observation_limit']='Current head is not a witness of original submitted head; no Git or ref operation performed.'
        row['success']=True
    except Exception as e:row.update(success=False,error=str(e))
    results.append(row)
(root/'TIME_SOURCES.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
