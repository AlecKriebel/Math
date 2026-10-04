"""Finalize this family only, with a captured native worker and parent HOLD inventory."""
from pathlib import Path
import datetime,hashlib,json,stat,subprocess,sys
root=Path(__file__).resolve().parent
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
baseline=json.loads((root/'baseline-freeze.json').read_bytes())
for name,want in baseline['sha256'].items():
    if sha((root/name).read_bytes())!=want:raise RuntimeError('Frozen independent baseline altered: '+name)

if '--worker' in sys.argv:
    updates=[
      ('2026-10-04T12:43:54.542125+00:00','Fresh generic Vieta tangent/secant derivation; exact kernel resultants and full Tate disc=5^11 Delta^22. Completion estimate: 45%.'),
      ('2026-10-04T12:47:30.320145+00:00','All inverse denominators and exact marked infinity slopes pass. Allowed lambda_v=-(13+5r)/2 gives two distinct torsion normalization points at each plane vertex. Two failed checker bodies/streams preserved before corrections. Completion estimate: 70%.'),
      ('2026-10-04T12:48:47.690661+00:00','Fresh finite direct-law enumeration passes 532 fibers/44308 points, 360 residual inverse checks and five finite vertex collisions. Finite evidence kept separate from universal proof. Completion estimate: 80%.'),
      ('2026-10-04T12:51:37.912498+00:00','Four public exports match archive and historical bodies exactly up to declared guard/path changes; PORTABILITY entries unchanged v01-v03. Coefficient dependency qualified. Completion estimate: 90%.'),
      ('2026-10-04T12:53:52.128051+00:00','All public generic coefficient outputs and all11 visually read actual Morton v4 p5 rows agree exactly with fresh derivation. Third local implementation failure preserved before correction. Completion estimate: 95%.'),
      (now(),'Detailed report/claim ledger complete. Baseline preservation rechecked. Assigned family audit completion estimate: 100%; HOLD for parent closure, no publication seal.')]
    with (root/'RESEARCH_LOG.md').open('a') as f:
        for utc,msg in updates:f.write('\n'+utc+' — '+msg+'\n')
    status={'family':'kernel/direct-group-law','status':'HOLD_FOR_PARENT_CLOSURE','completion_estimate_percent':100,
      'completed_utc':now(),'publication_seal':False,'report':'REPORT.md',
      'strongest_verified_result':'Universal direct chord iff fifth-kernel proof, full Tate discriminant/resultants and 25-point count; no residual inverse poles; exact marked infinity subgroup.',
      'boundary_finding':'At allowed lambda=-(13+5sqrt5)/2 two distinct fifth-torsion normalization points share each of five plane vertex images.',
      'remaining_dependencies':['Global whole-plane normalization C003, separate geometry family','Division-field/source/priority claims outside kernel scope','Parent extracted-package fresh replay'],
      'failed_checker_executions_preserved':['map_boundaries_v01','map_boundaries_v02','extra_exact_v01']}
    (root/'FINAL_FAMILY_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
    receipts={p.parent.name:json.loads(p.read_bytes()) for p in sorted((root/'native').glob('*/execution.json'))}
    artifacts={str(p.relative_to(root)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ['EVIDENCE_INVENTORY.json','HOLD_INVENTORY.json']}
    (root/'EVIDENCE_INVENTORY.json').write_text(json.dumps({'created_utc':now(),'completion_estimate_percent':100,
      'scope':'Evidence inventory before finalizer native receipt; HOLD_INVENTORY covers final complete namespace. No publication approval.',
      'source_only_baseline_preserved':True,'receipts':receipts,'artifacts':artifacts},indent=2)+'\n')
    print(json.dumps(status,indent=2))
    sys.exit(0)

argv=[sys.executable,str(Path(__file__).resolve()),'--worker']
started=now();r=subprocess.run(argv,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE);ended=now()
native=root/'native/finalize_family';native.mkdir(parents=True,exist_ok=True)
(native/'stdout.bin').write_bytes(r.stdout);(native/'stderr.bin').write_bytes(r.stderr)
receipt={'argv':argv,'cwd':str(root),'started_utc':started,'ended_utc':ended,'exit_code':r.returncode,
 'body_path':str(Path(__file__).resolve()),'body_sha256':sha(Path(__file__).read_bytes()),
 'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)}
(native/'execution.json').write_text(json.dumps(receipt,indent=2)+'\n')
if r.returncode:sys.stdout.buffer.write(r.stdout);sys.stderr.buffer.write(r.stderr);sys.exit(r.returncode)
files={str(p.relative_to(root)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'mode':f'{stat.S_IMODE(p.stat().st_mode):04o}'} for p in sorted(root.rglob('*')) if p.is_file() and p.name!='HOLD_INVENTORY.json'}
dirs={str(p.relative_to(root)):f'{stat.S_IMODE(p.stat().st_mode):04o}' for p in sorted(root.rglob('*')) if p.is_dir()}
hold={'held_utc':now(),'status':'HOLD_FOR_PARENT_CLOSURE','publication_seal':False,
 'scope':'Final family namespace inventory, excluding this self-referential inventory only. No further family writes pending parent closure.',
 'completion_estimate_percent':100,'files':files,'directory_modes':dirs}
(root/'HOLD_INVENTORY.json').write_text(json.dumps(hold,indent=2)+'\n')
print(json.dumps({'finalizer_worker_receipt':receipt,'report_sha256':files['REPORT.md']['sha256'],
 'hold_inventory_sha256':sha((root/'HOLD_INVENTORY.json').read_bytes()),'held_utc':hold['held_utc'],
 'owned_payload_files':len(files),'completion_estimate_percent':100,'publication_seal':False},indent=2))
sys.stdout.flush();sys.stdout.buffer.write(r.stdout)
