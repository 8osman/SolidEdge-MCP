"""
Solid Edge COM API Constants

These constants are defined by the Solid Edge API.
References: Solid Edge API documentation
"""


class RefPlaneConstants:
    """Reference plane type constants"""
    seRefPlaneTop = 1
    seRefPlaneFront = 2
    seRefPlaneRight = 3


class DocumentTypeConstants:
    """Document type constants"""
    igUnknownDocument = 0
    igPartDocument = 1
    igSheetMetalDocument = 2
    igAssemblyDocument = 3
    igDraftDocument = 4
    igWeldmentDocument = 5
    igWeldmentAssemblyDocument = 6


class FeaturePropertyConstants:
    """Feature property constants"""
    igStatusNormal = 0
    igStatusSuppressed = 1
    igStatusRollback = 2


class FeatureOperationConstants:
    """Feature operation type constants"""
    igFeatureAdd = 0
    igFeatureCut = 1
    igFeatureIntersect = 2
    igFeatureJoin = 3


class ExtrudedProtrusion:
    """Extrusion direction constants"""
    igRight = 0  # Normal direction
    igLeft = 1   # Reverse direction
    igSymmetric = 2  # Symmetric (both directions)


class HoleTypeConstants:
    """Hole type constants"""
    igRegularHole = 0
    igCounterboreHole = 1
    igCountersinkHole = 2
    igVHole = 3


class MateTypeConstants:
    """Assembly mate type constants"""
    igMate = 0
    igPlanarAlign = 1
    igAxialAlign = 2
    igInsert = 3
    igAngle = 4
    igTangent = 5
    igCam = 6
    igGear = 7
    igParallel = 8
    igConnect = 9
    igMatchCoordSys = 10


class ViewOrientationConstants:
    """View orientation constants"""
    seIsoView = 1
    seTopView = 2
    seFrontView = 3
    seRightView = 4
    seLeftView = 5
    seBackView = 6
    seBottomView = 7


class SaveAsConstants:
    """File save format constants"""
    igNormalSave = 0
    igSaveAsCopy = 1
