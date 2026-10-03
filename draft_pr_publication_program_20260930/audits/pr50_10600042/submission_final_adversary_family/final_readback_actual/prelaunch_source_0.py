#!/usr/bin/env python3
"""Full retained-stream and fixed-input readback in the reviewer-owned family."""
from pathlib import Path
import datetime, hashlib, json, stat, zipfile
base=Path(__file__).absolute().parent
package=base.parent/'publication_package_v1'
checks=0
def need(ok,msg):
    global checks
    if not ok: raise AssertionError(msg)
    checks+=1
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
    st=p.lstat();need(stat.S_ISREG(st.st_mode) and not p.is_symlink(),'regular '+str(p))
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(st.st_mode)}
captures=[]
for name in ('independent_controls_actual','artifact_extract_actual','fresh_crossref_actual',
             'author_checker_extracted_actual','zip_rebuild_extracted_actual','final_pdf_render_actual',
             'final_pdf_info_actual','final_pdf_text_actual'):
    folder=base/name; cap=json.loads((folder/'CAPTURE.json').read_bytes())
    need(type(cap['child_pid']) is int and cap['child_pid']>0 and cap['exit_code']==0,'completed real capture '+name)
    for stream in ('stdout','stderr'):
        b=(folder/(stream+'.bin')).read_bytes()
        need({'bytes':len(b),'sha256':sha(b)}==cap[stream],'full captured stream '+name+stream)
    need(not (folder/'stderr.bin').read_bytes(),'empty stderr '+name)
    for s in cap['source_pins']:
        b=Path(s['path']).read_bytes()
        need(b==(folder/s['copy']).read_bytes(),'whole prelaunch source '+name)
        need(len(b)==s['bytes'] and sha(b)==s['sha256'],'source pin '+name)
    captures.append({'name':name,'capture_binding':pin(folder/'CAPTURE.json'),'child_pid':cap['child_pid'],
                     'exit_code':cap['exit_code'],'complete_streams_match':True})
need((base/'author_checker_extracted_actual/stdout.bin').read_bytes()==(base/'extracted/expected_results.json').read_bytes(),'byte exact author reproduction')
actual=json.loads((base/'author_checker_extracted_actual/stdout.bin').read_bytes())
need(actual['checks']==7106 and type(actual['checks']) is int and actual['status']=='PASS_BOUNDED_DIAGNOSTICS','typed original result')
ind=json.loads((base/'independent_controls_actual/stdout.bin').read_bytes())
need(ind['checks']==19485 and ind['legal_scheme_cases']==2320 and ind['lifted_edge_cases']==1057 and ind['relation_context_cases']==861,'typed independent totals')
need((base/'extracted/even-strand-markov-verification-v1.zip').read_bytes()==(package/'even-strand-markov-verification-v1.zip').read_bytes(),'actual rebuilt ZIP equals submitted ZIP exactly on this machine')
images=[]
for i in range(1,5):
    p=base/('pdf_render/page-%d.png'%i)
    need(p.read_bytes()==(base.parent/('tmp/pdfs/submission_v1/page-%d.png'%i)).read_bytes(),'own render matches initial viewed ROOT pixels')
    images.append(pin(p))
need(len(list((base/'pdf_render').glob('page-*.png')))==4,'exactly four rendered pages')
info=(base/'final_pdf_info_actual/stdout.bin').read_text()
need('Pages:           4' in info and 'Author:          Alec Kriebel' in info and 'Encrypted:       no' in info,'four-page actual PDF metadata')
text=(base/'final_pdf_text_actual/stdout.bin').read_text()
need(text.count('\f')==4 and '(BR)' in text and '(BL)' in text and 'AI and review disclosure' in text and 'S0218216503002561' in text,'complete PDF text sections')
earlier=json.loads((base/'FINAL_INPUT_BINDINGS.json').read_bytes())
for row in earlier['input_pins']:
    b=Path(row['path']).read_bytes()
    need(len(b)==row['bytes'] and sha(b)==row['sha256'],'final submitted artifact unchanged across review')
external=[pin(p) for p in sorted(package.iterdir()) if p.is_file()]
external += [pin(base.parent/'publication_operations/ROOT_NATIVE_COMPILER_RESPONSE.json'),
             pin(base.parent/'preprint_v1/even_strand_markov.tex'),
             pin(base.parent.parent/'pr45_9900007/root_pr50_submission_pdf_export_actual_capture/CAPTURE.json'),
             pin(Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py'))]
for label,doi,page in (('survey','10.4064/bc103-0-1','9-61'),('GKS','10.1112/blms.12761','537-591'),('Fiedler','10.1142/s0218216503002561','575-577')):
    m=json.loads((base/('PRIMARY_'+label+'_crossref.json')).read_bytes())['message']
    need(m['DOI'].lower()==doi and m['page']==page,'primary source metadata exact '+label)
need('double Markov' in json.loads((base/'PRIMARY_Fiedler_crossref.json').read_bytes())['message']['abstract'],'primary Fiedler negative abstract')
record={'schema':'pr50-final-submission-adversary-complete-readback/v1',
        'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ALL_FINAL_READBACKS',
        'checks':checks,'actual_captures':captures,'external_inputs':external,'render_images':images,
        'visual_review':'All four own-rendered pages personally viewed; exact same bytes as initially inspected ROOT render. No clipping, overlap, missing formula, stale theorem or orphan bibliography page.',
        'publication_event_not_claimed':True,'root_acceptance_or_native_changes_not_authored':True}
(base/'COMPLETE_READBACK.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':record['status'],'checks':checks,'actual_captures':len(captures),'external_inputs':len(external),'rendered_pages':4},indent=2))
