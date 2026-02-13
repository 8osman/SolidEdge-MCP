# Solid Edge COM API Reference

This document captures detailed information about the Solid Edge COM API signatures and patterns discovered during development of the SolidEdge MCP Server.

## General COM API Patterns

### Units
- **Length/Distance**: Meters
- **Angles**: Radians
- **Indexing**: 1-based (COM standard)

### Array Handling
- COM arrays must be passed as tuples: `(item,)` for single item, `(item1, item2)` for multiple
- Python lists `[item]` may not convert properly to COM SAFEARRAY types
- For VARIANT arrays, use: `win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, (items,))`

### Optional Parameters
- Use `pythoncom.Empty` for optional COM parameters (though not all "optional" parameters accept this)
- Some methods show all parameters as `PyOleMissing` but still require certain parameters

### Keyword vs Positional Arguments
- **Some methods** accept keyword arguments (like `AddFiniteExtrudedProtrusion`)
- **Some methods** reject keyword arguments and require positional only
- **IMPORTANT**: Always test both approaches - COM API behavior is inconsistent

## Document Object Model

### Application
```python
application = win32com.client.Dispatch("SolidEdge.Application")

# Properties:
application.Version  # e.g., "226.0.0.113"
application.Path     # Installation path (may not always be available)
application.Visible  # Boolean - show/hide UI

# Methods:
application.GetActiveDocument()
application.Documents.Open(filepath)
application.Documents.Add(DocumentType)  # DocumentType from DocumentTypeConstants
```

### Documents
```python
# Create documents
documents = application.Documents
part_doc = documents.Add("SolidEdge.PartDocument")  # or use constant
asm_doc = documents.Add("SolidEdge.AssemblyDocument")

# Document types:
DocumentTypeConstants.igPartDocument
DocumentTypeConstants.igAssemblyDocument
DocumentTypeConstants.igSheetMetalDocument
DocumentTypeConstants.igDraftDocument

# Save
document.Save()
document.SaveAs(filepath)
document.Close()

# To suppress save prompt when closing:
document.Saved = True  # Mark as saved
document.Close()       # No prompt
```

### Reference Planes
```python
ref_planes = document.RefPlanes
ref_plane = ref_planes.Item(1)  # 1=Top, 2=Front, 3=Right (1-based!)

# Item() takes 1-based index
```

## Sketching API

### Profile Creation
```python
# Create profile set and profile
profile_sets = document.ProfileSets
profile_set = profile_sets.Add()
profiles = profile_set.Profiles
profile = profiles.Add(ref_plane)  # ref_plane from RefPlanes

# Draw on profile
lines = profile.Lines2d
circles = profile.Circles2d
arcs = profile.Arcs2d
ellipses = profile.Ellipses2d
# ... etc

# Close profile
profile.End(0)  # 0 = validation option

# IMPORTANT: Profile object remains valid after End() and can be used by feature operations
```

### 2D Geometry Methods

#### Lines
```python
lines = profile.Lines2d
line = lines.AddBy2Points(x1, y1, x2, y2)  # All in meters
```

#### Circles
```python
circles = profile.Circles2d
circle = circles.AddByCenterRadius(cx, cy, radius)
```

#### Arcs
```python
arcs = profile.Arcs2d
# Method: AddByCenterStartEnd(xc, yc, xs, ys, xe, ye)
arc = arcs.AddByCenterStartEnd(center_x, center_y, start_x, start_y, end_x, end_y)
```

#### Ellipses
```python
ellipses = profile.Ellipses2d
# Method: AddByCenter(cx, cy, major_radius, minor_radius, axis_x, axis_y)
# axis_x, axis_y define the major axis direction as a unit vector
import math
axis_x = math.cos(angle_rad)
axis_y = math.sin(angle_rad)
ellipse = ellipses.AddByCenter(cx, cy, major_radius, minor_radius, axis_x, axis_y)
```

#### Rectangles
```python
lines = profile.Lines2d
# No direct rectangle method - draw 4 lines
lines.AddBy2Points(x1, y1, x2, y1)
lines.AddBy2Points(x2, y1, x2, y2)
lines.AddBy2Points(x2, y2, x1, y2)
lines.AddBy2Points(x1, y2, x1, y1)
```

