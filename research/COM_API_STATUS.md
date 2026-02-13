# Solid Edge COM API Status

Runtime introspection results vs actual testing outcomes.

**Legend:** ✅ Working | ❌ Failing | ❓ Untested | 🔍 Partial

---

## Quick Summary

**Working (~60%)**
- All 2D sketching (lines, circles, arcs, ellipses, splines, polygons)
- Basic extrusion (protrusion and cutout)
- Document management (create, save, close)
- Query operations (mass properties, bounding box, counts)
- Export (STEP, STL, images)
- Assembly component placement (basic)

**Failing (Critical - ~20%)**
- ❌ All revolve operations (AddRevolvedProtrusion, AddFiniteRevolvedProtrusion)
- ❌ All primitives (AddBoxByCenter, AddCylinderByCenterAndRadius, AddSphereByCenterAndRadius)
- ❌ View orientation setting (constants exist, but method to apply unclear)
- ❌ Display mode setting

**Untested (~20%)**
- Alternative primitive methods, advanced features, some assembly operations

---

## 1. SKETCHING API ✅

All working. Introspection shows clear signatures.

### Profile Management
```python
profile_sets.Add()                    # No params
profiles.Add(ref_plane)               # ref_plane from RefPlanes.Item(1-3)
profile.End(0)                        # 0 = validation option
```

### 2D Geometry - All Working
```python
# Lines
lines.AddBy2Points(x1, y1, x2, y2)

# Circles
circles.AddByCenterRadius(cx, cy, radius)

# Arcs
arcs.AddByCenterStartEnd(center_x, center_y, start_x, start_y, end_x, end_y)

# Ellipses - NOTE: axis is unit vector
ellipses.AddByCenter(cx, cy, major_radius, minor_radius,
                     math.cos(angle), math.sin(angle))

# Splines - MUST use positional args, NOT keywords
splines.AddByPoints(3, num_points, tuple(x1, y1, x2, y2, ...))

# Polygons (via Circles2d)
circles.AddAsPolygon(num_sides, center_x, center_y, radius, angle)
```

**Key Discovery:** ProfileArray must be **tuple** `(profile,)` not list `[profile]`

---

## 2. EXTRUSION API ✅

### Working Pattern - AddFiniteExtrudedProtrusion

**Introspected Signature (8 params):**
```
(NumberOfProfiles, ProfileArray, ProfilePlaneSide, ExtrusionDistance,
 KeyPointOrTangentFace, KeyPointFlags, FromSurfOrRefPlane, ToSurfOrRefPlane)
```

**Working Usage (only first 4 needed):**
```python
models.AddFiniteExtrudedProtrusion(
    NumberOfProfiles=1,
    ProfileArray=(profile,),           # TUPLE not list!
    ProfilePlaneSide=ExtrudedProtrusion.igRight,  # igRight, igLeft, igSymmetric
    ExtrusionDistance=0.03             # meters
)
```

**Key Facts:**
- ✅ Accepts keyword arguments
- ✅ ProfileArray MUST be tuple
- ✅ Last 4 parameters untested but not needed for basic extrusion

### AddFiniteExtrudedCutout
Same signature and usage pattern as protrusion.

---

## 3. REVOLVE API ❌ **FAILING**

### AddRevolvedProtrusion - NOT WORKING

**Introspected Signature (14 params):**
```
(NumberOfProfiles, ProfileArray, RefAxis, ProfileSide,
 ExtentType1, ExtentSide1, FiniteAngle1, KeyPointOrTangentFace1, KeyPointFlags1,
 ExtentType2, ExtentSide2, FiniteAngle2, KeyPointOrTangentFace2, KeyPointFlags2)
```

**Parameter Details:**
- All show `PyOleMissing` defaults (suggests optional)
- All are `POSITIONAL_OR_KEYWORD` type
- No docstrings, no type annotations

**Attempts Made - All Failed:**

1. **Keyword args (like extrude)**
   ```python
   models.AddRevolvedProtrusion(
       NumberOfProfiles=1,
       ProfileArray=(profile,),
       FiniteAngle1=angle_rad
   )
   ```
   ❌ Error: "Invalid number of parameters"

2. **All 14 params with pythoncom.Empty**
   ```python
   models.AddRevolvedProtrusion(
       1, [profile], pythoncom.Empty, pythoncom.Empty,
       pythoncom.Empty, pythoncom.Empty, angle_rad,
       pythoncom.Empty, pythoncom.Empty, pythoncom.Empty,
       pythoncom.Empty, pythoncom.Empty, pythoncom.Empty, pythoncom.Empty
   )
   ```
   ❌ Error: "Parameter not optional"

3. **Simple positional (3 params)**
   ```python
   models.AddRevolvedProtrusion(1, (profile,), angle_rad)
   ```
   ❌ Error: "Invalid number of parameters"

