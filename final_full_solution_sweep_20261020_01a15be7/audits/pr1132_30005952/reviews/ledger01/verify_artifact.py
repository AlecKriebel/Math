#!/usr/bin/env python3
"""Read-only offline custody and publication-identity verifier; no live services."""
import argparse,hashlib,io,json,os,re,stat,zipfile
from pathlib import Path,PurePosixPath
PLAN='6d550ac55930e294fd2e544efb02510dc052b49852efd65d644add7ca56cad81'
HELPER='a213f0f14f19bcf94f4cb4396e2d487e8afa1f21ce8131d6af00c6be581f8900'
HEAD='bab329be46faab9d04bf1664a7183712239f88b2'
PUB={'.gitignore','REPORT.md','CHECK_RESULTS.json','MOCK_RESULTS.json','RESEARCH_LOG.md','mock_guard_tests.py','verify_artifact.py'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':sha(b)}
def pairs(items):
 d={}
 for k,v in items:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def badconst(s):raise ValueError('nonfinite JSON '+s)
def parse(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=badconst)
def safe(n):
 need(type(n) is str and n and '\\' not in n and '\x00' not in n,'bad path');p=PurePosixPath(n);need(not p.is_absolute() and p.as_posix()==n and not {'..','.'}.intersection(p.parts),'unsafe path');return n
def walk(root):
 need(root.is_dir() and not root.is_symlink(),'bad root');files={};dirs=[]
 for b,ds,ns in os.walk(root,followlinks=False):
  for n in ds+ns:
   p=Path(b)/n;need(not p.is_symlink(),'symlink');rel=safe(p.relative_to(root).as_posix())
   if p.is_dir():dirs.append(rel)
   else:need(p.is_file() and stat.S_ISREG(p.stat().st_mode),'special node');files[rel]=pin(p.read_bytes())
 return files,sorted(dirs)
def verify(root,anchor):
 need(re.fullmatch('[0-9a-f]{64}',anchor) is not None,'external digest');mb=(root/'MANIFEST.json').read_bytes();need(sha(mb)==anchor,'manifest anchor');m=parse(mb);need(m['schema']==1 and m['scope']=='pr1132_ledger01','manifest identity');need(set(m['public'])==PUB,'public closure')
 for n,p in m['public'].items():safe(n);need(pin((root/n).read_bytes())==p,'public digest')
 pb=(root/'private/INPUT_MANIFEST.json').read_bytes();need(pin(pb)==m['private_manifest'],'private manifest');pm=parse(pb);f,d=walk(root/'private');expected=dict(pm['files']);expected['INPUT_MANIFEST.json']=pin(pb);need(f==expected and d==pm['directories'],'private closure')
 f,d=walk(root);ef=dict(m['public']);ef['MANIFEST.json']=pin(mb);ef['MANIFEST.sha256']=pin((anchor+'  MANIFEST.json\n').encode());ef.update({'private/'+n:p for n,p in expected.items()});need(f==ef and d==sorted(['private']+['private/'+n for n in pm['directories']]),'whole closed tree')
 P=root/'private'
 def j(n):return parse((P/n).read_bytes())
 need(sha((P/'final_LEDGER_RECONCILIATION_PLAN.json').read_bytes())==PLAN,'reviewed plan');need(sha((P/'final_reconcile_external_ledger.py').read_bytes())==HELPER,'reviewed helper');plan=j('final_LEDGER_RECONCILIATION_PLAN.json');row=plan['proposed_row'];need(len(row)==4 and row[1]=='' and row[2]=='https://doi.org/10.5281/zenodo.23063072' and 'Alper Ferudun' in row[3] and 'not Alec Kriebel authorship' in row[3],'credited row')
 need(sha((P/'provider_baseline.json').read_bytes())==plan['baseline_provider_sha256'],'provider baseline')
 record=j('record.json');last=j('final_record.json');need(record['id']==23063072 and record['state']==last['state']=='done' and record['submitted'] is last['submitted'] is True and record['doi']=='10.5281/zenodo.23063072','published identity');need(record['metadata']==last['metadata'] and record['files']==last['files'],'provider unchanged');meta=record['metadata'];need(meta['title']==plan['existing_publication']['title'] and meta['publication_date']=='2026-09-30' and meta['version']=='1.0' and meta['creators']==[{'name':'Ferudun, Alper','affiliation':'Mercury Software GmbH'}],'source metadata')
 need(j('DOI_RESOLUTION.json')=={'status':200,'final_url':'https://zenodo.org/records/23063072'},'DOI destination')
 planfiles={x['name']:x for x in plan['existing_publication']['files']};need({x['key'] for x in record['files']}==set(planfiles),'public attachment closure')
 for x in record['files']:
  b=(P/safe(x['key'])).read_bytes();need(len(b)==x['size']==planfiles[x['key']]['size'] and x['checksum']=='md5:'+hashlib.md5(b).hexdigest()==planfiles[x['key']]['checksum'] and sha(b)==planfiles[x['key']]['sha256'],'public payload')
 z=zipfile.ZipFile(io.BytesIO((P/'OWR-14298580-008-source.zip').read_bytes()));names=z.namelist();need(len(names)==99==len(set(names))==len(set(n.casefold() for n in names)) and z.testzip() is None,'ZIP count/CRC');payloads={}
 for x in z.infolist():
  safe(x.filename[:-1] if x.is_dir() else x.filename);need(not x.flag_bits&1 and stat.S_IFMT(x.external_attr>>16) in (0,stat.S_IFREG,stat.S_IFDIR),'ZIP node');
  if not x.is_dir():payloads[x.filename]=pin(z.read(x))
 need(len(payloads)==92 and payloads==j('ARCHIVE_RESULTS.json')['payloads'],'ZIP payload inventory');need(z.read('verification_report.md')==(P/'OWR-14298580-008-verification-report.md').read_bytes(),'report agreement');need({'main.tex','references.bib','reproducibility/README.md','reproducibility/verifier/check_certificate.py'}.issubset(payloads),'supporting materials')
 certs=[z.read(n) for n in names if n.endswith('certificate_Sigma_30_47_83.txt')];need(len(certs)==2 and certs[0]==certs[1] and len(certs[0])==21829 and sha(certs[0])=='6d7130dbc0ecf948286ed5d2b7e51a2cdad322da0588a97f3c9ddf7a43f72943','certificate identity');points=[tuple(map(int,s.split())) for s in certs[0].decode().splitlines() if s and not s.startswith('#')];need(len(points)==1707 and points[0]==(0,0) and points[-1]==(109230,0) and all(a[0]<b[0] for a,b in zip(points,points[1:])),'certificate structure')
 sheet=j('sheet.json');need(sheet['values']==j('final_sheet.json')['values'] and len(sheet['values'])==180 and sheet['values'][0]==plan['schema_columns'],'ledger capture');pat=re.compile(r'30005952|14298580.?008|Alfieri|Binns|Floer|geography|Seifert|23063072',re.I);need(not any(pat.search(' '.join(map(str,r))) for r in sheet['values']),'semantic ledger lead');account=j('account.json');need(account['total']==len(account['records'])==197 and account['pages']==8,'complete account');pat=re.compile(r'30005952|14298580.?008|Alfieri|Binns|strong.geography|23063072|30[, ]+47[, ]+83',re.I);need(not any(pat.search(json.dumps(x.get('metadata',{}))) or pat.search(json.dumps(x.get('files',[]))) for x in account['records']),'semantic account lead')
 for n in ['live_pr.json','final_live_pr.json']:
  p=j(n);need(p['number']==1132 and p['head']['sha']==HEAD==plan['head'] and p['base']['sha']==plan['base'] and sha(p['body'].encode())==plan['body_sha256'] and p['state']=='open' and p['merged'] is False and p['draft'] is True,'reviewed live PR')
 checks=parse((root/'CHECK_RESULTS.json').read_bytes());mocks=parse((root/'MOCK_RESULTS.json').read_bytes());need(checks['ready_for_existing_publication_record'] is True and checks['plan_sha256']==PLAN and checks['helper_sha256']==HELPER,'review recommendation');need(mocks['status']=='pass' and mocks['cases_per_mode']==25 and mocks['semantic_results_identical'] is True and len(mocks['modes'])==3 and all(x['passed'] is True and x['cases']==25 and all(z['expected_confirmed'] is True for z in x['summary']) for x in mocks['modes']),'mock tests')
 return {'status':'pass','public_payloads':len(PUB),'private_payloads':len(pm['files']),'manifest_sha256':anchor,'reviewed_plan_sha256':PLAN,'reviewed_helper_sha256':HELPER,'mock_cases_per_mode':25,'scope':'Closed byte custody and captured identity only, not a live transaction, full mathematical audit or worldwide priority certificate.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--manifest-sha256',required=True);a=p.parse_args();print(json.dumps(verify(a.root,a.manifest_sha256),sort_keys=True,separators=(',',':')))
