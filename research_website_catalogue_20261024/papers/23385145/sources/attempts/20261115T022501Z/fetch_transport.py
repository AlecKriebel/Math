"""Whole public-source custody transport; never imports or runs source code."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256, md5
import json
import urllib.request
import urllib.error

HERE = Path(__file__).resolve().parent


def stamp():
    return datetime.now(timezone.utc).isoformat()


class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.hops = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.hops.append({"from_url":req.full_url,"HTTP_status":code,
                          "reason":msg,"headers_in_received_order":list(headers.raw_items()),
                          "to_url":newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, relative, request_headers=None):
    path = HERE/relative
    receipt = HERE/(relative.replace('/', '__')+'.transport.json')
    if path.exists() or receipt.exists():
        raise FileExistsError(str(path))
    path.parent.mkdir(parents=True,exist_ok=True)
    redirect = Redirects()
    opener = urllib.request.build_opener(redirect)
    request_headers = request_headers or {"User-Agent":"Mozilla/5.0", "Accept":"*/*"}
    req = urllib.request.Request(url,headers=request_headers)
    rec={"requested_url":url,"started_UTC":stamp(),"method":"GET",
         "request_headers":list(request_headers.items()),"path":str(path)}
    try:
        response=opener.open(req,timeout=60)
    except urllib.error.HTTPError as error:
        response=error
    except Exception as error:
        rec.update(completed_UTC=stamp(),transport_error=repr(error),redirect_hops=redirect.hops)
        receipt.write_text(json.dumps(rec,indent=2)+'\n')
        raise
    h,m=sha256(),md5();size=0
    with response, path.open('xb') as out:
        rec.update(HTTP_status=response.status,reason=response.reason,final_url=response.geturl(),
                   headers_in_received_order=list(response.headers.raw_items()))
        while True:
            part=response.read(1024*1024)
            if not part:break
            out.write(part);h.update(part);m.update(part);size+=len(part)
    rec.update(completed_UTC=stamp(),bytes=size,SHA256=h.hexdigest(),MD5=m.hexdigest(),
               redirect_hops=redirect.hops)
    receipt.write_text(json.dumps(rec,indent=2)+'\n')
    return rec


if __name__=='__main__':
    result=fetch('https://zenodo.org/api/records/23385145','record.raw.json')
    if result['HTTP_status']!=200:
        raise RuntimeError('Non-200 native record response retained')
    obj=json.loads(Path(result['path']).read_bytes())
    print(json.dumps({"record_transport":result,"id":obj['id'],
      "version":obj['metadata'].get('version'),"publication_date":obj['metadata'].get('publication_date'),
      "created":obj.get('created'),"updated":obj.get('updated'),"links":obj.get('links'),
      "files":obj.get('files')},indent=2))
