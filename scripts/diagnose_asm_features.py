#!/usr/bin/env python
"""Diagnose the AssemblyFeatures COM API on the active assembly document."""

import inspect
import json
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pythoncom
import win32com.client

print("Step 0: Binding ROT entry (real running SE instance)...")
app = None
try:
    rot = pythoncom.GetRunningObjectTable()
    ctx = pythoncom.CreateBindCtx(0)
    enum = rot.EnumRunning()
    while True:
        monikers = enum.Next(1)
        if not monikers:
            break
        moniker = monikers[0]
        try:
            obj = rot.GetObject(moniker)
            idisp = obj.QueryInterface(pythoncom.IID_IDispatch)
            wrapped = win32com.client.Dispatch(idisp)
            if "ActiveDocument" in dir(wrapped):
                app = wrapped
                print("  Bound to SE Application object via ROT")
                break
        except Exception:
            pass
except Exception as e:
    print(f"  ROT bind failed: {e}")
    sys.exit(1)

if app is None:
    print("  Could not bind SE Application from ROT")
    sys.exit(1)

print("\nStep 1: Probing app state...")
for prop in ["Version", "ApprenticeMode", "ActiveDocumentType", "Visible"]:
    try:
        val = getattr(app, prop)
        print(f"  {prop} = {val}")
    except Exception as ex:
        print(f"  {prop} = ERROR: {ex}")

print("\nStep 2: Checking Documents collection on bound app...")
try:
    docs = app.Documents
    count = docs.Count
    print(f"  Documents.Count = {count}")
    for i in range(1, count + 1):
        try:
            d = docs.Item(i)
            print(f"    [{i}] Name={getattr(d, 'Name', '?')}")
        except Exception as ex:
            print(f"    [{i}] error: {ex}")
except Exception as e:
    print(f"  Documents failed: {e}")

print("\nStep 3: Trying ActiveWindow...")
try:
    win = app.ActiveWindow
    print(f"  ActiveWindow type: {type(win).__name__}")
    print(f"  ActiveWindow attrs: {[a for a in dir(win) if not a.startswith('_')][:20]}")
    # Try to get document from window
    for attr in ["Document", "Parent", "Object"]:
        try:
            d = getattr(win, attr)
            print(f"  ActiveWindow.{attr} type: {type(d).__name__}")
        except Exception:
            pass
except Exception as e:
    print(f"  ActiveWindow failed: {e}")

print("\nStep 4: All windows...")
try:
    wins = app.Windows
    print(f"  Windows.Count = {wins.Count}")
    for i in range(1, wins.Count + 1):
        try:
            w = wins.Item(i)
            print(f"    [{i}] type={type(w).__name__} Caption={getattr(w, 'Caption', '?')}")
        except Exception as ex:
            print(f"    [{i}] error: {ex}")
except Exception as e:
    print(f"  Windows failed: {e}")

print("\nStep 5: ActiveObject...")
try:
    obj = app.ActiveObject
    print(f"  ActiveObject type: {type(obj).__name__}")
    print(f"  ActiveObject attrs: {[a for a in dir(obj) if not a.startswith('_')][:20]}")
except Exception as e:
    print(f"  ActiveObject failed: {e}")

print("\nStep 6: Full app attribute list...")
all_app_attrs = [a for a in dir(app) if not a.startswith("_")]
print(f"  All app attrs ({len(all_app_attrs)}): {all_app_attrs}")