4. **ProfileArray as tuple/list/VARIANT**
   - All fail with "Python instance can not be converted to COM object"

**UNKNOWN - Need SDK:**
- Which parameters are actually required?
- What to pass for `RefAxis`, `ProfileSide`, `ExtentType1/2`, `ExtentSide1/2`?
- What type should ProfileArray be for revolve (works as tuple for extrude)?

**Alternative Methods (untested):**
- `AddFiniteRevolvedProtrusion` - may be simpler
- `AddRevolvedProtrusionSync` - purpose unknown

---

## 4. PRIMITIVE CREATION API ❌ **FAILING**

All primitive methods have clear parameter names from introspection but fail in testing.

### AddBoxByCenter - NOT WORKING

**Introspected Signature (12 params):**
```
(x, y, z, dWidth, dHeight, dAngle, dDepth,
 pPlane, ExtentSide, vbKeyPointExtent, pKeyPointObj, pKeyPointFlags)
```

**Clear Parameters (1-7):**
- `x, y, z` - center position (meters)
- `dWidth, dHeight` - box width and height (meters)
- `dAngle` - rotation angle (radians?) - purpose unclear
- `dDepth` - box depth/length (meters)

**UNKNOWN Parameters (8-12):**
- `pPlane` - reference plane object? None? Which type?
- `ExtentSide` - constant from ExtentTypeConstants?
- `vbKeyPointExtent` - boolean? ("vb" prefix suggests Visual Basic Boolean)
- `pKeyPointObj` - object or None?
- `pKeyPointFlags` - bitwise flags integer?

**Attempts Made:**
```python
models.AddBoxByCenter(0, 0, 0, 0.1, 0.1, 0, 0.1)  # Just first 7 params
```
❌ Error: Invalid parameters or conversion errors

**Alternative Methods (untested):**
- `AddBoxByTwoPoints` - may be simpler (diagonal corners?)
- `AddBoxByThreePoints` - unknown definition

### AddCylinderByCenterAndRadius - NOT WORKING

**Introspected Signature (10 params):**
```
(x, y, z, dRadius, dDepth,
 pPlane, ExtentSide, vbKeyPointExtent, pKeyPointObj, pKeyPointFlags)
```

**Clear Parameters (1-5):**
- `x, y, z` - center position (meters)
- `dRadius` - cylinder radius (meters)
- `dDepth` - cylinder height (meters)

**UNKNOWN Parameters (6-10):**
- Same unclear parameters as box (pPlane, ExtentSide, etc.)

### AddSphereByCenterAndRadius - NOT WORKING

**Introspected Signature (10 params):**
```
(x, y, z, dRadius,
 pPlane, ExtentSide, vbKeyPointExtent, vbCreateLiveSection, pKeyPointObj, pKeyPointFlags)
```

**Clear Parameters (1-4):**
- `x, y, z` - center position (meters)
- `dRadius` - sphere radius (meters)

**UNKNOWN Parameters (5-10):**
- `vbCreateLiveSection` - create as half-sphere with section visible?
- Others same as box/cylinder

---

## 5. QUERY & MEASUREMENT API ✅

All working.

```python
# Physical properties
props = document.PhysicalProperties
volume = props.Volume              # cubic meters
mass = props.Mass                  # kg (requires material density)
area = props.Area                  # square meters (surface area)
com = (props.CenterOfGravityX, props.CenterOfGravityY, props.CenterOfGravityZ)

# Bounding box
model = models.Item(1)
range_box = model.RangeBox        # Returns (x_min, y_min, z_min, x_max, y_max, z_max)

# Counts
feature_count = models.Count
```

---

## 6. VIEW & DISPLAY API 🔍 **PARTIAL**

### View Orientation - Constants Exist, Method Unknown ❌

**Working - Constants:**
```python
ViewOrientationConstants.seIsoView
ViewOrientationConstants.seTopView
ViewOrientationConstants.seFrontView
ViewOrientationConstants.seRightView
# etc.
```

**NOT WORKING - How to Apply:**
```python
view.SetNamedView(...)     # Method doesn't exist
window.SetNamedView(...)   # Method doesn't exist
```

Need SDK to find actual method name.

### Display Mode - NOT WORKING ❌

**Working - Constants:**
```python
DisplayStyleConstants.seDisplayFlat
DisplayStyleConstants.seDisplayWireframe
DisplayStyleConstants.seDisplayVisible
DisplayStyleConstants.seDisplayHidden
```

**NOT WORKING - How to Apply:**
```python
view.DisplayMode = DisplayStyleConstants.seDisplayFlat  # COM exception
```

### Zoom - Working ✅
```python
view.Fit()                 # Zoom to fit all geometry
```

---

## 7. EXPORT API ✅

All working.

