"""
Diagnostic tools for Solid Edge API exploration
"""

import traceback
from typing import Any


def get_available_methods(obj, filter_prefix=None):
    """
    Get all available methods and properties on a COM object

    Args:
        obj: COM object to inspect
        filter_prefix: Optional prefix to filter methods (e.g., "Add")

    Returns:
        Dictionary with methods and properties
    """
    methods = []
    properties = []

    try:
        # Get all attributes
        for attr_name in dir(obj):
            if filter_prefix and not attr_name.startswith(filter_prefix):
                continue

            try:
                attr = getattr(obj, attr_name)
                if callable(attr):
                    methods.append(attr_name)
                else:
                    properties.append(attr_name)
            except Exception:
                pass
    except Exception:
        pass

    return {
        "methods": sorted(methods),
        "properties": sorted(properties),
        "total_methods": len(methods),
        "total_properties": len(properties),
    }


def diagnose_document(doc):
    """
    Diagnose available features and collections in a document

    Args:
        doc: Solid Edge document object

    Returns:
        Dictionary with available collections and methods
    """
    info = {
        "document_type": type(doc).__name__,
        "available_collections": [],
        "models_methods": [],
        "cutout_related_methods": [],
    }

    # Check for common collections
    collection_names = [
        "Models",
        "ExtrudedCutouts",
        "Cutouts",
        "Features",
        "ProfileSets",
        "Profiles",
        "ExtrudedProtrusions",
        "Holes",
        "Rounds",
        "Chamfers",
        "Patterns",
        "RibWebs",
        "Threads",
        "Constructions",
        "RefPlanes",
        "UserDefinedPatterns",
        "Assemblies",
        "Occurrences",
        "SolidEdgePart",
        "Sketches",
    ]

    for name in collection_names:
        if hasattr(doc, name):
            info["available_collections"].append(name)
            try:
                collection = getattr(doc, name)
                # Get Add methods for this collection
                add_methods = get_available_methods(collection, "Add")
                info[f"{name}_add_methods"] = add_methods["methods"]
            except Exception:
                pass

    # Get all methods on Models collection
    if hasattr(doc, "Models"):
        models = doc.Models
        all_methods = get_available_methods(models)
        info["models_methods"] = all_methods["methods"]

        # Filter cutout-related
        cutout_methods = [
            m for m in all_methods["methods"] if "cutout" in m.lower() or "cut" in m.lower()
        ]
        info["cutout_related_methods"] = cutout_methods

    return info


def diagnose_feature(model):
    """
    Diagnose properties and methods available on a feature/model object.

    Args:
        model: Solid Edge Model/Feature object

    Returns:
        Dictionary with available properties, methods, and their values
    """
    info = {
        "model_type": type(model).__name__,
        "properties": {},
        "all_attributes": [],
        "operation_related": [],
    }

    # Properties to check
    property_names = [
        "Name",
        "Type",
        "Visible",
        "Suppressed",
        "FeatureType",
        "Operation",
        "OperationType",
        "SideStep",
        "ExtrusionType",
        "ProfileSide",
        "ProfilePlaneSide",
        "KeypointType",
        "FeatureOperationType",
    ]

    for prop_name in property_names:
        try:
            value = getattr(model, prop_name, None)
            if value is not None:
                info["properties"][prop_name] = str(value)
        except Exception as e:
            info["properties"][prop_name] = f"Error: {str(e)}"

    # Get all attributes
    all_attrs = get_available_methods(model)
    info["all_attributes"] = all_attrs["methods"] + all_attrs["properties"]

    # Find operation-related attributes
    keywords = ["operation", "side", "type", "cut", "add", "subtract", "feature"]
    operation_attrs = [
        attr
        for attr in info["all_attributes"]
        if any(keyword in attr.lower() for keyword in keywords)
    ]
    info["operation_related"] = operation_attrs

    return info


