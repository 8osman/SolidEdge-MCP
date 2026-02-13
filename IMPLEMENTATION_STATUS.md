# Solid Edge MCP - Implementation Status

Last Updated: 2026-02-12

## MCP Server Status: **OPERATIONAL**

**241 MCP tools** are now registered and ready to use!

## Quick Summary

| Category | Implemented | Notes |
|----------|-------------|-------|
| **Connection** | 6 | Connect, disconnect, app info, quit, is_connected, process_info |
| **Document Management** | 13 | Create (part, assembly, sheet metal, draft), open, save, close, list, activate, undo, redo |
| **Sketching** | 22 | Lines, circles, arcs (multiple), rects, polygons, ellipses, splines, points, constraints (9 types), fillet, chamfer, mirror, construction, hide profile |
| **Basic Primitives** | 8 | Box (3 variants), cylinder, sphere, box cutout, cylinder cutout, sphere cutout |
| **Extrusions** | 4 | Finite, infinite, thin-wall, extruded surface |
| **Revolves** | 5 | Basic, finite, sync, thin-wall |
| **Cutouts** | 9 | Extruded finite/through-all/through-next, revolved, normal/normal-through-all, lofted, swept, helix |
| **Rounds/Chamfers/Holes** | 9 | Round (all/face), variable round, blend, chamfer (equal/unequal/angle/face), hole, hole through-all |
| **Reference Planes** | 5 | Offset, normal-to-curve, angle, 3-points, mid-plane |
| **Loft** | 2 | Basic, thin-wall |
| **Sweep** | 2 | Basic, thin-wall |
| **Helix/Spiral** | 4 | Basic, sync, thin-wall variants |
| **Construction Surfaces** | 3 | Revolved surface, lofted surface, swept surface |
| **Sheet Metal** | 8 | Base flange/tab, lofted flange, web network, advanced variants |
| **Body Operations** | 9 | Add body, thicken, mesh, tag, construction, delete holes, delete blends |
| **Simplification** | 4 | Auto-simplify, enclosure, duplicate |
| **View/Display** | 7 | Orientation, zoom, display mode, background color, get/set camera |
| **Variables** | 5 | Get all, get by name, set value, add variable, query/search |
| **Custom Properties** | 3 | Get all, set/create, delete |
| **Body Topology** | 3 | Body faces, body edges, face info |
| **Performance** | 2 | Set performance mode, recompute |
| **Query/Analysis** | 20 | Mass properties, bounding box, features, measurements, facet data, solid bodies, modeling mode, face/edge info, colors, angles, volume, delete feature, material table |
| **Feature Management** | 5 | Suppress, unsuppress, face rotate (2), draft angle |
| **Export** | 10 | STEP, STL, IGES, PDF, DXF, flat DXF, Parasolid, JT, drawing, screenshot |
| **Assembly** | 22 | Place, list, constraints, patterns, suppress, BOM, structured BOM, interference, bbox, relations, doc tree, replace, delete, visibility, color, transform, count |
| **Draft/Drawing** | 10 | Sheets (add, activate, delete, rename), views, annotations (dimension, balloon, note, leader, text box) |
| **Part Features** | 10 | Dimple, etch, rib, lip, drawn cutout, bead, louver, gusset, thread, slot, split |
| **Diagnostics** | 2 | API and feature inspection |
| **Select Set** | 3 | Get selection, clear selection, add to selection |
| **TOTAL** | **241** | |

---

## Tool Categories

### 1. Connection & Application (3)
| Tool | API Method | Status |
|------|-----------|--------|
| connect_to_solidedge | GetActiveObject/Dispatch | Working |
| get_application_info | Application properties | Working |
| quit_application | Application.Quit | **Working** |

### 2. Document Management (11)
| Tool | API Method | Status |
|------|-----------|--------|
| create_part_document | Documents.Add | Working |
| create_assembly_document | Documents.Add | Working |
| create_sheet_metal_document | Documents.Add("SolidEdge.SheetMetalDocument") | Implemented |
| open_document | Documents.Open | Working |
| save_document | Document.Save/SaveAs | Working |
| close_document | Document.Close | Working |
| list_documents | Documents collection | Working |
| activate_document | Document.Activate | **Working** |
| undo | Document.Undo | **Implemented** |
| redo | Document.Redo | **Implemented** |