#### Splines
```python
splines = profile.Splines2d
# Method: AddByPoints(Order, NumPoints, PointArray)
# Order: typically 3 for cubic spline
# PointArray: tuple of coordinates (x1, y1, x2, y2, ...)
points = [(x1, y1), (x2, y2), (x3, y3)]
point_array = tuple(coord for point in points for coord in point)  # Flatten
spline = splines.AddByPoints(3, len(points), point_array)

# IMPORTANT: Uses positional arguments, NOT keywords
```

## 3D Features API

### Models Collection
```python
models = document.Models

# First feature creates base body:
model = models.Add*Protrusion(...)

# Subsequent features can add/cut/intersect:
# - Use different methods or operation parameters
```

### Extrusion

#### Full Signature (AddFiniteExtrudedProtrusion)
```python
# Discovered signature (34 parameters!):
AddFiniteExtrudedProtrusion(
    NumberOfProfiles,
    ProfileArray,
    ProfileSide,
    ExtentType1,
    ExtentSide1,
    FiniteDepth1,
    KeyPointOrTangentFace1,
    KeyPointFlags1,
    FromFaceOrRefPlane,
    FromFaceOffsetSide,
    FromFaceOffsetDistance,
    TreatmentType1,
    TreatmentDraftSide1,
    TreatmentDraftAngle1,
    TreatmentCrownType1,
    TreatmentCrownSide1,
    TreatmentCrownCurvatureSide1,
    TreatmentCrownRadiusOrOffset1,
    TreatmentCrownTakeOffAngle1,
    ExtentType2,
    ExtentSide2,
    FiniteDepth2,
    KeyPointOrTangentFace2,
    KeyPointFlags2,
    ToFaceOrRefPlane,
    ToFaceOffsetSide,
    ToFaceOffsetDistance,
    TreatmentType2,
    TreatmentDraftSide2,
    TreatmentDraftAngle2,
    TreatmentCrownType2,
    TreatmentCrownSide2,
    TreatmentCrownCurvatureSide2,
    TreatmentCrownRadiusOrOffset2,
    TreatmentCrownTakeOffAngle2
)
```

#### Working Simple Extrusion
```python
# ACCEPTS KEYWORD ARGUMENTS:
model = models.AddFiniteExtrudedProtrusion(
    NumberOfProfiles=1,
    ProfileArray=(profile,),  # TUPLE, not list!
    ProfilePlaneSide=ExtrudedProtrusion.igRight,  # or igLeft, igSymmetric
    ExtrusionDistance=distance  # meters
)

# Direction constants:
ExtrudedProtrusion.igRight      # Normal direction
ExtrudedProtrusion.igLeft       # Reverse direction
ExtrudedProtrusion.igSymmetric  # Symmetric
```

#### Extruded Cutout
```python
model = models.AddFiniteExtrudedCutout(
    NumberOfProfiles=1,
    ProfileArray=(profile,),
    ProfilePlaneSide=ExtrudedProtrusion.igRight,
    ExtrusionDistance=distance
)
```

### Revolve

#### Full Signature (AddRevolvedProtrusion)
```python
# Discovered signature (14 parameters):
AddRevolvedProtrusion(
    NumberOfProfiles,
    ProfileArray,
    RefAxis,
    ProfileSide,
    ExtentType1,
    ExtentSide1,
    FiniteAngle1,
    KeyPointOrTangentFace1,
    KeyPointFlags1,
    ExtentType2,
    ExtentSide2,
    FiniteAngle2,
    KeyPointOrTangentFace2,
    KeyPointFlags2
)
```

