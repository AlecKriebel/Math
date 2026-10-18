#!/usr/bin/env python3
"""Read-only package/receipt accounting. Hashing does not certify semantic reading."""
from pathlib import Path
import datetime, difflib, hashlib, json
R=Path(__file__).absolute().parent;A=R.parent.parent
BASE=R/'private/source';PREFIX='draft_pr_actual_claims_1100_1200_20261017/audits/pr1150_30003045';B=BASE/PREFIX
def need(ok,msg):
    if not ok:raise ValueError(msg)
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(n,o):(R/n).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def pinrows(o):
    if isinstance(o,dict):
        if {'path','bytes','sha256'}<=set(o):yield o
        else:
            for v in o.values():yield from pinrows(v)
    elif isinstance(o,list):
        for v in o:yield from pinrows(v)

def main():
    family=[]
    expected_seals={'target_quadric_01':'1d4ead534dfcc657d34d1840d731579d4c8ef17d4a8b3aa350729baeea718465','norm_obstruction_01':'1cbc2d264af24d80be96730ddfe5a273225008a2c41c034da156a45e15fec049','symbols_01':'1aa864c7aaaefbcd3419b8cce4a751a2ce4cef067d7797c66bf1c662d2a60abe','priority_target_01':'99c4a09207b19aeb0381146f945d2c98abbe23ad489604f93165f50cd9881173','priority_mixed_01':'20700dd23e09cec9f0455702b2f5399c7a902af44cddb0d79e57f5eb3ebe4eeb','priority_brauer_01':'3b9056a6e6d8bf906f82f7ce50dd4825caf779e4bc129b9a15e54816a0ab6377'}
    for name,seal in expected_seals.items():
        d=B/'reviews'/name;p=d/('READ_RECEIPT.json' if name in ['priority_mixed_01','priority_brauer_01'] else 'RECEIPT.json');need(pin(p)['sha256']==seal,'family seal '+name)
        good=[];omitted=[]
        for row in pinrows(json.loads(p.read_text())):
            f=(d/row['path']).resolve();need(f.is_relative_to(BASE),'receipt path escapes own copy')
            if f.is_file():need(pin(f)=={'bytes':row['bytes'],'sha256':row['sha256']},'historical available pin '+str(f));good.append(row)
            else:omitted.append(row)
        family.append({'name':name,'external_seal':seal,'available':len(good),'intentionally_absent':len(omitted),'available_pins':good,'omitted_private_body_tool_or_history_pins':omitted})
    need(sum(x['available'] for x in family)==63,'available family count')
    need(sum(x['intentionally_absent'] for x in family)==163,'omitted family count')
    save('HISTORICAL_AUTHENTICATION.json',{'status':'PASS','available':63,'intentionally_absent':163,'families':family,'scope':'Authored available bytes only. Full-source custody scripts inspected but not run against intentionally incomplete release; no historical search execution or source reading reproduced.'})
    packages=[];gate=json.loads((A/'ACCEPTANCE_GATE.json').read_text())
    for i in range(1,5):
        name=f'package_{i:02d}';d=A/'reviews'/name;p=d/'EXTERNAL_FINAL_RECEIPT.json';v=json.loads(p.read_text());rows=v.get('evidence',v.get('artifacts'));checked=[]
        if isinstance(rows,dict):entries=[{'path':n,**w} for n,w in rows.items()]
        else:entries=rows
        for row in entries:
            f=Path(row['path']);f=f if f.is_absolute() else d/f
            need(f.is_relative_to(d),'prior public evidence outside assigned review')
            need(pin(f)=={'bytes':row['bytes'],'sha256':row['sha256']},'prior package evidence '+str(f));checked.append({'path':str(f.relative_to(d)),**pin(f)})
        g=next(x for x in gate['whole_package_reviews'] if x['round']==name)
        need(pin(p)['sha256']==g['external_receipt_sha256'],'gate prior receipt '+name)
        need(pin(d/'REPORT.md')['sha256']==g['report_sha256'],'gate prior report '+name)
        packages.append({'name':name,'receipt':pin(p),'report':pin(d/'REPORT.md'),'pinned_public_evidence_checked':checked,'status':g['status']})
    save('PRIOR_PACKAGE_AUTHENTICATION.json',{'status':'PASS','packages':packages,'meaning':'Historical edition evidence only; no preceding verdict is mathematical proof for this review.'})
    for root in ['inputs','pr_repair_candidate']:
        d=B/root;m=json.loads((d/'MANIFEST.json').read_text());entries=m['entries'];entries=entries if isinstance(entries,dict) else {x['file']:{'bytes':x['bytes'],'sha256':x['sha256']} for x in entries}
        need({p.name for p in d.iterdir()}==set(m['members']),'flat manifest '+root)
        for n,w in entries.items():need(pin(d/n)==w,'inner manifest '+root+'/'+n)
    need((B/'FINAL_PROOF.md').read_bytes()==(B/'pr_repair_candidate/COUNTEREXAMPLE.md').read_bytes(),'final proof copy')
    need((B/'reviews/symbols_01/verify_symbols.py').read_bytes()==(B/'pr_repair_candidate/verify_symbols.py').read_bytes(),'symbol program copy')
    changes={}
    for old,new in [('inputs/COUNTEREXAMPLE.md','REVIEWED_PROOF.md'),('REVIEWED_PROOF.md','FINAL_PROOF.md'),('reviews/norm_obstruction_01/diagnose_norm.py','pr_repair_candidate/diagnose_norm.py')]:
        changes[old+' -> '+new]=''.join(difflib.unified_diff((B/old).read_text().splitlines(True),(B/new).read_text().splitlines(True),fromfile=old,tofile=new))
    parsed=[]
    manifest=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    for n in sorted(set(manifest)|{'SOURCE_MANIFEST.json'}):
        p=BASE/n
        if p.suffix=='.json':json.loads(p.read_text());parsed.append(n)
    save('EDITION_ACCOUNTING.json',{'status':'PASS','original_manifest_members':11,'current_manifest_members':16,'all_json_members_parsed':len(parsed),'json_member_names':parsed,'full_diffs':changes,'gate_at_read':{k:gate[k] for k in ['operative_package_edition','published','package_reviews_clean','fresh_clean_reviews','head_sha']},'frozen_authored_allowlist_matches_workspace':all(pin(B/n)==pin(A/n) for n in json.loads((BASE/'verification/AUDIT_MEMBERS.json').read_text()))})
    print(json.dumps({'status':'PASS','family_available':63,'family_omitted':163,'prior_packages_authenticated':len(packages),'json_members':len(parsed)},indent=2))
if __name__=='__main__':main()