### 3. Sketching & 2D Geometry (11)
| Tool | API Method | Status |
|------|-----------|--------|
| create_sketch | ProfileSets.Add/Profiles.Add | Working |
| create_sketch_on_plane | ProfileSets.Add with plane index | Working |
| draw_line | Lines2d.AddBy2Points | Working |
| draw_circle | Circles2d.AddByCenterRadius | Working |
| draw_rectangle | Lines2d (4 lines) | Working |
| draw_arc | Arcs2d.AddByCenterStartEnd | Working |
| draw_polygon | Lines2d (n lines) | Working |
| draw_ellipse | Ellipses2d.AddByCenter | Working |
| draw_spline | BSplineCurves2d.AddByPoints | Working |
| set_axis_of_revolution | SetAxisOfRevolution | Working |
| close_sketch | Profile.End | Working |
| add_constraint | Relations2d | Stub (needs element refs) |

### 4. Primitives (5)
| Tool | API Method | Status |
|------|-----------|--------|
| create_box_by_center | Models.AddBoxByCenter | Working |
| create_box_by_two_points | Models.AddBoxByTwoPoints | Working |
| create_box_by_three_points | Models.AddBoxByThreePoints | Working |
| create_cylinder | Models.AddCylinderByCenterAndRadius | Working |
| create_sphere | Models.AddSphereByCenterAndRadius | Working |

### 5. Extrusions (3)
| Tool | API Method | Status |
|------|-----------|--------|
| create_extrude | Models.AddFiniteExtrudedProtrusion | Working |
| create_extrude_infinite | Models.AddExtrudedProtrusion | Untested |
| create_extrude_thin_wall | Models.AddExtrudedProtrusionWithThinWall | Untested |

### 6. Revolves (5)
| Tool | API Method | Status |
|------|-----------|--------|
| create_revolve | Models.AddFiniteRevolvedProtrusion | Working |
| create_revolve_finite | Models.AddFiniteRevolvedProtrusion | Working |
| create_revolve_sync | Models.AddRevolvedProtrusionSync | Untested |
| create_revolve_finite_sync | Models.AddFiniteRevolvedProtrusionSync | Untested |
| create_revolve_thin_wall | Models.AddRevolvedProtrusionWithThinWall | Untested |

### 7. Cutouts (5)
| Tool | API Method | Status |
|------|-----------|--------|
| create_extruded_cutout | ExtrudedCutouts.AddFiniteMulti | **Working** |
| create_extruded_cutout_through_all | ExtrudedCutouts.AddThroughAllMulti | **Working** |
| create_revolved_cutout | RevolvedCutouts.AddFiniteMulti | Implemented |
| create_normal_cutout | NormalCutouts.AddFiniteMulti | Implemented |
| create_lofted_cutout | LoftedCutouts.AddSimple | Implemented |

### 7b. Rounds, Chamfers & Holes (3)
| Tool | API Method | Status |
|------|-----------|--------|
| create_round | Rounds.Add | **Working** |
| create_chamfer | Chamfers.AddEqualSetback | **Working** |
| create_hole | ExtrudedCutouts.AddFiniteMulti (circular) | **Working** |

### 8. Reference Planes (2)
| Tool | API Method | Status |
|------|-----------|--------|
| create_ref_plane_by_offset | RefPlanes.AddParallelByDistance | **Working** |
| get_ref_planes | RefPlanes iteration | **Implemented** |

### 9. Loft (2)
| Tool | API Method | Status |
|------|-----------|--------|
| create_loft | LoftedProtrusions.AddSimple / Models.AddLoftedProtrusion | Working |
| create_loft_thin_wall | Models.AddLoftedProtrusionWithThinWall | Untested |

### 10. Sweep (2)
| Tool | API Method | Status |
|------|-----------|--------|
| create_sweep | Models.AddSweptProtrusion | Working |
| create_sweep_thin_wall | Models.AddSweptProtrusionWithThinWall | Untested |