def diagnose_se_ai(app) -> dict[str, Any]:
    """
    Probe Solid Edge 2026's application object for any COM-accessible AI
    assistant interface.

    Checks:
    1. AI-keyword attrs on the Application object (ai, assistant, copilot,
       nlp, chat, prompt, ask, gpt, llm)
    2. Known SE 2026 candidate entry-point names probed individually
    3. CommandBarManager / FrameBarManager for AI pane discovery
    4. For any AI object found: dir() + string-accepting methods probed

    All probes are wrapped in try/except — nothing here can crash SE.

    Returns:
        Dict with all findings.
    """
    result: dict[str, Any] = {}

    # ── 1. keyword scan of Application attributes ─────────────────────────
    ai_keywords = ("ai", "assistant", "copilot", "nlp", "chat", "prompt",
                   "ask", "gpt", "llm", "intelligence", "natural")
    try:
        all_app_attrs = [a for a in dir(app) if not a.startswith("_")]
        ai_attrs = [
            a for a in all_app_attrs
            if any(kw in a.lower() for kw in ai_keywords)
        ]
        result["app_ai_keyword_attrs"] = ai_attrs
        result["app_total_attrs"] = len(all_app_attrs)
    except Exception as e:
        result["app_attr_scan_error"] = str(e)

    # ── 2. targeted entry-point probes ────────────────────────────────────
    candidates = [
        "AIAssistant", "SEAssistant", "NLPEngine", "AskSolidEdge",
        "CopilotPane", "AIPane", "ChatPane", "PromptEngine",
        "IntelligentFeature", "SECopilot", "AIFeature",
        "GetAIAssistant", "GetCopilot",
    ]
    probe_results: dict[str, Any] = {}
    for name in candidates:
        try:
            obj = getattr(app, name)
            obj_dir = [a for a in dir(obj) if not a.startswith("_")]
            # Look for any method that might accept a string command
            string_methods = []
            for m in obj_dir:
                try:
                    attr = getattr(obj, m)
                    # inspect signature if possible
                    import inspect as _inspect
                    sig = str(_inspect.signature(attr)) if callable(attr) else None
                    if sig and ("str" in sig or "text" in sig or "command" in sig
                                or "prompt" in sig or "query" in sig):
                        string_methods.append({"method": m, "sig": sig})
                    elif callable(attr):
                        string_methods.append({"method": m, "sig": sig})
                except Exception:
                    pass
            probe_results[name] = {
                "found": True,
                "type": type(obj).__name__,
                "dir": obj_dir,
                "string_methods": string_methods,
            }
        except Exception as e:
            probe_results[name] = {"found": False, "error": str(e)}
    result["candidate_probes"] = probe_results

    # ── 3. CommandBarManager / FrameBarManager / Panes ───────────────────
    bar_candidates = [
        "CommandBarManager", "FrameBarManager", "DockableWindows",
        "Panes", "TaskPanes", "WindowManager",
    ]
    bar_results: dict[str, Any] = {}
    for name in bar_candidates:
        try:
            obj = getattr(app, name)
            obj_dir = [a for a in dir(obj) if not a.startswith("_")]
            # Try to list pane/bar names if iterable
            items = []
            try:
                count = obj.Count
                for i in range(min(count, 50)):
                    try:
                        item = obj.Item(i + 1)
                        item_name = None
                        for n_attr in ("Name", "Caption", "Key"):
                            try:
                                item_name = getattr(item, n_attr)
                                break
                            except Exception:
                                pass
                        items.append(item_name or f"Item{i+1}")
                    except Exception:
                        items.append(f"Item{i+1}_error")
            except Exception:
                pass
            bar_results[name] = {
                "found": True,
                "type": type(obj).__name__,
                "dir": obj_dir,
                "items": items,
            }
        except Exception as e:
            bar_results[name] = {"found": False, "error": str(e)}
    result["bar_manager_probes"] = bar_results

    # ── 4. StartCommand probe — SE 2026 AI command IDs (guesses) ─────────
    # SE AI pane is often invoked via a ribbon command; try a few plausible IDs
    # We do NOT actually call StartCommand here (could change UI state),
    # just document the approach.
    result["start_command_note"] = (
        "To find the AI pane command ID, inspect "
        "Application.CommandBars or use SE macro recorder while opening "
        "the AI assistant pane, then call Application.StartCommand(id)."
    )

    return result
