#!/usr/bin/env python3
"""Explicit ordinary public primary GET, inert default.
Prepared after full reading of original source/ordinary_get.py; not executed.
No auth/cookies/proxy/retry/bypass/project or scientific imports.
"""
from pathlib import Path
from urllib.parse import urlsplit,urljoin
import datetime
import hashlib
import http.client
import json
import ssl
import sys

A=Path(__file__).resolve().parent

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def digest(b):
    return hashlib.sha256(b).hexdigest()

def main():
    if len(sys.argv)!=4 or sys.argv[1]!='--acquire':
        print('Inert default; --acquire fresh-label cited-URL required.')
        return
    label,url=sys.argv[2:]
    if not label.replace('-','').replace('_','').isalnum():
        raise ValueError('fresh safe label required')
    D=A/'primary';D.mkdir(exist_ok=True)
    for hop in range(6):
        stem=D/(label+'-hop'+str(hop))
        bodypath,requestpath,receiptpath=stem.with_suffix('.body'),stem.with_suffix('.request.bin'),stem.with_suffix('.transport.json')
        if any(p.exists() for p in [bodypath,requestpath,receiptpath]):
            raise ValueError('refuse any overwrite')
        u=urlsplit(url)
        if u.scheme not in ('http','https') or not u.hostname or u.username or u.password:
            raise ValueError('ordinary public HTTP(S) URL required')
        target=(u.path or '/')+('?' + u.query if u.query else '')
        headers=[['Host',u.netloc],['User-Agent','Python-http.client/3 primary-source-reading'],['Accept','*/*']]
        r={'started_UTC':utc(),'method':'GET','URL':url,'actual_request_headers_in_sent_order':headers,'redirect_hop':hop,
           'authentication_cookies_proxy_retry_or_bypass':False,'HTTP_status':None,'HTTP_reason':None,'HTTP_version':None,
           'response_headers_in_received_order':None,'response_obtained':False,'body_complete':False,'error':None}
        sent=[];chunks=[];conn=None;location=None
        try:
            conn=(http.client.HTTPSConnection(u.hostname,u.port or 443,timeout=30,context=ssl.create_default_context())
                  if u.scheme=='https' else http.client.HTTPConnection(u.hostname,u.port or 80,timeout=30))
            original_send=conn.send
            def capture(data):
                if not isinstance(data,bytes):raise TypeError('unexpected nonbyte request buffer')
                sent.append(data)
                return original_send(data)
            conn.send=capture
            conn.putrequest('GET',target,skip_host=True,skip_accept_encoding=True)
            for k,v in headers:conn.putheader(k,v)
            conn.endheaders();response=conn.getresponse()
            r.update({'HTTP_status':response.status,'HTTP_reason':response.reason,'HTTP_version':response.version,
                      'response_headers_in_received_order':[list(pair) for pair in response.getheaders()],'response_obtained':True})
            location=response.getheader('Location')
            while True:
                chunk=response.read(65536)
                if not chunk:break
                chunks.append(chunk)
            if response.length not in (None,0):
                raise http.client.IncompleteRead(b'',response.length)
            r['body_complete']=True
        except Exception as e:
            if isinstance(e,http.client.IncompleteRead) and e.partial:chunks.append(e.partial)
            r['error']={'type':type(e).__name__,'message':str(e)}
        finally:
            if conn:conn.close()
        body,request=b''.join(chunks),b''.join(sent)
        # Persist the complete actually received body, including error/redirect
        # bodies or any partial failure bytes, before any bounded next request.
        bodypath.write_bytes(body);requestpath.write_bytes(request)
        r.update({'body':str(bodypath.relative_to(A)),'bytes':len(body),'SHA256':digest(body),
                  'request':str(requestpath.relative_to(A)),'request_bytes':len(request),'request_SHA256':digest(request),
                  'completed_UTC':utc()})
        receiptpath.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'transport':str(receiptpath.relative_to(A)),**r},ensure_ascii=False))
        if r['body_complete'] and r['HTTP_status'] in (301,302,303,307,308) and location:
            url=urljoin(url,location)
            continue
        return
    raise RuntimeError('six-hop finite redirect bound reached; all actual bytes retained')

if __name__=='__main__':
    main()