### 11. Helix/Spiral (4)
| Tool | API Method | Status |
|------|-----------|--------|
| create_helix | Models.AddFiniteBaseHelix | Untested |
| create_helix_sync | Models.AddFiniteBaseHelixSync | Untested |
| create_helix_thin_wall | Models.AddFiniteBaseHelixWithThinWall | Untested |
| create_helix_sync_thin_wall | Models.AddFiniteBaseHelixSyncWithThinWall | Untested |

### 12. Sheet Metal (8)
| Tool | API Method | Status |
|------|-----------|--------|
| create_base_flange | Models.AddBaseContourFlange | Untested |
| create_base_tab | Models.AddBaseTab | Untested |
| create_lofted_flange | Models.AddLoftedFlange | Untested |
| create_web_network | Models.AddWebNetwork | Untested |
| create_base_contour_flange_advanced | Models.AddBaseContourFlangeBy... | Untested |
| create_base_tab_multi_profile | Models.AddBaseTabWithMultipleProfiles | Untested |
| create_lofted_flange_advanced | Models.AddLoftedFlangeBy... | Untested |
| create_lofted_flange_ex | Models.AddLoftedFlangeEx | Untested |

### 13. Body Operations (7)
| Tool | API Method | Status |
|------|-----------|--------|
| add_body | Models.AddBody | Untested |
| thicken_surface | Models.AddThickenFeature | Untested |
| add_body_by_mesh | Models.AddBodyByMeshFacets | Untested |
| add_body_feature | Models.AddBodyFeature | Untested |
| add_by_construction | Models.AddByConstruction | Untested |
| add_body_by_tag | Models.AddBodyByTag | Untested |

### 14. Simplification (4)
| Tool | API Method | Status |
|------|-----------|--------|
| auto_simplify | Models.AddAutoSimplify | Untested |
| simplify_enclosure | Models.AddSimplifyEnclosure | Untested |
| simplify_duplicate | Models.AddSimplifyDuplicate | Untested |
| local_simplify_enclosure | Models.AddLocalSimplifyEnclosure | Untested |

### 15. View & Display (4)
| Tool | API Method | Status |
|------|-----------|--------|
| set_view | View.ApplyNamedView | Working |
| zoom_fit | View.Fit | Working |
| zoom_to_selection | View.Fit | Working |
| set_display_mode | View.SetRenderMode | Working |

### 16. Query & Analysis (10)
| Tool | API Method | Status |
|------|-----------|--------|
| get_mass_properties | Model.ComputePhysicalProperties... | Working |
| get_bounding_box | Body.GetRange | Working |
| list_features | DesignEdgebarFeatures | Working |
| get_feature_count | Models.Count | Working |
| get_document_properties | Document properties | Working |
| measure_distance | Math calculation | Working |
| get_body_facet_data | Body.GetFacetData | Implemented |
| get_solid_bodies | Models + Constructions iteration | Implemented |
| get_modeling_mode | Document.ModelingMode | Implemented |
| set_modeling_mode | Document.ModelingMode = value | Implemented |

### 17. Export (9)
| Tool | API Method | Status |
|------|-----------|--------|
| export_step | Document.SaveAs | Working |
| export_stl | Document.SaveAs | Working |
| export_iges | Document.SaveAs | Working |
| export_pdf | Document.SaveAs | Working |
| export_dxf | Document.SaveAs | Working |
| export_flat_dxf | FlatPatternModels.SaveAsFlatDXFEx | **Implemented** |
| export_parasolid | Document.SaveAs | Working |
| export_jt | Document.SaveAs | Working |
| create_drawing | DraftDocument + DrawingViews | Working |
| capture_screenshot | View.SaveAsImage | Working |

### 17b. Draft/Drawing (2)
| Tool | API Method | Status |
|------|-----------|--------|
| add_draft_sheet | Sheets.AddSheet | Implemented |
| add_assembly_drawing_view | DrawingViews.AddAssemblyView | Implemented |

