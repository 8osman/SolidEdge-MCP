"""
Probe v6 - finds where hole feature lands, supplies real profile to pats.Add,
tests mirror safely (one call at a time, check SE alive after each).

Run:  cd C:/Users/admin/SolidEdge-MCP && .venv/Scripts/python.exe probe_and_patch.py
"""
import win32com.client as w32
import pythoncom
import sys

pythoncom.CoInitialize()
sys.path.insert(0, r"C:\Users\admin\SolidEdge-MCP\src")

ASM_PATH = r"C:\Users\admin\Documents\damper_housing_parts\bottom_wall.asm"

def get_doc(se):
    try:
        d = se.ActiveDocument; _ = d.Name; return d
    except Exception: pass
    try:
        d = se.Documents.Item(1); _ = d.Name; return d
    except Exception: pass
    return se.Documents.Open(ASM_PATH)

def se_alive(se):
    try: _ = se.Version; return True
    except Exception: return False

def probe():
    se  = w32.GetActiveObject('SolidEdge.Application')
    doc = get_doc(se)
    print(f"Document: {doc.Name}")
    af  = doc.AssemblyFeatures

    rp1   = doc.AsmRefPlanes.Item(1)   # Top (xy)
    rp2   = doc.AsmRefPlanes.Item(2)   # Right (yz)
    occs  = doc.Occurrences
    scope = [occs.Item(i) for i in range(1, occs.Count + 1)]

    # ── Create hole ──────────────────────────────────────────────────────────
    print("\n--- Creating hole ---")
    ps1  = doc.ProfileSets.Add()
    prof1 = ps1.Profiles.Add(rp1)
    prof1.Circles2d.AddByCenterRadius(0.025, 0.025, 0.005)
    prof1.End(1)

    hole_feat = af.AssemblyFeaturesHoles.Add(
        len(scope), scope, 1, (prof1,), 2, None, 16, 0.0,
        None, None, None, None,
    )
    print(f"  hole_feat={hole_feat}, Name={getattr(hole_feat,'Name','?')}")

    # ── Where does the hole actually appear? ─────────────────────────────────
    print("\n--- All collection counts after hole creation ---")
    all_colls = [
        'AssemblyFeaturesExtrudedCutouts', 'AssemblyFeaturesHoles',
        'AssemblyFeaturesMirrors', 'AssemblyFeaturesPatterns',
        'AssemblyFeaturesRevolvedCutouts', 'AssemblyFeaturesSweptProtrusions',
        'ExtrudedProtrusions', 'RevolvedProtrusions',
        'FilletWelds', 'Threads',
    ]
    found_feat = None
    found_coll = None
    for cn in all_colls:
        try:
            coll = getattr(af, cn)
            cnt  = coll.Count
            print(f"  {cn}: {cnt}")
            for i in range(1, cnt + 1):
                item = coll.Item(i)
                nm   = getattr(item, 'Name', '?')
                print(f"    [{i}] {nm}")
                if found_feat is None:
                    found_feat = item
                    found_coll = cn
        except Exception as e:
            print(f"  {cn}: ERROR {e}")

    if found_feat is None:
        # hole_feat itself is valid even if not in any enumerable collection
        found_feat = hole_feat
        print("  (using hole_feat directly — not found in any collection)")

    print(f"\n  Using feature from: {found_coll or 'direct'}")
    print(f"  Feature type: {type(found_feat)}")
    attrs = sorted(a for a in dir(found_feat) if not a.startswith('_'))
    print(f"  Feature attrs: {attrs}")

    # ── Pattern Add — with a real profile ────────────────────────────────────
    # The profile defines the pattern layout (point locations for each instance)
    # For rectangular: draw points at each target location
    # Try first with None, then with a profile containing points
    print("\n--- Pattern Add with profile ---")
    pats = af.AssemblyFeaturesPatterns

    # Profile with two points defining a rectangular offset
    ps2  = doc.ProfileSets.Add()
    prof2 = ps2.Profiles.Add(rp1)
    prof2.Points2d.Add(0.025, 0.025)    # original location
    prof2.Points2d.Add(0.075, 0.025)    # +50mm in X
    prof2.End(1)

    for pt in (0, 1, 2, 3):
        for profile_arg in (None, prof2):
            for feat_arg in ((found_feat,), [found_feat]):
                label = f"type={pt} prof={'None' if profile_arg is None else 'prof2'} " \
                        f"feat={'tuple' if isinstance(feat_arg,tuple) else 'list'}"
                try:
                    r = pats.Add(1, feat_arg, profile_arg, pt)
                    print(f"  SUCCESS {label}: {getattr(r,'Name','?')}")
                    # undo immediately so we can try other combos
                    try: doc.Undo()
                    except Exception: pass
                    break
                except Exception as e:
                    # Only print first error per combo to keep output manageable
                    errmsg = str(e)
                    print(f"  FAIL    {label}: {errmsg[:80]}")
            if not se_alive(se):
                print("  SE DIED — stopping pattern tests")
                return

    # ── Mirror Add — one call, check alive ───────────────────────────────────
    print("\n--- Mirror Add (careful) ---")
    if not se_alive(se):
        print("  SE not alive, skipping")
        return

    mirs = af.AssemblyFeaturesMirrors
    # Try only tuple+type=0 first (safest)
    try:
        r = mirs.Add(1, (found_feat,), rp2, 0)
        print(f"  SUCCESS tuple type=0 rp2: {getattr(r,'Name','?')}")
    except Exception as e:
        print(f"  FAIL    tuple type=0 rp2: {e}")

    if not se_alive(se):
        print("  SE died after mirror attempt")
        return

    try:
        r = mirs.Add(1, (found_feat,), rp2, 1)
        print(f"  SUCCESS tuple type=1 rp2: {getattr(r,'Name','?')}")
    except Exception as e:
        print(f"  FAIL    tuple type=1 rp2: {e}")


if __name__ == '__main__':
    probe()