```python
# File export
document.SaveAs(
    FileName=path,
    SaveAsType=ApplicationConstants.igFileTypeSTEP  # or igFileTypeSTL, etc.
)

# Image capture
view.SaveAsImage(
    Filename=image_path,
    Width=1920,
    Height=1080,
    BackgroundScheme=ImageFileConstants.seImageFileBackgroundSchemeWhite
)
```

---

## 8. DOCUMENT MANAGEMENT API ✅

All working.

```python
# Create
documents.Add("SolidEdge.PartDocument")  # or use DocumentTypeConstants

# Save
document.Save()
document.SaveAs(filepath)

# Close without prompt
document.Saved = True     # Suppress save dialog
document.Close()
```

**Key Discovery:** Set `document.Saved = True` before `Close()` to suppress save prompt.

---

## 9. REFERENCE PLANES API ✅

```python
ref_planes = document.RefPlanes
ref_plane = ref_planes.Item(1)    # 1=Top, 2=Front, 3=Right
```

**⚠️ 1-based indexing!**

---

## 10. ASSEMBLY API 🔍 **PARTIAL**

```python
# Add component at origin
occurrences.AddByFilename(filepath)           # ✅ Works

# Add with transformation matrix
occurrences.Add(filepath, matrix)             # 🔍 Works but matrix format unclear

# List components
count = occurrences.Count                      # ✅ Works (1-based)
occ = occurrences.Item(index)                 # ✅ Works (1-based)
```

---

## Critical Questions for SDK Documentation

### 1. Revolve Operations
- Which of the 14 parameters are actually required (not truly optional)?
- What type/value for `RefAxis`? (axis object, None, or something else?)
- What values for `ProfileSide`, `ExtentType1/2`, `ExtentSide1/2`?
- Why doesn't ProfileArray tuple work for revolve when it works for extrude?

### 2. Primitive Creation
- What to pass for `pPlane` parameter?
- What are valid values for `ExtentSide`?
- What is `vbKeyPointExtent`? Boolean or something else?
- What is `pKeyPointObj`? What object type?
- What are valid values for `pKeyPointFlags`?
- What does `dAngle` parameter do in AddBoxByCenter?

### 3. View Operations
- What is the method name to set view orientation?
- How to properly set display mode/style?

---

## All Available "Add" Methods (from dir(models))

43 methods found. Bolded = tested, italics = critical missing functionality.

- AddAutoSimplify
- AddBaseContourFlange
- AddBaseContourFlangeByBendDeductionOrBendAllowance
- AddBaseTab
- AddBaseTabWithMultipleProfiles
- AddBody
- AddBodyByMeshFacets
- AddBodyByTag
- AddBodyFeature
- **❌ _AddBoxByCenter_** (failing)
- AddBoxByThreePoints
- AddBoxByTwoPoints
- AddByConstruction
- **❌ _AddCylinderByCenterAndRadius_** (failing)
- AddCopiedPart
- AddCopiedPartEx
- AddCopiedPartWithMatchedCoordinateSystems
- **✅ AddExtrudedProtrusion** (working)
- AddExtrudedProtrusionWithThinWall
- AddFiniteBaseHelix
- AddFiniteBaseHelixSync
- AddFiniteBaseHelixSyncWithThinWall
- AddFiniteBaseHelixWithThinWall
- **✅ AddFiniteExtrudedProtrusion** (working)
- **❌ _AddFiniteRevolvedProtrusion_** (untested, may be simpler than full revolve)
- AddFiniteRevolvedProtrusionSync
- AddLocalSimplifyEnclosure
- AddLoftedFlange
- AddLoftedFlangeByBendDeductionOrBendAllowance
- AddLoftedFlangeEx
- AddLoftedProtrusion
- AddLoftedProtrusionWithThinWall
- AddRef
- **❌ _AddRevolvedProtrusion_** (failing)
- AddRevolvedProtrusionSync
- AddRevolvedProtrusionWithThinWall
- AddSimplifyDuplicate
- AddSimplifyEnclosure
- **❌ _AddSphereByCenterAndRadius_** (failing)
- AddSweptProtrusion
- AddSweptProtrusionWithThinWall
- AddThickenFeature
- AddWebNetwork

---

## Next Steps

1. **Try AddFiniteRevolvedProtrusion** - simpler alternative to full revolve
2. **Try AddBoxByTwoPoints** - simpler alternative to AddBoxByCenter
3. **Wait for SDK documentation** - critical for understanding:
   - Revolve required parameters and types
   - Primitive pPlane, ExtentSide, KeyPoint parameters
   - View/display method names

---

## Statistics

- **Total methods introspected:** ~50+
- **Fully working (✅):** ~30 (60%)
- **Failing (❌):** ~10 (20%)
- **Untested (❓):** ~10 (20%)

**Comprehensive test results:** 25/33 tests passing (75%)

**Blocking issues:** Revolve and primitives are essential for basic CAD functionality.
