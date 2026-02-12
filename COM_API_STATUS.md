# Solid Edge COM API Status - Introspection vs Testing

This document shows what runtime introspection reveals versus what we've proven through actual testing.

## Legend
- ✅ **Working**: Tested and confirmed working
- ❌ **Failing**: Tested but not working yet
- ❓ **Unknown**: Not yet tested
- 🔍 **Partially Known**: Some aspects work, others unclear

---

## 1. SKETCHING API

### Profile Management

| Method | Parameters (from introspection) | Status | Known Working Pattern | Unknown/Issues |
|--------|--------------------------------|--------|----------------------|----------------|
| `ProfileSets.Add` | None (no params) | ✅ | `profile_sets.Add()` | None |
| `Profiles.Add` | `RefPlane` | ✅ | `profiles.Add(ref_plane)` where ref_plane from RefPlanes.Item(1-3) | None |
| `Profile.End` | `ValidationOption` | ✅ | `profile.End(0)` | Other validation option values |

### 2D Geometry - Lines

| Method | Parameters | Status | Known Working Pattern | Unknown/Issues |
|--------|-----------|--------|----------------------|----------------|
| `Lines2d.AddBy2Points` | `x1, y1, x2, y2` | ✅ | `lines.AddBy2Points(0, 0, 0.05, 0)` (meters) | None |

### 2D Geometry - Circles

| Method | Parameters | Status | Known Working Pattern | Unknown/Issues |
|--------|-----------|--------|----------------------|----------------|
| `Circles2d.AddByCenterRadius` | `cx, cy, radius` | ✅ | `circles.AddByCenterRadius(0.1, 0.1, 0.02)` | None |

### 2D Geometry - Arcs

| Method | Parameters | Status | Known Working Pattern | Unknown/Issues |
|--------|-----------|--------|----------------------|----------------|
| `Arcs2d.AddByCenterStartEnd` | `xc, yc, xs, ys, xe, ye` | ✅ | `arcs.AddByCenterStartEnd(cx, cy, sx, sy, ex, ey)` | None |

### 2D Geometry - Ellipses

| Method | Parameters | Status | Known Working Pattern | Unknown/Issues |
|--------|-----------|--------|----------------------|----------------|
| `Ellipses2d.AddByCenter` | `cx, cy, major_radius, minor_radius, axis_x, axis_y` | ✅ | `ellipses.AddByCenter(cx, cy, 0.04, 0.02, cos(angle), sin(angle))` - axis is unit vector | None |
| ~~`Ellipses2d.AddByCenterRadii`~~ | N/A | ❌ | Does not exist | Method doesn't exist |

### 2D Geometry - Splines

| Method | Parameters | Status | Known Working Pattern | Unknown/Issues |
|--------|-----------|--------|----------------------|----------------|
| `Splines2d.AddByPoints` | `Order, NumPoints, PointArray` | ✅ | `splines.AddByPoints(3, num_points, tuple(x1,y1,x2,y2,...))` - POSITIONAL ONLY | Must use positional args, not keywords. PointArray is flattened tuple |

### 2D Geometry - Polygons

| Method | Parameters | Status | Known Working Pattern | Unknown/Issues |
|--------|-----------|--------|----------------------|----------------|
| `Circles2d.AddAsPolygon` | `NumberOfSides, CenterX, CenterY, Radius, Angle` | ✅ | Tested via draw_polygon | Actual method signature needs verification |

---

## 2. EXTRUSION API

### AddFiniteExtrudedProtrusion

| Aspect | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| **Full Signature** | `(NumberOfProfiles, ProfileArray, ProfilePlaneSide, ExtrusionDistance, KeyPointOrTangentFace, KeyPointFlags, FromSurfOrRefPlane, ToSurfOrRefPlane)` - 8 params total | 🔍 | Partial | Full 8-param signature untested |
| **Simple Usage** | See above | ✅ | `models.AddFiniteExtrudedProtrusion(NumberOfProfiles=1, ProfileArray=(profile,), ProfilePlaneSide=ExtrudedProtrusion.igRight, ExtrusionDistance=0.03)` | Last 4 params (KeyPoint*, FromSurf*, ToSurf*) not tested |
| **ProfileArray Type** | PyOleMissing default | ✅ | **MUST be tuple**: `(profile,)` NOT list `[profile]` | List fails with conversion error |
| **Keyword Args** | POSITIONAL_OR_KEYWORD | ✅ | Accepts keyword arguments | None |
| **Direction Constants** | Not in signature | ✅ | `ExtrudedProtrusion.igRight` (normal), `.igLeft` (reverse), `.igSymmetric` | None |

