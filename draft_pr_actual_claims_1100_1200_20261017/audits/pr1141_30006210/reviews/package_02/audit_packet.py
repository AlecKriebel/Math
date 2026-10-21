#!/usr/bin/env python3
"""Read-only packet/custody checks. Writes only this review's evidence."""
from pathlib import Path, PurePosixPath
import hashlib,json,subprocess,sys,zipfile,re
from review_io import BASE,REVIEW,pin

def require(c,m):
    if not c:raise RuntimeError(m)
def fingerprint(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p,purpose='machine-authenticated custody input'):
    return pin(p,purpose)
def load(p,purpose='structured custody input'):
    return json.loads(read(p,purpose))
PUB=BASE/'publication';EX=REVIEW/'tmp/extracted'
PREFIX='draft_pr_actual_claims_1100_1200_20261017/audits/pr1141_30006210'

def main():
    result={}
    z=zipfile.ZipFile(PUB/'output/polynomial-compatibility-source-and-verification.zip')
    names=z.namelist();require(len(names)==111 and len(set(names))==111,'source names')
    for i in z.infolist():
        n=i.filename;p=PurePosixPath(n)
        require(not p.is_absolute() and '..' not in p.parts and '\\' not in n,'unsafe archive path')
        require((i.external_attr>>16)&0o170000!=0o120000,'symlink source')
        require(not any(s in p.parts for s in ['private','tmp','__pycache__','sources','rendered']),'private member '+n)
        require(i.date_time==(2026,10,17,0,0,0),'deterministic timestamp')
    manifest=json.loads(z.read('SOURCE_MANIFEST.json'))
    require(len(manifest)==110 and set(manifest)==set(names)-{'SOURCE_MANIFEST.json'},'manifest exact coverage')
    for n,w in manifest.items():require(fingerprint(z.read(n))==w,'source manifest pin '+n)
    allowed=load(PUB/'verification/AUDIT_MEMBERS.json')
    require(len(allowed)==98,'frozen audit count')
    for n,w in allowed.items():
        b=read(BASE/n,'every frozen authored audit member and archive comparison')
        require(fingerprint(b)==w and z.read(PREFIX+'/'+n)==b,'audit allowlist pin '+n)
    own=set(names)-{PREFIX+'/'+n for n in allowed}
    require(len(own)==13,'authored top member count')
    for n in own-{'PROVENANCE.json','SOURCE_MANIFEST.json'}:
        require(z.read(n)==read(PUB/n,'all top publication member comparisons'),'top member byte identity '+n)
    receipt=load(PUB/'PACKAGE_RECEIPT.json')
    require(receipt['source_members']==manifest and receipt['source_members_including_manifest']==111 and receipt['kit_members']==5,'package receipt coverage')
    for n,w in receipt['files'].items():require(fingerprint(read(PUB/n,'six operative release pins'))==w,'operative receipt '+n)
    kit=zipfile.ZipFile(PUB/'output/zenodo-upload-kit.zip');kn=kit.namelist()
    require(len(kn)==len(set(kn))==5,'kit unique count')
    wanted={'README.md','zenodo-metadata.json','zenodo-deposit.json','polynomial-compatibility.pdf','polynomial-compatibility-source-and-verification.zip'}
    require(set(kn)==wanted,'kit member exact names')
    require(kit.read('README.md')==z.read('README.md'),'kit README')
    require(kit.read('polynomial-compatibility.pdf')==z.read('output/pdf/polynomial-compatibility.pdf'),'kit PDF')
    require(kit.read('polynomial-compatibility-source-and-verification.zip')==(PUB/'output/polynomial-compatibility-source-and-verification.zip').read_bytes(),'kit source')
    meta=load(PUB/'zenodo-metadata.json');dep=load(PUB/'zenodo-deposit.json')
    payloads=[meta,dep['metadata'],json.loads(z.read('zenodo-metadata.json')),json.loads(z.read('zenodo-deposit.json'))['metadata'],json.loads(kit.read('zenodo-metadata.json')),json.loads(kit.read('zenodo-deposit.json'))['metadata']]
    require(all(x==meta for x in payloads),'six metadata payloads')
    portable=json.loads(kit.read('zenodo-deposit.json'));portable['files']=dep['files']
    require(portable==dep,'flat deposit path-only difference')
    require(dep['files']==[{'path':'output/pdf/polynomial-compatibility.pdf'},{'path':'output/polynomial-compatibility-source-and-verification.zip'}],'two upload files')
    require(meta['creators'][0]['orcid']=='0009-0001-9320-500X' and meta['version']=='1.0.0' and meta['publication_date']=='2026-10-17' and meta['license']=='cc-by-4.0','metadata identifiers')
    result['archives']={'source_members':111,'manifest_entries':110,'frozen_audit_members':98,'kit_members':5,'metadata_payloads_equal':6,'flat_deposit_path_only_difference':True,'safe_unique_no_symlink_private_members':True}
    originals=load(BASE/'inputs/MANIFEST.json');retrieval=load(BASE/'RETRIEVAL_RECEIPT.json')
    require(set(originals['members'])==set(p.name for p in (BASE/'inputs').iterdir() if p.is_file()) and len(originals['members'])==10,'ten original allowlist')
    for w in originals['entries']:require(fingerprint(read(BASE/'inputs'/w['file']))=={'bytes':w['bytes'],'sha256':w['sha256']},'historical input manifest')
    source_matches=[]
    for w in retrieval['files']:
        b=read(BASE/'inputs'/w['name'])
        require(fingerprint(b)=={'bytes':w['bytes'],'sha256':w['sha256']},'retrieval original pin')
        blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        require(blob==w['git_blob_sha'],'Git object content hash')
        p=subprocess.run(['git','cat-file','blob',retrieval['head']+':'+w['path']],cwd='/Users/alec/Documents/Math',capture_output=True)
        require(p.returncode==0 and p.stdout==b,'exact source commit '+w['path'])
        source_matches.append(w['name'])
    result['original_inputs']={'exact_source_commit':retrieval['head'],'all_ten_exact_bytes_and_git_blobs':source_matches,'git_operation':'read-only cat-file only; no index/ref/branch mutation'}
    # Authenticate every explicit file pin in all six final family receipts.
    receipts=['reviews/separator_01/ARTIFACT_RECEIPT.json','reviews/covariance_01/RECEIPT.json','reviews/target_01/ARTIFACT_RECEIPT.json','reviews/priority_separator_01/RECEIPT.json','reviews/priority_target_01/RECEIPT.json','reviews/priority_classification_01/RECEIPT.json']
    rr=[]
    for name in receipts:
        data=load(BASE/name);checked=[];named=[]
        def walk(v):
            if isinstance(v,dict):
                p=v.get('path');h=v.get('sha256');size=v.get('bytes')
                if p and h and size is not None:
                    require(fingerprint(read(Path(p),'all six review receipt explicit custody input pins'))=={'bytes':size,'sha256':h},'review receipt '+p)
                    checked.append(p)
                if p and 'start_sha256' in v:
                    b=read(p);require(hashlib.sha256(b).hexdigest()==v['start_sha256']==v['end_sha256'] and len(b)==v['start_bytes']==v['end_bytes'],'start/end receipt')
                    checked.append(p)
                if 'name' in v and h and size is not None:
                    p=BASE/'reviews/separator_01/sources/private'/v['name']
                    require(fingerprint(read(p))=={'bytes':size,'sha256':h},'named primary pin')
                    named.append(str(p))
                for a in v.values():walk(a)
            elif isinstance(v,list):
                for a in v:walk(a)
        walk(data);rr.append({'receipt':name,'receipt_sha256':fingerprint((BASE/name).read_bytes())['sha256'],'explicit_path_pins':len(checked),'named_private_pins':len(named)})
    result['six_review_receipt_authentication']=rr
    # Recompute the distribution-only repair, without displaying source lines.
    folder=BASE/'reviews/priority_classification_01'
    scope=load(folder/'BODY_SCOPE.json');old=load(folder/'sources/private/historical_seal_v1/BODY_SCOPE.json','private historical scope comparison only, no source excerpts redistributed')
    rows=0
    require(len(scope['bodies'])==len(old['bodies'])==11,'source-scope body coverage')
    for b,bo in zip(scope['bodies'],old['bodies']):
        source=read(b['text_path'],'primary full body pin and heading position/length/hash validation').decode()
        require(fingerprint(source.encode())=={'bytes':b['bytes'],'sha256':b['sha256']},'body source pin')
        lines=source.splitlines()
        # Python splitlines also treats formfeed as line boundaries; original
        # scope line numbers use the same convention.
        for row in b['result_heading_scan']:
            line=lines[row['line']-1].encode()
            require(len(line)==row['source_line_utf8_bytes'] and hashlib.sha256(line).hexdigest()==row['source_line_sha256'],'heading source pin')
            require(set(row)=={'line','source_line_utf8_bytes','source_line_sha256'},'copied heading field')
            rows+=1
        require([x['line'] for x in b['result_heading_scan']]==[x['line'] for x in bo['result_heading_scan']],'historical heading positions')
        require({k:v for k,v in b.items() if k!='result_heading_scan'}=={k:v for k,v in bo.items() if k!='result_heading_scan'},'unchanged source scope')
    require(rows==249,'heading coverage')
    chrono=load(folder/'CHRONOLOGY_METADATA.json');oldc=load(folder/'sources/private/historical_seal_v1/CHRONOLOGY_METADATA.json')
    import html,datetime
    require(len(chrono['sources'])==len(oldc['sources'])==11,'chronology source coverage')
    parsed_versions=0
    for now,previous in zip(chrono['sources'],oldc['sources']):
        require(now['file']==previous['file'] and now['sha256']==previous['sha256'],'chronology original identity')
        historical=previous['submission_history_html_text'].encode()
        require(len(historical)==now['historical_extraction_utf8_bytes'] and hashlib.sha256(historical).hexdigest()==now['historical_extraction_sha256'],'historical chronology exact text pin')
        primary=read(folder/now['file'],'primary factual chronology validation only; no copied text distributed')
        require(hashlib.sha256(primary).hexdigest()==now['sha256'],'chronology primary HTML identity')
        clean=html.unescape(re.sub('<[^>]+>',' ',primary.decode()))
        clean=re.sub(r'\s+',' ',clean)
        for version in now['versions']:
            date=datetime.datetime.strptime(version['submission_utc'],'%Y-%m-%dT%H:%M:%SZ')
            stamp=date.strftime('%d %b %Y %H:%M:%S').lstrip('0')
            require(stamp in clean,'chronology date parsed primary')
            require('['+version['version']+']' in clean and str(version['source_archive_kilobytes'])+' KB' in clean,'chronology version size primary')
            parsed_versions+=1
    result['distribution_repair']={'heading_rows_source_authenticated':rows,'all_other_original_body_scope_fields_equal':True,'current_chronology_sources':len(chrono['sources']),'historical_chronology_sources':len(oldc['sources']),'primary_version_dates_sizes_checked':parsed_versions,'historical_extraction_pins_checked':11,'source_line_strings_not_redistributed':True}
    # Full byte rebuild check after builder was executed ONLY in this extraction.
    for name in ['polynomial-compatibility-source-and-verification.zip','zenodo-upload-kit.zip']:
        require((EX/'output'/name).read_bytes()==(PUB/'output'/name).read_bytes(),'rebuilt archive bytes')
    result['rebuild']={'python':sys.version,'both_frozen_archives_identical':True,'executed_only_under':str(EX)}
    (REVIEW/'PACKET_AUTHENTICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
