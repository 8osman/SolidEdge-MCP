# SolidEdge-MCP TODO

## Optional Future Improvements

### Enclosure Tools
- Implement correct `create_enclosure_box` / `create_enclosure_cylinder` tools using
  `models.AddBoxByCenter` / `models.AddCylinderByCenterAndRadius` with proper body
  geometry references — these are SE simplification/assembly enclosure APIs, not
  freestanding primitives.

### Bug Fixes Pending
- Bug 2: `create_extrude` from Front plane has unexpected Y origin offset.
  Sketch centred at X=0, Z=0 but bounding box shows Y=-0.216 to +0.054 instead
  of Y=0 to +0.216. Front plane sketch origin appears offset — needs investigation.
- Bug 4: `create_sketch_on_plane` — `SketchManager` loses its `doc` reference.
  Method exists but `'SketchManager' object has no attribute 'doc'` at runtime.

## Known Limitations

- `create_extruded_cutout_through_all(direction="Symmetric")` and
  `create_extruded_cutout_through_next(direction="Symmetric")` are each
  implemented as two sequential cuts (one `igRight`, one `igLeft`) because
  SE has no native symmetric through-all / through-next COM API.  As a
  result each "Symmetric" call produces **two separate features** in the
  pathfinder tree rather than one.
- `create_extruded_cutout_through_all`, `create_extruded_cutout_through_next`,
  and `create_extruded_cutout` (finite) do **not** auto-swap `igRight`/`igLeft`
  for Front plane sketches, unlike `create_extrude`.  This is intentional — see
  the `DELIBERATE DESIGN DECISION` comment in `backends/features.py` above the
  `dir_const` resolution in each cutout function.  Use `direction="Symmetric"` on
  Front plane cutouts to guarantee full penetration regardless of plane orientation.
  The response dict includes a `"warning"` key when a single-direction cut is made
  on a Front plane sketch, so callers (including AI agents) can self-correct.
- SE2026 does not support multiple disjoint closed profiles in a single extruded
  cutout sketch. Each hole/profile must be a separate sketch + cutout operation.
  Attempting multiple profiles in one sketch produces a topology error with no
  geometry created and no clear error message returned to the caller.

### API Improvements
- `create_box_by_three_points` — current implementation approximates; a proper
  3-point oriented box would require computing the local coordinate frame from
  the three points and rotating the sketch accordingly.
- Sphere primitive — revolve approach works but leaves a seam; investigate if SE
  has a better native sphere workflow.
- Add `create_torus` via revolve of a circle profile around an offset axis.
- Plane-offset support for `create_box_by_center`, `create_cylinder`, and
  `create_sphere` — the `center_z` / `base_center_z` parameter is currently
  recorded but not applied as a sketch-plane offset.
