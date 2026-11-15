"""Sequential ordinary public GET custody, no retry/header/proxy alterations."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256,md5
import json
import urllib.request
import urllib.error
from urllib.parse import urljoin,urlparse

P=Path(__file__).resolve().parent


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):return None


def get(url,name):
    records=[]
    opener=urllib.request.build_opener(NoRedirect())
    for ordinal in range(4):
        target=P/(name if ordinal==0 else name+'.redirect-%02d'%ordinal)
        receipt=Path(str(target)+'.transport.json')
        if target.exists() or receipt.exists():raise FileExistsError(str(target))
        target.parent.mkdir(parents=True,exist_ok=True)
        req=urllib.request.Request(url,method='GET')
        rec={'requested_url':url,'started_UTC':datetime.now(timezone.utc).isoformat(),
             'method':'GET','custom_request_headers':[],'custom_proxy_or_authentication_or_query':False,
             'automatic_redirect_following':False,'body_path':str(target)}
        try:
            try:response=opener.open(req,timeout=45)
            except urllib.error.HTTPError as error:response=error
            with response:
                rec.update(HTTP_status=response.status,reason=response.reason,final_url=response.geturl(),
                  response_headers_in_received_order=list(response.headers.raw_items()))
                sh,mh=sha256(),md5();size=0
                with target.open('xb') as out:
                    while True:
                        part=response.read(1024*1024)
                        if not part:break
                        out.write(part);sh.update(part);mh.update(part);size+=len(part)
            rec.update(body_bytes=size,body_SHA256=sh.hexdigest(),body_MD5=mh.hexdigest(),
                       whole_response_body_captured=True)
        except Exception as error:
            rec.update(transport_exception_type=type(error).__name__,transport_exception=repr(error),
                       whole_response_body_captured=False)
        rec.update(completed_UTC=datetime.now(timezone.utc).isoformat(),
                   request_headers_observed_after_dispatch=list(req.header_items()))
        receipt.write_text(json.dumps(rec,indent=2)+'\n');records.append(rec)
        if rec.get('HTTP_status')==403:
            raise RuntimeError('STOP_NETWORK_403; full response retained; no retry')
        if rec.get('HTTP_status') in (301,302,303,307,308):
            location=next((v for k,v in rec['response_headers_in_received_order'] if k.lower()=='location'),None)
            next_url=urljoin(url,location) if location else None
            if not next_url or urlparse(next_url).scheme!='https' or urlparse(next_url).hostname!='zenodo.org':
                raise RuntimeError('STOP_NETWORK_UNEXPECTED_REDIRECT; response retained')
            url=next_url
            continue
        if rec.get('HTTP_status')!=200:
            raise RuntimeError('STOP_NETWORK_NON200; response retained')
        return records,rec
    raise RuntimeError('STOP_NETWORK_REDIRECT_LIMIT; no retry')


if __name__=='__main__':
    record=json.loads((P/'record.response.body').read_bytes())
    results=[]
    for role in ('latest','versions','files'):
        rows,final=get(record['links'][role],role+'.response.body')
        results.extend(rows)
        obj=json.loads(Path(final['body_path']).read_bytes())
        print(json.dumps({'role':role,'HTTP_status':final['HTTP_status'],'body_bytes':final['body_bytes'],
             'body_SHA256':final['body_SHA256'],'top_type':type(obj).__name__,
             'top_keys':list(obj) if isinstance(obj,dict) else None,
             'id':obj.get('id'),'hits_total':obj.get('hits',{}).get('total'),
             'pagination_links':obj.get('links') if role=='versions' else None},indent=2))
    (P/'metadata.requests.json').write_text(json.dumps(results,indent=2)+'\n')
