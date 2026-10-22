"""Caller-pinned offline complete closure/fidelity verifier.
Usage: python3 -I -S -B verify_readonly.py --manifest-sha256 SHA --verifier-sha256 SHA
Only standard-library reads; no imports of evidence code, writes, subprocesses or network.
Does not certify mathematical proofs, freshness after closure or production authority.
"""
import argparse,gzip,hashlib,json,os,pathlib,re,stat
O=pathlib.Path(__file__).resolve().parent;B=O.parents[1]
def need(x,msg):
 if not x:raise ValueError(msg)
def sh(b):return hashlib.sha256(b).hexdigest()
def pairs(xs):
 d={}
 for k,v in xs:
  need(k not in d,'duplicate JSON key');d[k]=v
 return d
def ld(p):return json.loads(p.read_bytes(),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def gz(p):return json.loads(gzip.decompress(p.read_bytes()),object_pairs_hook=pairs)
def can(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def equal(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(equal(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(equal(c,d)for c,d in zip(a,b))
 return a==b
def inv(root,exclude=None):
 out={}
 for p in [root,*sorted(root.rglob('*'))]:
  n='.'if p==root else p.relative_to(root).as_posix()
  if n==exclude:continue
  s=p.lstat();need(stat.S_ISDIR(s.st_mode)or stat.S_ISREG(s.st_mode),'unsupported namespace')
  v={'kind':'file'if stat.S_ISREG(s.st_mode)else'directory','mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink}
  if v['kind']=='file':v.update(bytes=s.st_size,sha256=sh(p.read_bytes()))
  out[n]=v
 return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--verifier-sha256',required=True);a=ap.parse_args()
 need(all(re.fullmatch('[a-f0-9]{64}',v)for v in [a.manifest_sha256,a.verifier_sha256]),'external hash format')
 need(sh(pathlib.Path(__file__).read_bytes())==a.verifier_sha256,'external verifier SHA mismatch')
 mp=O/'CLOSED_MANIFEST.json';need(sh(mp.read_bytes())==a.manifest_sha256,'external manifest SHA mismatch');m=ld(mp)
 need(m['self_excluded_exact']=='CLOSED_MANIFEST.json'and m['reserved_before_inventory']is True,'self contract')
 need(m['execution_ready']is False and m['service_writes']==m['Git_index_writes']==m['new_publications']==0,'scope flags')
 need(inv(O,'CLOSED_MANIFEST.json')==m['entries'],'own complete closure drift')
 need(stat.S_IMODE(mp.stat().st_mode)==0o444 and mp.stat().st_nlink==1,'self-file mode/link contract')
 for name,expected in gz(O/'SOURCE_PACKET_BASELINES.json.gz').items():need(inv(pathlib.Path(name))==expected,'old complete source packet drift '+name)
 for v in ld(O/'INPUT_BASELINE.json'):
  p=pathlib.Path(v['path']);s=p.lstat();need(stat.S_ISREG(s.st_mode),'input regular')
  need({'path':str(p),'bytes':s.st_size,'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink,'sha256':sh(p.read_bytes())}==v,'root input drift')
 target=B/'PRIOR_SOURCE_ELEVEN_ROOT_ADOPTED_LITERAL_ROWS.json';need(sh(target.read_bytes())=='6b04efe97c275ff255299d1e827292702dd0b6bec8cb80b9a1b7b414bf1f6bf1','root eleven pin')
 raw=ld(target);rows=raw['rows'];prs=[932,967,1036,1063,1170,1182,1183,1184,1189,1190,1224]
 need([x['pr']for x in rows]==prs and raw['schema']==['Original Problem','Solution Chat URL','DOI','Notes'],'eleven schema/order')
 need(ld(O/'REVIEWED_LITERAL_ROWS.json')==rows,'literal bytes projection')
 for x in rows:need(len(x['values'])==4 and all(type(y)is str for y in x['values'])and x['values'][1:3]==['',''],'four exact strings/blank BC')
 need(ld(B/'ROOT_NINE_PRIOR_SOURCE_ACCOUNTING_LITERAL_ADOPTION.json')['exact_proposed_rows']==[x for x in rows if x['pr']not in[1189,1224]],'nine projection')
 need(ld(B/'audits/unadopted_prior_reviews_reconciliation01/FREUD_SOURCE_ONLY_FOUR_CELLS.json')['literal_cells']==rows[8]['values'],'Freud projection')
 need(ld(B/'audits/pr1224_2302/ROOT_SOURCE_ONLY_LITERAL_ROW_AND_FRESH_INDEPENDENT_REVIEW_ADOPTION.json')['literal_row']==rows[10]['values'],'Tao projection')
 obs=[gz(O/(n+'_observation.json.gz'))for n in ['initial','closing']]
 for z in obs:
  need(equal(z['metadata_first'],z['metadata_last'])and equal(z['value_raw'],z['formula_raw']),'raw typed observation drift')
  mm=z['metadata_first'];need(mm['spreadsheetId']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','workbook')
  t=[s['properties']for s in mm['sheets']if s['properties']['sheetId']==1254632077];need(len(t)==1 and t[0]['title']=='Math Puzzles'and t[0]['gridProperties']=={'rowCount':1178,'columnCount':43,'frozenRowCount':1},'numeric extent')
  vr=z['value_raw']['valueRanges'];need(len(vr)==1,'range count');rr=vr[0]['valueRange'];need(rr['range']=="'Math Puzzles'!A1:AQ1178"and len(rr['values'])==239 and rr['values'][0]==raw['schema'],'full range/header')
  need(len(z['local'])==250 and len({x['path']for x in z['local']})==250,'all250local')
 for key in ['metadata_first','metadata_last','value_raw','formula_raw','local']:need(equal(obs[0][key],obs[1][key]),'initial closing full evidence drift')
 C={('ledger',str(i)):r for i,r in enumerate(obs[0]['value_raw']['valueRanges'][0]['valueRange']['values'],1)}
 C.update({('local',pathlib.Path(v['path']).name):v['value']for v in obs[0]['local']})
 passes=[];R=B/'audits/pr1330_30003185/root_ledger_preflight01/private'
 for k in [0,1]:
  rec=[];files=sorted(R.glob('account_pass'+str(k)+'_page*.json.gz'),key=lambda p:int(re.search('page([0-9]+)',p.name)[1]));need(len(files)==10 and gz(files[-1])==[],'owned terminal page')
  for p in files:rec+=gz(p)
  need(len(rec)==204 and len({str(x['id'])for x in rec})==204,'dated204owned');passes.append({str(x['id']):x for x in rec})
 need(equal(*passes),'dated owned full typed two-pass drift')
 for k,v in passes[0].items():C['dated_owned',k]=v
 f=ld(B/'audits/existing_publication_remaining_rows_inventory01/FROZEN_PROPOSALS.json');need(len(f['items'])==34,'frozen34')
 for v in f['items']:C['frozen34',str(v['pr'])]=v['row']
 decisions=ld(O/'INDIVIDUAL_CARRIER_DECISIONS.json');need(len(decisions)==81,'81 scoped carrier decisions')
 for v in decisions:need(sh(can(C[v['kind'],v['key']]))==v['complete_carrier_sha256']and v['status']=='SCOPED_DISTINCT'and v['action_ready']is False and bool(v['reason'])and bool(v['peer_scientific_statement']),'individual full carrier binding')
 needles=ld(O/'CARRIER_LEADS.json')['patterns'];leads={(int(pr),kind,key)for pr,pat in needles.items()for(kind,key),v in C.items()if re.search(pat,json.dumps(v,ensure_ascii=False,sort_keys=True),re.I)}
 need(leads=={(v['pr'],v['kind'],v['key'])for v in decisions},'complete broad matching lead coverage')
 need(len(ld(O/'PAIRWISE_ELEVEN_DISTINCTIONS.json'))==55 and len(ld(O/'FROZEN34_CROSS_BATCH_DISTINCTIONS.json'))==34,'pair counts')
 source=ld(O/'FRESH_SOURCE_GETS.json');need(len(source)==11 and {v['pr']for v in source}==set(prs)and all(v.get('hash_matches')is True and v.get('status')==200 for v in source),'source freshness receipts')
 for v in source:need(all(v['sha256']not in json.dumps(z,ensure_ascii=False)for z in C.values()),'exact target source appears in a carrier')
 need(all(v['current_complete_carrier_hash_matches']is True for v in ld(O/'TAO_25_PRIOR_DISTINCTIONS_RECONCILED.json'))and len(ld(O/'TAO_25_PRIOR_DISTINCTIONS_RECONCILED.json'))==25,'older25reconciliation')
 status=ld(O/'FINAL_STATUS.json');need(status['literal_status']=='PASS'and status['execution_ready']is False and status['repair_requests']==[]and status['root_adoption_of_this_whole_review']is False,'final scope')
 need(ld(O/'CONTROLS_RECEIPT.json')['status']=='PASS','finite controls')
 used=sum(p.lstat().st_blocks*512 for p in [O,*O.rglob('*')]);s=os.statvfs(O);free=s.f_bavail*s.f_frsize;need(used<=8*1024*1024 and free>=150*1024*1024,'resource cap/reserve')
 return {'status':'PASS','literal_status':'PASS','own_payloads':sum(v['kind']=='file'for v in m['entries'].values()),'old_packet_entries':sum(len(v)for v in gz(O/'SOURCE_PACKET_BASELINES.json.gz').values()),'rows':11,'carrier_distinctions':81,'dated_owned':204,'local_states':250,'ledger_rows':239,'allocated_bytes':used,'free_bytes':free,'execution_ready':False,'service_writes':0,'Git_index_writes':0,'scope':'offline closure/literal/carrier/source-receipt fidelity; no proof or action certification'}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True))
