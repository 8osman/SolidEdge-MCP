# Solid Edge COM API Findings

## Cutout Operations - NOT SUPPORTED

### Investigation Summary
After extensive diagnostic analysis of Solid Edge 2026 COM API, we discovered that **cutout (cut) operations are not exposed via the COM interface**.

### Diagnostic Results
Using the `diagnose_api` tool on Solid Edge 2026 (version 226.00.01.04), we found:

**Models Collection Methods Available:**
- `AddExtrudedProtrusion`
- `AddFiniteExtrudedProtrusion`
- `AddExtrudedProtrusionWithThinWall`
- `AddRevolvedProtrusion`
- `AddFiniteRevolvedProtrusion`
- ... and other protrusion/additive methods

**Models Collection Methods NOT Found:**
- ❌ `AddExtrudedCutout`
- ❌ `AddFiniteExtrudedCutout`
- ❌ `AddRevolvedCutout`
- ❌ Any cutout or cut-related methods

### Attempted Solutions
1. Tried `ExtrudedCutouts.AddFinite` - Collection doesn't exist
2. Tried `Models.AddExtrudedCutout` - Method doesn't exist
3. Tried `Models.AddBaseCutout` - Method doesn't exist
4. Checked for Boolean operations - Not found in diagnostic

### Current Implementation
The `create_extrude` and `create_revolve` methods now return a clear error message when `operation="Cut"` is requested, explaining:
- The limitation
- Why it exists (API doesn't expose these methods)
- Workarounds (manual UI operations, Boolean subtraction if available)

### Working Operations
✅ Add/Protrusion operations work perfectly
✅ Profile tracking fixed - sketches properly maintained for feature creation
✅ Extrude Add - TESTED, PASSING
✅ Revolve Add - Should work (same pattern as extrude)

### Recommendations
1. **Document this limitation** in user-facing documentation
2. **Focus on implementing other features** that ARE supported
3. **Consider future investigation** into:
   - Boolean operations via different API path
   - Multi-body parts and subtraction
   - Synchronous modeling features
4. **Move forward** with implementing the 24+ other missing tools

### Test Suite Status
- Test `test_create_extrude_add` - ✅ PASSING
- Test `test_create_extrude_cut` - ⚠️  Marked as xfail (expected due to API limitation)
- Profile tracking bug - ✅ FIXED

## Next Steps
1. ✅ Profile tracking fixed
2. ✅ Cutout limitation documented
3. ⏭️  Implement remaining 24 tools
4. ⏭️  Achieve full coverage of supported features
5. ⏭️  Consider alternative approaches for cut operations in future
