"""Authenticate complete retained evidence and first seals, without executing sources."""
from pathlib import Path
import hashlib,json,stat,datetime
A=Path(__file__).resolve().parent
def require(c,m):
 if not c:raise RuntimeError(m)
def digest(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
def rows(j):
 for k in ['inventory','all_retained_files_except_this_seal','manifest_before_seal_creation']:
  if k in j:return j[k]
 raise RuntimeError('Unsupported manifest schema')
def check_rows(base,items):
 seen=set()
 for r in items:
  n=r['path'];p=Path(n);require(not p.is_absolute() and '..' not in p.parts and n not in seen,'Unsafe or repeated inventory path');seen.add(n);f=base/p
  require(f.is_file() and not f.is_symlink(),'Missing or symlink evidence '+n);d=digest(f)
  require(d['bytes']==r.get('bytes',r.get('size')) and d['sha256']==r['sha256'] and d['mode']=='0444','Evidence identity/mode differs '+n)
 return seen
def auth(family,final,expected_final,first,expected_first,allow,key):
 b=A/family;fp=b/final;require(digest(fp)['sha256']==expected_final,'Final external seal differs');j=json.loads(fp.read_text());seen=check_rows(b,rows(j));require(final not in seen,'Recursive selfhash prohibited');seen.add(final)
 actual={p.relative_to(b).as_posix() for p in b.rglob('*') if p.is_file()};require(actual==seen,'Missing/extra retained evidence in '+family);require(digest(fp)['mode']=='0444','Writable final seal')
 f=b/first;require(digest(f)['sha256']==expected_first and digest(f)['mode']=='0444','First seal differs');first_seen=check_rows(b,rows(json.loads(f.read_text())));require(first_seen<=seen,'First seal no longer retained')
 al=json.loads((b/allow).read_text())[key];require(len(al)==len(set(al)) and set(al)<=seen,'Unsafe or incomplete explicit allowlist')
 require(all(Path(n).parts[0]=='public' for n in al),'Private material in public selection')
 return {'family':family,'final_seal':dict(path=final,**digest(fp)),'first_seal':dict(path=first,**digest(f)),'all_retained_files_authenticated':len(seen),'first_retained_files_authenticated':len(first_seen)+1,'public_allowlist':al,'private_files_excluded_from_publication':len(seen)-len(al),'public_companions_do_not_contain_private_primary_bodies':True,'retained_files':[{ 'path':n,**digest(b/n)} for n in sorted(seen)]}
if __name__=='__main__':
 out=A/'ROOT_FINISHED_PRIORITY_EVIDENCE_AUTHENTICATION.json';require(not out.exists(),'Preserve sealed prior authentication; use a new additive receipt')
 r=[auth('priority_source_lineage','public/FINAL_SEAL.json','9e10950ef4a62cfd5571dbe99fd7a654139619369515cfe85992238d43c4a594','public/FIRST_SEAL.json','655a17cfec66d36384307fea485afa352967ede6e5439a61ebe3ed2581caf211','public/PUBLIC_ALLOWLIST.json','public_files'),auth('priority_strategic_recent','public/FINAL_SEAL_v2.json','8e829c58057d90229029e953cf61f2531af30497757ce394be21ecd60c871f01','public/FIRST_SEAL.json','3eebd5482c44c9f8577aaf544babd168a943a91389c4310ad0e509926ffb0827','public/PUBLIC_ALLOWLIST_v2.json','allowed_files_exactly')]
 j={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'TWO_FINISHED_PRIORITY_FAMILIES_ALL_RETAINED_BYTES_MODES_MEMBERSHIP_FIRST_SEALS_AUTHENTICATED','families':r,'whole_priority_adjudication_complete':False,'fresh_implication_and_configuration_final_evidence_pending':True,'mandatory_strategic_report_companion':'priority_strategic_recent/public/CORRECTION_01.md','privacy_semantics':'Full inventories verified locally; private primary bodies/headers/extracts remain excluded, and a public metadata hash is not a publicly supplied body.'};out.write_text(json.dumps(j,indent=2)+'\n');out.chmod(0o444)
 print(json.dumps({'status':j['status'],'counts':[{'family':x['family'],'retained':x['all_retained_files_authenticated'],'public':len(x['public_allowlist'])} for x in r]}))
