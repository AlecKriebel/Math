"""Read-only verification of this correction and its retained execution receipts.

No rendering, target/legacy checker invocation, network, Git, or file write.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import ast,json,hashlib
R=Path(__file__).resolve().parent;P=R.parents[1]
S=P/'verification/local-ambient-block-modulus-stage-sol-20261025'
A=P/'verification/audit-ambient-block-modulus-code-sol-20261025'
LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
def info(p):
 d=p.read_bytes();return {'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
def require(ok,message):
 if not ok:raise RuntimeError(message)
before=json.loads((R/'BEFORE.json').read_text())
for name,x in before['files'].items():require(info(Path(name))==x,'protected original changed:'+name)
for base,key in [(S,'stage_file_set'),(A,'audit_file_set'),(LIVE,'current_public_file_set')]:
 require([str(p.relative_to(base))for p in sorted(base.rglob('*'))if p.is_file()]==before[key],'original file set changed:'+key)
src=(S/'final-content-check.proposed.py').read_text();proposed=(R/'final-content-check.proposed.py').read_text();ins=(R/'INSERTION.txt').read_text()
needle="  test('exact_visible_h1',contract.headings==[c['title']])\n"
require(src.count(needle)==1 and proposed==src.replace(needle,needle+ins),'narrow exact source insertion')
require(proposed.replace(ins,'',1)==src,'every old branch byte preserved')
require(proposed.rfind(' if rid in ABM_IDS:\n',0,proposed.index(ins))>proposed.rfind(' if rid in SG_IDS:\n',0,proposed.index(ins)),'insertion inside final ABM branch')
module=ast.parse((S/'ambient_block_modulus_source.py').read_text())
actual_ids=next(ast.literal_eval(n.value)for n in module.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='ABM_IDS'for x in n.targets))
require(actual_ids=={'23333353','23416806','23441617'},'exact three existing IDs only')
old="R=Path(__file__).resolve().parents[1]\n";new='R=Path('+repr(str(P))+')\n'
require(proposed.count(old)==1 and (R/'final-content-check.stage.py').read_text()==proposed.replace(old,new),'one explicit private execution override')
ast.parse(proposed);ast.parse((R/'final-content-check.stage.py').read_text())
results=json.loads((R/'RESULTS.json').read_text());rows=results['rows']
require(len(rows)==18,'exact18 bounded executions')
expected={(rid,case,mode)for rid in sorted(actual_ids)for case in ['pristine','h1_valid_but_wrong_href','Research_valid_but_wrong_href']for mode in ['normal','optimized']}
require({(x['record_id'],x['case'],x['mode'])for x in rows}==expected,'exact cases and modes')
for row in rows:
 rid,case,mode=row['record_id'],row['case'],row['mode'];q=R/row['receipt'];qa=json.loads(q.read_text());checks=qa['papers'][rid]['checks']
 require(info(q)['sha256']==row['receipt_sha256'] and set(qa['papers'])=={rid},'actual single-target receipt')
 if case=='pristine':require(row['exit_code']==0 and qa['status']=='PASS' and not qa['issues'] and all(checks.values()),'pristine acceptance')
 else:
  guard='exact_h1_selflink_destination' if case=='h1_valid_but_wrong_href' else 'exact_main_Research_destination'
  require(row['exit_code']==1 and qa['status']=='ISSUES_FOUND' and qa['issues']==[rid+': '+guard] and checks[guard] is False and all(v for k,v in checks.items()if k!=guard),'isolated expected guard rejection')
  c=json.loads((P/'papers'/rid/'publication.json').read_text());original=(S/'public/research'/c['slug']/'index.html').read_text()
  oldtag,newtag=('<h1><a href="/research/'+c['slug']+'/">','<h1><a href="/research/">') if case=='h1_valid_but_wrong_href' else ('<a href="/research/">Research</a>','<a href="/blog/">Research</a>')
  require(original.count(oldtag)==1,'single exact original link')
  sample=A/'navigation-fault-samples'/f'{rid}-{case}.html'
  require(sample.read_text()==original.replace(oldtag,newtag,1),'retained exact single-link fault')
  receipt=json.loads((A/'mutations'/f'{rid}-{case}-{mode}.json').read_text())
  require(info(sample)['sha256']==receipt['changed_read_SHA256'],'original false-negative sample binding')
  actual=json.loads((R/'read-overrides'/f'{rid}-{case}-{mode}.json').read_text())
  require(actual['exact_read_bytes_sha256']==receipt['changed_read_SHA256'],'exact same changed bytes actually tested')
oldfalse=json.loads((A/'CONFIRMED_NAVIGATION_GAPS.json').read_text())
require(len(oldfalse['runs'])==12 and all(x['exit_code']==0 and x['checker_status']=='PASS'for x in oldfalse['runs']),'honest unchanged original twelve false negatives')
if (R/'MANIFEST.json').exists():
 m=json.loads((R/'MANIFEST.json').read_text())
 for n,v in m['files'].items():require(info(R/n)==v,'owned file hash:'+n)
 z=json.loads((R/'SEAL.json').read_text());require(info(R/'MANIFEST.json')['sha256']==z['manifest_sha256'],'seal manifest')
print(json.dumps({'status':'PASS','protected_originals':len(before['files']),'stage_files':len(before['stage_file_set']),'audit_files':len(before['audit_file_set']),'public_files':len(before['current_public_file_set']),'pristine_acceptances':6,'retained_fault_rejections':12,'distinct_retained_faults':6,'old12_false_negatives_preserved':True,'all_old_branch_bytes_preserved':True,'test_suite_replayed':False,'read_only_verifier':True}))
