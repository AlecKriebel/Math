"""Read-only evidence authentication; writes only its new root adoption receipt."""
from pathlib import Path
import hashlib
import json
import stat
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
PAPER = ROOT.parent.parent


def mode(value):
    return value if isinstance(value, int) else int(value, 8)


def pin(path):
    assert path.is_file() and not path.is_symlink(), str(path)
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data),
            "SHA256": hashlib.sha256(data).hexdigest(),
            "mode": stat.S_IMODE(path.stat().st_mode)}


def authenticate(base, name, key, exclusions):
    manifest = json.loads((base / name).read_text())
    assert stat.S_IMODE(base.stat().st_mode) == mode(manifest["root_mode"])
    expected = {item["path"]: item for item in manifest[key]}
    actual_files, actual_dirs = {}, {}
    for path in sorted(base.rglob("*")):
        assert not path.is_symlink(), str(path)
        relative = path.relative_to(base).as_posix()
        if path.is_file():
            actual_files[relative] = pin(path)
        else:
            assert path.is_dir(), str(path)
            actual_dirs[relative] = stat.S_IMODE(path.stat().st_mode)
    assert set(actual_files) == set(expected) | set(exclusions)
    for relative, item in expected.items():
        actual = actual_files[relative]
        assert actual["bytes"] == item["bytes"], relative
        assert actual["SHA256"] == item["SHA256"], relative
        assert actual["mode"] == mode(item["mode"]), relative
    expected_dirs = {item["path"]: mode(item["mode"]) for item in manifest["directories"]}
    assert actual_dirs == expected_dirs
    return {"manifest": pin(base / name), "all_files": list(actual_files.values()),
            "child_directories": actual_dirs, "files": len(actual_files),
            "payloads": len(expected), "all_bytes_modes_topology_exact": True}


source = authenticate(PAPER / "sources", "SOURCE_MANIFEST.json", "files",
                      ["SOURCE_MANIFEST.json", "SOURCE_FINAL.json"])
scope = authenticate(PAPER / "reviews/scope-sol", "OWNED_MANIFEST.json", "payloads",
                     ["OWNED_MANIFEST.json", "FINAL.json"])
adversarial = authenticate(PAPER / "reviews/adversarial-sol", "OWNED_MANIFEST.json", "files",
                           ["OWNED_MANIFEST.json", "FINAL.json"])
initial = json.loads((ROOT / "INITIAL_MANIFEST.json").read_text())
for item in initial["files"]:
    actual = pin(ROOT / item["path"])
    assert actual["bytes"] == item["bytes"]
    assert actual["SHA256"] == item["SHA256"]
    assert actual["mode"] == mode(item["mode"])
assert pin(ROOT / "INITIAL_SEAL.json")["SHA256"] == "df7b4ac5601d36c8fb678580216aacc199982429312a880b70d0ee997edba609"
primary = [
    (Path('/Users/alec/Documents/Math/radial_statistical_counterexample/tmp/original_1998.pdf'), 'fa552d73c0f1e1017608102a7a80eff048cd3d95ed413ae04c2fdf710da3b8f5', 'PDF identity; actual printed125/126/127 pixels read from authenticated family rasters'),
    (Path('/Users/alec/Documents/Math/radial_statistical_counterexample/tmp/kurose_1994.pdf'), 'adfe06cd01217b31e82d3371dd7cd50803c3ff24380a168b2db215883875d138', 'printed428 pixels and official parsed427–429 text personally read; no whole-body claim'),
    (PAPER/'reviews/scope-sol/primary-pages/fmu-1.png', '30ea9a37ae6a8c1f1e6d640201541b9d7b1c24779c8cbee9562758504e047fbe', 'printed125 pixels'),
    (PAPER/'reviews/scope-sol/primary-pages/fmu-2.png', '1f61dbba01a4676c7ce763ebcb587e588723de718992d8e72fdcf9e53e20d2cd', 'printed126 pixels, exact3(e)'),
    (PAPER/'reviews/adversarial-sol/primary-pages/fmu-3.png', '652423fbf0b6a336cd7b0ed6d8f0e028351db61f5ec3186d1a9a049040a6e265', 'printed127 pixels, references'),
    (PAPER/'reviews/scope-sol/primary-pages/kurose428.png', '82f6c8468f94b0c42a7c2c14328dc2b1f839ba6bda2289e216074fd457f20470', 'printed428 pixels, alpha/conformal definition and dual criterion'),
    (Path('/Users/alec/Documents/Math/radial_statistical_counterexample/tmp/priority_supplied_pdfs/matsuzoe1999-p178.png'), 'af6cad1cc1999c8f623562f545f507e967192572c0bd5aa5ccbf03f48f258f05', 'printed178 pixels,2.1 and metric relation'),
    (Path('/Users/alec/Documents/Math/radial_statistical_counterexample/tmp/priority_supplied_pdfs/matsuzoe1999_agent/page-01.png'), 'a4ca52a94f1f0477f4e2cfb093191d7e781ac0d00140438434cdf917909f8156', 'printed175 title/edition and introduction pixels')]
primary_pins = []
for path, expected_hash, extent in primary:
    actual = pin(path)
    assert actual['SHA256'] == expected_hash, str(path)
    actual['root_personally_read_extent'] = extent
    primary_pins.append(actual)
native = json.loads((PAPER/'sources/record.response.body').read_text())
originals = []
for item in native['files']:
    path = PAPER/'sources/assets'/item['key']
    data = path.read_bytes()
    assert len(data) == item['size']
    assert item['checksum'] == 'md5:' + hashlib.md5(data).hexdigest()
    originals.append(pin(path))
assert [item['key'] for item in native['files']] == ['SHA256SUMS.txt','source-and-verification.zip','paper.pdf']
receipt = {'UTC': datetime.now(timezone.utc).isoformat(), 'row':184,'record':22983519,
           'source':source,'scope':scope,'adversarial':adversarial,
           'original_root_INITIAL_unchanged':True,'native_ordered_originals':originals,
           'primary_finite_references':primary_pins,
           'cached_current_host_byte_equivalence_claimed':False,
           'complete_Matsuzoe1999_body_read_or_acquired':False,
           'scientific_programs_executed_by_this_helper':0,
           'root_new_scientific_native_runs':0,'source_or_peer_writes':False}
target=ROOT/'ROOT_FINAL_EVIDENCE_ADOPTION.json'
assert not target.exists()
target.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'result':'authenticated','source_files':source['files'],
                  'scope_files':scope['files'],'adversarial_files':adversarial['files'],
                  'primary_references':len(primary_pins),'receipt':pin(target)}))