#### Attempted Working Pattern (NOT YET SUCCESSFUL)
```python
# STATUS: Still debugging - multiple approaches tried, none working yet
# Issue: Parameter conversion errors or "Invalid number of parameters"

# Attempt 1: Keyword arguments (like extrude)
model = models.AddRevolvedProtrusion(
    NumberOfProfiles=1,
    ProfileArray=(profile,),
    FiniteAngle1=angle_rad  # radians
)
# Result: "Invalid number of parameters"

# Attempt 2: All parameters with pythoncom.Empty
model = models.AddRevolvedProtrusion(
    1,  # NumberOfProfiles
    [profile],  # ProfileArray as list
    pythoncom.Empty,  # RefAxis
    pythoncom.Empty,  # ProfileSide
    pythoncom.Empty,  # ExtentType1
    pythoncom.Empty,  # ExtentSide1
    angle_rad,  # FiniteAngle1
    pythoncom.Empty,  # KeyPointOrTangentFace1
    pythoncom.Empty,  # KeyPointFlags1
    pythoncom.Empty,  # ExtentType2
    pythoncom.Empty,  # ExtentSide2
    pythoncom.Empty,  # FiniteAngle2
    pythoncom.Empty,  # KeyPointOrTangentFace2
    pythoncom.Empty   # KeyPointFlags2
)
# Result: "Parameter not optional"

# TODO: Find actual working pattern - may need to check Solid Edge VBA/C# examples
```

### Primitives

#### Box (AddBoxByCenter)
```python
# STATUS: NOT WORKING YET
# Attempted signatures have failed with conversion errors
# TODO: Investigate proper signature

# Expected usage:
models.AddBoxByCenter(x, y, z, length, width, height)
```

#### Cylinder (AddCylinderByCenterAndRadius)
```python
# STATUS: NOT WORKING YET
# TODO: Investigate proper signature

# Expected usage:
models.AddCylinderByCenterAndRadius(x, y, z, radius, height)
```

#### Sphere (AddSphereByCenterAndRadius)
```python
# STATUS: NOT WORKING YET
# TODO: Investigate proper signature

# Expected usage:
models.AddSphereByCenterAndRadius(x, y, z, radius)
```

## Query and Measurement API

### Physical Properties
```python
# Get mass properties
props = document.PhysicalProperties
volume = props.Volume       # cubic meters
mass = props.Mass          # kg (if density set)
surface_area = props.Area  # square meters

# Center of mass
com_x = props.CenterOfGravityX
com_y = props.CenterOfGravityY
com_z = props.CenterOfGravityZ
```

### Bounding Box
```python
# STATUS: Working but may need refinement
models = document.Models
if models.Count > 0:
    model = models.Item(1)
    # Get range box (bounding box)
    range_box = model.RangeBox
    # Returns: (x_min, y_min, z_min, x_max, y_max, z_max)
```

### Distance Measurement
```python
# Direct calculation for point-to-point:
import math
distance = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

# For feature-to-feature: use MeasureDistanceBetween (if available)
```

## View and Display API

### View Orientation
```python
window = application.ActiveWindow
view = window.View

# Set named view
ViewOrientationConstants.seIsoView
ViewOrientationConstants.seTopView
ViewOrientationConstants.seFrontView
ViewOrientationConstants.seRightView
ViewOrientationConstants.seBottomView
ViewOrientationConstants.seBackView
ViewOrientationConstants.seLeftView

# Apply view (METHOD NAME MAY VARY - check actual API):
# view.SetNamedView(ViewOrientationConstants.seIsoView)  # May not exist
# OR:
# window.ViewOrientationConstants = ViewOrientationConstants.seIsoView  # May not exist
# STATUS: Still debugging correct method to set view
```

### Display Mode
```python
view = application.ActiveWindow.View

# Display style constants:
DisplayStyleConstants.seDisplayFlat
DisplayStyleConstants.seDisplayWireframe
DisplayStyleConstants.seDisplayVisible
DisplayStyleConstants.seDisplayHidden

# Apply (METHOD UNCERTAIN):
# view.DisplayMode = DisplayStyleConstants.seDisplayFlat
# STATUS: Still debugging - COM exception when trying to set
```

### Zoom Operations
```python
view = application.ActiveWindow.View

# Zoom to fit
view.Fit()  # Fits all visible geometry

# Zoom by percentage
view.ZoomByPercentage(1.5)  # 150% zoom
```

## Export API

