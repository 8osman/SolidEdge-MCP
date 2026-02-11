# Solid Edge 2026 COM API - Complete Available Methods

Based on diagnostic analysis of Solid Edge 2026 (version 226.00.01.04)

## Available Collections on Document
- Models
- ProfileSets

## Models Collection - ALL Add Methods Available

### Basic Primitives (NEW - Not Yet Implemented)
- `AddBoxByCenter` - Add box by center point
- `AddBoxByThreePoints` - Add box by three points
- `AddBoxByTwoPoints` - Add box by two points
- `AddCylinderByCenterAndRadius` - Add cylinder primitive
- `AddSphereByCenterAndRadius` - Add sphere primitive

### Extrusion Operations (PARTIALLY Implemented)
- ✅ `AddFiniteExtrudedProtrusion` - Currently implemented
- `AddExtrudedProtrusion` - Infinite/bounded extrusion
- `AddExtrudedProtrusionWithThinWall` - Thin-walled extrusion

### Revolution Operations (PARTIALLY Implemented)
- ✅ `AddRevolvedProtrusion` - Currently implemented (but may have issues)
- `AddRevolvedProtrusionSync` - Synchronous revolve
- `AddFiniteRevolvedProtrusion` - Finite revolve
- `AddFiniteRevolvedProtrusionSync` - Finite synchronous revolve
- `AddRevolvedProtrusionWithThinWall` - Thin-walled revolve

### Loft Operations (NEW - Not Implemented)
- `AddLoftedProtrusion` - Create lofted feature
- `AddLoftedProtrusionWithThinWall` - Thin-walled loft

### Sweep Operations (NEW - Not Implemented)
- `AddSweptProtrusion` - Sweep along path
- `AddSweptProtrusionWithThinWall` - Thin-walled sweep

### Helix/Spiral Operations (NEW - Not Implemented)
- `AddFiniteBaseHelix` - Create helical feature
- `AddFiniteBaseHelixSync` - Synchronous helix
- `AddFiniteBaseHelixWithThinWall` - Thin-walled helix
- `AddFiniteBaseHelixSyncWithThinWall` - Sync thin-walled helix

### Sheet Metal Operations (NEW - Not Implemented)
- `AddBaseContourFlange` - Base contour flange
- `AddBaseContourFlangeByBendDeductionOrBendAllowance` - Advanced flange
- `AddBaseTab` - Base tab feature
- `AddBaseTabWithMultipleProfiles` - Multi-profile tab
- `AddLoftedFlange` - Lofted flange
- `AddLoftedFlangeByBendDeductionOrBendAllowance` - Advanced lofted flange
- `AddLoftedFlangeEx` - Extended lofted flange
- `AddWebNetwork` - Web network for sheet metal

### Body/Part Operations (NEW - Not Implemented)
- `AddBody` - Add body to part
- `AddBodyByMeshFacets` - Create body from mesh
- `AddBodyByTag` - Add body by tag
- `AddBodyFeature` - Generic body feature
- `AddByConstruction` - Add construction body
- `AddThickenFeature` - Thicken surface to solid

### Simplification/Mesh Operations (NEW - Not Implemented)
- `AddAutoSimplify` - Auto simplify feature
- `AddSimplifyDuplicate` - Duplicate simplified
- `AddSimplifyEnclosure` - Simplify enclosure
- `AddLocalSimplifyEnclosure` - Local simplify

### Assembly/Copy Operations (NEW - Not Implemented)
- `AddCopiedPart` - Copy part into assembly
- `AddCopiedPartEx` - Extended copy part
- `AddCopiedPartWithMatchedCoordinateSystems` - Copy with coordinate matching

### NOT AVAILABLE (Confirmed Missing)
- ❌ `AddExtrudedCutout` - NOT AVAILABLE
- ❌ `AddFiniteExtrudedCutout` - NOT AVAILABLE
- ❌ `AddRevolvedCutout` - NOT AVAILABLE
- ❌ ANY cutout/cut operations - NOT AVAILABLE

## What About Other Features?

### Features NOT in Models Collection
The diagnostic only checked Models and ProfileSets collections. We need to check if these collections exist:
- Holes collection (for AddHole, etc.)
- Rounds collection (for AddRound/Fillet, etc.)
- Chamfers collection (for AddChamfer, etc.)
- Patterns collection (for AddPattern, etc.)
- RibWebs collection
- Threads collection

### Document Operations
Not yet diagnosed - need to check document-level operations for:
- Open/Close documents
- Export (STEP, STL, IGES, DXF, PDF)
- Drawing creation
- Properties and queries

## Current Implementation Status

### Implemented (16 tools)
1. connect_to_solidedge
2. get_application_info
3. create_part_document
4. create_assembly_document
5. save_document
6. list_documents
7. create_sketch
8. draw_line
9. draw_circle
10. draw_rectangle
11. close_sketch
12. create_extrude (AddFiniteExtrudedProtrusion only)
13. create_revolve (AddRevolvedProtrusion - may need testing)
14. set_view
15. zoom_fit
16. diagnose_api

### Can Definitely Implement from Models Collection
- Primitive shapes (box, cylinder, sphere) - 5 methods
- Loft operations - 2 methods
- Sweep operations - 2 methods
- Helix operations - 4 methods
- Sheet metal - 8+ methods
- Body/simplification - 9+ methods

### Unknown - Need Further Diagnostic
- Holes (via Holes collection?)
- Rounds/Fillets (via Rounds collection?)
- Chamfers (via Chamfers collection?)
- Patterns (via Patterns collection?)
- Thread features
- Export operations
- Drawing creation
- Query/measurement tools

## Recommendation
1. Run expanded diagnostic to check for other collections on document
2. Implement the ~30 methods we KNOW are available from Models
3. Check what's available for holes/rounds/chamfers/patterns
4. Then assess the actual gap vs original plan
