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
