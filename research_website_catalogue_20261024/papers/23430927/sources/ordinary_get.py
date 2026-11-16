#!/usr/bin/env python3
"""Fresh ordinary GET custody. No supplied scientific program/code is imported."""
from pathlib import Path
from urllib.parse import urlsplit,urljoin
import datetime,hashlib,http.client,json,sys
ROOT=Path(__file__).resolve().parent
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(x,m):
    if not x:raise RuntimeError(m)
def fetch(url,role,accept="application/json",asset=False):
    require(role and all(c.isalnum() or c in "-_." for c in role),"Unsafe role")
    receipts_path=ROOT/"ALL_TRANSPORT_RECEIPTS.json"
    receipts=json.loads(receipts_path.read_text()) if receipts_path.exists() else []
    redirects=[];current=url
    for hop in range(6):
        parsed=urlsplit(current);require(parsed.scheme=="https" and parsed.hostname=="zenodo.org","Unexpected native transport target")
        path=parsed.path+("?"+parsed.query if parsed.query else "")
        suffix="" if hop==0 else ".redirect-%02d"%hop
        stem=role+".response.body"+suffix
        destination=ROOT/stem
        require(not destination.exists(),"Preserve preexisting attempt; choose a new role")
        headers=[["Host",parsed.netloc],["User-Agent","Python-http.client (source-only custody)"],["Accept",accept]]
        start=utc();connection=http.client.HTTPSConnection(parsed.hostname,parsed.port or 443,timeout=30)
        try:
            connection.putrequest("GET",path,skip_host=True,skip_accept_encoding=True)
            for k,v in headers:connection.putheader(k,v)
            connection.endheaders();response=connection.getresponse();body=response.read()
            status=response.status;reason=response.reason;received=response.getheaders()
            destination.write_bytes(body)
            receipt={"started_UTC":start,"completed_UTC":utc(),"logical_role":role,"redirect_hop":hop,"method":"GET","request_URL":current,"actual_request_headers_in_sent_order":headers,"HTTP_status":status,"HTTP_reason":reason,"response_headers_in_received_order":received,"body_path":str(destination),"bytes":len(body),"SHA256":hashlib.sha256(body).hexdigest(),"error_type":None}
        except Exception as e:
            receipt={"started_UTC":start,"completed_UTC":utc(),"logical_role":role,"redirect_hop":hop,"method":"GET","request_URL":current,"actual_request_headers_in_sent_order":headers,"HTTP_status":None,"error_type":type(e).__name__,"error_message":str(e)}
            receipts.append(receipt);receipts_path.write_text(json.dumps(receipts,indent=2)+"\n");(ROOT/(stem+".transport.json")).write_text(json.dumps(receipt,indent=2)+"\n");raise
        finally:connection.close()
        receipts.append(receipt);receipts_path.write_text(json.dumps(receipts,indent=2)+"\n");(ROOT/(stem+".transport.json")).write_text(json.dumps(receipt,indent=2)+"\n")
        if status in [301,302,303,307,308]:
            locations=[v for k,v in received if k.lower()=="location"];require(len(locations)==1,"Ambiguous native redirect")
            redirects.append({"status":status,"actual_Location":locations[0]});current=urljoin(current,locations[0]);continue
        require(status==200,"Non200 native response retained: "+str(status))
        return body,receipt,redirects
    raise RuntimeError("Too many native redirects, all responses retained")
if __name__=="__main__":
    require(len(sys.argv)==3,"Usage: ordinary_get.py URL role")
    body,receipt,redirects=fetch(sys.argv[1],sys.argv[2])
    print(json.dumps({k:receipt[k] for k in ["HTTP_status","bytes","SHA256","body_path"]}|{"redirects":redirects}))
