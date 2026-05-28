---
name: blender-mcp
description: Use when modeling, editing, or exporting 3D scenes in Blender via the BlenderMCP addon over a TCP socket (default port 9876). Covers running bpy scripts, building primitives, and exporting STL/OBJ.
user-invocable: false
---

# Blender MCP

Drive a running Blender instance that has the BlenderMCP addon listening on a TCP port (default `127.0.0.1:9876`). Commands are JSON; responses are JSON.

## Preflight

1. Confirm Blender is open and the addon is started (port shown in addon panel).
2. Default port is `9876`; the user may pass another.
3. The helper script lives at `/home/tpk/.openclaw/workspace/blender_send.py`.

## Sending commands

Use `blender_send.py <command_type> '<json_params>'`. Common command types:

- `get_scene_info` — sanity check connectivity.
- `execute_code` — run arbitrary `bpy` Python in Blender. Params: `{"code": "..."}`. This is the workhorse.
- `get_object_info` — inspect a named object.

Example connectivity check:

```bash
python3 /home/tpk/.openclaw/workspace/blender_send.py get_scene_info
```

Example running a script:

```bash
python3 /home/tpk/.openclaw/workspace/blender_send.py execute_code \
  "$(jq -Rs '{code: .}' < blender_build.py)"
```

For long scripts, write a `.py` file (see `blender_build.py` as a template) and pass its contents inline via `execute_code`. Keep scripts idempotent: clear the scene at the top with `bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()`.

## Building from a reference image

1. Read the reference (Read tool on the image) and inventory parts, proportions, colors, materials.
2. Draft a `bpy` script that:
   - Clears the scene.
   - Defines reusable materials via `Principled BSDF`.
   - Builds parts from primitives (`cube`, `sphere`, `cyl`, `cone`, `torus`) with `scale`, `rotation_euler`, `location`.
   - Applies `BEVEL`/`SUBSURF` modifiers and `shade_smooth()` where helpful.
3. Send via `execute_code`.
4. Verify with `get_scene_info` — check object count and names match expectations.

`blender_build.py` in the workspace is a working reference (keychain man + lobster).

## Exporting

After building, run via `execute_code`:

```python
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_mesh.stl(filepath='/absolute/path/out.stl', use_selection=True)
```

For OBJ: `bpy.ops.wm.obj_export(filepath=...)`.

## Failure modes

- **Connection refused**: addon not started or wrong port — ask the user to start it.
- **Socket timeout (30s)**: long scripts may exceed the helper's timeout; split the work or raise the timeout in `blender_send.py`.
- **Partial JSON**: the helper accumulates chunks; if it returns `None`, the script ran but Blender didn't reply — verify with `get_scene_info`.
- **`bpy.ops` context errors**: ensure objects are selected/active before ops that need them; prefer setting `bpy.context.view_layer.objects.active`.