### AddFiniteExtrudedCutout

| Aspect | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| **Simple Usage** | Same as AddFiniteExtrudedProtrusion | ✅ | `models.AddFiniteExtrudedCutout(NumberOfProfiles=1, ProfileArray=(profile,), ProfilePlaneSide=dir, ExtrusionDistance=depth)` | None |

### AddExtrudedProtrusion (full signature)

| Aspect | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| **Full Signature** | 34 parameters including TreatmentType, Draft, Crown options | ❓ | Not tested | Not needed for basic extrusion |

---

## 3. REVOLVE API

### AddRevolvedProtrusion

| Aspect | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| **Full Signature** | `(NumberOfProfiles, ProfileArray, RefAxis, ProfileSide, ExtentType1, ExtentSide1, FiniteAngle1, KeyPointOrTangentFace1, KeyPointFlags1, ExtentType2, ExtentSide2, FiniteAngle2, KeyPointOrTangentFace2, KeyPointFlags2)` - 14 params | ❌ | **NONE** | All attempts fail |
| **Attempt 1: Keywords** | POSITIONAL_OR_KEYWORD | ❌ | `models.AddRevolvedProtrusion(NumberOfProfiles=1, ProfileArray=(profile,), FiniteAngle1=angle)` | Error: "Invalid number of parameters" |
| **Attempt 2: All 14 params** | All PyOleMissing defaults | ❌ | With pythoncom.Empty for optional params | Error: "Parameter not optional" |
| **Attempt 3: Simple positional** | N/A | ❌ | `models.AddRevolvedProtrusion(1, (profile,), angle)` | Error: "Invalid number of parameters" |
| **ProfileArray Type** | PyOleMissing | ❌ | Tried tuple `(profile,)` and list `[profile]` | Both fail with "Python instance can not be converted to COM object" |
| **Required Parameters** | All show PyOleMissing | ❓ | Unknown which are truly required | Despite PyOleMissing defaults, some are required |
| **RefAxis** | PyOleMissing | ❓ | Unknown what to pass or if None/Empty acceptable | May need actual axis object |
| **ProfileSide** | PyOleMissing | ❓ | Unknown what constant/value | No documentation |
| **ExtentType1/2** | PyOleMissing | ❓ | Unknown what constant/value | May be from FeaturePropertyConstants enum |

### AddFiniteRevolvedProtrusion

| Aspect | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| **Existence** | Listed in dir(models) | ❓ | Not yet tested | May be simpler than full AddRevolvedProtrusion |
| **Signature** | Not yet introspected | ❓ | Unknown | Need to run introspection |

### AddRevolvedProtrusionSync

| Aspect | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| **Existence** | Listed in dir(models) | ❓ | Not tested | Unknown purpose of "Sync" variant |

---

## 4. PRIMITIVE CREATION API

### AddBoxByCenter

| Aspect | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| **Full Signature** | `(x, y, z, dWidth, dHeight, dAngle, dDepth, pPlane, ExtentSide, vbKeyPointExtent, pKeyPointObj, pKeyPointFlags)` - 12 params | ❌ | **NONE** | All attempts fail |
| **Basic Params (1-7)** | `x, y, z, dWidth, dHeight, dAngle, dDepth` | ❌ | Tried: `models.AddBoxByCenter(0, 0, 0, 0.1, 0.1, 0, 0.1)` | Error: Invalid parameters or conversion errors |
| **pPlane** | PyOleMissing | ❓ | Unknown - reference plane object? None? | Unclear what to pass |
| **ExtentSide** | PyOleMissing | ❓ | Unknown - constant value? | May be from ExtentTypeConstants |
| **vbKeyPointExtent** | PyOleMissing | ❓ | Unknown - boolean? | "vb" prefix suggests VB Boolean |
| **pKeyPointObj** | PyOleMissing | ❓ | Unknown - object or None? | "p" prefix suggests pointer/object |
| **pKeyPointFlags** | PyOleMissing | ❓ | Unknown - flags integer? | Likely bitwise flags |
| **dAngle** | In signature | ❓ | Unknown purpose - rotation angle? | Unclear what this rotates |

