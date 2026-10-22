#!/usr/bin/env python3
"""Offline identity/date controls. No writes; run from a copied review to reacquire."""
import base64,datetime,email.utils,hashlib,json,pathlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
P=ROOT/'private'
checks=[]
def require(label,condition,detail=None):
 checks.append({'check':label,'passed':bool(condition),'detail':detail})
 if not condition:raise ValueError(label)
def read_receipt(key):return json.loads((ROOT/(key+'.receipt.json')).read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
def header(row,key):
 return next((v for k,v in row['headers'].items() if k.lower()==key.lower()),None)
for key in ('current_math','archive_math','notebook_v48','sipacheva_v1','arxiv_history','official_repository','wayback_cdx','wayback_timemap'):
 row=read_receipt(key);body=(ROOT/row['body']).read_bytes()
 require(key+' successful exact body',row['status']==200 and row['bytes']==len(body) and row['sha256']==digest(body),{'bytes':len(body),'sha256':digest(body),'url':row['url']})
a=(P/'archive_math.body').read_bytes();c=(P/'current_math.body').read_bytes()
require('actual archive/current byte equality',a==c,{'bytes':len(a),'sha256':digest(a)})
require('actual body is PDF',a.startswith(b'%PDF-'))
pr=json.loads((P/'pr_info.json').read_text())['structuredContent']
require('original PR exact head',pr['head_sha']=='b356dec5cb01e5f536b9cfeece56ad08844c03cb')
require('closed and unmerged',pr['state']=='closed' and pr['merged'] is False)
created=datetime.datetime.fromisoformat(pr['created_at'].replace('Z','+00:00'))
ar=read_receipt('archive_math'); memento=email.utils.parsedate_to_datetime(header(ar,'memento-datetime'))
require('archive memento before PR',memento<created,{'memento_utc':memento.isoformat(),'pr_created_utc':created.isoformat(),'elapsed_seconds':(created-memento).total_seconds()})
require('raw replay exact final URL no redirect',ar['url']==ar['final_url'])
require('archive provenance headers present',bool(header(ar,'x-archive-src')) and bool(header(ar,'x-archive-orig-date')))
cdx=json.loads((P/'wayback_cdx.body').read_text()); cols=cdx[0]; rows=[dict(zip(cols,r)) for r in cdx[1:]]
s1=base64.b32encode(hashlib.sha1(a).digest()).decode()
exact=[r for r in rows if r['timestamp']=='20261002014549' and r['original']==read_receipt('current_math')['url']]
require('CDX exact original/time/status/type/digest',any(r['digest']==s1 and r['statuscode']=='200' and r['mimetype']=='application/pdf' for r in exact),{'actual_sha1_base32':s1,'matching_rows':exact})
tm=(P/'wayback_timemap.body').read_text()
require('timemap consistent original and memento',read_receipt('current_math')['url'] in tm and '20261002014549' in tm and 'Fri, 02 Oct 2026 01:45:49 GMT' in tm)
def page(key,index):
 r=subprocess.run(['pdftotext','-layout',str(P/(key+'.body')),'-'],check=True,capture_output=True,text=True)
 return r.stdout.split('\f')[index-1]
p60=page('archive_math',60)
require('re-extracted full section at printed p60',all(x in p60 for x in ('3.44','21.107','ultrafilter','dense subsets','pairwise disjoint','max','parity','no selectivity')))
require('archive/current p60 extraction equal',p60==page('current_math',60))
p193=page('notebook_v48',193)
require('exact countable target located at p193','21.107.' in p193 and 'countable group G' in p193 and 'countably' in p193)
p97=page('notebook_v48',97)
require('predecessor p97 distinct scope','15.80.' in p97 and 'box topology' in p97 and 'finite set of elements of' in p97)
p25=page('sipacheva_v1',25)
require('old Mathias/free Boolean linear identity','Mathias topology' in p25 and 'Boolean linear' in p25 and 'subgroups generated' in p25)
snapshot=json.loads((ROOT.parent.parent/'SOURCE_SNAPSHOT.json').read_text())
original=ROOT.parent.parent/'original'; integrity=[]
for row in snapshot['files']:
 body=(original/row['path']).read_bytes(); integrity.append(len(body)==row['bytes'] and digest(body)==row['sha256'])
require('all 26 original scientific files unchanged',len(integrity)==26 and all(integrity))
print(json.dumps({'schema_version':1,'status':'PASS','checks':checks,'interpretation':'Content identity and archive chronology controls; not proof mechanization, ultimate firstness, or referee approval.'},indent=2))
