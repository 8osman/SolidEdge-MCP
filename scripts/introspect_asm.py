import win32com.client
import pythoncom
from win32com.client import GetObject
import pywintypes

def connect_to_se():
    """Try multiple methods to get the real SE app with documents"""

    # Method 1: ROT moniker binding (you already have this working partially)
    ctx = pythoncom.CreateBindCtx(0)
    rot = pythoncom.GetRunningObjectTable()

    for moniker in rot:
        try:
            name = moniker.GetDisplayName(ctx, None)
            obj = moniker.BindToObject(ctx, None, pythoncom.IID_IDispatch)
            wrapped = win32com.client.Dispatch(obj)

            # Check if it's SE app or a document directly
            if hasattr(wrapped, 'Documents'):
                print(f"Found app via ROT: {name}, docs: {wrapped.Documents.Count}")
                return wrapped, None
            elif hasattr(wrapped, 'AssemblyFeatures'):
                print(f"Found assembly doc directly via ROT: {name}")
                return None, wrapped
            elif hasattr(wrapped, 'Models'):
                print(f"Found part doc via ROT: {name}")
        except Exception as e:
            pass

    return None, None

app, direct_doc = connect_to_se()

doc = None
if direct_doc:
    doc = direct_doc
elif app:
    # Try each document
    for i in range(1, app.Documents.Count + 1):
        try:
            d = app.Documents.Item(i)
            if hasattr(d, 'AssemblyFeatures'):
                doc = d
                print(f"Found assembly doc at index {i}")
                break
        except Exception as e:
            print(f"Doc {i} error: {e}")

if not doc:
    # Method 2: Try binding the ROT entry by CLSID directly
    try:
        # SE Assembly document CLSID
        for clsid in [
            '{2FC1EFA0-D400-11CE-8732-0800363A1E02}',  # PartDocument
            '{2FC1EFA1-D400-11CE-8732-0800363A1E02}',  # AssemblyDocument
        ]:
            try:
                obj = GetObject(f"clsid:{clsid}")
                if hasattr(obj, 'AssemblyFeatures'):
                    doc = obj
                    print(f"Got doc via CLSID {clsid}")
                    break
            except:
                pass
    except Exception as e:
        print(f"CLSID method failed: {e}")

if not doc:
    print("Could not get document. Try running from within SE's macro environment.")
else:
    print(f"\nGot doc: {doc}")
    print("\n=== ASSEMBLY FEATURES ===")
    try:
        asm = doc.AssemblyFeatures
        print(f"AssemblyFeatures object: {asm}")

        for attr in sorted(dir(asm)):
            if attr.startswith("_"):
                continue
            try:
                coll = getattr(asm, attr)
                adds = [m for m in dir(coll) if m.startswith("Add")]
                if adds:
                    print(f"\n{attr}:")
                    for a in adds:
                        print(f"  {a}")
            except:
                pass
    except Exception as e:
        print(f"AssemblyFeatures failed: {e}")
