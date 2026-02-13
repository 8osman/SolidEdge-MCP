# Key Findings from Comprehensive Introspection

## CRITICAL DISCOVERIES

### 1. AddFiniteRevolvedProtrusion - SIMPLER REVOLVE! ⭐
**Only 7 parameters** (vs 14 for full AddRevolvedProtrusion)

```python
AddFiniteRevolvedProtrusion(
    NumberOfProfiles,      # Integer count
    ProfileArray,          # Tuple of profile objects
    ReferenceAxis,         # Axis object or ???
    ProfilePlaneSide,      # Constant (like ExtrudedProtrusion.igRight?)
    AngleofRevolution,     # Radians
    KeyPointOrTangentFace, # Optional?
    KeyPointFlags          # Optional?
)
```

**Comparison to extrude:**
- Extrude (AddFiniteExtrudedProtrusion): 8 params, only first 4 needed
- Revolve (AddFiniteRevolvedProtrusion): 7 params, likely similar - maybe only first 5 needed?

**Next step:** Test with first 5 params, using patterns from working extrude

---

### 2. ApplyNamedView - VIEW ORIENTATION FOUND! ⭐

```python
View.ApplyNamedView(Name)
```

**Single parameter:** `Name` (string or constant?)

**To test:**
- `view.ApplyNamedView("Iso")` - string name
- `view.ApplyNamedView(ViewOrientationConstants.seIsoView)` - constant

---

### 3. AddBoxByTwoPoints - Alternative Box Method

**13 parameters total**

**Clear parameters (1-6):** Corner points
```python
AddBoxByTwoPoints(
    x1, y1, Z1,    # First corner (meters)
    x2, y2, Z2,    # Opposite corner (meters)
    dAngle,        # Rotation?
    dDepth,        # Extrusion depth?
    pPlane,        # Reference plane (unclear)
    ExtentSide,    # Direction constant (unclear)
    vbKeyPointExtent,  # Boolean? (unclear)
    pKeyPointObj,  # Object? (unclear)
    pKeyPointFlags # Flags? (unclear)
)
```

**Note:** Still has the same unclear params as AddBoxByCenter

---

## ALL "ADD" METHODS ON MODELS (43 total)

Full list introspected with signatures:

### Feature Creation
- AddFiniteExtrudedProtrusion (8 params) ✅ WORKING
- **AddFiniteRevolvedProtrusion (7 params)** ⭐ TO TEST
- AddRevolvedProtrusion (14 params) ❌ FAILING
- AddLoftedProtrusion
- AddSweptProtrusion
- AddExtrudedProtrusionWithThinWall
- AddRevolvedProtrusionWithThinWall

### Primitives
- AddBoxByCenter (12 params) ❌ FAILING
- **AddBoxByTwoPoints (13 params)** ⭐ TO TEST
- AddBoxByThreePoints
- AddCylinderByCenterAndRadius (10 params) ❌ FAILING
- AddSphereByCenterAndRadius (10 params) ❌ FAILING

### Other Features
- AddBaseContourFlange (18 params)
- AddBaseTab
- AddCopiedPart
- AddBody
- AddThickenFeature
- AddWebNetwork
- ... and 27 more

---

## VIEW OBJECT METHODS (96 total)

### Key Methods Found

**Orientation:**
- **ApplyNamedView(Name)** ⭐ TO TEST
- OrientCamera(xCenter, yCenter, xMajor, yMajor, Ratio, Orientation)
- OrientCameraEx(...)

**Display:**
- (Need to search output for Display/Style methods)

**Zoom:**
- Fit() ✅ WORKING
- PanCamera
- ZoomByPercentage

**Animation/Movie:**
- AddFrameToMovie
- MovieTitle

---

## CONSTANTS AVAILABLE

From win32com.client.constants

### ViewOrientation Constants
```python
ViewOrientationConstants.seIsoView
ViewOrientationConstants.seTopView
ViewOrientationConstants.seFrontView
# etc.
```

### DisplayStyle Constants
```python
DisplayStyleConstants.seDisplayFlat
DisplayStyleConstants.seDisplayWireframe
# etc.
```

### FeatureOperation Constants
```python
FeatureOperationConstants.igFeatureAdd
FeatureOperationConstants.igFeatureCut
# etc.
```

---

## IMMEDIATE TESTING PRIORITIES

### 1. Test AddFiniteRevolvedProtrusion ⭐ HIGH PRIORITY
Pattern based on working extrude:
```python
# Working extrude pattern:
models.AddFiniteExtrudedProtrusion(
    NumberOfProfiles=1,
    ProfileArray=(profile,),
    ProfilePlaneSide=ExtrudedProtrusion.igRight,
    ExtrusionDistance=0.05
)

# Try revolve with similar pattern:
models.AddFiniteRevolvedProtrusion(
    NumberOfProfiles=1,
    ProfileArray=(profile,),
    ReferenceAxis=???,  # What to pass? None? An axis object?
    ProfilePlaneSide=ExtrudedProtrusion.igRight,  # Same constant?
    AngleofRevolution=math.radians(360)
)
```

**Questions:**
- What to pass for ReferenceAxis?
  - None?
  - pythoncom.Empty?
  - An actual Line2d object from the sketch?
  - One of the RefPlanes edges?

### 2. Test ApplyNamedView ⭐ HIGH PRIORITY
```python
view = app.ActiveWindow.View
view.ApplyNamedView("Iso")  # Try string
# or
view.ApplyNamedView(ViewOrientationConstants.seIsoView)  # Try constant
```

### 3. Test AddBoxByTwoPoints
```python
# Try just the first 6-8 params
models.AddBoxByTwoPoints(
    -0.1, -0.15, 0,      # Corner 1
    0.1, 0.15, 0.05,     # Corner 2
    0,                   # dAngle
    ???                  # dDepth - what does this mean if we already have Z1 and Z2?
)
```

---

## QUESTIONS REMAINING

### Revolve
- **ReferenceAxis parameter:** What type of object? How to get/create it?
- Can we pass None or pythoncom.Empty?
- Does ProfilePlaneSide use the same constants as extrude?

### Primitives
- **pPlane parameter:** What to pass? None? A RefPlane object?
- **ExtentSide parameter:** Constant value? Which enum?
- **vbKeyPointExtent:** True/False? 0/1?
- **pKeyPointObj:** None? An object?
- **pKeyPointFlags:** 0? Some flag value?

### Box Methods
- AddBoxByTwoPoints has 13 params but first 6 are two corners - seems redundant with dDepth
- What's the relationship between Z1/Z2 and dDepth?

---

## NEXT STEPS

1. ✅ Create test script for AddFiniteRevolvedProtrusion
2. ✅ Create test script for ApplyNamedView
3. ✅ Update features.py with working methods
4. ⏳ Test AddBoxByTwoPoints
5. ⏳ Document all working patterns
6. ⏳ Update COM_API_STATUS.md with new findings