### STEP Export
```python
document.SaveAs(
    FileName=output_path,
    SaveAsType=ApplicationConstants.igFileTypeSTEP
)
```

### STL Export
```python
document.SaveAs(
    FileName=output_path,
    SaveAsType=ApplicationConstants.igFileTypeSTL
)
```

### Screenshot/Image Capture
```python
window = application.ActiveWindow
view = window.View

# Save image
view.SaveAsImage(
    Filename=image_path,
    Width=1920,
    Height=1080,
    BackgroundScheme=ImageFileConstants.seImageFileBackgroundSchemeWhite
)
```

## Assembly API

### Component Placement
```python
occurrences = assembly_doc.Occurrences

# Add component
occurrence = occurrences.Add(
    FileName=part_filepath,
    DestinationMatrix=matrix  # 4x4 transformation matrix
)

# OR simpler placement:
occurrence = occurrences.AddByFilename(part_filepath)
# Then set position programmatically
```

### List Components
```python
occurrences = assembly_doc.Occurrences
for i in range(1, occurrences.Count + 1):  # 1-based!
    occ = occurrences.Item(i)
    name = occ.Name
    # ... access properties
```

## Constants Reference

### Feature Operation Constants
```python
FeatureOperationConstants.igFeatureAdd
FeatureOperationConstants.igFeatureCut
FeatureOperationConstants.igFeatureIntersect
```

### Document Type Constants
```python
DocumentTypeConstants.igPartDocument
DocumentTypeConstants.igAssemblyDocument
DocumentTypeConstants.igSheetMetalDocument
DocumentTypeConstants.igDraftDocument
```

### Application Constants (File Types)
```python
ApplicationConstants.igFileTypeSTEP
ApplicationConstants.igFileTypeSTL
ApplicationConstants.igFileTypeIGES
ApplicationConstants.igFileTypeParasolid
```

## Known Issues and Limitations

### 1. Revolve Operations
- **Status**: Not working
- **Issue**: Unclear which parameters are actually required vs optional
- **Attempted**: Both keyword and positional arguments, pythoncom.Empty for optionals
- **Next Steps**: Need to find VBA/C#/official documentation examples

### 2. Primitive Creation (Box, Cylinder, Sphere)
- **Status**: Not working
- **Issue**: Array/coordinate parameter conversion failures
- **Next Steps**: Investigate actual signatures and required parameter types

### 3. View Setting
- **Status**: Partially working
- **Issue**: SetNamedView method may not exist; unclear how to programmatically set view orientation
- **Next Steps**: Check Window vs View object methods

### 4. Display Mode
- **Status**: Not working
- **Issue**: COM exception when trying to set display mode
- **Next Steps**: Verify property name and acceptable values

## Best Practices

### 1. Error Handling
Always wrap COM calls in try-except:
```python
try:
    result = com_object.Method(params)
except Exception as e:
    # COM errors come as tuples: (error_code, message, None, None)
    print(f"COM Error: {e}")
```

### 2. Object Lifetime
- Keep references to COM objects while in use
- Don't rely on Python garbage collection for cleanup
- Explicitly release when done (though Python usually handles this)

### 3. Discovery Pattern
To find actual method signatures:
```python
import inspect
sig = inspect.signature(com_object.Method)
print(f"Signature: {sig}")
```

### 4. Array Parameters
When in doubt about array format:
- Try tuple first: `(item,)`
- Then list: `[item]`
- Then VARIANT: `win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, (item,))`

### 5. Keyword vs Positional
Always test both:
```python
# Try keywords first (more readable):
obj.Method(ParamName=value)

# If that fails, try positional:
obj.Method(value)
```

## Documentation Resources

### Official Sources
- Solid Edge SDK Documentation (install with Solid Edge)
- VBA API Reference (Help > API Reference in Solid Edge)
- C# .NET Examples (included with SDK)

### Community Resources
- Solid Edge Forums
- Stack Overflow `solidedge` tag
- GitHub examples (search "solidedge automation")

## Update Log

- **2026-02-11**: Initial creation with discovered signatures for extrude, revolve, sketching
- **Status**: ~75% of tools working, key missing: revolve, primitives, some view operations