### 18. Assembly (16)
| Tool | API Method | Status |
|------|-----------|--------|
| place_component | Occurrences.AddByFilename/AddWithMatrix | Working |
| list_assembly_components | Occurrences iteration | Working |
| get_component_info | Occurrence properties + GetTransform | Working |
| update_component_position | Occurrence.SetMatrix | Working |
| pattern_component | Occurrences.AddWithMatrix (copies) | Working |
| suppress_component | Occurrence.Suppress/Unsuppress | Working |
| get_occurrence_bounding_box | Occurrence.GetRangeBox | Implemented |
| get_bom | Occurrences iteration + dedup | Implemented |
| check_interference | AssemblyDocument.CheckInterference | Implemented |
| get_assembly_relations | Relations3d iteration | **Implemented** |
| get_document_tree | Occurrences + SubOccurrences recursion | **Implemented** |
| create_mate | Relations3d | Stub (needs face selection) |
| add_align_constraint | Relations3d | Stub (needs face selection) |
| add_angle_constraint | Relations3d | Stub (needs face selection) |
| add_planar_align_constraint | Relations3d | Stub (needs face selection) |
| add_axial_align_constraint | Relations3d | Stub (needs face selection) |

### 19. Diagnostics (2)
| Tool | API Method | Status |
|------|-----------|--------|
| diagnose_api | Runtime introspection | Working |
| diagnose_feature | Feature property inspection | Working |

### 20. Variables (3)
| Tool | API Method | Status |
|------|-----------|--------|
| get_variables | Document.Variables iteration | Implemented |
| get_variable | Variable.DisplayName match | Implemented |
| set_variable | Variable.Value = newValue | Implemented |

### 21. Custom Properties (3)
| Tool | API Method | Status |
|------|-----------|--------|
| get_custom_properties | Document.Properties iteration | Implemented |
| set_custom_property | Property.Value / Properties.Add | Implemented |
| delete_custom_property | Property.Delete | Implemented |

### 22. Body Topology (3)
| Tool | API Method | Status |
|------|-----------|--------|
| get_body_faces | Body.Faces(igQueryAll) | Implemented |
| get_body_edges | Face.Edges iteration | Implemented |
| get_face_info | Face properties (Type, Area, Edges) | Implemented |

### 23. Feature Management (2)
| Tool | API Method | Status |
|------|-----------|--------|
| suppress_feature | Feature.Suppress | Implemented |
| unsuppress_feature | Feature.Unsuppress | Implemented |

### 24. Performance (2)
| Tool | API Method | Status |
|------|-----------|--------|
| set_performance_mode | App.DelayCompute/ScreenUpdating/etc | Implemented |
| recompute | Model.Recompute + Document.Recompute | Implemented |

### 25. Select Set (2)
| Tool | API Method | Status |
|------|-----------|--------|
| get_select_set | Document.SelectSet iteration | **Implemented** |
| clear_select_set | SelectSet.RemoveAll | **Implemented** |

---

## Known Limitations

1. **Assembly constraints** require face/edge geometry selection which is complex to automate via COM
2. **Feature patterns** (model.Patterns) require SAFEARRAY(IDispatch) marshaling that fails in late binding
3. **Shell/Thinwalls** requires face selection for open faces, not automatable via COM
4. **Sketch constraints** (add_constraint) needs specific element references, partially stubbed
5. **Cutout via models.Add*Cutout** does NOT work - must use collection-level methods (ExtrudedCutouts.AddFiniteMulti)

## Available but Not Yet Implemented

Feature collections accessible on Model object that could be wrapped as tools:
- **MirrorCopies** - Add(PatternPlane, NumFeatures, FeatureArray), AddSync
- **Drafts** - Add(DraftPlane, NumFaceSets, FaceSetArray, DraftAngleArray, DraftSide)
- **Threads** - Add(HoleData, NumCylinders, CylinderArray, CylinderEndArray)
- **Ribs** - Add(RibProfile, ExtensionType, ThicknessType, MaterialSide, ThicknessSide, Thickness)
- **Slots** - Add (22 params, complex)
- **Blends** - Add, AddSurfaceBlend, AddVariable
- **DeleteFaces** - Add(FaceSetToDelete)
- **Dimples, Gussets, Louvers, Beads, Lips** - Various sheet metal features
