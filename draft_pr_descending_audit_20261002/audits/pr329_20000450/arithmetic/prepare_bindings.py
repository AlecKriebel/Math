#!/usr/bin/env python3
"""Assemble source/dependency pins; packaging, not a mathematical proof."""
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
import stat

base=Path(__file__).resolve().parent
parent=base.parent
candidate=parent/'snapshot/unsolved_math_prioritization/attempts/20000450'
runtime=parent/'geometry/.runtime'
def pin(p):
    p=Path(p).resolve(); data=p.read_bytes()
    return {'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'mode':stat.S_IMODE(p.stat().st_mode)}
def write(name,obj): (base/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
now=datetime.now(timezone.utc).isoformat()
original=parent/'root_sources_private/access002'
external=[{'role':'original AIM question PDF',**pin(original/'candidate_0.pdf')},
          {'role':'original physical/printed51 render',**pin(original/'operative-51.png')}]
external.extend({'role':'released candidate '+name,**pin(candidate/name)} for name in
                ['TURN_1.md','FINAL_RESULT.md','verify_turn1.py','SOURCE_THEORY.md'])
write('EXTERNAL_BINDINGS.json',{'prepared_utc':now,'candidate_head':'96395a4f506af6a6045e3cd59afcba2db6b7e2e7',
                              'scope':'Only the originally allowed sources and four released candidate files; not inherited reviews or sibling mathematics.',
                              'files':external})
source_data=[
 ('fisher2001.pdf','https://ems.press/content/serial-article-files/31488','Fisher, JEMS3(2001),169-201',
  'Full operative text printed172-182 and194-195. Original renders172-173,179,194-195 inspected. Native191-195 captured,191-193 combined display partly truncated; not an extra complete reading.',
  '003_retrieve_fisher',['005_read_fisher_172_175','008_reread_fisher_194_195','011_read_fisher_176_179','015_read_fisher_179_182'],
  ['fisher_tate-04.png','fisher_tate-05.png','fisher_moduli-11.png','fisher_cover-26.png','fisher_cover-27.png']),
 ('sutherland2023_lecture5.pdf','https://math.mit.edu/classes/18.783/2023/LectureNotes5.pdf','Sutherland official MIT Lecture5',
  'Full operative text pages10-14,sections5.5-5.6. Whole14-page extraction captured but combined display truncated; not a full14-page reading. Native direct PDF access succeeds despite browser open error.',
  '004_retrieve_sutherland',['012_reread_sutherland_10_14'],[]),
 ('sutherland2023_lecture23.pdf','https://math.mit.edu/classes/18.783/2023/LectureNotes23.pdf','Sutherland official MIT Lecture23',
  'Full operative text pages12-14,original render13 inspected;Theorem23.29/Corollaries23.30-31. Referenced independent proofs of standard pairing nondegeneracy not separately read.',
  '024_retrieve_sutherland_pairing',['025_read_pairing_theorem'],['pairing-13.png'])]
sources=[]
for filename,url,title,scope,retrieval,reads,renders in source_data:
    sources.append({'title':title,'url':url,'reading_scope':scope,'pdf':pin(base/filename),
                    'native_retrieval':retrieval,'operative_extractions':reads,
                    'inspected_original_renders':[pin(base/x) for x in renders]})
write('SOURCES.json',{'prepared_utc':now,'direct_primary_sources':sources,
                     'original_question':external[:2],'unread_material':'Inherited author/reviewer verdicts,imported report,root baseline,sibling scientific files.'})
# Explicitly authorized environment-only read: scientific sibling files excluded.
site=runtime/'lib/python3.14/site-packages'
roots=[site/'sympy',site/'mpmath']
files=[]
for root in roots:
    files.extend(pin(p) for p in sorted(root.rglob('*')) if p.is_file() and
                 '__pycache__' not in p.parts and p.suffix!='.pyc')
tools=[pin(runtime/'bin/python'),pin(runtime/'pyvenv.cfg'),pin('/opt/homebrew/bin/python3')]
write('RUNTIME_BINDINGS.json',{'prepared_utc':now,'runtime_roots':[str(p) for p in roots],
                             'inventory_filter':'regular files,excluding __pycache__ and .pyc',
                             'files':files,'tools':tools,'version':'Python3.14.6/SymPy1.14.0',
                             'scope':'Existing approved SymPy/mpmath source/resource trees plus interpreter/config;does not pin every OS shared library or stdlib file.'})
print(json.dumps({'status':'PREPARED','external_files':len(external),'primary_sources':len(sources),
                  'dependency_files':len(files),'prepared_utc':now},sort_keys=True))
