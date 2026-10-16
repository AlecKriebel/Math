from pathlib import Path
import json,hashlib,zipfile,io,re,datetime,difflib,subprocess,unicodedata
R=Path(__file__).resolve().parent;B=R.parent.parent;P=B/'publication';sha=lambda d:hashlib.sha256(d).hexdigest();pin=lambda p:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
base=json.loads((B/'repairs/package_01/BASELINE_FILE_PINS.json').read_text());changes=json.loads((B/'repairs/package_01/CHANGED_PATHS.json').read_text());changed={q['path'] for q in changes['changes']};protected=[q for q in base['files'] if q['path'] not in changed];bad=[q['path'] for q in protected if not (B/q['path']).exists() or pin(B/q['path'])!={'bytes':q['bytes'],'sha256':q['sha256']}];priv=[q for q in protected if q['path'].startswith('reviews/')]
old=B/'reviews/package_01/extracted/teichmuller_original_ball_paths_v1';buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=8,compresslevel=9) as z:
 for p in sorted(old.rglob('*')):
  if not p.is_file():continue
  info=zipfile.ZipInfo('teichmuller_original_ball_paths_v1/'+p.relative_to(old).as_posix(),(2026,10,13,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=8;z.writestr(info,p.read_bytes())
oldhash=sha(buf.getvalue());oldsize=len(buf.getvalue())
# Historical before-title bytes differ only by exact bibliographic title substitution.
a=(B/'history/ROOT_MATH_AUDIT_before_title_correction.md').read_text();b=(B/'ROOT_MATH_AUDIT.md').read_text();diff=list(difflib.unified_diff(a.splitlines(),b.splitlines(),lineterm=''))
# Original whole-tree inventory, including absence of extra fixture or checker at attempt prefix.
tree=subprocess.check_output(['git','ls-tree','-r','--name-only','6322305d37b8131f034a1b4c3c5e861e4b04844f'],text=True).splitlines()
# Inspect every text payload using type/UTF8 parsing plus primary-source overlap screening.
raw=R/'sources/raw';sources={p.stem:re.findall(r'\w+',unicodedata.normalize('NFKD',p.read_text()).lower()) for p in raw.glob('*.txt') if p.stem!='candidate_pdf'}
sourcegrams={n:set(tuple(v[i:i+30]) for i in range(len(v)-29)) for n,v in sources.items()};rows=[];longjson=[]
with zipfile.ZipFile(P/'teichmuller_original_ball_paths_source_audits_v1.zip') as z:
 for name in z.namelist():
  rel=name.removeprefix('teichmuller_original_ball_paths_v1/');data=z.read(name)
  if rel=='research_note.pdf':continue
  t=data.decode('utf8');tokens=re.findall(r'\w+',unicodedata.normalize('NFKD',t).lower());matches=[]
  for sn,grams in sourcegrams.items():
   count=sum(tuple(tokens[i:i+30]) in grams for i in range(len(tokens)-29))
   if count:matches.append({'source':sn,'matching_30word_windows':count})
  rows.append({'path':rel,'bytes':len(data),'words':len(tokens),'matching_source_windows':matches})
  if rel.endswith('.json'):
   def strings(x,loc=''):
    if isinstance(x,str) and len(x)>600:longjson.append({'file':rel,'locator':loc,'length':len(x),'start':x[:100]})
    elif isinstance(x,dict):
     for k,v in x.items():strings(v,loc+'/'+k)
    elif isinstance(x,list):
     for j,v in enumerate(x):strings(v,loc+'/'+str(j))
   strings(json.loads(t))
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_files':len(base['files']),'protected_baseline_files':len(protected),'protected_private_review_files':len(priv),'protected_mismatches':bad,'historical_old_archive_independently_reconstructed':{'sha256':oldhash,'bytes':oldsize,'matches_declared':oldhash=='0ec9d589631f5c645fb3130eb453cd1324b4c628cdd1e254446ce08a218ce9a7' and oldsize==201814,'method':'In-memory deterministic rebuild from retained private package_01 extraction; no raw-source body copied to authored output'},'root_title_only_diff':diff,'original_head_whole_tree_count':len(tree),'text_payload_inspection':rows,'long_json_strings':longjson}
(R/'REPAIR_AND_PAYLOAD_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['text_payload_inspection','long_json_strings']},indent=2));print('SOURCE-OVERLAP:',json.dumps([q for q in rows if q['matching_source_windows']],indent=2));print('LONG JSON STRINGS:',json.dumps(longjson,indent=2))