### AddCylinderByCenterAndRadius

| Aspect | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| **Full Signature** | `(x, y, z, dRadius, dDepth, pPlane, ExtentSide, vbKeyPointExtent, pKeyPointObj, pKeyPointFlags)` - 10 params | ❌ | **NONE** | All attempts fail |
| **Basic Params (1-5)** | `x, y, z, dRadius, dDepth` | ❌ | Tried: `models.AddCylinderByCenterAndRadius(0, 0, 0, 0.03, 0.15)` | Error: Invalid parameters |
| **pPlane** | PyOleMissing | ❓ | Unknown - which plane to extrude from? | Unclear |
| **ExtentSide** | PyOleMissing | ❓ | Unknown - direction constant? | Unclear |
| **vbKeyPointExtent** | PyOleMissing | ❓ | Unknown | Unclear |
| **pKeyPointObj** | PyOleMissing | ❓ | Unknown | Unclear |
| **pKeyPointFlags** | PyOleMissing | ❓ | Unknown | Unclear |

### AddSphereByCenterAndRadius

| Aspect | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| **Full Signature** | `(x, y, z, dRadius, pPlane, ExtentSide, vbKeyPointExtent, vbCreateLiveSection, pKeyPointObj, pKeyPointFlags)` - 10 params | ❌ | **NONE** | All attempts fail |
| **Basic Params (1-4)** | `x, y, z, dRadius` | ❌ | Tried: `models.AddSphereByCenterAndRadius(0, 0, 0, 0.04)` | Error: Invalid parameters |
| **vbCreateLiveSection** | PyOleMissing | ❓ | Unknown - create as half sphere with section? | "LiveSection" suggests cross-section feature |
| **Other params** | See cylinder | ❓ | Same unknowns as cylinder | Same issues |

### Alternative Box Methods

| Method | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| `AddBoxByTwoPoints` | Listed in dir(models) | ❓ | Not tested | May be simpler - define by diagonal corners? |
| `AddBoxByThreePoints` | Listed in dir(models) | ❓ | Not tested | Unknown what three points define |

---

## 5. QUERY & MEASUREMENT API

### Physical Properties

| Property/Method | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|----------------|---------------------|--------|----------------------|----------------|
| `document.PhysicalProperties` | Object with properties | ✅ | `props = doc.PhysicalProperties` | None |
| `PhysicalProperties.Volume` | Property | ✅ | `props.Volume` returns cubic meters | None |
| `PhysicalProperties.Mass` | Property | ✅ | `props.Mass` returns kg | Requires material/density to be set |
| `PhysicalProperties.Area` | Property | ✅ | `props.Area` returns square meters (surface area) | None |
| `PhysicalProperties.CenterOfGravityX/Y/Z` | Properties | ✅ | Individual properties for COM coordinates | None |

### Bounding Box

| Method | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| `Model.RangeBox` | Property | 🔍 | `model.RangeBox` returns tuple of 6 values | Exact return format needs verification (min/max coords) |

### Feature Count

| Method | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| `Models.Count` | Property | ✅ | `models.Count` returns integer | None |

---

## 6. VIEW & DISPLAY API

### View Orientation

| Method/Constant | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|-----------------|---------------------|--------|----------------------|----------------|
| `ViewOrientationConstants.seIsoView` | Enum constant | ✅ | Constant exists and resolves | Actual method to SET view unclear |
| `ViewOrientationConstants.seTopView` | Enum constant | ✅ | Constant exists | Same |
| `ViewOrientationConstants.seFrontView` | Enum constant | ✅ | Constant exists | Same |
| `View.SetNamedView()` | Not found | ❌ | Method doesn't exist | Need to find actual method name |
| `Window.SetNamedView()` | Not found | ❌ | Method doesn't exist | Alternative not found |

### Display Mode

| Method/Constant | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|-----------------|---------------------|--------|----------------------|----------------|
| `DisplayStyleConstants.seDisplayFlat` | Enum constant | ✅ | Constant exists | How to apply it? |
| `DisplayStyleConstants.seDisplayWireframe` | Enum constant | ✅ | Constant exists | Same |
| `View.DisplayMode` | Property likely exists | ❌ | Setting it causes COM exception | May be read-only or need different approach |

### Zoom Operations

| Method | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| `View.Fit()` | Method exists | ✅ | `view.Fit()` zooms to fit all geometry | None |

