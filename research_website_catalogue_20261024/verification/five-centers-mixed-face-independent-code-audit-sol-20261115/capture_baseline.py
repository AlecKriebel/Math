#!/usr/bin/env python3
"""Fresh authorized baseline capture; only this audit folder is written."""
from pathlib import Path
from datetime import datetime,timezone
from html.parser import HTMLParser
import hashlib,json,os,re,subprocess
import xml.etree.ElementTree as ET

A=Path(__file__).resolve().parent;P=A.parents[1]
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
if (A/'BASELINE_SEAL.json').exists():raise RuntimeError('baseline already sealed')
if not (A/'INITIAL_EXPECTATIONS_SEAL.json').is_file():raise RuntimeError('independent source seal first')
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'SHA256':sha(b)}
def load(p):return json.loads(p.read_bytes())
def put(n,x):
    p=A/n
    if not p.resolve().is_relative_to(A):raise ValueError('outside own namespace')
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def snapshot(b):
    p=A/'private/baseline-blobs'/sha(b);p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists() and p.read_bytes()!=b:raise ValueError('hash collision')
    if not p.exists():p.write_bytes(b)
    return pin(p)
commands=[]
def git(args,label):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0';start=now()
    x=subprocess.run(['git',*args],cwd=W,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    rec={'arguments':['git',*args],'cwd':str(W),'UTC_started':start,'UTC_completed':now(),'GIT_OPTIONAL_LOCKS':'0','exit_code':x.returncode,'stdout':snapshot(x.stdout),'stderr':snapshot(x.stderr)};commands.append(rec)
    if x.returncode!=0:raise RuntimeError('read-only git command failed '+label)
    return x.stdout
start=now();head=git(['rev-parse','HEAD'],'HEAD').decode().strip();branch=git(['symbolic-ref','--short','HEAD'],'branch').decode().strip()
if head!='46773fd3d0e7289f5ab79bfc9f8ddf382fa508fc' or branch!='master':raise ValueError('actual authorized baseline HEAD/branch mismatch')
indexloc=Path(git(['rev-parse','--git-path','index'],'index path').decode().strip())
if not indexloc.is_absolute():indexloc=W/indexloc
index_before=pin(indexloc)
raw=git(['ls-files','--stage','-z'],'complete index records')
flags=git(['ls-files','-v','-z'],'complete index flags')
expected=load(A/'EXPECTED_OUTPUT_PATHS.json')
# The source-only proposal did not inspect the website. Actual authorized baseline resolves this aggregate locator.
for e in expected['paths']:
    if e['kind']=='aggregate_exact_existing_locations_preserved_plus_two_new_locations':e['website_relative_path']='research/sitemap.xml'
excluded={('public/'+e['website_relative_path']).encode() for e in expected['paths']}
records=raw.split(b'\0');records=records[:-1] if records[-1]==b'' else records
parsed=[];protected=[]
for r in records:
    meta,path=r.split(b'\t',1);mode,blob,stage=meta.decode().split(' ')
    parsed.append({'path':path.decode(),'mode':mode,'blob':blob,'stage':stage})
    if path not in excluded:protected.append(r)
protected_raw=b'\0'.join(protected)+(b'\0' if protected else b'')
public=[];directories=[]
for q in sorted((W/'public').rglob('*')):
    if q.is_symlink():raise ValueError('public namespace symlink '+str(q))
    if q.is_dir():directories.append(q.relative_to(W/'public').as_posix())
    elif q.is_file():
        b=q.read_bytes();public.append({'public_relative_path':q.relative_to(W/'public').as_posix(),'source_path':str(q),'bytes':len(b),'SHA256':sha(b),'snapshot':snapshot(b),'mode_octal':oct(q.stat().st_mode&0o777)})
    else:raise ValueError('nonregular public node '+str(q))
if len(public)!=614:raise ValueError('fresh public count is not614')
by={e['public_relative_path']:e for e in public}
for e in expected['paths']:
    if e['kind'] not in ['aggregate_exact_existing_cards_preserved_plus_two_new_cards','aggregate_exact_existing_locations_preserved_plus_two_new_locations'] and e['website_relative_path'] in by:raise ValueError('new leaf unexpectedly exists')
index=(W/'public/research/index.html').read_text()
ld=[json.loads(s) for s in re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',index,re.S)]
lists=[]
def walk(x):
    if isinstance(x,dict):
        if x.get('@type')=='ItemList':lists.append(x)
        for v in x.values():walk(v)
    elif isinstance(x,list):
        for v in x:walk(v)
walk(ld)
if len(lists)!=1 or lists[0]['numberOfItems']!=92 or len(lists[0]['itemListElement'])!=92:raise ValueError('fresh typed index count')
class Visible(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.ul=0;self.li=0;self.rows=[];self.current=None;self.links=[];self.a=None
    def handle_starttag(self,t,attrs):
        d=dict(attrs)
        if t=='ul':self.ul+=1
        if t=='li' and self.ul:self.li+=1;self.current=[];self.links=[]
        if t=='a' and self.li:self.a=d.get('href');self.links.append(d.get('href'))
    def handle_data(self,s):
        if self.li:self.current.append(s)
    def handle_endtag(self,t):
        if t=='li' and self.li:self.rows.append({'links':self.links,'text':''.join(self.current)});self.li-=1
        if t=='ul':self.ul-=1
v=Visible();v.feed(index)
if len(v.rows)!=92:raise ValueError('fresh visible index count')
typed=lists[0]['itemListElement']
if [x['position'] for x in typed]!=list(range(1,93)):raise ValueError('typed positions')
if ['https://aleckriebel.com'+x['links'][0] for x in v.rows]!=[x['url'] for x in typed]:raise ValueError('visible/typed URL order mismatch')
mapraw=(W/'public/research/sitemap.xml').read_bytes();xml=ET.fromstring(mapraw);locs=[e.text for e in xml.findall('{*}url/{*}loc')]
if len(locs)!=93 or len(set(locs))!=93:raise ValueError('fresh sitemap count')
configs=[]
for n in ['.firebaserc','firebase.json']:
    q=W/n;b=q.read_bytes();configs.append({'source_path':str(q),'bytes':len(b),'SHA256':sha(b),'snapshot':snapshot(b)})
coreauthority=P/'verification/nash-quotient-robinson-private-stage-sol-20261115/CORE_INPUTS.json';core=load(coreauthority);actualcore=[]
for e in core['files']:
    q=Path(e['path']);b=q.read_bytes()
    if len(b)!=e['bytes'] or sha(b)!=e['SHA256']:raise ValueError('core original/authorized qualification drift '+str(q))
    actualcore.append({'source':pin(q),'snapshot':snapshot(b)})
if core['original17_files_unchanged']!=17 or core['current_checkpoint_SHA256']!='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0':raise ValueError('original17 plus authorized checkpoint qualification')
if {str(q) for q in (P/'scripts').iterdir() if q.is_file()}!=set(core['scripts_namespace']):raise ValueError('scripts namespace drift')
endhead=git(['rev-parse','HEAD'],'closing HEAD').decode().strip();index_after=pin(indexloc)
if endhead!=head or index_after!=index_before:raise ValueError('Git control changed during baseline capture')
priorfiles=[]
for n in ['lefschetz-link-production-integration-root-20261115/installation.json','root-lefschetz-link-stage-adoption-20261115.json','root-lefschetz-link-commit-approval-20261115.json','lefschetz-link-production-integration-root-20261115/live-http.json']:
    q=P/'verification'/n;priorfiles.append(pin(q))
put('FRESH_WEBSITE_BASELINE.json',{'schema':'fresh_authorized614_independent_baseline_before_writer_exposure_v1','UTC_started':start,'UTC_completed':now(),'website_root':str(W),'HEAD':head,'branch':branch,'public_files':public,'public_directories':directories,'measured_counts':{'public_files':614,'typed_index_entries':92,'visible_index_entries':92,'sitemap_locations':93},'whole_index_JSONLD_original_typed_objects':ld,'whole_visible_index_entries':v.rows,'whole_sitemap_locations':locs,'configs':configs,'proposed_only_candidate_counts':[623,94,95],'actual_new_leaves_absent':9,'writer_stage_code_copy_or_opinion_reads':0,'prior_publication_receipts':priorfiles,'native_verified_count':{'value':88,'source':'current parent root report only','independently_reverified':False},'browser_native_gates_for_preceding_pair_incomplete':True,'website_Git_Sheet_deploy_redirect_contact_mutation':False})
put('FRESH_GIT_OBSERVATIONS.json',{'UTC':now(),'website_HEAD':head,'branch':branch,'actual_raw_index_file_observation':index_before,'raw_index_records':snapshot(raw),'raw_index_flags':snapshot(flags),'all_index_record_count':len(records),'parsed_index_records':parsed,'excluded_future11_gitpaths':sorted(x.decode() for x in excluded),'fresh_protected_index_record_count':len(protected),'fresh_protected_raw_records':snapshot(protected_raw),'old_protected_count_not_reused':True,'actual_read_only_command_receipts':commands,'local_controls_are_bounded_observations_not_permanent_future_preconditions':True,'fresh_remote_read_claim':False})
put('CORE17_AND_AUTHORIZED_CHECKPOINT.json',{'UTC':now(),'prior_whole_qualification':core,'prior_authority_metadata':pin(coreauthority),'current_actual_file_snapshots':actualcore,'original17_files_unchanged':17,'authorized_checkpoint_current_SHA256':'405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','claim_all18_match_original_baseline':False,'core_scientific_or_generator_programmes_executed':False})
put('ROOT_WEBSITE_GO_OBSERVATION.json',{'UTC':now(),'recorded_parent_instruction':'Explicit new website GO after source expectation seal a68847e508323bd640b75368e3b01e4ce06ea9cfe64fcda8e83e2d1052a01b77; capture actual614/92/93 after preceding127128 publication at46773fd3d0e7289f5ab79bfc9f8ddf382fa508fc before writer exposure; await immutable writer FINAL; private audit only.','authority':'parent root message, recorded here by the auditor; not a production adoption receipt','production_authority':False,'writer_FINAL_received':False})
(A/'BASELINE_RESEARCH_LOG.md').write_text('# Authorized baseline checkpoint log\n\n- '+now()+' — 40% overall audit: Explicit website GO received; independently captured actual46773fd3… master baseline614public/92typed+visibleindex/93sitemap before writer exposure. Fresh index protection observations and original17 plus sole authorized405b checkpoint qualification recorded. Await immutable writer FINAL; no website/Git mutation.\n')
print(json.dumps({'status':'FRESH614_BASELINE_CAPTURED_BEFORE_WRITER_EXPOSURE','HEAD':head,'branch':branch,'public':len(public),'typed_and_visible_index':len(v.rows),'sitemap':len(locs),'fresh_protected_index_records':len(protected),'writer_stage_reads':0,'mutations_outside_own_audit':0}))
