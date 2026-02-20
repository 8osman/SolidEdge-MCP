import win32com.client
app = win32com.client.GetActiveObject("SolidEdge.Application")
doc = app.ActiveDocument

# Check both collection types
try:
    ps_count = doc.ProfileSets.Count
    print(f"ProfileSets.Count: {ps_count}")
except Exception as e:
    print(f"ProfileSets failed: {e}")

try:
    sk_count = doc.Sketches.Count
    print(f"Sketches.Count: {sk_count}")
    if sk_count > 0:
        sk = doc.Sketches.Item(1)
        print(f"Sketch type: {type(sk)}")
        print(f"Sketch methods: {[m for m in dir(sk) if not m.startswith('_')]}")
except Exception as e:
    print(f"Sketches failed: {e}")