---

## 7. EXPORT API

### File Export

| Method | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| `document.SaveAs` | `(FileName, SaveAsType)` | ✅ | `doc.SaveAs(FileName=path, SaveAsType=ApplicationConstants.igFileTypeSTEP)` | None |
| `ApplicationConstants.igFileTypeSTEP` | Constant | ✅ | Works for STEP export | None |
| `ApplicationConstants.igFileTypeSTL` | Constant | ✅ | Works for STL export | None |

### Image Capture

| Method | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| `View.SaveAsImage` | `(Filename, Width, Height, BackgroundScheme)` | ✅ | `view.SaveAsImage(Filename=path, Width=1920, Height=1080, BackgroundScheme=ImageFileConstants.seImageFileBackgroundSchemeWhite)` | Other BackgroundScheme options not tested |

---

## 8. DOCUMENT MANAGEMENT API

### Document Creation

| Method | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| `Documents.Add` | `DocumentType` parameter | ✅ | `docs.Add("SolidEdge.PartDocument")` or with constant | String or constant both work |

### Document Save/Close

| Method | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| `Document.Save()` | No params | ✅ | `doc.Save()` | None |
| `Document.SaveAs()` | See Export section | ✅ | Works | None |
| `Document.Close()` | No params | 🔍 | `doc.Close()` but triggers save prompt | Need `doc.Saved = True` before Close to suppress |
| `Document.Saved` | Property | ✅ | Set to `True` to suppress save prompts | None |

---

## 9. REFERENCE PLANES API

| Method | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| `document.RefPlanes` | Collection | ✅ | `ref_planes = doc.RefPlanes` | None |
| `RefPlanes.Item(index)` | 1-based index | ✅ | `Item(1)=Top, Item(2)=Front, Item(3)=Right` | **1-based indexing!** |

---

## 10. ASSEMBLY API

### Component Management

| Method | Introspection Result | Status | Known Working Pattern | Unknown/Issues |
|--------|---------------------|--------|----------------------|----------------|
| `Occurrences.Add` | `(FileName, DestinationMatrix)` | 🔍 | Tested but matrix format unclear | 4x4 transformation matrix format needs docs |
| `Occurrences.AddByFilename` | `FileName` parameter | ✅ | `occurrences.AddByFilename(filepath)` places at origin | None |
| `Occurrences.Count` | Property | ✅ | Returns component count | None |
| `Occurrences.Item(index)` | 1-based index | ✅ | 1-based indexing | None |

---

## SUMMARY STATISTICS

### Overall Status
- **Total methods introspected**: ~50+
- **Fully working (✅)**: ~30 (60%)
- **Failing (❌)**: ~10 (20%)
- **Unknown/Untested (❓)**: ~10 (20%)

### Critical Gaps (blocking basic functionality)
1. **Revolve operations** - All variants failing
2. **Primitive creation** - Box, Cylinder, Sphere all failing
3. **View orientation setting** - Method name unclear
4. **Display mode setting** - COM exception

### What Works Well
- ✅ All 2D sketching operations
- ✅ Basic extrusion (protrusion and cutout)
- ✅ Document management (create, save, close)
- ✅ Query operations (mass properties, counts)
- ✅ Export (STEP, STL, images)
- ✅ Assembly component placement (basic)

### What Needs SDK Documentation
1. **Revolve**: Which parameters are required? What to pass for RefAxis, ProfileSide, ExtentType?
2. **Primitives**: What to pass for pPlane, ExtentSide, KeyPoint parameters?
3. **View Setting**: What's the actual method name to set view orientation?
4. **Display Mode**: How to properly set display style?

---

## NEXT STEPS

### Immediate Actions
1. ⏳ **Waiting on SDK documentation** from user
2. 🔍 **Try AddFiniteRevolvedProtrusion** - may be simpler than full AddRevolvedProtrusion
3. 🔍 **Try AddBoxByTwoPoints** - may be simpler than AddBoxByCenter

### Once SDK Available
1. Look up actual required parameters for revolve operations
2. Find documentation for pPlane, ExtentSide, KeyPoint parameters
3. Find correct method to set view orientation
4. Find correct approach for display mode

### Testing Priorities
1. Get revolve working (critical for basic functionality)
2. Get one primitive working (box/cylinder/sphere)
3. Get view orientation working
4. Test remaining untested methods
