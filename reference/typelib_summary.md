# Solid Edge Type Library Reference

Generated: 2026-02-13T01:37:43 | SE 2026 | 40 type libraries

## Global Statistics

| Metric | Count |
|--------|-------|
| Type libraries | 40 |
| Enums | 1586 |
| Enum values | 14575 |
| Interfaces (dispatch+vtable) | 2240 |
| Methods | 21237 |
| Properties | 23445 |
| CoClasses | 278 |

## Type Library Overview

| File | Description | Enums | Interfaces | CoClasses |
|------|-------------|-------|------------|-----------|
| Program/CAEInterfaces.tlb | CAEInterfaces 1.0 Type Library | 2 | 14 | 0 |
| Program/CadenasWebViewAPI.tlb |  | 0 | 1 | 1 |
| Program/DataPath.tlb | DataPath 1.0 Type Library | 0 | 1 | 0 |
| Program/DesMgr.tlb | Solid Edge Design Manager Object Library | 16 | 7 | 7 |
| Program/DotNetEdge.tlb |  | 0 | 2 | 1 |
| Program/DotNetEdge4.tlb |  | 0 | 2 | 1 |
| Program/DotNetExcel.tlb |  | 0 | 2 | 1 |
| Program/EdgeManager.tlb | EdgeManager 1.0 Type Library | 0 | 0 | 22 |
| Program/FEAnalysisAdaptor.tlb | FEAnalysisAdaptor 1.0 Type Library | 0 | 6 | 6 |
| Program/InstallData.tlb | Solid Edge Install Data Library | 0 | 1 | 1 |
| Program/JUTIL3.tlb |  | 1 | 1 | 0 |
| Program/Part.tlb | Solid Edge Part Type Library | 176 | 915 | 0 |
| Program/PolarionConnector.tlb |  | 0 | 1 | 1 |
| Program/REFATTR.tlb |  | 0 | 5 | 0 |
| Program/RevMgr.tlb | Solid Edge Revision Manager Object Library (Deprecated) | 16 | 7 | 7 |
| Program/SE3Dtrans.tlb | SE3Dtrans 1.0 Type Library | 0 | 5 | 4 |
| Program/SE3dPrinting/SE3DPrint3YourMind.tlb |  | 0 | 0 | 1 |
| Program/SE3dPrinting/SE3DPrintDialog.tlb |  | 0 | 1 | 1 |
| Program/SE3dPrinting/SE3DPrintShinning.tlb |  | 0 | 0 | 1 |
| Program/SE3dPrinting/SE3DPrinting.tlb |  | 0 | 1 | 0 |
| Program/SEAcisTrans.tlb | SEAcisTrans 1.0 Type Library | 0 | 2 | 1 |
| Program/SEElectricalConnector.tlb |  | 0 | 1 | 1 |
| Program/SEPreview.tlb | SEPreview ActiveX Control module | 0 | 2 | 1 |
| Program/SERecordAndPublish/SERecordAndPublish.tlb |  | 0 | 2 | 1 |
| Program/SeThumbnail.tlb | SeThumbnail 1.0 Type Library | 0 | 2 | 2 |
| Program/SolidEdgeGateway.tlb |  | 0 | 3 | 2 |
| Program/StdParts/PFCOM.tlb | PFCOM | 5 | 1 | 1 |
| Program/StdParts/StdParts.tlb | StdParts 1.0 Type Library | 0 | 1 | 1 |
| Program/StructureEditor.tlb | Solid Edge Structure Editor Object Library | 0 | 3 | 3 |
| Program/assembly.tlb | Solid Edge Assembly Type Library | 75 | 288 | 0 |
| Program/constant.tlb | Solid Edge Constants Type Library | 745 | 0 | 0 |
| Program/ddmseapi.tlb | Dynamic Designer Motion Solid Edge Type Library | 17 | 47 | 46 |
| Program/draft.tlb | Solid Edge Draft Type Library | 78 | 197 | 0 |
| Program/framewrk.tlb | Solid Edge Framework Type Library | 113 | 301 | 44 |
| Program/fwksupp.tlb | Solid Edge FrameworkSupport Type Library | 120 | 228 | 0 |
| Program/geometry.tlb | Solid Edge Geometry Type Library | 5 | 68 | 0 |
| Program/iCnct.tlb | Solid Edge View And Markup Object Library | 1 | 1 | 1 |
| Program/onnxML.tlb |  | 0 | 1 | 1 |
| Program/partattr.tlb | Part Dynamic Attributes Type Library | 0 | 3 | 0 |
| Simulation/x64/femap.tlb | Simcenter™ Femap™ v2506.0 Type Library | 216 | 117 | 118 |

---
## Program/CAEInterfaces.tlb
**CAEInterfaces 1.0 Type Library** (GUID: `{AAAC8060-4AD5-101B-B826-00DD01103DE1}`, v1.0)

### Enums (2)

- **__MIDL___MIDL_itf_CAEInterfaces_0000_0000_0001** [20]: UnknownState=0, Ready=1, GeometryLoadError=2, GeometryLoaded=3, NoAnalysisModel=4, ... (20 total)
- **__MIDL___MIDL_itf_CAEInterfaces_0000_0000_0002** [4]: SolidStatic=0, SolidModal=1, SheetStatic=2, SheetModal=3

### Interfaces (14)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| IAnalysisModelAuto | dispatch | 6 | 7 |
| ICAEProcessMgrAuto | dispatch | 13 | 6 |
| IConstraintAuto | dispatch | 0 | 2 |
| IConstraintSetAuto | dispatch | 2 | 0 |
| IForceAuto | dispatch | 2 | 4 |
| IFullConstraintAuto | dispatch | 0 | 2 |
| IIncidentMgr | dispatch | 5 | 0 |
| ILoadAuto | dispatch | 0 | 2 |
| ILoadSetAuto | dispatch | 2 | 0 |
| IModalSheetAnalysisAuto | dispatch | 8 | 11 |
| IModalVolumeAnalysisAuto | dispatch | 8 | 10 |
| IPressureAuto | dispatch | 0 | 4 |
| IStaticSheetAnalysisAuto | dispatch | 6 | 8 |
| IStaticVolumeAnalysisAuto | dispatch | 6 | 7 |

### Aliases (2)

- AnalysisState = __MIDL___MIDL_itf_CAEInterfaces_0000_0000_0001
- AnalysisType = __MIDL___MIDL_itf_CAEInterfaces_0000_0000_0002

---
## Program/CadenasWebViewAPI.tlb
**** (GUID: `{BC3185F1-C597-49AF-BC44-E5E53DBEF847}`, v1.0)

### Interfaces (1)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| IThreeDfindITNativeAPI | interface | 2 | 0 |

### CoClasses (1)

- **ThreeDfindITNativeAPI** (`{0E946730-0BDB-4BBB-B0D4-47FA9B9E3AD5}`): IThreeDfindITNativeAPI, IDispatch

---
## Program/DataPath.tlb
**DataPath 1.0 Type Library** (GUID: `{FFE478E7-3FA9-11D3-BEF5-080036D7B302}`, v1.0)

### Interfaces (1)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| _IJBindStatusEvents | interface | 3 | 0 |

---
## Program/DesMgr.tlb
**Solid Edge Design Manager Object Library** (GUID: `{427C71BD-B200-4421-AB49-12DA610B369E}`, v1.0)

### Enums (16)

- **ApplicationGlobalConstants** [24]: seApplicationGlobalCheckInOnClose=0, seApplicationGlobalLogFilesLocation=1, seApplicationGlobalInsightCacheLocation=2, seApplicationGlobalInsightFolderMappingFileLocation=3, seApplicationGlobalSearchScope=4, ... (24 total)
- **CheckInOptions** [2]: DoNotCheckInOption=0, UploadAndCheckInOption=1
- **CookieDataToGet** [1]: GET_REVISION_RULE=0
- **DesignManagerAction** [15]: UnknownAction=0, SaveAsAction=1, SaveAsAllAction=2, ReviseAction=3, ReviseAllAction=4, ... (15 total)
- **DocFOPStatus** [5]: FopStatusUnknown=0, NotInvolvedInFOP=1, FOPMasterDocument=2, FOPMemberDocument=4, FOPMasterAndChild=6
- **DocFOPStatusEx** [5]: FopStatusUnknownEx=0, NotInvolvedInFOPEx=1, FOPSourceDocumentEx=2, FOPMemberDocumentEx=4, FOPSourceAndChildEx=6
- **DocumentAccess** [3]: igReadWrite=0, igReadOnly=1, igReadExclusive=2
- **DocumentStatus** [6]: igStatusAvailable=0, igStatusInWork=1, igStatusInReview=2, igStatusReleased=3, igStatusBaselined=4, ... (6 total)
- **InsightSPUserRights** [23]: seViewListItems=1, seAddListItems=2, seEditListItems=4, seDeleteListItems=8, seCancelCheckout=256, ... (23 total)
- **InterPartLinkOption** [4]: eInterPartLinkUnknown=0, eCopyAllLinkedDocs=1, eUpdateLinksToNewDoc=2, eOutOfContextWithNewDoc=3
- **LinkTypeConstants** [3]: seLinkTypeAll=0, seLinkTypeNormal=1, seLinkTypeInterpart=2
- **OverWriteFilesOption** [2]: NoToAll=0, YesToAll=1
- **RevisionRuleType** [4]: LastSavedType=0, LatestReleasedRevision=1, LatestRevision=2, ExternalBOM=3
- **SPServerType** [4]: SERVER_TYPE_NOT_SHAREPOINT=0, SHAREPOINT_V1_SERVER=1, SHAREPOINT_V2_SERVER=2, SHAREPOINT_V3_SERVER=3
- **SearchType** [2]: ShallowSearch=0, DeepSearch=1
- **UploadType** [2]: DeepUploadType=0, ShallowUploadType=1

### Interfaces (7)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| IDMgrApp | dispatch | 31 | 3 |
| IDocAuto | dispatch | 14 | 1 |
| IInsight | dispatch | 60 | 0 |
| ILinkedDocsAuto | dispatch | 0 | 3 |
| IPropertiesAuto | dispatch | 2 | 3 |
| IPropertyAuto | dispatch | 1 | 0 |
| IPropertySetsAuto | dispatch | 4 | 2 |

### CoClasses (7)

- **Application** (`{F3C2777E-C913-4859-96BA-722B5F0276E7}`): IDMgrApp
- **Document** (`{5CAC1974-0CD0-11D1-BC6F-0800360E1E02}`): IDocAuto
- **Insight** (`{06AEF304-AD7E-4C10-9904-29463E231246}`): IInsight
- **LinkedDocuments** (`{5CAC1977-0CD0-11D1-BC6F-0800360E1E02}`): ILinkedDocsAuto
- **Properties** (`{1EA5BA57-78F6-44BD-B68B-C3DD52632080}`): IPropertiesAuto
- **Property** (`{DE2F5653-8899-4355-A14B-27B5DC32A0FE}`): IPropertyAuto
- **PropertySets** (`{0323A7D6-9F38-4000-BF00-7AFAF7A40F99}`): IPropertySetsAuto

---
## Program/DotNetEdge.tlb
**** (GUID: `{6012B7D6-560B-32BE-BF56-BECDA5A0749A}`, v226.0)

### Interfaces (2)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| Refuse | dispatch | 2 | 0 |
| _DotNetRefuse | dispatch | 0 | 0 |

### CoClasses (1)

- **DotNetRefuse** (`{31267087-EE1A-3E0B-8F6A-5A90BFDC331C}`): _DotNetRefuse, _Object, Refuse

---
## Program/DotNetEdge4.tlb
**** (GUID: `{42FBE0F2-BDC1-41CB-9DD6-9252E2A94E3D}`, v226.0)

### Interfaces (2)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| Refuse4 | dispatch | 2 | 0 |
| _DotNetRefuse4 | dispatch | 0 | 0 |

### CoClasses (1)

- **DotNetRefuse4** (`{3A4D2AB6-C637-3916-8D77-7C7AFA91250E}`): _DotNetRefuse4, _Object, Refuse4

---
## Program/DotNetExcel.tlb
**** (GUID: `{CE5FA11D-0B44-427F-809F-BCD1FC087048}`, v226.0)

### Interfaces (2)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| ExcelReader | dispatch | 3 | 0 |
| _DotNetExcelReader | dispatch | 0 | 0 |

### CoClasses (1)

- **DotNetExcelReader** (`{D4F6E02E-B02E-4F5F-BE97-E1356DABA65E}`): _DotNetExcelReader, _Object, ExcelReader

---
## Program/EdgeManager.tlb
**EdgeManager 1.0 Type Library** (GUID: `{934F7164-E501-4BE7-ABF6-021AABF55E49}`, v1.0)

### CoClasses (22)

- **CommandEvents** (`{31C948CB-EC74-46D8-884E-08E7DD4DA2B6}`): ISECommandEvents
- **CommandWindowEvents** (`{3E695F92-7617-4600-9D8D-751CA6BF9A52}`): ISECommandWindowEvents
- **Commands** (`{28175248-9930-4A1E-A8DF-E4E117DB43C7}`): IUnknown
- **EDGEMANAGERAddInEvents** (`{FD4645A2-3167-440B-AA2F-B440E144D921}`): ISEAddInEvents
- **EDGEMANAGERApplicationEvents** (`{D1E02795-5DBF-4A40-9F8A-58993F13D215}`): IUnknown
- **EDGEMANAGERApplicationWindowEvents** (`{129A7C91-EF05-4D2F-AFDE-A0C73FC2825F}`): IUnknown
- **EDGEMANAGERAssemblyRecomputeEvents** (`{A9431525-4DDE-415B-8F7A-2B9F975CFB51}`): ISEAssemblyRecomputeEvents
- **EDGEMANAGERCommand** (`{12E2E139-DEFD-499A-BDD1-FD4A19AE181A}`): IUnknown
- **EDGEMANAGERDividePartEvents** (`{FF36717C-8C3C-41A3-90BB-1F4F8774DC84}`): ISEDividePartEvents
- **EDGEMANAGERDocument** (`{EFF4D97C-0405-4AA7-988C-2744EE35762F}`): IUnknown
- **EDGEMANAGERDocumentEvents** (`{D5033624-CF0E-4AD7-B818-1C014E266EEE}`): ISEDocumentEvents
- **EDGEMANAGERDrawingViewEvents** (`{82729C59-E91D-4473-BE4D-C52EB9F44ECD}`): ISEDrawingViewEvents
- **EDGEMANAGERFamilyOfPartsEvents** (`{181B1371-9704-4B09-BA7D-A539B5F849F3}`): ISEFamilyOfPartsEvents
- **EDGEMANAGERFeatureLibraryEvents** (`{BA574906-FE1C-40C0-B6DE-2B060BFF22BF}`): ISEFeatureLibraryEvents
- **EDGEMANAGERFileUIEvents** (`{13C76E4C-78EF-4CAC-B560-00D67354F01F}`): ISEFileUIEvents
- **EDGEMANAGERGLDisplayEvents** (`{E06EC383-9088-4FEF-BE86-6D6759F499A1}`): ISEIGLDisplayEvents
- **EDGEMANAGERModel** (`{8F836C94-258D-4F08-B9EF-D77181610CED}`): IUnknown
- **EDGEMANAGERModelRecomputeEvents** (`{5F9C7268-B649-48D7-9585-1B7DFD5EC201}`): ISEModelRecomputeEvents
- **EDGEMANAGERView** (`{6FEEDEF1-FACE-450D-AD7F-0C2B72FEB5F4}`): IUnknown
- **EDGEMANAGERViewEvents** (`{F91D18CD-101A-4E41-86BD-C9D37548EEF1}`): ISEViewEvents
- **EDGEMANAGERhDCDisplayEvents** (`{E51C3D69-317B-40D9-950E-261DB0358542}`): ISEhDCDisplayEvents
- **MouseEvents** (`{4EB18198-9485-4372-93C8-7628018C1F83}`): ISEMouseEvents

---
## Program/FEAnalysisAdaptor.tlb
**FEAnalysisAdaptor 1.0 Type Library** (GUID: `{4BCB26FC-5C89-43E5-BA88-D30247FBF5BD}`, v1.0)

### Interfaces (6)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| IAnalysisAdaptor | dispatch | 1 | 3 |
| IConstraintSet | dispatch | 0 | 0 |
| IForce | dispatch | 0 | 0 |
| IFullConstraint | dispatch | 0 | 0 |
| ILoadSet | dispatch | 0 | 0 |
| IPressure | dispatch | 0 | 0 |

### CoClasses (6)

- **AnalysisAdaptor** (`{7EFED384-841F-4E3C-B373-22C18827E60E}`): IAnalysisAdaptor
- **ConstraintSet** (`{34049C51-8DEC-4C9D-995F-5A20039347C1}`): IConstraintSet
- **Force** (`{ABDF5CCC-1AFD-4553-9850-B7A56C404DEA}`): IForce
- **FullConstraint** (`{C4891C71-9EF8-4F5D-997E-EF2E5E4E6536}`): IFullConstraint
- **LoadSet** (`{0F48B9A3-6C15-4D22-B805-47B8795B6C4C}`): ILoadSet
- **Pressure** (`{6B9E6E6A-2449-4DC2-8DE0-0AC295F10515}`): IPressure

---
## Program/InstallData.tlb
**Solid Edge Install Data Library** (GUID: `{42E04299-18A0-11D5-BBB2-00C04F79BEA5}`, v1.0)

### Interfaces (1)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| ISEInstallData | dispatch | 12 | 0 |

### CoClasses (1)

- **SEInstallData** (`{42E042A6-18A0-11D5-BBB2-00C04F79BEA5}`): ISEInstallData

---
## Program/JUTIL3.tlb
**** (GUID: `{5F3BD9F9-B22F-43B9-A77D-48DE156C1A96}`, v1.0)

### Enums (1)

- **LicenseMessageContext** [3]: LicensorStartup=1, LicensorCheckout=2, LicensorGetDaysUntilExpiration=3

### Interfaces (1)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| ILicenseMessage | interface | 1 | 0 |

---
## Program/Part.tlb
**Solid Edge Part Type Library** (GUID: `{8A7EFA42-F000-11D1-BDFC-080036B4D502}`, v1.0)

### Enums (176)

- **AddBodyTypeConstants** [7]: igPartType=1, igSheetMetalType=2, igSubdivisionType=3, igSubdivisionControlCageType=4, igConstructionPartType=5, ... (7 total)
- **AlignBodyFaceType** [6]: seAlignBodyFaceTypeFront=0, seAlignBodyFaceTypeBack=1, seAlignBodyFaceTypeTop=2, seAlignBodyFaceTypeBottom=3, seAlignBodyFaceTypeLeft=4, ... (6 total)
- **AlignBodyPointTypeOnFace** [9]: seAlignBodyPointTypeOnFaceLeftBottom=0, seAlignBodyPointTypeOnFaceLeftMiddle=1, seAlignBodyPointTypeOnFaceLeftTop=2, seAlignBodyPointTypeOnFaceCenterBottom=3, seAlignBodyPointTypeOnFaceCenterMiddle=4, ... (9 total)
- **AssemblyWeldmentOccurrencesOptionsConstants** [3]: seIncludeAllOccurrences=1, seIncludeInputOccurrences=2, seExcludeInputOccurrences=3
- **AttachedStatusConstants** [8]: seStatusOK=0, seStatusMissingPropertyObject=1, seStatusMissingPropertyTable=2, seStatusMissingAttachedEntites=3, seStatusDuplicateProperties=4, ... (8 total)
- **BendCalculationMethodConstants** [3]: BendCalculationMethodNeutralFactor=0, BendCalculationMethodBendDeduction=1, BendCalculationMethodBendAllowance=2
- **BendDirectionConstants** [3]: seBendDirectionUnknown=0, seBendDirectionUp=1, seBendDirectionDown=2
- **BendFeatureConstants** [20]: seBendOnlyCornerRelief=1, seBendAndFaceCornerRelief=2, seBendExtendMoldlines=3, seBendNoExtendMoldines=4, seBendMoveRight=5, ... (20 total)
- **BlendShapeConstants** [6]: igBlendShapeConstantRadius=1, igBlendShapeConstantWidth=2, igBlendShapeChamfer=3, igBlendShapeRatioChamfer=4, igBlendShapeConic=5, ... (6 total)
- **BlockLabelOriginLocationConstants** [12]: igBlockLabelTopLeft=0, igBlockLabelTopCenter=1, igBlockLabelTopRight=2, igBlockLabelMiddleLeft=3, igBlockLabelMiddleCenter=4, ... (12 total)
- **BooleanFeatureConstants** [5]: seBooleanIntersect=1, seBooleanSubtract=2, seBooleanUnite=3, seBooleanPlaneFront=4, seBooleanPlaneBack=5
- **CageOffsetTypes** [2]: CageOffsetTypeTip=1, CageOffsetTypeLift=2
- **CleanProfileOptions** [2]: igCleanProfileDelete=1, igCleanProfileMove=2
- **CloseCornerFeatureConstants** [9]: seCloseCornerCloseFaces=1, seCloseCornerOverlapFaces=2, seCloseCornerTreatmentOff=3, seCloseCornerTreatmentIntersect=4, seCloseCornerTreatmentCircularCutout=5, ... (9 total)
- **ConstraintTypeConstants** [8]: igRelationConcentric=1, igRelationCoincident=2, igRelationParallel=3, igRelationPerpendicular=4, igRelationTangent=5, ... (8 total)
- **CoordinateSystemFeatureConstants** [6]: seCoordSysXAxis=1, seCoordSysYAxis=2, seCoordSysZAxis=3, seCoordSysXYPlane=4, seCoordSysYZPlane=5, ... (6 total)
- **CoordinateSystemOffsetTypeConstants** [2]: seCoordSysOffsetGlobal=1, seCoordSysOffsetRelative=2
- **CoordinateSystemRotationTypeConstants** [2]: seCoordSysRotateAboutSelf=1, seCoordSysRotateAboutParent=2
- **CoordinateSystemTypeConstants** [3]: seCoordSysGeometryBased=1, seCoordSysNonGeometryBased=2, seCoordSysNonGeometricRelativeTo=3
- **CopySurfaceExternalBoundaryConstants** [2]: igCopySurfaceRemoveExternalBoundaries=1, igCopySurfaceCopyExternalBoundaries=2
- **CopySurfaceInternalBoundaryConstants** [2]: igCopySurfaceRemoveInternalBoundaries=1, igCopySurfaceCopyInternalBoundaries=2
- **DecalMappingType** [2]: seLabel=1, sePlanarProjection=2
- **DeleteFaceConstants** [2]: igDeleteFaceApplyHeal=1, igDeleteFaceApplyNoHeal=2
- **DerivedCurveTypeConstants** [2]: igDCComposite=1, igDCCurve=2
- **DimpleFeatureConstants** [12]: seDimpleDepthLeft=1, seDimpleDepthRight=2, seDimpleDimensionOffset=3, seDimpleDimensionFull=4, seDimpleProfileLeft=5, ... (12 total)
- **DividedPartCutDirectionConstants** [2]: seDividedPartCutNormal=0, seDividedPartCutReverseNormal=1
- **DividedPartStatusConstants** [4]: seDividedPartStatusNotCreated=0, seDividedStatusUpToDate=1, seDividedStatusOutOfDate=2, seDividedStatusLinkBroken=3
- **DraftSideConstants** [3]: seDraftInside=4, seDraftOutside=5, seDraftNone=44
- **DrawnCutoutFeatureConstants** [10]: seDrawnCutoutDepthLeft=1, seDrawnCutoutDepthRight=2, seDrawnCutoutMaterialInside=3, seDrawnCutoutMaterialOutside=4, seDrawnCutoutProfileLeft=5, ... (10 total)
- **EnclosureTypeConstant** [3]: igEnclosureTypeBox=0, igEnclosureTypeInsideCylinder=1, igEnclosureTypeOutsideCylinder=2
- **EquationDrivenCurveErrorCode** [5]: seEquationDrivenCurveErrorCodeUnknownError=-1, seEquationDrivenCurveErrorCodeNoError=0, seEquationDrivenCurveErrorCodeInvalidExpression=1, seEquationDrivenCurveErrorCodeSelfIntersecting=2, seEquationDrivenCurveErrorCodeDiscontinuous=3
- **ExtendSurfaceExtentTypeConstants** [6]: igESNatural=1, igESLinear=2, igESLinearTangentContinuous=3, igESLinearCurvatureContinuous=4, igESReflective=5, ... (6 total)
- **FEABoltConnHoleTypeEnum_Auto** [4]: eBoltConnHoleTypeNone_Auto=0, eBoltConnHoleTypeAutomatic_Auto=1, eBoltConnHoleTypeThreaded_Auto=2, eBoltConnHoleTypeLooseFit_Auto=3
- **FEAConnectorTypeEnum_Auto** [8]: eConnectorTypeNone_Auto=0, eConnectorTypeLinear_Auto=1, eConnectorTypeGlue_Auto=2, eConnectorTypeBoltConnection_Auto=3, eConnectorTypeEdgeConnector_Auto=4, ... (8 total)
- **FEAConstraintTypeEnum_Auto** [7]: eCnstrTypeNone_Auto=0, eCnstrTypeFixed_Auto=1, eCnstrTypePinned_Auto=2, eCnstrTypeNoRotation_Auto=3, eCnstrTypeSlidingAlongSurface_Auto=4, ... (7 total)
- **FEADesBoundType_Auto** [2]: eFEADesBoundTypeValue_Auto=0, eFEADesBoundTypeNone_Auto=1
- **FEADesObjAction_Auto** [4]: eDesObjActionNone_Auto=0, eDesObjActionMin_Auto=1, eDesObjActionMax_Auto=2, eDesObjActionTarget_Auto=3
- **FEADesObjType_Auto** [7]: eDesObjTypeNone_Auto=0, eDesObjTypeMass_Auto=1, eDesObjTypeVloume_Auto=2, eDesObjTypeSurfArea_Auto=3, eDesObjTypeResComp_Auto=4, ... (7 total)
- **FEADesObjValueType_Auto** [3]: eDesObjValueTyeNone_Auto=0, eDesObjValueTypeMin_Auto=1, eDesObjValueypeMax_Auto=2
- **FEADesignVarType_Auto** [4]: eFEADesignVarTypeNone_Auto=0, eFEADesignVarTypeDim_Auto=1, eFEADesignVarTypeVar_Auto=2, eFEADesignVarTypeSimVar_Auto=3
- **FEAFileType_Auto** [2]: eFEAModFile_Auto=0, eFEANastranFile_Auto=1
- **FEAFunctionType_Auto** [4]: eFunctionTypeNone_Auto=0, eFunctionTypeFreqVsFactor_Auto=1, eFunctionTypeTimeVsFactor_Auto=2, eFunctionTypeFreqVsStructDamping_Auto=3
- **FEAInitialPenetrationTypeEnum_Auto** [3]: eCalculatedType_Auto=0, eCalculatedOrZeroType_Auto=1, eZeroGapType_Auto=2
- **FEALoadTypeEnum_Auto** [19]: eLoadTypeNone_Auto=0, eLoadTypeForce_Auto=1, eLoadTypePressure_Auto=2, eLoadTypeTorque_Auto=3, eLoadTypeGravity_Auto=4, ... (19 total)
- **FEAMeshTypeEnum_Auto** [5]: eMeshTypeNone_Auto=0, eMeshTypeTetrahedral_Auto=1, eMeshType2D_Auto=2, eMeshTypeMixed_Auto=3, eMeshTypeBeam_Auto=4
- **FEAMesherType_Auto** [2]: eFEAMesherTypeLegacy_Auto=0, eFEAMesherTypeBody_Auto=1
- **FEAPlotsOwnerTypeEnum_Auto** [17]: ePlotsOwnerTypeNone_Auto=0, ePlotsOwnerTypeDisplacement_Auto=1, ePlotsOwnerTypeRotation_Auto=2, ePlotsOwnerTypeAppliedForce_Auto=3, ePlotsOwnerTypeAppliedMoment_Auto=4, ... (17 total)
- **FEAStudyGeomTypeEnum_Auto** [5]: eStudyGeomTypeNone_Auto=0, eStudyGeomTypeSync_Auto=1, eStudyGeomTypeOrdered_Auto=2, eStudyGeomTypeSimplify_Auto=3, eStudyGeomTypeDesigned_Auto=4
- **FEAStudyTypeEnum_Auto** [9]: eStudyTypeNone_Auto=0, eStudyTypeLinearStatic_Auto=1, eStudyTypeNormalModal_Auto=2, eStudyTypeLinearBuckling_Auto=3, eStudyTypeSSHT_Auto=4, ... (9 total)
- **FaceMoveConstants** [13]: igFaceMoveNone=0, igFaceMoveAlong2PointVector=1, igFaceMoveAlongFaceNormal=2, igFaceMoveAlongEdge=3, igFaceMoveInPlane=4, ... (13 total)
- **FaceOffsetConstants** [3]: igFaceOffsetNone=0, igFaceOffsetBySynchronousOffset=1, igFaceOffsetByOffset=2
- **FaceRotateConstants** [8]: igFaceRotateNone=0, igFaceRotateByPoints=1, igFaceRotateByGeometry=2, igFaceRotateAxisStart=3, igFaceRotateAxisEnd=4, ... (8 total)
- **FamilyMemberStatusConstants** [6]: seStatusUnknown=0, seStatusNotCreated=1, seStatusUpToDate=2, seStatusOutOfDate=3, seStatusLinkBroken=4, ... (6 total)
- **FeatureLoopType** [3]: eIncludeInternalLoop=1, eExcludeInternalLoop=2, eUseOnlyInternalLoop=3
- **FeaturePropertyConstants** [258]: igNullConstant=0, igLeft=1, igRight=2, igSymmetric=3, igInside=4, ... (258 total)
- **FeatureStatusConstants** [5]: igFeatureOK=1216476310, igFeatureFailed=1216476311, igFeatureWarned=1216476312, igFeatureSuppressed=1216476313, igFeatureRolledBack=1216476314
- **FeatureTypeConstants** [129]: igEmbossFeatureObject=-2101998503, igSweptProtrusionFeatureObject=-2101194894, igBeadFeatureObject=-2099521208, igWeldPatternFeatureObject=-1994967864, igUnitedBodyObject=-1974090952, ... (129 total)
- **FillHoleType** [4]: seFillHoleTypeLinear=0, seFillHoleTypeRefined=1, seFillHoleTypeTangent=2, seFillHoleTypeCurvature=3
- **FillPatternMethodConstants** [6]: seRectangularFillMethod=1, seStaggerPolarFillMethod=2, seStaggerLinearOffsetFillMethod=3, seRadialTargetSpacingFillMethod=4, seRadialInstanceCountFillMethod=5, ... (6 total)
- **FilletWeldSetbackConstants** [3]: seFilletWeldEqualSetback=0, seFilletWeldUnequalSetback=1, seFilletWeldThickness=2
- **FlangeFeatureConstants** [10]: seFlangeBendOnlyCornerRelief=1, seFlangeBendAndFaceCornerRelief=2, seFlangeBendAndFaceChainRelief=3, seFlangeMaterialInside=4, seFlangeMaterialOutside=5, ... (10 total)
- **FlattenPatternModelTypeConstants** [3]: igFlattenPatternModelTypeDevelopable=0, igFlattenPatternModelTypeNonDevelopable=1, igFlattenPatternModelTypeFlattenAnything=2
- **GenerativeConstraintTypeConstants** [5]: seGenerativeDesignUnknownConstraint=0, seGenerativeDesignFixedConstraint=1, seGenerativeDesignPinnedConstraint=2, seGenerativeDesignDisplacementConstraint=3, seGenerativeDesignMaximumDisplacementConstraint=4
- **GenerativeDirectionTypeConstants** [8]: seGenerativeDesignDirectionTypeUnknown=0, seGenerativeDesignDirectionTypeNormalToFace=1, seGenerativeDesignDirectionTypeAlongVector=2, seGenerativeDesignDirectionTypeByXYZComponents=3, seGenerativeDesignDirectionTypeAbsoluteMagnitude=4, ... (8 total)
- **GenerativeLoadTypeConstants** [4]: seGenerativeDesignUnknownLoad=0, seGenerativeDesignForceLoad=1, seGenerativeDesignPressureLoad=2, seGenerativeDesignTorqueLoad=3
- **GenerativeMaterialExtrusionAxisConstants** [4]: seGenerativeMaterialExtrusionAxisConstantsNone=0, seGenerativeMaterialExtrusionAxisConstantsX=1, seGenerativeMaterialExtrusionAxisConstantsY=2, seGenerativeMaterialExtrusionAxisConstantsZ=3
- **GenerativeMaterialExtrusionDirectionConstants** [3]: seGenerativeMaterialExtrusionDirectionConstantsPositive=0, seGenerativeMaterialExtrusionDirectionConstantsNegative=1, seGenerativeMaterialExtrusionDirectionConstantsBoth=2
- **GenerativeOverhangDraftAngleDirectionConstants** [4]: seGenerativeOverhangDraftAngleDirectionConstantsNone=0, seGenerativeOverhangDraftAngleDirectionConstantsX=1, seGenerativeOverhangDraftAngleDirectionConstantsY=2, seGenerativeOverhangDraftAngleDirectionConstantsZ=3
- **GenerativePlanarSymmetryTypeConstants** [3]: seGenerativePlanarSymmetryTypeHalf=1, seGenerativePlanarSymmetryTypeQuarter=2, seGenerativePlanarSymmetryTypeOneEighth=3
- **GenerativeStudyNotReadyForSolveReasons** [6]: seGenerativeDesignStudyNotReadyForSolveUnknownReason=0, seGenerativeDesignStudyNotReadyForSolveDesignSpaceUndefined=1, seGenerativeDesignStudyNotReadyForSolveMaterialNotDefined=2, seGenerativeDesignStudyNotReadyForSolveDoesNotHaveAtLeastOneValidLoadCase=3, seGenerativeDesignStudyNotReadyForSolveAllLoadCasesSuppressed=4, ... (6 total)
- **GenerativeStudyOptimizationType** [3]: seGenerativeStudyOptimizationTypeUnknown=0, seGenerativeStudyOptimizationTypeReduceMassByPercentage=1, seGenerativeStudyOptimizationTypeFactorOfSafety=2
- **GussetConstants** [9]: igGussetNone=0, igAutomaticProfile=1, igUserDrawnProfile=2, igRoundShape=3, igSquareShape=4, ... (9 total)
- **GussetPlateAlignmentConstants** [3]: GussetPlateAlignType_Center=0, GussetPlateAlignType_Right=1, GussetPlateAlignType_Left=2
- **GussetPlateErrorCode** [6]: GussetPlateErrorCodeUnknownError=-1, GussetPlateErrorCodeNoError=0, GussetPlateErrorCodeMissingParameter=1, GussetPlateErrorCodeInvalidParameter=2, GussetPlateErrorCodeNoReferencePlane=3, ... (6 total)
- **GussetPlateThicknessDirConstants** [3]: GussetPlateDir_Center=0, GussetPlateDir_Right=1, GussetPlateDir_Left=2
- **HelicalCurveMethodType** [3]: igHelicalCurveMethodPitchAndHeight=0, igHelicalCurveMethodPitchAndTurns=1, igHelicalCurveMethodHeightAndTurns=2
- **HelicalCurveTaperByType** [3]: igHelicalCurveTaperNone=0, igHelicalCurveTaperByAngle=1, igHelicalCurveTaperByDiameter=2
- **HemFeatureConstants** [15]: seHemTypeClosed=1, seHemTypeOpen=2, seHemTypeSFlange=3, seHemTypeCurl=4, seHemTypeOpenLoop=5, ... (15 total)
- **HoleDataUnitsConstants** [2]: igHoleDataUnitsInches=0, igHoleDataUnitsMillimeters=1
- **HoleToleranceTypeConstants** [2]: seStandardFit_Tolerance=0, seUnit_Tolerance=1
- **HoleTypeToDeleteConstants** [3]: seHoleTypeToDeleteFeaturesOnly=0, seHoleTypeToDeleteCylindersAndConesOnly=1, seHoleTypeToDeleteAll=2
- **IsoclineDirectionConstants** [2]: igIsoclineleft=1, igIsoclineRight=2
- **JogFeatureConstants** [19]: seJogBendNFT=1, seJogBendEqn=2, seJogBRRectangular=3, seJogBRFillet=4, seJogBendOnlyCR=5, ... (19 total)
- **KeyPointExtentConstants** [4]: igTangentNormal=1, igReverseTangentNormal=2, igInteriorTangentNormal=3, igInteriorReverseTangentNormal=4
- **KeypointEndConditionConstants** [5]: seKeypointEndConditionNatural=1, seKeypointEndConditionPeriodic=2, seKeypointEndConditionTangent=3, seKeypointEndConditionNormalToFace=4, seKeypointEndConditionCurvatureContinuous=5
- **LiveRulesConstants** [18]: igConcentricLiveRule=1, igCoplanarLiveRule=2, igTangentEdgeLiveRule=3, igTangentTouchingLiveRule=4, igParallelLiveRule=5, ... (18 total)
- **LoadSymbDirOptsEnum_Auto** [10]: eLoadDirDefault_Auto=0, eLoadDirAlongVec_Auto=1, eLoadDirNormalToFace_Auto=2, eLoadDirTorque_Auto=3, eLoadDirGravity_Auto=4, ... (10 total)
- **LoftedFlangeFeatureAutoReliefConstants** [2]: igLoftedFlangeAutoReliefSpherical=251, igLoftedFlangeAutoReliefLinear=252
- **LoftedFlangeFeatureAutoReliefTrimConstants** [2]: igLoftedFlangeAutoReliefTrimEndPlates=253, igLoftedFlangeAutoReliefTrimNone=254
- **LoftedFlangeFeatureBendingMethodConstants** [4]: igLoftedFlangeFeatureBendingMethodNone=1, igLoftedFlangeFeatureBendingMethodGraphicBends=2, igLoftedFlangeFeatureBendingMethodRealBends=3, igLoftedFlangeFeatureBendingMethodFormedBends=4
- **LoftedFlangeFeatureDivideBendConstants** [4]: igLoftedFlangeDivideBendByCount=255, igLoftedFlangeDivideBendByMaximumChordHeight=256, igLoftedFlangeDivideBendByMaximumSegmentLength=257, igLoftedFlangeDivideBendByMaximumSegmentAngle=258
- **LouverFeatureConstants** [10]: seLouverDepthDirectionLeft=1, seLouverDepthDirectionRight=2, seLouverDimensionOffset=3, seLouverDimensionFull=4, seLouverFormedEnd=5, ... (10 total)
- **MeasureDistanceTypeConstants** [3]: MeasureDistanceTypeConstants_MinimumDistance=1, MeasureDistanceTypeConstants_MaximumDistance=2, MeasureDistanceTypeConstants_SmartDistance=3
- **MeasureVariableTypeConstants** [4]: MeasureVariableTypeConstants_Distance=1, MeasureVariableTypeConstants_MinimumDistance=2, MeasureVariableTypeConstants_NormalDistance=3, MeasureVariableTypeConstants_Angle=4
- **MeasureVariableValueConstants** [1]: MeasureVariableValueConstants_TrueMeasure=1
- **MeshControlType_Auto** [4]: eNoneMeshControl_Auto=0, eBodyMeshControl_Auto=1, eSurfaceMeshControl_Auto=2, eEdgeMeshControl_Auto=3
- **MirrorOptionConstants** [4]: MirrorOptionNormal=1, MirrorOptionDetach=2, MirrorOptionPersist=4, MirrorOptionRemoveOriginal=8
- **ModelingModeConstants** [2]: seModelingModeSynchronous=1, seModelingModeOrdered=2
- **MoveConnectedFaceTypes** [3]: seMoveConnectedFaceTypeExtendTrim=0, seMoveConnectedFaceTypeTip=1, seMoveConnectedFaceTypeLift=2
- **MovePrecedenceConstants** [2]: igSelectSetMovePrecedence=1, igModelMovePredecence=2
- **MultiBodyPublishStatusConstants** [7]: seMBPStatusUnknown=0, seMBPStatusNotCreated=1, seMBPStatusUpToDate=2, seMBPStatusOutOfDate=3, seMBPStatusFailed=4, ... (7 total)
- **OffsetSideConstants** [3]: seOffsetLeft=1, seOffsetRight=2, seOffsetNone=44
- **PMIModelStateConstants** [3]: seDesignModelState=1, seFlatModelState=2, seSimplifyModelState=3
- **PartBaseStylesConstants** [6]: sePartBaseStyle=0, seConstructionBaseStyle=1, seThreadedCylindersBaseStyle=2, seCurveBaseStyle=3, seWeldBeadBaseStyle=4, ... (6 total)
- **PartGlobalConstants** [8]: sePartGlobalDensity=1, sePartGlobalAccuracyForDensity=2, sePartGlobalMaterial=3, sePartGlobalCombMaximumDensity=4, sePartGlobalCombMaximumMagnitude=5, ... (8 total)
- **PatternCurveAnchorSideConstants** [2]: sePatternCurveLeftSide=1, sePatternCurveRightSide=2
- **PatternTransformRotateTypeConstants** [2]: sePatternTransformRotateOnCurvePosition=0, sePatternTransformRotateOnFeaturePosition=1
- **PatternTransformTypeConstants** [4]: sePatternTransformLinear=0, sePatternTransformFullRotation=1, sePatternTransformProjectedRotation=2, sePatternTransformFullRotationFromSurface=3
- **PatternTypeConstants** [2]: seSmartPattern=0, seFastPattern=1
- **PhysicalPropertiesStatusConstants** [3]: sePhysicalPropertiesStatus_None=0, sePhysicalPropertiesStatus_Model=1, sePhysicalPropertiesStatus_User=2
- **PhysicalThreadClearanceTypeConstants** [2]: sePhysicalThreadClearanceTypePercentage=0, sePhysicalThreadClearanceTypeAbsolute=1
- **PhysicalThreadErrorCode** [8]: sePhysicalThreadNoError=0, sePhysicalThreadUnknownError=1, sePhysicalThreadProfileCreationError=2, sePhysicalThreadHelixCreationError=3, sePhysicalThreadBooleanOperationError=4, ... (8 total)
- **PointTypeConstants** [4]: igSpacePoint=0, igKeyPoint=1, igCylinderStartPoint=2, igCylinderEndPoint=3
- **Print3DFileType** [2]: e3DPrint_STL=1, e3DPrint_3MF=2
- **ProfileValidationType** [7]: igProfileClosed=1, igProfileSingle=4, igProfileNoSelfIntersect=8, igProfileRefAxisRequired=16, igProfileNoRefAxisIntersect=32, ... (7 total)
- **PropertyFilterTypeConstants** [7]: sePropertyFilterTypeFace=1, sePropertyFilterTypeFaceChain=2, sePropertyFilterTypeFeatureEdges=3, sePropertyFilterTypeFeatureFaces=4, sePropertyFilterTypeEdge=5, ... (7 total)
- **PropertyTableConstants** [3]: seCustomPropertyQueryAllProperties=1, seCustomPropertyQueryByTable=2, seCustomPropertyQueryByNameAndValue=3
- **PropertyTypeConstants** [3]: sePropertyTypeDouble=1, sePropertyTypeString=2, sePropertyTypeInteger=3
- **RayIntersectionEntityConstants** [3]: seFace=1, seEdge=2, seVertex=3
- **RedefineFaceTangencyType** [4]: igRedefineFaceNormalToPlane=20, igRedefineFaceTangentContinuous=50, igRedefineFaceNatural=113, igRedefineFaceCurvatureContinuous=171
- **ReferenceElementConstants** [29]: igRefEleInit=0, igReverseNormalSide=1, igNormalSide=2, igPivotStart=3, igPivotEnd=4, ... (29 total)
- **ReferencePointCloudDensity** [4]: seMaximumDensity=1, seMediumDensity=2, seLowDensity=3, seMinimumDensity=4
- **ReferencePointTypeEnumForFromPointOption** [2]: sePatternReferenceTypeFromCoOrdinateSystem=0, sePatternReferenceTypeFromKeyPoint=1
- **ReferencePointTypeEnumForToPointOption** [2]: sePatternReferenceTypeToKeyPoint=0, sePatternReferenceTypeToExcelFirstRow=1
- **ReflectivePlaneConstants** [9]: igReflectivePlane=1, igTopPlane=2, igRightPlane=3, igFrontPlane=4, igTopPlaneDistance=5, ... (9 total)
- **RoundTypeConstants** [2]: igConstantRadius=1, igVariableRadius=2
- **RuledSurfaceDirectionConstants** [2]: igRuledSurfaceleft=1, igRuledSurfacRight=2
- **RuledSurfaceSideConstants** [2]: igRuledSurfaceInside=1, igRuledSurfaceOutside=2
- **RuledSurfaceTypeConstants** [5]: igRuledTangentContinuous=1, igRuledNormalToPlane=2, igRuledNatural=3, igRuledTaperedToPlane=4, igRuledAlongAnAxis=5
- **SEFamilyOfPartsOptionConstants** [7]: SEFamilyOfPartsOptionFlatPattern=1, SEFamilyOfPartsOptionSimplify=2, SEFamilyOfPartsOptionCoordinateSystems=4, SEFamilyOfPartsOptionReferencePlanes=8, SEFamilyOfPartsOptionSketches=16, ... (7 total)
- **SEFixedLengthConstraintDirection** [6]: igConstraintDirectionNone=0, igConstraintDirectionNoAxis=1, igConstraintDirectionXAxis=2, igConstraintDirectionYAxis=3, igConstraintDirectionZAxis=4, ... (6 total)
- **SEPatternRecognitionLevel** [3]: igFeaturesPattern=0, igLevelTwoPattern=1, igLevelThreePattern=2
- **SESubtractDirection** [3]: igSubtractDirectionNone=0, igSubtractDirectionRight=1, igSubtractDirectionLeft=2
- **SETargetConstructionBodyOption** [2]: igCreateMultipleConstructionBodiesOnNonManifoldOption=0, igCreateSingleConstructionGeneralBodyOnNonManifoldOption=1
- **SETargetDesignBodyOption** [3]: igCreateMultipleDesignBodiesOnNonManifoldOption=0, igFailOnNonManifoldOption=1, igCreateSingleDesignBodyOnNonManifoldOption=2
- **SaveAsFlatFileTypes** [3]: igAutoCAD=0, igPart_Document=1, igSheet_Metal_Document=2
- **SectionSketchesErrorCode** [4]: seSectionSketchesUnknownError=-1, seSectionSketchesNoError=0, seSectionSketchesNotPlaneIntersecting=1, seSectionSketchesSomePlaneIntersecting=2
- **SectionSketchesPlanesDirection** [3]: seSectionSketchesPlaneReverseNormalSide=-1, seSectionSketchesPlaneNormalSide=0, seSectionSketchesPlaneBothSide=1
- **SeedOptionConstants** [2]: igSeedSingle=1, igSeedAll=2
- **SheetMetalGlobalConstants** [26]: seSheetMetalGlobalDensity=1, seSheetMetalGlobalAccuracyForDensity=2, seSheetMetalGlobalMaterial=3, seSheetMetalGlobalMaterialThickness=4, seSheetMetalGlobalBendRadius=5, ... (26 total)
- **Sketch3DCurveEndConditionConstants** [3]: seSketch3DCurveEndConditionNatural=1, seSketch3DCurveEndConditionNormalToFace=2, seSketch3DCurveEndConditionCurvatureContinuous=3
- **Sketch3DKeypointType** [9]: igSketch3DUnknown=0, igSketch3DStartPoint=1, igSketch3DEndPoint=2, igSketch3DMidPoint=4, igSketch3DCenter=5, ... (9 total)
- **Sketch3DRelationTypeConstants** [16]: igSketch3DConnect=0, igSketch3DParallel=1, igSketch3DPerpendicular=2, igSketch3DPointOn=3, igSketch3DInclude=4, ... (16 total)
- **SolveTypeConstants** [2]: igSimple=1, igAdvanced=2
- **SpiralCurveMethodType** [3]: igSpiralCurveMethodEndDiameterAndTurns=0, igSpiralCurveMethodEndDiameterAndRadialPitch=1, igSpiralCurveMethodRadialPitchAndTurns=2
- **StitchWeldAnnotationFormat** [3]: seLengthPitch=1, seNXL=2, seNXL_E=3
- **StitchWeldType** [3]: seStitchOnly=1, seStitchPlusOffsets=2, seOffsetsOnly=3
- **StudyStatusType_Auto** [11]: eNoneStatus_Auto=0, eStudyGeomInError_Auto=1, eStudyMeshInError_Auto=2, eStudyResultsInError_Auto=3, eStudyReadyForMesh_Auto=4, ... (11 total)
- **SubdivisionDragTypeConstants** [2]: igLinearMoveType=1, igRotateType=2
- **SuppressRegionsConstants** [2]: seSuppressRegionInside=4, seSuppressRegionOutside=5
- **SurfaceByBoundaryConstants** [2]: igSurfaceByBoundaryPreferPlanar=1, igSurfaceByBoundaryTangent=2
- **SurfaceByBoundaryFillPreference** [4]: igSurfaceByBoundaryFillSmooth=1, igSurfaceByBoundaryFillNonSmooth=2, igSurfaceByBoundaryFillPreferPlane=3, igSurfaceByBoundaryFillPlaneOnly=4
- **SurfaceByBoundaryInternalSmoothness** [2]: igSurfaceByBoundarySharp=1, igSurfaceByBoundarySmooth=2
- **SurfaceByBoundaryPatchTopology** [3]: igSurfaceByBoundaryMinimal=1, igSurfaceByBoundarySingle=2, igSurfaceByBoundaryMultiple=3
- **SurfaceByBoundaryTangencyType** [3]: igSurfaceByBoundaryTangential=50, igSurfaceByBoundaryNatural=113, igSurfaceByBoundaryCurvatureContinuous=171
- **TabAndSlotExtentTypeConstants** [3]: TabAndSlotExtentTypeFinite=13, TabAndSlotExtentTypeFromTo=15, TabAndSlotExtentTypeToKeyPoint=72
- **TabAndSlotGapTypeConstants** [2]: SlotGapTypeSingle=0, SlotGapTypeMultiple=1
- **TabAndSlotPatternOffsetTypeConstants** [2]: TabAndSlotPatternOffsetTypeFit=0, TabAndSlotPatternOffsetTypeFill=1
- **TabAndSlotTreatmentTypeConstants** [3]: TabAndSlotTreatmentTypeNone=0, TabAndSlotTreatmentTypeRound=1, TabAndSlotTreatmentTypeChamfer=2
- **ThreadDiameterOptionConstants** [4]: seTapDrillDiameter=0, seInternalMinorDiameter=1, seNominalDiameter=2, seInsidePipeDiameter=3
- **TreatmentCrownCurvatureSideConstants** [3]: seTreatmentCrownCurvatureInside=4, seTreatmentCrownCurvatureOutside=5, seTreatmentCrownCurvatureNone=44
- **TreatmentCrownSideConstants** [3]: seTreatmentCrownSideInside=4, seTreatmentCrownSideOutside=5, seTreatmentCrownSideNone=44
- **TreatmentCrownTypeConstants** [5]: seTreatmentCrownNone=0, seTreatmentCrownByRadius=1, seTreatmentCrownByRadiusAndTakeOffAngle=2, seTreatmentCrownByOffset=3, seTreatmentCrownByOffsetAndTakeOffAngle=4
- **TreatmentTypeConstants** [3]: seTreatmentNone=44, seTreatmentDraft=173, seTreatmentCrown=174
- **TrimExtendErrorCode** [6]: TrimExtendErrorCodeUnknownError=-1, TrimExtendErrorCodeNoError=0, TrimExtendErrorCodeMissingParameter=1, TrimExtendErrorCodeInvalidParameter=2, TrimExtendErrorCodeNoReferencePlane=3, ... (6 total)
- **TrimSurfaceAreaSideConstants** [2]: igTSLeft=1, igTSRight=2
- **UnitOfMeasureAngleReadoutConstants** [10]: seAngleRadian=0, seAngleDegree=1, seAngleMinute=2, seAngleSecond=3, seAngleGradient=4, ... (10 total)
- **UnitOfMeasureLengthReadoutConstants** [20]: seLengthInch=0, seLengthFoot=1, seLengthInchAbbr=2, seLengthFootAbbr=3, seLengthFootInch=4, ... (20 total)
- **VentDraftSideConstants** [2]: seVentDraftSideInward=4, seVentDraftSideOutward=5
- **VentExtentSideConstants** [2]: seVentReverseSketchPlaneNormalSide=1, seVentSketchPlaneNormalSide=2
- **VentExtentTypeConstants** [4]: seVentExtentTypeFinite=13, seVentExtentTypeThroughNext=14, seVentExtentTypeThroughAll=16, seVentExtentToKeyPoint=72
- **WebNetworkFeatureConstants** [6]: seWebNormal=1, seWebReverseNormal=2, seWebExtendToNext=3, seWebExtendFinite=4, seWebProfileExtend=5, ... (6 total)
- **WeldmentGlobalConstants** [7]: seWeldmentGlobalDensity=1, seWeldmentGlobalAccuracyForDensity=2, seWeldmentGlobalBeadsDensity=3, seWeldmentGlobalMaterial=4, seWeldmentGlobalBeadMaterial=5, ... (7 total)
- **WeldmentLinkStatusConstants** [3]: seLinkOK=1, seLinkOutOfDate=2, seLinkBroken=3
- **WeldmentSectionTypeConstants** [4]: seWeldmentSectionTypeComponent=0, seWeldmentSectionTypeSurfacePrep=1, seWeldmentSectionTypeBead=2, seWeldmentSectionTypeMachining=3
- **seCopytoPMIConstants** [3]: seCopytoPMIConstantsDimension=1, seCopytoPMIConstantsAnnotation=2, seCopytoPMIConstantsAll=3

### Interfaces (915)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| AdjustableDefinition | dispatch | 4 | 5 |
| Arc3D | dispatch | 3 | 5 |
| Arcs3D | dispatch | 4 | 3 |
| AsmGussetPlate | dispatch | 1 | 10 |
| AsmGussetPlateCollection | dispatch | 1 | 4 |
| AsmTrimExtend | dispatch | 2 | 5 |
| AsmTrimExtendCollection | dispatch | 2 | 3 |
| AssemblyTrimTubeFeature | dispatch | 10 | 14 |
| AssemblyTrimTubeFeatures | dispatch | 2 | 3 |
| AssemblyWeldment | dispatch | 8 | 7 |
| AssemblyWeldments | dispatch | 1 | 3 |
| AttachedProperties | dispatch | 1 | 3 |
| AttachedProperty | dispatch | 1 | 5 |
| AttachedPropertyTable | dispatch | 5 | 10 |
| AttachedPropertyTables | dispatch | 2 | 3 |
| AutoSimplifyFeature | dispatch | 2 | 0 |
| AutoSimplifyFeatures | dispatch | 3 | 3 |
| BSplineCurve3D | dispatch | 7 | 7 |
| BSplineCurves3D | dispatch | 3 | 3 |
| BSplineSurfaces | dispatch | 2 | 3 |
| Bead | dispatch | 10 | 31 |
| Beads | dispatch | 2 | 3 |
| Bend | dispatch | 12 | 39 |
| BendBulgeReliefFeature | dispatch | 11 | 21 |
| BendBulgeReliefFeatures | dispatch | 2 | 3 |
| BendTable | dispatch | 12 | 10 |
| Bends | dispatch | 3 | 3 |
| Blank | dispatch | 14 | 23 |
| BlankSurface | dispatch | 12 | 21 |
| BlankSurfaces | dispatch | 2 | 3 |
| Blanks | dispatch | 2 | 3 |
| Blend | dispatch | 5 | 14 |
| Blends | dispatch | 4 | 3 |
| BlueSurf | dispatch | 21 | 24 |
| BlueSurfs | dispatch | 2 | 3 |
| BodyFeature | dispatch | 10 | 17 |
| BooleanFeature | dispatch | 10 | 18 |
| BooleanFeatures | dispatch | 2 | 3 |
| BoxFeature | dispatch | 2 | 7 |
| BoxFeatures | dispatch | 7 | 3 |
| BreakCorner | dispatch | 9 | 18 |
| BreakCorners | dispatch | 2 | 3 |
| Chamfer | dispatch | 10 | 23 |
| Chamfers | dispatch | 5 | 3 |
| ChangeBendAngle | dispatch | 8 | 21 |
| ChangeBendAngles | dispatch | 2 | 3 |
| CloseCorner | dispatch | 9 | 26 |
| CloseCorners | dispatch | 2 | 3 |
| ComponentSketch | dispatch | 1 | 9 |
| ComponentSketches | dispatch | 2 | 3 |
| ConnectorOwner | dispatch | 14 | 0 |
| Constraint | dispatch | 5 | 7 |
| ConstraintOwner | dispatch | 3 | 1 |
| Constraints | dispatch | 6 | 3 |
| ConstructionModel | dispatch | 21 | 39 |
| Constructions | dispatch | 1 | 38 |
| ContourCurve | dispatch | 9 | 19 |
| ContourCurves | dispatch | 2 | 3 |
| ContourFlange | dispatch | 17 | 47 |
| ContourFlanges | dispatch | 8 | 3 |
| ConvToSM | dispatch | 11 | 27 |
| ConvToSMs | dispatch | 4 | 3 |
| ConvertPartToSM | dispatch | 20 | 43 |
| ConvertPartToSMCollection | dispatch | 3 | 3 |
| ConvertToMesh | dispatch | 4 | 10 |
| ConvertToMeshes | dispatch | 2 | 3 |
| CoordinateSystem | dispatch | 8 | 19 |
| CoordinateSystems | dispatch | 5 | 4 |
| CopiedPart | dispatch | 12 | 29 |
| CopiedParts | dispatch | 1 | 3 |
| CopyConstruction | dispatch | 17 | 39 |
| CopyConstructions | dispatch | 8 | 3 |
| CopySurface | dispatch | 10 | 20 |
| CopySurfaces | dispatch | 2 | 3 |
| CrossBrake | dispatch | 5 | 15 |
| CrossBrakes | dispatch | 2 | 3 |
| CrossCurve | dispatch | 8 | 19 |
| CrossCurves | dispatch | 2 | 3 |
| CurveByTable | dispatch | 9 | 24 |
| CurvesByTables | dispatch | 2 | 3 |
| CylinderFeature | dispatch | 2 | 7 |
| CylinderFeatures | dispatch | 3 | 3 |
| Decal | dispatch | 6 | 16 |
| Decals | dispatch | 3 | 4 |
| DelSMFace | dispatch | 8 | 18 |
| DelSMFaces | dispatch | 2 | 3 |
| DeleteBlend | dispatch | 9 | 17 |
| DeleteBlends | dispatch | 2 | 3 |
| DeleteFace | dispatch | 11 | 18 |
| DeleteFaces | dispatch | 4 | 3 |
| DeleteHole | dispatch | 9 | 17 |
| DeleteHoles | dispatch | 3 | 3 |
| DeleteRegion | dispatch | 9 | 17 |
| DeleteRegions | dispatch | 2 | 3 |
| DerivedCurve | dispatch | 10 | 20 |
| DerivedCurves | dispatch | 2 | 3 |
| Dimple | dispatch | 10 | 31 |
| Dimples | dispatch | 3 | 3 |
| DividedPart | dispatch | 3 | 10 |
| DividedParts | dispatch | 3 | 3 |
| Draft | dispatch | 12 | 20 |
| Drafts | dispatch | 2 | 3 |
| DrawnCutout | dispatch | 10 | 29 |
| DrawnCutouts | dispatch | 3 | 3 |
| Duplicate | dispatch | 0 | 2 |
| Duplicates | dispatch | 2 | 3 |
| EdgebarFeatures | dispatch | 1 | 3 |
| Ellipse3D | dispatch | 4 | 5 |
| Ellipses3D | dispatch | 3 | 3 |
| EmbossFeature | dispatch | 9 | 26 |
| EmbossFeatures | dispatch | 2 | 3 |
| Enclosure | dispatch | 5 | 10 |
| Enclosures | dispatch | 1 | 3 |
| Etch | dispatch | 11 | 20 |
| Etches | dispatch | 4 | 3 |
| ExtendSurface | dispatch | 8 | 21 |
| ExtendSurfaces | dispatch | 5 | 3 |
| ExtrudedCutout | dispatch | 25 | 30 |
| ExtrudedCutouts | dispatch | 17 | 3 |
| ExtrudedProtrusion | dispatch | 24 | 31 |
| ExtrudedProtrusions | dispatch | 13 | 3 |
| ExtrudedSurface | dispatch | 23 | 21 |
| ExtrudedSurfaces | dispatch | 6 | 3 |
| FEAConnector | dispatch | 40 | 1 |
| FEAConstraint | dispatch | 9 | 2 |
| FaceMove | dispatch | 11 | 33 |
| FaceMoves | dispatch | 3 | 3 |
| FaceOffset | dispatch | 10 | 26 |
| FaceOffsets | dispatch | 3 | 3 |
| FaceRotate | dispatch | 11 | 27 |
| FaceRotates | dispatch | 3 | 3 |
| FaceSet | dispatch | 6 | 15 |
| FamilyMember | dispatch | 17 | 25 |
| FamilyMembers | dispatch | 6 | 6 |
| FeatureGroup | dispatch | 11 | 18 |
| FeatureGroups | dispatch | 3 | 3 |
| Features | dispatch | 1 | 3 |
| FilletWeld | dispatch | 6 | 19 |
| FilletWelds | dispatch | 2 | 3 |
| Flange | dispatch | 14 | 36 |
| Flanges | dispatch | 9 | 3 |
| FlatPattern | dispatch | 10 | 19 |
| FlatPatternModel | dispatch | 12 | 31 |
| FlatPatternModels | dispatch | 3 | 3 |
| FlatPatterns | dispatch | 3 | 3 |
| Function | dispatch | 3 | 1 |
| FunctionOwner | dispatch | 2 | 1 |
| GenerativeConstraint | dispatch | 20 | 12 |
| GenerativeConstraints | dispatch | 2 | 3 |
| GenerativeGlobalGravityLoad | dispatch | 3 | 6 |
| GenerativeGlobalPlanarSymmetry | dispatch | 3 | 3 |
| GenerativeLoad | dispatch | 14 | 12 |
| GenerativeLoadCase | dispatch | 10 | 7 |
| GenerativeLoadCases | dispatch | 7 | 3 |
| GenerativeLoads | dispatch | 2 | 3 |
| GenerativePreserveRegion | dispatch | 4 | 9 |
| GenerativePreserveRegions | dispatch | 2 | 3 |
| GenerativeStudies | dispatch | 2 | 4 |
| GenerativeStudy | dispatch | 6 | 21 |
| GrooveWeld | dispatch | 6 | 22 |
| GrooveWelds | dispatch | 2 | 3 |
| Gusset | dispatch | 6 | 31 |
| Gussets | dispatch | 3 | 3 |
| HelicalCurve | dispatch | 15 | 18 |
| HelicalCurves | dispatch | 4 | 3 |
| HelixCutout | dispatch | 10 | 19 |
| HelixCutouts | dispatch | 5 | 3 |
| HelixProtrusion | dispatch | 12 | 19 |
| HelixProtrusions | dispatch | 9 | 3 |
| Hem | dispatch | 10 | 27 |
| Hems | dispatch | 3 | 3 |
| Hole | dispatch | 15 | 30 |
| Hole2d | dispatch | 12 | 11 |
| HoleData | dispatch | 10 | 103 |
| HoleDataCollection | dispatch | 4 | 3 |
| HoleGeometries | dispatch | 1 | 3 |
| HoleGeometry | dispatch | 0 | 4 |
| Holes | dispatch | 14 | 3 |
| Holes2d | dispatch | 2 | 3 |
| InterpartConstruction | dispatch | 12 | 21 |
| InterpartConstructions | dispatch | 3 | 3 |
| Intersect | dispatch | 12 | 20 |
| IntersectSurface | dispatch | 15 | 18 |
| IntersectSurfaces | dispatch | 4 | 3 |
| IntersectionCurve | dispatch | 8 | 19 |
| IntersectionCurves | dispatch | 2 | 3 |
| IntersectionPoint | dispatch | 7 | 18 |
| IntersectionPoints | dispatch | 2 | 3 |
| Intersects | dispatch | 2 | 3 |
| IsoclineCurve | dispatch | 11 | 21 |
| IsoclineCurves | dispatch | 2 | 3 |
| Iteration | dispatch | 7 | 0 |
| IterationOwner | dispatch | 4 | 0 |
| Jog | dispatch | 12 | 39 |
| Jogs | dispatch | 5 | 3 |
| KeyPointCurve | dispatch | 13 | 25 |
| KeyPointCurves | dispatch | 4 | 3 |
| LabelWeld | dispatch | 10 | 17 |
| LabelWeldData | dispatch | 0 | 37 |
| LabelWeldDataCollection | dispatch | 2 | 3 |
| LabelWelds | dispatch | 2 | 3 |
| Line3D | dispatch | 2 | 5 |
| Lines3D | dispatch | 4 | 3 |
| Lip | dispatch | 8 | 22 |
| Lips | dispatch | 2 | 3 |
| LiveSection | dispatch | 3 | 11 |
| LiveSections | dispatch | 2 | 3 |
| Load | dispatch | 22 | 2 |
| LoadOwner | dispatch | 13 | 1 |
| LoftedCutout | dispatch | 10 | 19 |
| LoftedCutouts | dispatch | 3 | 3 |
| LoftedFlange | dispatch | 17 | 35 |
| LoftedFlanges | dispatch | 4 | 3 |
| LoftedProtrusion | dispatch | 12 | 19 |
| LoftedProtrusions | dispatch | 4 | 3 |
| LoftedSurface | dispatch | 12 | 21 |
| LoftedSurfaces | dispatch | 3 | 3 |
| Louver | dispatch | 12 | 28 |
| Louvers | dispatch | 3 | 3 |
| MatchFlangeFace | dispatch | 6 | 21 |
| MatchFlangeFaces | dispatch | 2 | 3 |
| MeasureVariable | dispatch | 6 | 17 |
| MeshControl | dispatch | 6 | 1 |
| MeshOwner | dispatch | 14 | 4 |
| MidSurface | dispatch | 9 | 21 |
| MidSurfaces | dispatch | 3 | 3 |
| MirrorCopies | dispatch | 4 | 3 |
| MirrorCopy | dispatch | 11 | 21 |
| MirrorCopyGeometries | dispatch | 3 | 3 |
| MirrorCopyGeometry | dispatch | 9 | 20 |
| MirrorPart | dispatch | 11 | 19 |
| MirrorParts | dispatch | 3 | 3 |
| Mode | dispatch | 4 | 0 |
| Model | dispatch | 33 | 130 |
| Models | dispatch | 51 | 5 |
| ModesOwner | dispatch | 4 | 0 |
| MountingBoss | dispatch | 12 | 38 |
| MountingBoss2d | dispatch | 12 | 11 |
| MountingBoss2dCollection | dispatch | 2 | 3 |
| MountingBossCollection | dispatch | 2 | 3 |
| MultiEdgeFlange | dispatch | 25 | 34 |
| MultiEdgeFlanges | dispatch | 3 | 3 |
| NormalCutout | dispatch | 10 | 31 |
| NormalCutouts | dispatch | 6 | 3 |
| NormalToFaceCutout | dispatch | 10 | 20 |
| NormalToFaceCutouts | dispatch | 2 | 3 |
| NormalToFaceProtrusion | dispatch | 10 | 20 |
| NormalToFaceProtrusions | dispatch | 2 | 3 |
| OffsetEdge | dispatch | 10 | 18 |
| OffsetEdges | dispatch | 2 | 3 |
| OffsetSurface | dispatch | 9 | 22 |
| OffsetSurfaces | dispatch | 2 | 3 |
| Optimization | dispatch | 18 | 0 |
| OptimizationOwner | dispatch | 2 | 0 |
| OverProp | dispatch | 7 | 0 |
| PartConfiguration | dispatch | 3 | 8 |
| PartConfigurations | dispatch | 6 | 3 |
| PartDocument | dispatch | 97 | 103 |
| PartFilletWeld | dispatch | 6 | 19 |
| PartFilletWelds | dispatch | 2 | 3 |
| PartGrooveWeld | dispatch | 6 | 22 |
| PartGrooveWelds | dispatch | 2 | 3 |
| PartLabelWeld | dispatch | 10 | 17 |
| PartLabelWelds | dispatch | 2 | 3 |
| PartStitchWeld | dispatch | 6 | 21 |
| PartStitchWelds | dispatch | 2 | 3 |
| PartingSplit | dispatch | 12 | 19 |
| PartingSplits | dispatch | 2 | 3 |
| PartingSurface | dispatch | 10 | 20 |
| PartingSurfaces | dispatch | 2 | 3 |
| Pattern | dispatch | 40 | 36 |
| PatternCopyGeometries | dispatch | 7 | 3 |
| PatternCopyGeometry | dispatch | 33 | 30 |
| PatternPart | dispatch | 30 | 27 |
| PatternParts | dispatch | 7 | 3 |
| Patterns | dispatch | 18 | 3 |
| Plot | dispatch | 15 | 0 |
| PlotsOwner | dispatch | 4 | 0 |
| Point3D | dispatch | 1 | 3 |
| Points3D | dispatch | 7 | 4 |
| Profile | dispatch | 26 | 49 |
| ProfileSet | dispatch | 2 | 10 |
| ProfileSets | dispatch | 4 | 3 |
| Profiles | dispatch | 2 | 5 |
| ProjectCurve | dispatch | 9 | 19 |
| ProjectCurves | dispatch | 4 | 3 |
| PropOwner | dispatch | 3 | 0 |
| PropertyDefinition | dispatch | 1 | 5 |
| PropertyDefinitions | dispatch | 2 | 3 |
| PropertyTableDefinition | dispatch | 2 | 7 |
| PropertyTableDefinitions | dispatch | 3 | 3 |
| Rebend | dispatch | 9 | 17 |
| Rebends | dispatch | 2 | 3 |
| RecoveredBodies | dispatch | 2 | 3 |
| RecoveredBody | dispatch | 10 | 18 |
| RedefineFace | dispatch | 11 | 19 |
| RedefineFaces | dispatch | 2 | 3 |
| RefAxes | dispatch | 1 | 3 |
| RefAxis | dispatch | 7 | 12 |
| RefPlane | dispatch | 10 | 18 |
| RefPlanes | dispatch | 14 | 4 |
| ReferencePointCloud | dispatch | 2 | 13 |
| ReferencePointClouds | dispatch | 3 | 4 |
| Release | dispatch | 0 | 0 |
| ReleaseOwner | dispatch | 0 | 0 |
| ReliefPatchFeature | dispatch | 11 | 17 |
| ReliefPatchFeatures | dispatch | 3 | 3 |
| ReplaceFace | dispatch | 9 | 19 |
| ReplaceFaces | dispatch | 2 | 3 |
| ResizeBend | dispatch | 10 | 19 |
| ResizeBends | dispatch | 2 | 3 |
| ResizeHole | dispatch | 9 | 21 |
| ResizeHoles | dispatch | 2 | 3 |
| ResizeRound | dispatch | 10 | 19 |
| ResizeRounds | dispatch | 2 | 3 |
| ResultsOwner | dispatch | 6 | 0 |
| RevolvedCutout | dispatch | 17 | 29 |
| RevolvedCutouts | dispatch | 17 | 3 |
| RevolvedProtrusion | dispatch | 17 | 30 |
| RevolvedProtrusions | dispatch | 12 | 3 |
| RevolvedSurface | dispatch | 15 | 21 |
| RevolvedSurfaces | dispatch | 7 | 3 |
| Rib | dispatch | 10 | 24 |
| Ribs | dispatch | 2 | 3 |
| RipEdge | dispatch | 10 | 17 |
| RipEdges | dispatch | 2 | 3 |
| Round | dispatch | 13 | 23 |
| Rounds | dispatch | 5 | 3 |
| RuledSurface | dispatch | 12 | 24 |
| RuledSurfaces | dispatch | 2 | 3 |
| ScaleBodyFeature | dispatch | 10 | 19 |
| ScaleBodyFeatures | dispatch | 2 | 3 |
| SheetMetalDocument | dispatch | 94 | 100 |
| SimplifiedAssemblyModel | dispatch | 23 | 22 |
| SimplifiedModel | dispatch | 8 | 23 |
| SimplifiedModels | dispatch | 2 | 3 |
| Sketch | dispatch | 8 | 23 |
| Sketch3D | dispatch | 11 | 23 |
| Sketch3DFeature | dispatch | 7 | 18 |
| Sketch3DFeatures | dispatch | 2 | 3 |
| Sketch3DRelation | dispatch | 3 | 4 |
| Sketch3DRelations | dispatch | 19 | 3 |
| SketchBlock | dispatch | 1 | 9 |
| SketchBlockLabel | dispatch | 16 | 18 |
| SketchBlockLabelOccurrence | dispatch | 2 | 15 |
| SketchBlockLabelOccurrences | dispatch | 1 | 3 |
| SketchBlockLabels | dispatch | 2 | 3 |
| SketchBlockOccurrence | dispatch | 19 | 17 |
| SketchBlockOccurrences | dispatch | 2 | 3 |
| SketchBlockView | dispatch | 5 | 38 |
| SketchBlockViews | dispatch | 2 | 4 |
| SketchBlocks | dispatch | 5 | 3 |
| SketchDrawingViews | dispatch | 0 | 0 |
| Sketches3D | dispatch | 2 | 3 |
| Sketchs | dispatch | 8 | 4 |
| Slot | dispatch | 23 | 23 |
| SlotGroup | dispatch | 6 | 9 |
| SlotGroups | dispatch | 1 | 3 |
| Slots | dispatch | 6 | 3 |
| SolidSweptCutout | dispatch | 7 | 17 |
| SolidSweptCutouts | dispatch | 2 | 3 |
| SolidSweptProtrusion | dispatch | 7 | 17 |
| SolidSweptProtrusions | dispatch | 2 | 3 |
| SphereFeature | dispatch | 2 | 7 |
| SphereFeatures | dispatch | 3 | 3 |
| Split | dispatch | 12 | 20 |
| SplitCurve | dispatch | 8 | 19 |
| SplitCurves | dispatch | 3 | 3 |
| SplitFace | dispatch | 11 | 18 |
| SplitFaces | dispatch | 4 | 3 |
| Splits | dispatch | 2 | 3 |
| StitchSurface | dispatch | 11 | 20 |
| StitchSurfaces | dispatch | 3 | 3 |
| StitchWeld | dispatch | 6 | 21 |
| StitchWelds | dispatch | 2 | 3 |
| Study | dispatch | 62 | 0 |
| StudyOwner | dispatch | 12 | 4 |
| SubdivisionFeature | dispatch | 23 | 18 |
| SubdivisionFeatures | dispatch | 5 | 3 |
| Subtract | dispatch | 14 | 20 |
| Subtracts | dispatch | 4 | 3 |
| SuppressVariable | dispatch | 6 | 17 |
| SurfaceByBoundaries | dispatch | 4 | 3 |
| SurfaceByBoundary | dispatch | 22 | 18 |
| SweptCutout | dispatch | 14 | 24 |
| SweptCutouts | dispatch | 3 | 3 |
| SweptProtrusion | dispatch | 14 | 24 |
| SweptProtrusions | dispatch | 3 | 3 |
| SweptSurface | dispatch | 14 | 25 |
| SweptSurfaces | dispatch | 3 | 3 |
| Tab | dispatch | 10 | 20 |
| TabAndSlotFeature | dispatch | 12 | 32 |
| TabAndSlotFeatures | dispatch | 2 | 3 |
| Tabs | dispatch | 2 | 3 |
| Terminal | dispatch | 2 | 6 |
| Terminals | dispatch | 2 | 3 |
| Thicken | dispatch | 9 | 18 |
| Thickens | dispatch | 3 | 3 |
| Thin | dispatch | 9 | 18 |
| ThinWall | dispatch | 11 | 20 |
| Thins | dispatch | 1 | 3 |
| Thinwalls | dispatch | 2 | 3 |
| Thread | dispatch | 10 | 20 |
| Threads | dispatch | 3 | 3 |
| ToggleToConstruction | dispatch | 4 | 10 |
| ToggleToConstructions | dispatch | 2 | 3 |
| ToggleToDesign | dispatch | 4 | 10 |
| ToggleToDesigns | dispatch | 2 | 3 |
| TrimSurface | dispatch | 11 | 17 |
| TrimSurfaces | dispatch | 3 | 3 |
| TubeFeature | dispatch | 6 | 16 |
| TubeFeatures | dispatch | 1 | 3 |
| Unbend | dispatch | 9 | 17 |
| Unbends | dispatch | 2 | 3 |
| Union | dispatch | 12 | 20 |
| Unions | dispatch | 2 | 3 |
| UnitedBodies | dispatch | 2 | 3 |
| UnitedBody | dispatch | 10 | 18 |
| UsedSketch | dispatch | 2 | 6 |
| UsedSketches | dispatch | 1 | 3 |
| UserDefinedPattern | dispatch | 10 | 22 |
| UserDefinedPatterns | dispatch | 2 | 3 |
| UserDefinedSet | dispatch | 3 | 7 |
| UserDefinedSets | dispatch | 2 | 3 |
| Vent | dispatch | 14 | 35 |
| Vents | dispatch | 5 | 3 |
| WebNetwork | dispatch | 12 | 24 |
| WebNetworks | dispatch | 3 | 3 |
| WeldBeadByExtrudedProtrusion | dispatch | 8 | 23 |
| WeldBeadByExtrudedProtrusions | dispatch | 4 | 3 |
| WeldBeadByRevolvedProtrusion | dispatch | 8 | 22 |
| WeldBeadByRevolvedProtrusions | dispatch | 3 | 3 |
| WeldBeadBySweptProtrusion | dispatch | 6 | 15 |
| WeldBeadBySweptProtrusions | dispatch | 2 | 3 |
| WeldBeadModel | dispatch | 2 | 10 |
| WeldBeadModels | dispatch | 1 | 3 |
| WeldChamfer | dispatch | 8 | 19 |
| WeldChamfers | dispatch | 4 | 3 |
| WeldExtrudedCutout | dispatch | 8 | 24 |
| WeldExtrudedCutouts | dispatch | 9 | 3 |
| WeldHole | dispatch | 8 | 21 |
| WeldHoles | dispatch | 5 | 3 |
| WeldMirror | dispatch | 7 | 18 |
| WeldMirrors | dispatch | 2 | 3 |
| WeldPartModel | dispatch | 2 | 12 |
| WeldPartModels | dispatch | 1 | 3 |
| WeldPattern | dispatch | 18 | 23 |
| WeldPatterns | dispatch | 4 | 3 |
| WeldRevolvedCutout | dispatch | 8 | 23 |
| WeldRevolvedCutouts | dispatch | 5 | 3 |
| WeldRound | dispatch | 10 | 17 |
| WeldRounds | dispatch | 4 | 3 |
| WeldmentDocument | dispatch | 55 | 55 |
| WeldmentModel | dispatch | 6 | 31 |
| WeldmentModels | dispatch | 3 | 3 |
| WireFeature | dispatch | 7 | 16 |
| WireFeatures | dispatch | 1 | 3 |
| WrapSketch | dispatch | 11 | 18 |
| WrapSketchs | dispatch | 2 | 3 |
| _IAdjustableDefinitionAuto | interface | 4 | 5 |
| _IArc3DAuto | interface | 3 | 5 |
| _IArcs3DAuto | interface | 4 | 3 |
| _IAsmGussetPlateAuto | interface | 1 | 10 |
| _IAsmGussetPlateCollectionAuto | interface | 1 | 4 |
| _IAsmTrimExtendAuto | interface | 2 | 5 |
| _IAsmTrimExtendCollectionAuto | interface | 2 | 3 |
| _IAssemblyTrimTubeFeatureAuto | interface | 10 | 14 |
| _IAssemblyTrimTubeFeaturesAuto | interface | 2 | 3 |
| _IAssemblyWeldmentAuto | interface | 8 | 7 |
| _IAssemblyWeldmentsAuto | interface | 1 | 3 |
| _IAttachedPropertiesAuto | interface | 1 | 3 |
| _IAttachedPropertyAuto | interface | 1 | 5 |
| _IAttachedPropertyTableAuto | interface | 5 | 10 |
| _IAttachedPropertyTablesAuto | interface | 2 | 3 |
| _IAutoSimplifyFeatureAuto | interface | 2 | 0 |
| _IAutoSimplifyFeaturesAuto | interface | 3 | 3 |
| _IBSplineCurve3DAuto | interface | 7 | 7 |
| _IBSplineCurves3DAuto | interface | 3 | 3 |
| _IBSplineSurfacesAuto | interface | 2 | 3 |
| _IBeadAuto | interface | 10 | 31 |
| _IBeadsAuto | interface | 2 | 3 |
| _IBendAuto | interface | 12 | 39 |
| _IBendBulgeReliefFeatureAuto | interface | 11 | 21 |
| _IBendBulgeReliefFeaturesAuto | interface | 2 | 3 |
| _IBendTableAuto | interface | 12 | 10 |
| _IBendsAuto | interface | 3 | 3 |
| _IBlankAuto | interface | 14 | 23 |
| _IBlankSurfaceAuto | interface | 12 | 21 |
| _IBlankSurfacesAuto | interface | 2 | 3 |
| _IBlanksAuto | interface | 2 | 3 |
| _IBlendAuto | interface | 5 | 14 |
| _IBlendsAuto | interface | 4 | 3 |
| _IBlueSurfAuto | interface | 21 | 24 |
| _IBlueSurfsAuto | interface | 2 | 3 |
| _IBodyFeatureAuto | interface | 10 | 17 |
| _IBooleanFeatureAuto | interface | 10 | 18 |
| _IBooleanFeaturesAuto | interface | 2 | 3 |
| _IBoxFeatureAuto | interface | 2 | 7 |
| _IBoxFeaturesAuto | interface | 7 | 3 |
| _IBreakCornerAuto | interface | 9 | 18 |
| _IBreakCornersAuto | interface | 2 | 3 |
| _IChamferAuto | interface | 10 | 23 |
| _IChamfersAuto | interface | 5 | 3 |
| _IChangeBendAngleAuto | interface | 8 | 21 |
| _IChangeBendAnglesAuto | interface | 2 | 3 |
| _ICloseCornerAuto | interface | 9 | 26 |
| _ICloseCornersAuto | interface | 2 | 3 |
| _IComponentSketchAuto | interface | 1 | 9 |
| _IComponentSketchesAuto | interface | 2 | 3 |
| _IConnectorOwnerAuto | interface | 14 | 0 |
| _IConstraintAuto | interface | 5 | 7 |
| _IConstraintOwnerAuto | interface | 3 | 1 |
| _IConstraintsAuto | interface | 6 | 3 |
| _IConstructionModelAuto | interface | 21 | 39 |
| _IConstructionsAuto | interface | 1 | 38 |
| _IContourCurveAuto | interface | 9 | 19 |
| _IContourCurvesAuto | interface | 2 | 3 |
| _IContourFlangeAuto | interface | 17 | 47 |
| _IContourFlangesAuto | interface | 8 | 3 |
| _IConvToSMAuto | interface | 11 | 27 |
| _IConvToSMsAuto | interface | 4 | 3 |
| _IConvertPartToSMAuto | interface | 20 | 43 |
| _IConvertPartToSMCollectionAuto | interface | 3 | 3 |
| _IConvertToMeshAuto | interface | 4 | 10 |
| _IConvertToMeshesAuto | interface | 2 | 3 |
| _ICoordinateSystemAuto | interface | 8 | 19 |
| _ICoordinateSystemsAuto | interface | 5 | 4 |
| _ICopiedPartAuto | interface | 12 | 29 |
| _ICopiedPartsAuto | interface | 1 | 3 |
| _ICopyConstructionAuto | interface | 17 | 39 |
| _ICopyConstructionsAuto | interface | 8 | 3 |
| _ICopySurfaceAuto | interface | 10 | 20 |
| _ICopySurfacesAuto | interface | 2 | 3 |
| _ICrossBrakeAuto | interface | 5 | 15 |
| _ICrossBrakesAuto | interface | 2 | 3 |
| _ICrossCurveAuto | interface | 8 | 19 |
| _ICrossCurvesAuto | interface | 2 | 3 |
| _ICurveByTableAuto | interface | 9 | 24 |
| _ICurvesByTablesAuto | interface | 2 | 3 |
| _ICylinderFeatureAuto | interface | 2 | 7 |
| _ICylinderFeaturesAuto | interface | 3 | 3 |
| _IDecalAuto | interface | 6 | 16 |
| _IDecalsAuto | interface | 3 | 4 |
| _IDelSMFaceAuto | interface | 8 | 18 |
| _IDelSMFacesAuto | interface | 2 | 3 |
| _IDeleteBlendAuto | interface | 9 | 17 |
| _IDeleteBlendsAuto | interface | 2 | 3 |
| _IDeleteFaceAuto | interface | 11 | 18 |
| _IDeleteFacesAuto | interface | 4 | 3 |
| _IDeleteHoleAuto | interface | 9 | 17 |
| _IDeleteHolesAuto | interface | 3 | 3 |
| _IDeleteRegionAuto | interface | 9 | 17 |
| _IDeleteRegionsAuto | interface | 2 | 3 |
| _IDerivedCurveAuto | interface | 10 | 20 |
| _IDerivedCurvesAuto | interface | 2 | 3 |
| _IDimpleAuto | interface | 10 | 31 |
| _IDimplesAuto | interface | 3 | 3 |
| _IDividedPartAuto | interface | 3 | 10 |
| _IDividedPartsAuto | interface | 3 | 3 |
| _IDraftAuto | interface | 12 | 20 |
| _IDraftsAuto | interface | 2 | 3 |
| _IDrawnCutoutAuto | interface | 10 | 29 |
| _IDrawnCutoutsAuto | interface | 3 | 3 |
| _IDuplicateAuto | interface | 0 | 2 |
| _IDuplicatesAuto | interface | 2 | 3 |
| _IEdgebarFeaturesAuto | interface | 1 | 3 |
| _IEllipse3DAuto | interface | 4 | 5 |
| _IEllipses3DAuto | interface | 3 | 3 |
| _IEmbossFeatureAuto | interface | 9 | 26 |
| _IEmbossFeaturesAuto | interface | 2 | 3 |
| _IEnclosureAuto | interface | 5 | 10 |
| _IEnclosuresAuto | interface | 1 | 3 |
| _IEtchAuto | interface | 11 | 20 |
| _IEtchesAuto | interface | 4 | 3 |
| _IExtendSurfaceAuto | interface | 8 | 21 |
| _IExtendSurfacesAuto | interface | 5 | 3 |
| _IExtrudedCutoutAuto | interface | 25 | 30 |
| _IExtrudedCutoutsAuto | interface | 17 | 3 |
| _IExtrudedProtrusionAuto | interface | 24 | 31 |
| _IExtrudedProtrusionsAuto | interface | 13 | 3 |
| _IExtrudedSurfaceAuto | interface | 23 | 21 |
| _IExtrudedSurfacesAuto | interface | 6 | 3 |
| _IFEAConnectorAuto | interface | 40 | 1 |
| _IFEAConstraintAuto | interface | 9 | 2 |
| _IFaceMoveAuto | interface | 11 | 33 |
| _IFaceMovesAuto | interface | 3 | 3 |
| _IFaceOffsetAuto | interface | 10 | 26 |
| _IFaceOffsetsAuto | interface | 3 | 3 |
| _IFaceRotateAuto | interface | 11 | 27 |
| _IFaceRotatesAuto | interface | 3 | 3 |
| _IFaceSetAuto | interface | 6 | 15 |
| _IFamilyMemberAuto | interface | 17 | 25 |
| _IFamilyMembersAuto | interface | 6 | 6 |
| _IFeatureGroupAuto | interface | 11 | 18 |
| _IFeatureGroupsAuto | interface | 3 | 3 |
| _IFeaturesAuto | interface | 1 | 3 |
| _IFilletWeldAuto | interface | 6 | 19 |
| _IFilletWeldsAuto | interface | 2 | 3 |
| _IFlangeAuto | interface | 14 | 36 |
| _IFlangesAuto | interface | 9 | 3 |
| _IFlatPatternAuto | interface | 10 | 19 |
| _IFlatPatternModelAuto | interface | 12 | 31 |
| _IFlatPatternModelsAuto | interface | 3 | 3 |
| _IFlatPatternsAuto | interface | 3 | 3 |
| _IFunctionAuto | interface | 3 | 1 |
| _IFunctionOwnerAuto | interface | 2 | 1 |
| _IGenerativeConstraintAuto | interface | 20 | 12 |
| _IGenerativeConstraintsAuto | interface | 2 | 3 |
| _IGenerativeGlobalGravityLoadAuto | interface | 3 | 6 |
| _IGenerativeGlobalPlanarSymmetryAuto | interface | 3 | 3 |
| _IGenerativeLoadAuto | interface | 14 | 12 |
| _IGenerativeLoadCaseAuto | interface | 10 | 7 |
| _IGenerativeLoadCasesAuto | interface | 7 | 3 |
| _IGenerativeLoadsAuto | interface | 2 | 3 |
| _IGenerativePreserveRegionAuto | interface | 4 | 9 |
| _IGenerativePreserveRegionsAuto | interface | 2 | 3 |
| _IGenerativeStudiesAuto | interface | 2 | 4 |
| _IGenerativeStudyAuto | interface | 6 | 21 |
| _IGrooveWeldAuto | interface | 6 | 22 |
| _IGrooveWeldsAuto | interface | 2 | 3 |
| _IGussetAuto | interface | 6 | 31 |
| _IGussetsAuto | interface | 3 | 3 |
| _IHelicalCurveAuto | interface | 15 | 18 |
| _IHelicalCurvesAuto | interface | 4 | 3 |
| _IHelixCutoutAuto | interface | 10 | 19 |
| _IHelixCutoutsAuto | interface | 5 | 3 |
| _IHelixProtrusionAuto | interface | 12 | 19 |
| _IHelixProtrusionsAuto | interface | 9 | 3 |
| _IHemAuto | interface | 10 | 27 |
| _IHemsAuto | interface | 3 | 3 |
| _IHole2dAuto | interface | 12 | 11 |
| _IHoleAuto | interface | 15 | 30 |
| _IHoleDataAuto | interface | 10 | 103 |
| _IHoleDataCollectionAuto | interface | 4 | 3 |
| _IHoleGeometriesAuto | interface | 1 | 3 |
| _IHoleGeometryAuto | interface | 0 | 4 |
| _IHoles2dAuto | interface | 2 | 3 |
| _IHolesAuto | interface | 14 | 3 |
| _IInterpartConstructionAuto | interface | 12 | 21 |
| _IInterpartConstructionsAuto | interface | 3 | 3 |
| _IIntersectAuto | interface | 12 | 20 |
| _IIntersectSurfaceAuto | interface | 15 | 18 |
| _IIntersectSurfacesAuto | interface | 4 | 3 |
| _IIntersectionCurveAuto | interface | 8 | 19 |
| _IIntersectionCurvesAuto | interface | 2 | 3 |
| _IIntersectionPointAuto | interface | 7 | 18 |
| _IIntersectionPointsAuto | interface | 2 | 3 |
| _IIntersectsAuto | interface | 2 | 3 |
| _IIsoclineCurveAuto | interface | 11 | 21 |
| _IIsoclineCurvesAuto | interface | 2 | 3 |
| _IIterationAuto | interface | 7 | 0 |
| _IIterationOwnerAuto | interface | 4 | 0 |
| _IJogAuto | interface | 12 | 39 |
| _IJogsAuto | interface | 5 | 3 |
| _IKeyPointCurveAuto | interface | 13 | 25 |
| _IKeyPointCurvesAuto | interface | 4 | 3 |
| _ILabelWeldAuto | interface | 10 | 17 |
| _ILabelWeldDataAuto | interface | 0 | 37 |
| _ILabelWeldDataCollectionAuto | interface | 2 | 3 |
| _ILabelWeldsAuto | interface | 2 | 3 |
| _ILine3DAuto | interface | 2 | 5 |
| _ILines3DAuto | interface | 4 | 3 |
| _ILipAuto | interface | 8 | 22 |
| _ILipsAuto | interface | 2 | 3 |
| _ILiveSectionAuto | interface | 3 | 11 |
| _ILiveSectionsAuto | interface | 2 | 3 |
| _ILoadAuto | interface | 22 | 2 |
| _ILoadOwnerAuto | interface | 13 | 1 |
| _ILoftedCutoutAuto | interface | 10 | 19 |
| _ILoftedCutoutsAuto | interface | 3 | 3 |
| _ILoftedFlangeAuto | interface | 17 | 35 |
| _ILoftedFlangesAuto | interface | 4 | 3 |
| _ILoftedProtrusionAuto | interface | 12 | 19 |
| _ILoftedProtrusionsAuto | interface | 4 | 3 |
| _ILoftedSurfaceAuto | interface | 12 | 21 |
| _ILoftedSurfacesAuto | interface | 3 | 3 |
| _ILouverAuto | interface | 12 | 28 |
| _ILouversAuto | interface | 3 | 3 |
| _IMatchFlangeFaceAuto | interface | 6 | 21 |
| _IMatchFlangeFacesAuto | interface | 2 | 3 |
| _IMeasureVariableAuto | interface | 6 | 17 |
| _IMeshControlAuto | interface | 6 | 1 |
| _IMeshOwnerAuto | interface | 14 | 4 |
| _IMidSurfaceAuto | interface | 9 | 21 |
| _IMidSurfacesAuto | interface | 3 | 3 |
| _IMirrorCopiesAuto | interface | 4 | 3 |
| _IMirrorCopyAuto | interface | 11 | 21 |
| _IMirrorCopyGeometriesAuto | interface | 3 | 3 |
| _IMirrorCopyGeometryAuto | interface | 9 | 20 |
| _IMirrorPartAuto | interface | 11 | 19 |
| _IMirrorPartsAuto | interface | 3 | 3 |
| _IModeAuto | interface | 4 | 0 |
| _IModelAuto | interface | 33 | 130 |
| _IModelsAuto | interface | 51 | 5 |
| _IModesOwnerAuto | interface | 4 | 0 |
| _IMountingBoss2dAuto | interface | 12 | 11 |
| _IMountingBoss2dCollectionAuto | interface | 2 | 3 |
| _IMountingBossAuto | interface | 12 | 38 |
| _IMountingBossCollectionAuto | interface | 2 | 3 |
| _IMultiEdgeFlangeAuto | interface | 25 | 34 |
| _IMultiEdgeFlangesAuto | interface | 3 | 3 |
| _INormalCutoutAuto | interface | 10 | 31 |
| _INormalCutoutsAuto | interface | 6 | 3 |
| _INormalToFaceCutoutAuto | interface | 10 | 20 |
| _INormalToFaceCutoutsAuto | interface | 2 | 3 |
| _INormalToFaceProtrusionAuto | interface | 10 | 20 |
| _INormalToFaceProtrusionsAuto | interface | 2 | 3 |
| _IOffsetEdgeAuto | interface | 10 | 18 |
| _IOffsetEdgesAuto | interface | 2 | 3 |
| _IOffsetSurfaceAuto | interface | 9 | 22 |
| _IOffsetSurfacesAuto | interface | 2 | 3 |
| _IOptimizationAuto | interface | 18 | 0 |
| _IOptimizationOwnerAuto | interface | 2 | 0 |
| _IOverPropAuto | interface | 7 | 0 |
| _IPartConfigurationAuto | interface | 3 | 8 |
| _IPartConfigurationsAuto | interface | 6 | 3 |
| _IPartDocumentAuto | interface | 97 | 103 |
| _IPartFilletWeldAuto | interface | 6 | 19 |
| _IPartFilletWeldsAuto | interface | 2 | 3 |
| _IPartGrooveWeldAuto | interface | 6 | 22 |
| _IPartGrooveWeldsAuto | interface | 2 | 3 |
| _IPartLabelWeldAuto | interface | 10 | 17 |
| _IPartLabelWeldsAuto | interface | 2 | 3 |
| _IPartStitchWeldAuto | interface | 6 | 21 |
| _IPartStitchWeldsAuto | interface | 2 | 3 |
| _IPartingSplitAuto | interface | 12 | 19 |
| _IPartingSplitsAuto | interface | 2 | 3 |
| _IPartingSurfaceAuto | interface | 10 | 20 |
| _IPartingSurfacesAuto | interface | 2 | 3 |
| _IPatternAuto | interface | 40 | 36 |
| _IPatternCopyGeometriesAuto | interface | 7 | 3 |
| _IPatternCopyGeometryAuto | interface | 33 | 30 |
| _IPatternPartAuto | interface | 30 | 27 |
| _IPatternPartsAuto | interface | 7 | 3 |
| _IPatternsAuto | interface | 18 | 3 |
| _IPlotAuto | interface | 15 | 0 |
| _IPlotsOwnerAuto | interface | 4 | 0 |
| _IPoint3DAuto | interface | 1 | 3 |
| _IPoints3DAuto | interface | 7 | 4 |
| _IProfileAuto | interface | 26 | 49 |
| _IProfileSetAuto | interface | 2 | 10 |
| _IProfileSetsAuto | interface | 4 | 3 |
| _IProfilesAuto | interface | 2 | 5 |
| _IProjectCurveAuto | interface | 9 | 19 |
| _IProjectCurvesAuto | interface | 4 | 3 |
| _IPropOwnerAuto | interface | 3 | 0 |
| _IPropertyDefinitionAuto | interface | 1 | 5 |
| _IPropertyDefinitionsAuto | interface | 2 | 3 |
| _IPropertyTableDefinitionAuto | interface | 2 | 7 |
| _IPropertyTableDefinitionsAuto | interface | 3 | 3 |
| _IRebendAuto | interface | 9 | 17 |
| _IRebendsAuto | interface | 2 | 3 |
| _IRecoveredBodiesAuto | interface | 2 | 3 |
| _IRecoveredBodyAuto | interface | 10 | 18 |
| _IRedefineFaceAuto | interface | 11 | 19 |
| _IRedefineFacesAuto | interface | 2 | 3 |
| _IRefAxesAuto | interface | 1 | 3 |
| _IRefAxisAuto | interface | 7 | 12 |
| _IRefPlaneAuto | interface | 10 | 18 |
| _IRefPlanesAuto | interface | 14 | 4 |
| _IReferencePointCloudAuto | interface | 2 | 13 |
| _IReferencePointCloudsAuto | interface | 3 | 4 |
| _IReliefPatchFeatureAuto | interface | 11 | 17 |
| _IReliefPatchFeaturesAuto | interface | 3 | 3 |
| _IReplaceFaceAuto | interface | 9 | 19 |
| _IReplaceFacesAuto | interface | 2 | 3 |
| _IResizeBendAuto | interface | 10 | 19 |
| _IResizeBendsAuto | interface | 2 | 3 |
| _IResizeHoleAuto | interface | 9 | 21 |
| _IResizeHolesAuto | interface | 2 | 3 |
| _IResizeRoundAuto | interface | 10 | 19 |
| _IResizeRoundsAuto | interface | 2 | 3 |
| _IResultsOwnerAuto | interface | 6 | 0 |
| _IRevolvedCutoutAuto | interface | 17 | 29 |
| _IRevolvedCutoutsAuto | interface | 17 | 3 |
| _IRevolvedProtrusionAuto | interface | 17 | 30 |
| _IRevolvedProtrusionsAuto | interface | 12 | 3 |
| _IRevolvedSurfaceAuto | interface | 15 | 21 |
| _IRevolvedSurfacesAuto | interface | 7 | 3 |
| _IRibAuto | interface | 10 | 24 |
| _IRibsAuto | interface | 2 | 3 |
| _IRipEdgeAuto | interface | 10 | 17 |
| _IRipEdgesAuto | interface | 2 | 3 |
| _IRoundAuto | interface | 13 | 23 |
| _IRoundsAuto | interface | 5 | 3 |
| _IRuledSurfaceAuto | interface | 12 | 24 |
| _IRuledSurfacesAuto | interface | 2 | 3 |
| _IScaleBodyFeatureAuto | interface | 10 | 19 |
| _IScaleBodyFeaturesAuto | interface | 2 | 3 |
| _ISheetMetalDocumentAuto | interface | 94 | 100 |
| _ISimplifiedAssemblyModelAuto | interface | 23 | 22 |
| _ISimplifiedModelAuto | interface | 8 | 23 |
| _ISimplifiedModelsAuto | interface | 2 | 3 |
| _ISketch3DAuto | interface | 11 | 23 |
| _ISketch3DFeatureAuto | interface | 7 | 18 |
| _ISketch3DFeaturesAuto | interface | 2 | 3 |
| _ISketch3DRelationAuto | interface | 3 | 4 |
| _ISketch3DRelationsAuto | interface | 19 | 3 |
| _ISketchAuto | interface | 8 | 23 |
| _ISketchBlockAuto | interface | 1 | 9 |
| _ISketchBlockLabelAuto | interface | 16 | 18 |
| _ISketchBlockLabelOccurrenceAuto | interface | 2 | 15 |
| _ISketchBlockLabelOccurrencesAuto | interface | 1 | 3 |
| _ISketchBlockLabelsAuto | interface | 2 | 3 |
| _ISketchBlockOccurrenceAuto | interface | 19 | 17 |
| _ISketchBlockOccurrencesAuto | interface | 2 | 3 |
| _ISketchBlockViewAuto | interface | 5 | 38 |
| _ISketchBlockViewsAuto | interface | 2 | 4 |
| _ISketchBlocksAuto | interface | 5 | 3 |
| _ISketches3DAuto | interface | 2 | 3 |
| _ISketchsAuto | interface | 8 | 4 |
| _ISlotAuto | interface | 23 | 23 |
| _ISlotGroupAuto | interface | 6 | 9 |
| _ISlotGroupsAuto | interface | 1 | 3 |
| _ISlotsAuto | interface | 6 | 3 |
| _ISolidSweptCutoutAuto | interface | 7 | 17 |
| _ISolidSweptCutoutsAuto | interface | 2 | 3 |
| _ISolidSweptProtrusionAuto | interface | 7 | 17 |
| _ISolidSweptProtrusionsAuto | interface | 2 | 3 |
| _ISphereFeatureAuto | interface | 2 | 7 |
| _ISphereFeaturesAuto | interface | 3 | 3 |
| _ISplitAuto | interface | 12 | 20 |
| _ISplitCurveAuto | interface | 8 | 19 |
| _ISplitCurvesAuto | interface | 3 | 3 |
| _ISplitFaceAuto | interface | 11 | 18 |
| _ISplitFacesAuto | interface | 4 | 3 |
| _ISplitsAuto | interface | 2 | 3 |
| _IStitchSurfaceAuto | interface | 11 | 20 |
| _IStitchSurfacesAuto | interface | 3 | 3 |
| _IStitchWeldAuto | interface | 6 | 21 |
| _IStitchWeldsAuto | interface | 2 | 3 |
| _IStudyAuto | interface | 62 | 0 |
| _IStudyOwnerAuto | interface | 12 | 4 |
| _ISubdivisionFeatureAuto | interface | 23 | 18 |
| _ISubdivisionFeaturesAuto | interface | 5 | 3 |
| _ISubtractAuto | interface | 14 | 20 |
| _ISubtractsAuto | interface | 4 | 3 |
| _ISuppressVariableAuto | interface | 6 | 17 |
| _ISurfaceByBoundariesAuto | interface | 4 | 3 |
| _ISurfaceByBoundaryAuto | interface | 22 | 18 |
| _ISweptCutoutAuto | interface | 14 | 24 |
| _ISweptCutoutsAuto | interface | 3 | 3 |
| _ISweptProtrusionAuto | interface | 14 | 24 |
| _ISweptProtrusionsAuto | interface | 3 | 3 |
| _ISweptSurfaceAuto | interface | 14 | 25 |
| _ISweptSurfacesAuto | interface | 3 | 3 |
| _ITabAndSlotFeatureAuto | interface | 12 | 32 |
| _ITabAndSlotFeaturesAuto | interface | 2 | 3 |
| _ITabAuto | interface | 10 | 20 |
| _ITabsAuto | interface | 2 | 3 |
| _ITerminalAuto | interface | 2 | 6 |
| _ITerminalsAuto | interface | 2 | 3 |
| _IThickenAuto | interface | 9 | 18 |
| _IThickensAuto | interface | 3 | 3 |
| _IThinAuto | interface | 9 | 18 |
| _IThinsAuto | interface | 1 | 3 |
| _IThinwallAuto | interface | 11 | 20 |
| _IThinwallsAuto | interface | 2 | 3 |
| _IThreadAuto | interface | 10 | 20 |
| _IThreadsAuto | interface | 3 | 3 |
| _IToggleToConstructionAuto | interface | 4 | 10 |
| _IToggleToConstructionsAuto | interface | 2 | 3 |
| _IToggleToDesignAuto | interface | 4 | 10 |
| _IToggleToDesignsAuto | interface | 2 | 3 |
| _ITrimSurfaceAuto | interface | 11 | 17 |
| _ITrimSurfacesAuto | interface | 3 | 3 |
| _ITubeFeatureAuto | interface | 6 | 16 |
| _ITubeFeaturesAuto | interface | 1 | 3 |
| _IUnbendAuto | interface | 9 | 17 |
| _IUnbendsAuto | interface | 2 | 3 |
| _IUnionAuto | interface | 12 | 20 |
| _IUnionsAuto | interface | 2 | 3 |
| _IUnitedBodiesAuto | interface | 2 | 3 |
| _IUnitedBodyAuto | interface | 10 | 18 |
| _IUsedSketchAuto | interface | 2 | 6 |
| _IUsedSketchesAuto | interface | 1 | 3 |
| _IUserDefinedPatternAuto | interface | 10 | 22 |
| _IUserDefinedPatternsAuto | interface | 2 | 3 |
| _IUserDefinedSetAuto | interface | 3 | 7 |
| _IUserDefinedSetsAuto | interface | 2 | 3 |
| _IVentAuto | interface | 14 | 35 |
| _IVentsAuto | interface | 5 | 3 |
| _IWebNetworkAuto | interface | 12 | 24 |
| _IWebNetworksAuto | interface | 3 | 3 |
| _IWeldBeadByExtrudedProtrusionAuto | interface | 8 | 23 |
| _IWeldBeadByExtrudedProtrusionsAuto | interface | 4 | 3 |
| _IWeldBeadByRevolvedProtrusionAuto | interface | 8 | 22 |
| _IWeldBeadByRevolvedProtrusionsAuto | interface | 3 | 3 |
| _IWeldBeadBySweptProtrusionAuto | interface | 6 | 15 |
| _IWeldBeadBySweptProtrusionsAuto | interface | 2 | 3 |
| _IWeldBeadModelAuto | interface | 2 | 10 |
| _IWeldBeadModelsAuto | interface | 1 | 3 |
| _IWeldChamferAuto | interface | 8 | 19 |
| _IWeldChamfersAuto | interface | 4 | 3 |
| _IWeldExtrudedCutoutFeatureAuto | interface | 8 | 24 |
| _IWeldExtrudedCutoutFeaturesAuto | interface | 9 | 3 |
| _IWeldHoleFeatureAuto | interface | 8 | 21 |
| _IWeldHoleFeaturesAuto | interface | 5 | 3 |
| _IWeldMirrorAuto | interface | 7 | 18 |
| _IWeldMirrorsAuto | interface | 2 | 3 |
| _IWeldPartModelAuto | interface | 2 | 12 |
| _IWeldPartModelsAuto | interface | 1 | 3 |
| _IWeldPatternAuto | interface | 18 | 23 |
| _IWeldPatternsAuto | interface | 4 | 3 |
| _IWeldRevolvedCutoutFeatureAuto | interface | 8 | 23 |
| _IWeldRevolvedCutoutFeaturesAuto | interface | 5 | 3 |
| _IWeldRoundAuto | interface | 10 | 17 |
| _IWeldRoundsAuto | interface | 4 | 3 |
| _IWeldmentDocumentAuto | interface | 55 | 55 |
| _IWeldmentModelAuto | interface | 6 | 31 |
| _IWeldmentModelsAuto | interface | 3 | 3 |
| _IWireFeatureAuto | interface | 7 | 16 |
| _IWireFeaturesAuto | interface | 1 | 3 |
| _IWrapSketchAuto | interface | 11 | 18 |
| _IWrapSketchsAuto | interface | 2 | 3 |

---
## Program/PolarionConnector.tlb
**** (GUID: `{02ACF83F-A6A2-4BCB-80D7-C1F4510E9FC0}`, v1.0)

### Interfaces (1)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| IPolarionConnector | interface | 7 | 0 |

### CoClasses (1)

- **ConConsumer** (`{7212CD0B-E033-31DC-B27F-B3157D95C768}`): _Object, IPolarionConnector

---
## Program/REFATTR.tlb
**** (GUID: `{31039810-9535-11CE-91D1-080036661F02}`, v1.0)

### Interfaces (5)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| AsmPhysPropsAttrs | dispatch | 0 | 0 |
| Identification | dispatch | 0 | 0 |
| Identification2 | dispatch | 0 | 0 |
| RefAttr | dispatch | 0 | 0 |
| RefAttr2 | dispatch | 0 | 0 |

---
## Program/RevMgr.tlb
**Solid Edge Revision Manager Object Library (Deprecated)** (GUID: `{DF778D1A-0AA4-11D1-BC6E-0800360E1E02}`, v1.0)

### Enums (16)

- **ApplicationGlobalConstants** [24]: seApplicationGlobalCheckInOnClose=0, seApplicationGlobalLogFilesLocation=1, seApplicationGlobalInsightCacheLocation=2, seApplicationGlobalInsightFolderMappingFileLocation=3, seApplicationGlobalSearchScope=4, ... (24 total)
- **CheckInOptions** [2]: DoNotCheckInOption=0, UploadAndCheckInOption=1
- **CookieDataToGet** [1]: GET_REVISION_RULE=0
- **DocFOPStatus** [5]: FopStatusUnknown=0, NotInvolvedInFOP=1, FOPMasterDocument=2, FOPMemberDocument=4, FOPMasterAndChild=6
- **DocumentAccess** [3]: igReadWrite=0, igReadOnly=1, igReadExclusive=2
- **DocumentStatus** [6]: igStatusAvailable=0, igStatusInWork=1, igStatusInReview=2, igStatusReleased=3, igStatusBaselined=4, ... (6 total)
- **InsightSPUserRights** [23]: seViewListItems=1, seAddListItems=2, seEditListItems=4, seDeleteListItems=8, seCancelCheckout=256, ... (23 total)
- **InterPartLinkOption** [4]: eInterPartLinkUnknown=0, eCopyAllLinkedDocs=1, eUpdateLinksToNewDoc=2, eOutOfContextWithNewDoc=3
- **LinkTypeConstants** [3]: seLinkTypeAll=0, seLinkTypeNormal=1, seLinkTypeInterpart=2
- **OverWriteFilesOption** [2]: NoToAll=0, YesToAll=1
- **PCFFilePermissions** [9]: NoPermissions=0, PMIPermissions=2, CrossSectionPermissions=8, MeasurePermissions=80, MarkupPermissions=768, ... (9 total)
- **RevisionManagerAction** [14]: UnknownAction=0, CopyAction=1, CopyAllAction=2, ReviseAction=3, ReviseAllAction=4, ... (14 total)
- **RevisionRuleType** [4]: LastSavedType=0, LatestReleasedRevision=1, LatestRevision=2, ExternalBOM=3
- **SPServerType** [4]: SERVER_TYPE_NOT_SHAREPOINT=0, SHAREPOINT_V1_SERVER=1, SHAREPOINT_V2_SERVER=2, SHAREPOINT_V3_SERVER=3
- **SearchType** [2]: ShallowSearch=0, DeepSearch=1
- **UploadType** [2]: DeepUploadType=0, ShallowUploadType=1

### Interfaces (7)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| IDocAuto | dispatch | 14 | 1 |
| IInsight | dispatch | 60 | 0 |
| ILinkedDocsAuto | dispatch | 0 | 3 |
| IPropertiesAuto | dispatch | 2 | 3 |
| IPropertyAuto | dispatch | 1 | 0 |
| IPropertySetsAuto | dispatch | 4 | 2 |
| IRMgrApp | dispatch | 34 | 3 |

### CoClasses (7)

- **Application** (`{DF778D19-0AA4-11D1-BC6E-0800360E1E02}`): IRMgrApp
- **Document** (`{5CAC1974-0CD0-11D1-BC6F-0800360E1E02}`): IDocAuto
- **Insight** (`{06AEF304-AD7E-4C10-9904-29463E231246}`): IInsight
- **LinkedDocuments** (`{5CAC1977-0CD0-11D1-BC6F-0800360E1E02}`): ILinkedDocsAuto
- **Properties** (`{1EA5BA57-78F6-44BD-B68B-C3DD52632080}`): IPropertiesAuto
- **Property** (`{DE2F5653-8899-4355-A14B-27B5DC32A0FE}`): IPropertyAuto
- **PropertySets** (`{0323A7D6-9F38-4000-BF00-7AFAF7A40F99}`): IPropertySetsAuto

---
## Program/SE3Dtrans.tlb
**SE3Dtrans 1.0 Type Library** (GUID: `{CC13ED95-5B97-4B36-8AA4-546860079EAF}`, v1.0)

### Interfaces (5)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| ICatia3D | interface | 3 | 0 |
| IIges3D | interface | 3 | 0 |
| IJTransMessage | interface | 1 | 0 |
| IProE3D | interface | 3 | 0 |
| IStep3D | interface | 3 | 0 |

### CoClasses (4)

- **Catia3D** (`{9304061A-2475-40BA-AEF4-EC8F2BF5091B}`): ICatia3D
- **Iges3D** (`{83BD8C2E-C783-41BA-BBE9-299EEA6CE390}`): IIges3D
- **ProE3D** (`{57F08AC8-B4F5-4F41-B91B-E701C1E54A68}`): IProE3D
- **Step3D** (`{C29DA953-0D9D-40F1-BBE8-9F9751FE63B9}`): IStep3D

---
## Program/SE3dPrinting/SE3DPrint3YourMind.tlb
**** (GUID: `{139FF47F-995D-49EA-86A9-6ADF0F326A07}`, v221.0)

### CoClasses (1)

- **SE3DPrintService** (`{34D5F9FA-B109-40E3-86BC-4ECE4A2873BD}`): _Object, ISE3DPrintServices

---
## Program/SE3dPrinting/SE3DPrintDialog.tlb
**** (GUID: `{FF95F5F3-9DD7-41CB-8191-C3B99D13DF0E}`, v1.0)

### Interfaces (1)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| ISE3DPrintDlg | interface | 4 | 0 |

### CoClasses (1)

- **SE3DPrintDlg** (`{975EB2E7-A6A8-44B1-84F5-EE0394C0FB6F}`): _Object, ISE3DPrintDlg

---
## Program/SE3dPrinting/SE3DPrintShinning.tlb
**** (GUID: `{47313FF5-0D2B-49FA-82AD-BF9C23A8D965}`, v221.0)

### CoClasses (1)

- **SE3DPrintService** (`{18107AE1-33B8-4CEF-B0BF-17895BEA06FC}`): _Object, ISE3DPrintServices

---
## Program/SE3dPrinting/SE3DPrinting.tlb
**** (GUID: `{58576979-DA2C-46E4-9574-D3C849446A8E}`, v221.0)

### Interfaces (1)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| ISE3DPrintServices | interface | 3 | 0 |

---
## Program/SEAcisTrans.tlb
**SEAcisTrans 1.0 Type Library** (GUID: `{823C4DDE-D9A5-4F3A-96C8-4D500ED73D9B}`, v1.0)

### Interfaces (2)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| IJTransMessage | interface | 1 | 0 |
| ISat3D | interface | 3 | 0 |

### CoClasses (1)

- **Sat3D** (`{80188601-731C-4336-8DC0-483580C192EF}`): ISat3D

---
## Program/SEElectricalConnector.tlb
**** (GUID: `{A3B22E58-92DE-4410-B148-35A64615E502}`, v226.0)

### Interfaces (1)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| ISEElectricalConnector | interface | 6 | 0 |

### CoClasses (1)

- **ConConsumer** (`{0C50F9C6-A656-3111-9409-6103DB825D35}`): _Object, ISEElectricalConnector

---
## Program/SEPreview.tlb
**SEPreview ActiveX Control module** (GUID: `{7940C9BD-91D6-4884-8967-659987ACAC0A}`, v1.0)

### Interfaces (2)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| _DSEPreview | dispatch | 2 | 0 |
| _DSEPreviewEvents | dispatch | 0 | 0 |

### CoClasses (1)

- **SEPreview** (`{7F0AA8A5-3928-4B4B-AE60-4E3C1E331103}`): _DSEPreview, _DSEPreviewEvents

---
## Program/SERecordAndPublish/SERecordAndPublish.tlb
**** (GUID: `{F1CAC65B-F28D-4081-977F-9330BDD40BA7}`, v226.0)

### Interfaces (2)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| ISEPublishAndSearchVideos | interface | 24 | 0 |
| ISERecord | interface | 16 | 0 |

### CoClasses (1)

- **SERecordAndPublishClass** (`{9DA872C5-E913-4D5E-B69E-5614771E1A1A}`): _Object, ISEPublishAndSearchVideos, ISERecord

---
## Program/SeThumbnail.tlb
**SeThumbnail 1.0 Type Library** (GUID: `{4F322DC8-10E3-40F4-AA89-4367BA4FA755}`, v1.0)

### Interfaces (2)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| ICSEPreviewHandler | interface | 0 | 0 |
| ISeThumbnailExtractor | dispatch | 1 | 0 |

### CoClasses (2)

- **CSEPreviewHandler** (`{52E07B83-5E67-4CBB-832D-67F599D4D086}`): ICSEPreviewHandler
- **SeThumbnailExtractor** (`{D5E1D8F7-7570-490B-93A4-3B106BAB13AD}`): ISeThumbnailExtractor

---
## Program/SolidEdgeGateway.tlb
**** (GUID: `{05406F26-4B8F-407A-8750-D81A82CE14A8}`, v226.0)

### Interfaces (3)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| ICESE | dispatch | 5 | 0 |
| _DashboardFeatures | dispatch | 0 | 0 |
| _SESAMAccessHelper | dispatch | 0 | 0 |

### CoClasses (2)

- **DashboardFeatures** (`{F5839BF1-5B1D-4890-9884-3EB73E672A79}`): _DashboardFeatures, _Object, ICESE, IDisposable
- **SESAMAccessHelper** (`{EF934D6E-D970-3AB6-BA98-3AAFA2DC6D4A}`): _SESAMAccessHelper, _Object

---
## Program/StdParts/PFCOM.tlb
**PFCOM** (GUID: `{444657C2-CC6B-4DCF-B835-8C653AE63528}`, v1.0)

### Enums (5)

- **DocSortBy** [6]: DocSortBy_FilePath=0, DocSortBy_PartName=1, DocSortBy_Priority=2, DocSortBy_Status=3, DocSortBy_SourceFilePath=4, ... (6 total)
- **LICENSE_RESULT** [4]: LICENSE_RESULT_LIC_INVALID_DOC=-1, LICENSE_RESULT_LIC_OK=0, LICENSE_RESULT_LIC_ERROR_ML=1, LICENSE_RESULT_LIC_ERROR_PL=2
- **PropAttrIndex** [7]: PropAttrIndex_GUID=0, PropAttrIndex_Name=1, PropAttrIndex_StrValue=2, PropAttrIndex_NumValue0=3, PropAttrIndex_NumValue1=4, ... (7 total)
- **SP_RESULT** [3]: SP_RESULT_NOT_STANDARD=0, SP_RESULT_MULTI_PART=1, SP_RESULT_GENERATED_PART=2
- **TC_RESULT** [5]: TC_RESULT_FOUND=0, TC_RESULT_NO_STREAM=1, TC_RESULT_NOT_IN_DB=2, TC_RESULT_NOT_GENERATED=3, TC_RESULT_NO_TC_ID=4

### Interfaces (1)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| _PFCOM | dispatch | 31 | 28 |

### CoClasses (1)

- **PFCOM** (`{62296821-23FE-3280-B115-57DF123F6E1D}`): _PFCOM, _Object, IDisposable

---
## Program/StdParts/StdParts.tlb
**StdParts 1.0 Type Library** (GUID: `{DB33F102-2FBF-4996-AAA4-4400E8330B8D}`, v1.0)

### Interfaces (1)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| IPFCOM | dispatch | 18 | 26 |

### CoClasses (1)

- **CPFCOM** (`{EC61C63E-1598-4871-832C-6F3714920CE5}`): IPFCOM

---
## Program/StructureEditor.tlb
**Solid Edge Structure Editor Object Library** (GUID: `{A91AA076-8091-48A7-9F9B-B59BDAF78127}`, v1.0)

### Interfaces (3)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| ISEECStructureEditor | dispatch | 31 | 0 |
| ISEECStructureEditorATP | dispatch | 12 | 0 |
| IStructureEditor | dispatch | 5 | 2 |

### CoClasses (3)

- **Application** (`{064642EA-9913-4303-9C3E-B1E5AE467231}`): IStructureEditor
- **SEECStructureEditor** (`{070F7A6C-8621-466C-9318-92461EC1B716}`): ISEECStructureEditor
- **SEECStructureEditorATP** (`{C8EDF44D-2C0E-4956-9709-A438528FD52A}`): ISEECStructureEditorATP

---
## Program/assembly.tlb
**Solid Edge Assembly Type Library** (GUID: `{3E2B3BD4-F0B9-11D1-BDFD-080036B4D502}`, v1.0)

### Enums (75)

- **AlternateAssemblyTypeConstants** [2]: seAlternateAssemblyType_Family=1, seAlternateAssemblyType_AlternatePosition=2
- **AssemblyBaseStylesConstants** [6]: seAssemblyBaseStyle=0, seAssemblyConstructionStyle=1, seAssemblyThreadedCylindersStyle=2, seAssemblyCurveStyle=3, seAssemblyWeldBeadStyle=4, ... (6 total)
- **AssemblyComponentTypeConstants** [7]: seAssemblyComponentTypeAll=0, seAssemblyComponentTypeReference=1, seAssemblyComponentTypeFramePart=2, seAssemblyComponentTypeEndCapPart=3, seAssemblyComponentTypePatterns=4, ... (7 total)
- **AssemblyCopyActionConstants** [6]: seAssemblyCopyActionInclude=0, seAssemblyCopyActionExclude=1, seAssemblyCopyActionPending=2, seAssemblyCopyActionMirror=3, seAssemblyCopyActionRotate=4, ... (6 total)
- **AssemblyCopyComponentConstants** [4]: seAssemblyCopyComponentsIncludeAll=0, seAssemblyCopyComponentsExcludeAll=1, seAssemblyCopyComponentsIncludeSpecified=2, seAssemblyCopyComponentsExcludeSpecified=3
- **AssemblyCopyStatusConstants** [7]: seAssemblyCopyStatusOK=0, seAssemblyCopyStatusOutOfDate=1, seAssemblyCopyStatusFrozen=2, seAssemblyCopyStatusPending=3, seAssemblyCopyStatusMirrorPlaneMissing=4, ... (7 total)
- **AssemblyCopyTypeConstants** [3]: seAssemblyCopyTypeDefault=0, seAssemblyCopyTypeMirror=1, seAssemblyCopyTypeMultiBodyPart=2
- **AssemblyFaceStyleOverrideConstants** [3]: UseNoneStyle=0, UsePartStyle=1, UseValidStyle=2
- **AssemblyFamilyMemberPropertyConstants** [3]: seAssemblyFamilyMemberPropertyDocumentNumber=0, seAssemblyFamilyMemberPropertyRevisionNumber=1, seAssemblyFamilyMemberPropertyProjectName=2
- **AssemblyFamilyMemberStatusConstants** [3]: seAssemblyFamilyMemberStatusUpToDate=0, seAssemblyFamilyMemberStatusNotPopulated=1, seAssemblyFamilyMemberStatusPopulatedAndOutOfDate=2
- **AssemblyFeaturePresenceConstants** [3]: AssemblyFeaturePresence_None=0, AssemblyFeaturePresence_Legacy=1, AssemblyFeaturePresence_Enhanced=2
- **AssemblyFileOpenActivateChangedPartOptions** [3]: seAssemblyFileOpenActivateChangedPart_Prompt=0, seAssemblyFileOpenActivateChangedPart_Activate=1, seAssemblyFileOpenActivateChangedPart_Inactivate=1
- **AssemblyFileOpenPartActivationOptions** [3]: seAssemblyFileOpenPartActivation_ActivateAll=0, seAssemblyFileOpenPartActivation_InactivateAll=1, seAssemblyFileOpenPartActivation_LastSaved=2
- **AssemblyFileOpenSimplificationOptions** [3]: seAssemblyFileOpenSimplification_AllSimplified=0, seAssemblyFileOpenSimplification_AllDesigned=1, seAssemblyFileOpenSimplification_LastSaved=2
- **AssemblyGlobalConstants** [21]: seAssemblyGlobalTubeWallThickness=1, seAssemblyGlobalTubeBendRadius=2, seAssemblyGlobalTubeOuterDiameter=3, seAssemblyGlobalTubeMinimumFlatLength=4, seAssemblyGlobalTubeEndTreatmentOutsideDiameter=5, ... (21 total)
- **AssemblyPathfinderUpdateConstants** [6]: seUpdate=1, seRebuild=2, seSuspend=3, seResume=4, seExpandAll=5, ... (6 total)
- **AssemblyPatternTypeConstants** [3]: seAssemblyPatternType=1, seAssemblyDuplicatePatternType=2, seAssemblyPatternAlongCurveType=3
- **AssemblyReportTypeConstants** [2]: seAssemblyWireReportAtomic=0, seAssemblyWireReportExpanded=1
- **AssemblyWireHarnessReportTypeConstants** [3]: seAssemblyWireHarnessReportComponents=1, seAssemblyWireHarnessReportConnections=2, seAssemblyWireHarnessReportHBom=3
- **AutoExplodeSelectionTypeConstants** [2]: seTopLevelAssembly=0, seSubassembly=1
- **AutoExplodeTechniqueConstants** [2]: seBySubassemblyLevel=0, seByIndividualPart=1
- **CloneComponentOptions** [3]: seRepairUnsatisfiedRelationships=0, seDoNotCreateRelationships=2, seCreateGroundRelationships=3
- **CloneMatchTypeOptions** [2]: CloneMatchTypeAutomatic=0, CloneMatchTypeExact=1
- **ConfigurationTypeConstants** [2]: seConfigurationType_Display=0, seConfigurationType_Explode=1
- **ConstraintReplacementConstants** [3]: seConstraintReplacementNone=0, seConstraintReplacementSuppress=1, seConstraintReplacementDelete=2
- **CurveSegmentPathAdditionStatusConstants** [9]: seCurveSegmentPathAdditionStatusSucceeded=0, seCurveSegmentPathAdditionStatusFailedUnknownReason=1, seCurveSegmentPathAdditionStatusFailedBreak=2, seCurveSegmentPathAdditionStatusFailedDuplicate=3, seCurveSegmentPathAdditionStatusFailedFork=4, ... (9 total)
- **CurveSegmentPathRemovalStatusConstants** [6]: seCurveSegmentPathRemovalStatusSucceeded=0, seCurveSegmentPathRemovalStatusFailedUnknownReason=1, seCurveSegmentPathRemovalStatusFailedBreak=2, seCurveSegmentPathRemovalStatusFailedNotInPath=3, seCurveSegmentPathRemovalStatusFailedSingle=4, ... (6 total)
- **CurveSegmentValidationConstants** [15]: seCurveSegmentValidation_valid=0, seCurveSegmentValidation_break=1, seCurveSegmentValidation_angle=2, seCurveSegmentValidation_length=4, seCurveSegmentValidation_intersection=8, ... (15 total)
- **CurveSegmentWhichKeypointsConstants** [3]: seCurveSegmentWhichKeypoints_mid_points=1, seCurveSegmentWhichKeypoints_end_points=2, seCurveSegmentWhichKeypoints_all_points=3
- **DragComponentAnalysisOptionConstants** [2]: seNoAnalysis=0, seDetectCollisions=1
- **DragComponentCollisionOptionConstants** [2]: seDetectCollisionsEncounteredBySelectedPartOrSubassemblyOnly=0, seDetectCollisionsAmongAllAnalyzedPartsOrSubassemblies=1
- **EndCapTreatmentConstants** [3]: NoCornerTreatment=0, ApplyChamfer=1, ApplyFillet=2
- **EndCapTypeConstants** [2]: Inward=0, Outward=1
- **HarnessSaveAsEcadStatusConstants** [11]: seHarnessSaveAsEcadStatus_Success=0, seHarnessSaveAsEcadStatus_Failed=1, seHarnessSaveAsEcadStatus_FailedBadArgs=2, seHarnessSaveAsEcadStatus_FailedNoComps=3, seHarnessSaveAsEcadStatus_FailedNoConns=4, ... (11 total)
- **HarnessTypeConstants** [8]: seHarnessType_Wire=1, seHarnessType_Cable=2, seHarnessType_Bundle=3, seHarnessType_Wires=4, seHarnessType_Cables=5, ... (8 total)
- **InterferenceStatusConstants** [5]: seInterferenceStatusNoInterference=1, seInterferenceStatusConfirmedInterference=2, seInterferenceStatusProbableInterference=3, seInterferenceStatusConfirmedAndProbableInterference=4, seInterferenceStatusIncompleteAnalysis=5
- **InternalComponentTypeConstant** [4]: InternalComponentTypeConstant_Unknown=0, InternalComponentTypeConstant_Part=1, InternalComponentTypeConstant_Assembly=2, InternalComponentTypeConstant_SheetMetal=3
- **ItemNumberModeConstants** [5]: seItemNumber_None=0, seItemNumber_Toplevel=1, seItemNumber_Atomic=2, seItemNumber_Exploded=3, seItemNumber_LevelBased=4
- **MoveMultipleMoveTypeConstants** [2]: seMoveMultipleMove=1, seMoveMultipleCopy=2
- **MoveMultipleRelationshipConstants** [3]: seMoveMultipleMaintainInternalRelationships=1, seMoveMultipleDropInternalRelationships=2, seMoveMultipleDropInternalRelationshipsAndGround=3
- **OccurrenceSectionedFacetDataConstants** [3]: seOccurrenceSectionedFacetDataPresent=0, seOccurrenceSectionedFacetDataNotPresent=1, seOccurrenceNotSectioned=2
- **OccurrenceStatusConstants** [8]: seOccurrenceStatusWellDefined=1, seOccurrenceStatusFixed=2, seOccurrenceStatusUnderDefined=4, seOccurrenceStatusOverDefined=32776, seOccurrenceStatusNotConsistent=32784, ... (8 total)
- **PartStatusConstants** [8]: igPartStatusWellDefined=1, igPartStatusFixed=2, igPartStatusUnderDefined=4, igPartStatusOverDefined=32776, igPartStatusNotConsistent=32784, ... (8 total)
- **PatternOffsetTypeConstants** [4]: sePatternFitOffset=0, sePatternFillOffset=1, sePatternFixedOffset=2, sePatternChordLengthOffset=3
- **PipeFittingEndTreatmentConstants** [6]: sePipeFittingEndTreatmentNone=0, sePipeFittingEndTreatmentSocketWeld=1, sePipeFittingEndTreatmentButtWeld=2, sePipeFittingEndTreatmentFlange=3, sePipeFittingEndTreatmentThread=4, ... (6 total)
- **PipeFittingTypeConstants** [10]: sePipeFittingTypeNone=0, sePipeFittingTypeElbow=1, sePipeFittingTypeY=2, sePipeFittingTypeTee=3, sePipeFittingTypeCoupling=4, ... (10 total)
- **QueryConditionConstants** [3]: seQueryConditionContains=0, seQueryConditionIs=1, seQueryConditionIsNot=2
- **QueryPropertyConstants** [17]: seQueryPropertyName=0, seQueryPropertyTitle=1, seQueryPropertySubject=2, seQueryPropertyAuthor=3, seQueryPropertyManager=4, ... (17 total)
- **QueryScopeConstants** [4]: seQueryScopeAllParts=0, seQueryScopeShownParts=1, seQueryScopeHiddenParts=2, seQueryScopeSelectedParts=3
- **Relation3dDetailedStatusConstants** [7]: igRelation3dDetailedStatusUnknown=0, igRelation3dDetailedStatusSolved=1, igRelation3dDetailedStatusSuppressed=2, igRelation3dDetailedStatusBetweenSetMembers=3, igRelation3dDetailedStatusBetweenFixed=4, ... (7 total)
- **Relation3dGearRatioTypeConstants** [2]: igRelation3dGearRatioTypeNumberOfTurns=0, igRelation3dGearRatioTypeNumberOfTeeth=1
- **Relation3dGearTypeConstants** [3]: igRelation3dGearTypeRotaryRotary=0, igRelation3dGearTypeRotaryLinear=1, igRelation3dGearTypeLinearLinear=2
- **Relation3dGeometryConstants** [12]: igRelation3dGeometryPlane=1, igRelation3dGeometryLine=2, igRelation3dGeometryPoint=3, igRelation3dStartPoint=4, igRelation3dMidPoint=5, ... (12 total)
- **Relation3dOrientationConstants** [3]: igRelation3dOrientationNotspecified=0, igRelation3dOrientationAlign=1, igRelation3dOrientationAntialign=2
- **Relation3dStatusConstants** [2]: igRelation3dStatusUnsolved=0, igRelation3dStatusSolved=1
- **SaveAsHarnessFileFormats** [3]: HarnessFileFormatHX2ML=0, HarnessFileFormatDSI=1, HarnessFileFormatX2ML=2
- **SaveAsHarnessTopologyStatusConstants** [2]: seSaveAsHarnessTopologyStatus_Success=0, seSaveAsHarnessTopologyStatus_FailedBadArgs=1
- **SegmentRelation3dDirectionConstants** [3]: seSegmentRelation3dDirectionParallel=0, seSegmentRelation3dDirectionPerpendicular=1, seSegmentRelation3dDirectionCoincident=2
- **SegmentRelation3dDistanceConstants** [3]: seSegmentRelation3dDistanceNormal=0, seSegmentRelation3dDistanceReverse=1, seSegmentRelation3dDistanceTrueLength=2
- **SegmentRelation3dGeometryConstants** [9]: seSegmentRelation3dStartPoint=1, seSegmentRelation3dEndPoint=2, seSegmentRelation3dUnbounded=3, seSegmentRelation3dArcCenter=4, seSegmentRelation3dEllipseCenter=5, ... (9 total)
- **SegmentRelation3dStatusConstants** [2]: seSegmentRelation3dStatusUnsolved=0, seSegmentRelation3dStatusSolved=1
- **SimplifiedAssemblyMode** [3]: seSimplifiedAssemblyModeUnknown=0, seSimplifiedAssemblyModeModeled=1, seSimplifiedAssemblyModeVisibleFaces=2
- **StructuralFrameEndConditionConstants** [12]: seMiter=0, seButt1=1, seButt2=2, seNone=3, seRadius=4, ... (12 total)
- **StructuralFrameExtendTrimPositionConstants** [2]: startPosition=0, endPosition=1
- **TubePropertyPidConstants** [9]: seTubePropertyPid_TubeBendRadius=1508, seTubePropertyPid_TubeOuterDiameter=1509, seTubePropertyPid_TubeMinimumFlatLength=1510, seTubePropertyPid_TubeWallThickness=1511, seTubePropertyPid_TubeFlatLength=1512, ... (9 total)
- **TubeSegmentAdditionStatusConstants** [4]: seTubeSegmentAdditionStatusSucceeded=1, seTubeSegmentAdditionStatusFailedSplit=2, seTubeSegmentAdditionStatusFailedDisjoint=3, seTubeSegmentAdditionStatusFailedUnknownReason=4
- **TubeSegmentRemovalStatusConstants** [4]: seTubeSegmentRemovalStatusSucceeded=1, seTubeSegmentRemovalStatusFailedNotPartOfTube=2, seTubeSegmentRemovalStatusFailedDueToDisjoint=3, seTubeSegmentRemovalStatusFailedUnknownReason=4
- **UpdateStructureCacheConstants** [2]: seUseOpenDocuments=1, seWalkFilesOnDisk=2
- **VirtualComponentPublishConstants** [4]: seVCPublishOn_FrontView=1, seVCPublishOn_TopView=2, seVCPublishOn_RightView=3, seVCPublishOn_SketchView=4
- **VirtualComponentStatusConstants** [11]: seVCStatus_Success=1, seVCStatus_Fail=2, seVCStatus_AddUnManagedToManaged=3, seVCStatus_AddManagedToUnManaged=4, seVCStatus_ReplaceConflictWithVirtualComponent=5, ... (11 total)
- **VirtualComponentTypeConstants** [4]: seVirtualComponentType_Unknown=1, seVirtualComponentType_Assembly=2, seVirtualComponentType_Part=3, seVirtualComponentType_Sheetmetal=4
- **VisibilityBasedSimplifiedAssemblyCopyType** [2]: seVisibilityBasedSimplifiedAssemblyCopyTypeFaces=0, seVisibilityBasedSimplifiedAssemblyCopyTypeBodies=1
- **WirePathConstants** [3]: seSingleWirePath=0, seCableWirePathMaster=1, seCableWirePathMember=2
- **WirePathConstantsEx** [3]: seSingleWirePathEx=0, seCableWirePathSource=1, seCableWirePathMemberEx=2
- **seAssemblyBodyTypeConstants** [3]: seAssemblyBodyType_WeldBeadBody=1, seAssemblyBodyType_HarnessBody=2, seAssemblyBodyType_GenericAssemblyBody=3

### Interfaces (288)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| AFGrooveWeld | dispatch | 8 | 10 |
| AFGrooveWelds | dispatch | 1 | 3 |
| AdjustablePart | dispatch | 4 | 6 |
| AngularRelation3d | dispatch | 11 | 17 |
| ArcSegment | dispatch | 4 | 7 |
| ArcSegments | dispatch | 2 | 3 |
| AsmCADDirect | dispatch | 5 | 3 |
| AsmCADDirects | dispatch | 2 | 3 |
| AsmRefPlane | dispatch | 6 | 11 |
| AsmRefPlanes | dispatch | 16 | 4 |
| AssemblyBodies | dispatch | 1 | 6 |
| AssemblyBody | dispatch | 4 | 12 |
| AssemblyCopies | dispatch | 3 | 4 |
| AssemblyCopy | dispatch | 5 | 13 |
| AssemblyDocument | dispatch | 98 | 122 |
| AssemblyDrivenPartFeatures | dispatch | 0 | 7 |
| AssemblyDrivenPartFeaturesExtrudedCutout | dispatch | 20 | 8 |
| AssemblyDrivenPartFeaturesExtrudedCutouts | dispatch | 2 | 3 |
| AssemblyDrivenPartFeaturesHole | dispatch | 20 | 8 |
| AssemblyDrivenPartFeaturesHoles | dispatch | 2 | 3 |
| AssemblyDrivenPartFeaturesRevolvedCutout | dispatch | 18 | 8 |
| AssemblyDrivenPartFeaturesRevolvedCutouts | dispatch | 2 | 3 |
| AssemblyDrivenPartFeaturesTabAndSlot | dispatch | 6 | 18 |
| AssemblyDrivenPartFeaturesTabAndSlots | dispatch | 2 | 3 |
| AssemblyDrivenPartFeaturesTrimTube | dispatch | 6 | 4 |
| AssemblyDrivenPartFeaturesTrimTubes | dispatch | 2 | 3 |
| AssemblyFamilyMember | dispatch | 8 | 8 |
| AssemblyFamilyMembers | dispatch | 12 | 8 |
| AssemblyFeatures | dispatch | 1 | 15 |
| AssemblyFeaturesExtrudedCutout | dispatch | 23 | 12 |
| AssemblyFeaturesExtrudedCutouts | dispatch | 2 | 3 |
| AssemblyFeaturesExtrudedProtrusion | dispatch | 21 | 10 |
| AssemblyFeaturesExtrudedProtrusions | dispatch | 2 | 3 |
| AssemblyFeaturesHole | dispatch | 23 | 12 |
| AssemblyFeaturesHoles | dispatch | 2 | 3 |
| AssemblyFeaturesMirror | dispatch | 13 | 12 |
| AssemblyFeaturesMirrors | dispatch | 2 | 3 |
| AssemblyFeaturesPattern | dispatch | 13 | 12 |
| AssemblyFeaturesPatterns | dispatch | 2 | 3 |
| AssemblyFeaturesRevolvedCutout | dispatch | 21 | 12 |
| AssemblyFeaturesRevolvedCutouts | dispatch | 2 | 3 |
| AssemblyFeaturesRevolvedProtrusion | dispatch | 19 | 10 |
| AssemblyFeaturesRevolvedProtrusions | dispatch | 2 | 3 |
| AssemblyFeaturesSweptProtrusion | dispatch | 7 | 10 |
| AssemblyFeaturesSweptProtrusions | dispatch | 2 | 3 |
| AssemblyFilletWeld | dispatch | 9 | 16 |
| AssemblyFilletWelds | dispatch | 2 | 3 |
| AssemblyGroup | dispatch | 11 | 6 |
| AssemblyGroups | dispatch | 3 | 4 |
| AssemblyLabelWeld | dispatch | 8 | 9 |
| AssemblyLabelWelds | dispatch | 2 | 5 |
| AssemblyMirror | dispatch | 2 | 5 |
| AssemblyMirrors | dispatch | 1 | 3 |
| AssemblyPattern | dispatch | 15 | 5 |
| AssemblyPatternOccurrence | dispatch | 2 | 5 |
| AssemblyPatterns | dispatch | 12 | 3 |
| AssemblyProperties | dispatch | 4 | 4 |
| AssemblyProperty | dispatch | 8 | 4 |
| AssemblyStitchWeld | dispatch | 7 | 15 |
| AssemblyStitchWelds | dispatch | 2 | 3 |
| AssemblyThread | dispatch | 8 | 11 |
| AssemblyThreads | dispatch | 2 | 3 |
| AxialRelation3d | dispatch | 11 | 21 |
| Bundle | dispatch | 13 | 18 |
| Bundles | dispatch | 2 | 4 |
| Cable | dispatch | 13 | 27 |
| Cables | dispatch | 2 | 4 |
| CamFollowerRelation3d | dispatch | 6 | 11 |
| CenterPlaneRelation3d | dispatch | 11 | 9 |
| ComponentLayout | dispatch | 1 | 8 |
| ComponentLayouts | dispatch | 2 | 3 |
| Configuration | dispatch | 4 | 5 |
| Configurations | dispatch | 6 | 4 |
| CoordinateSystemRelation3d | dispatch | 10 | 11 |
| CurveSegment | dispatch | 6 | 10 |
| CurveSegments | dispatch | 2 | 3 |
| DefaultCustomOccurrenceProperties | dispatch | 1 | 3 |
| EndCap | dispatch | 6 | 8 |
| EndCaps | dispatch | 3 | 2 |
| FastenerSystem | dispatch | 7 | 4 |
| FastenerSystems | dispatch | 5 | 3 |
| GearRelation3d | dispatch | 11 | 13 |
| GroundRelation3d | dispatch | 6 | 11 |
| Harness | dispatch | 6 | 6 |
| Harnesses | dispatch | 3 | 3 |
| InternalComponent | dispatch | 20 | 16 |
| InternalComponents | dispatch | 3 | 4 |
| ItemNumbers | dispatch | 5 | 3 |
| Layout | dispatch | 1 | 11 |
| Layouts | dispatch | 3 | 4 |
| LineSegment | dispatch | 5 | 5 |
| LineSegments | dispatch | 2 | 3 |
| Occurrence | dispatch | 66 | 73 |
| Occurrences | dispatch | 13 | 6 |
| Part | dispatch | 12 | 23 |
| Parts | dispatch | 4 | 3 |
| Path | dispatch | 12 | 10 |
| PathRelation3d | dispatch | 6 | 11 |
| Paths | dispatch | 2 | 3 |
| PhysicalProperties | dispatch | 9 | 9 |
| Pipe | dispatch | 9 | 7 |
| Pipes | dispatch | 2 | 3 |
| PlanarRelation3d | dispatch | 10 | 19 |
| PointRelation3d | dispatch | 10 | 16 |
| Queries | dispatch | 6 | 5 |
| Query | dispatch | 5 | 8 |
| Relations3d | dispatch | 16 | 3 |
| RigidSetRelation3d | dispatch | 8 | 12 |
| SegmentAngularRelation3d | dispatch | 4 | 12 |
| SegmentDirectionRelation3d | dispatch | 4 | 8 |
| SegmentDistanceRelation3d | dispatch | 5 | 10 |
| SegmentPointRelation3d | dispatch | 4 | 7 |
| SegmentRadiusRelation3d | dispatch | 3 | 10 |
| SegmentRelations3d | dispatch | 7 | 3 |
| SegmentTangentRelation3d | dispatch | 4 | 7 |
| Segments | dispatch | 1 | 3 |
| SimplifiedAssemblies | dispatch | 1 | 5 |
| SimplifiedAssembly | dispatch | 5 | 6 |
| Splice | dispatch | 10 | 15 |
| Splices | dispatch | 2 | 4 |
| StructuralFrame | dispatch | 35 | 9 |
| StructuralFrames | dispatch | 9 | 3 |
| SubOccurrence | dispatch | 31 | 49 |
| SubOccurrences | dispatch | 1 | 3 |
| SubassemblyBodies | dispatch | 1 | 5 |
| SubassemblyBody | dispatch | 3 | 12 |
| SuppressComponent | dispatch | 6 | 5 |
| TangentRelation3d | dispatch | 10 | 16 |
| TopologyReference | dispatch | 3 | 4 |
| Tube | dispatch | 17 | 20 |
| VirtualComponent | dispatch | 5 | 11 |
| VirtualComponentOccurrence | dispatch | 17 | 10 |
| VirtualComponentOccurrences | dispatch | 4 | 3 |
| Wire | dispatch | 12 | 26 |
| WirePath | dispatch | 6 | 18 |
| WirePathCableMembers | dispatch | 1 | 3 |
| WirePathSegments | dispatch | 1 | 3 |
| WirePaths | dispatch | 3 | 3 |
| WireRun | dispatch | 7 | 6 |
| WireRunPaths | dispatch | 1 | 3 |
| WireRuns | dispatch | 3 | 3 |
| Wires | dispatch | 2 | 4 |
| Zone | dispatch | 11 | 4 |
| Zones | dispatch | 9 | 3 |
| _IAFGrooveWeldAuto | interface | 8 | 10 |
| _IAFGrooveWeldsAuto | interface | 1 | 3 |
| _IAdjustablePartAuto | interface | 4 | 6 |
| _IAngularRelation3dAuto | interface | 11 | 17 |
| _IArcSegmentAuto | interface | 4 | 7 |
| _IArcSegmentsAuto | interface | 2 | 3 |
| _IAsmCADDirectAuto | interface | 5 | 3 |
| _IAsmCADDirectsAuto | interface | 2 | 3 |
| _IAsmRefPlaneAuto | interface | 6 | 11 |
| _IAsmRefPlanesAuto | interface | 16 | 4 |
| _IAssemblyBodiesAuto | interface | 1 | 6 |
| _IAssemblyBodyAuto | interface | 4 | 12 |
| _IAssemblyCopiesAuto | interface | 3 | 4 |
| _IAssemblyCopyAuto | interface | 5 | 13 |
| _IAssemblyDocumentAuto | interface | 98 | 122 |
| _IAssemblyDrivenPartFeaturesAuto | interface | 0 | 7 |
| _IAssemblyDrivenPartFeaturesExtrudedCutoutAuto | interface | 20 | 8 |
| _IAssemblyDrivenPartFeaturesExtrudedCutoutsAuto | interface | 2 | 3 |
| _IAssemblyDrivenPartFeaturesHoleAuto | interface | 20 | 8 |
| _IAssemblyDrivenPartFeaturesHolesAuto | interface | 2 | 3 |
| _IAssemblyDrivenPartFeaturesRevolvedCutoutAuto | interface | 18 | 8 |
| _IAssemblyDrivenPartFeaturesRevolvedCutoutsAuto | interface | 2 | 3 |
| _IAssemblyDrivenPartFeaturesTabAndSlotAuto | interface | 6 | 18 |
| _IAssemblyDrivenPartFeaturesTabAndSlotsAuto | interface | 2 | 3 |
| _IAssemblyDrivenPartFeaturesTrimTubeAuto | interface | 6 | 4 |
| _IAssemblyDrivenPartFeaturesTrimTubesAuto | interface | 2 | 3 |
| _IAssemblyFamilyMemberAuto | interface | 8 | 8 |
| _IAssemblyFamilyMembersAuto | interface | 12 | 8 |
| _IAssemblyFeaturesAuto | interface | 1 | 15 |
| _IAssemblyFeaturesExtrudedCutoutAuto | interface | 23 | 12 |
| _IAssemblyFeaturesExtrudedCutoutsAuto | interface | 2 | 3 |
| _IAssemblyFeaturesExtrudedProtrusionAuto | interface | 21 | 10 |
| _IAssemblyFeaturesExtrudedProtrusionsAuto | interface | 2 | 3 |
| _IAssemblyFeaturesHoleAuto | interface | 23 | 12 |
| _IAssemblyFeaturesHolesAuto | interface | 2 | 3 |
| _IAssemblyFeaturesMirrorAuto | interface | 13 | 12 |
| _IAssemblyFeaturesMirrorsAuto | interface | 2 | 3 |
| _IAssemblyFeaturesPatternAuto | interface | 13 | 12 |
| _IAssemblyFeaturesPatternsAuto | interface | 2 | 3 |
| _IAssemblyFeaturesRevolvedCutoutAuto | interface | 21 | 12 |
| _IAssemblyFeaturesRevolvedCutoutsAuto | interface | 2 | 3 |
| _IAssemblyFeaturesRevolvedProtrusionAuto | interface | 19 | 10 |
| _IAssemblyFeaturesRevolvedProtrusionsAuto | interface | 2 | 3 |
| _IAssemblyFeaturesSweptProtrusionAuto | interface | 7 | 10 |
| _IAssemblyFeaturesSweptProtrusionsAuto | interface | 2 | 3 |
| _IAssemblyFilletWeldAuto | interface | 9 | 16 |
| _IAssemblyFilletWeldsAuto | interface | 2 | 3 |
| _IAssemblyGroupAuto | interface | 11 | 6 |
| _IAssemblyGroupsAuto | interface | 3 | 4 |
| _IAssemblyLabelWeldAuto | interface | 8 | 9 |
| _IAssemblyLabelWeldsAuto | interface | 2 | 5 |
| _IAssemblyMirrorAuto | interface | 2 | 5 |
| _IAssemblyMirrorsAuto | interface | 1 | 3 |
| _IAssemblyPatternAuto | interface | 15 | 5 |
| _IAssemblyPatternOccurrenceAuto | interface | 2 | 5 |
| _IAssemblyPatternsAuto | interface | 12 | 3 |
| _IAssemblyPropertiesAuto | interface | 4 | 4 |
| _IAssemblyPropertyAuto | interface | 8 | 4 |
| _IAssemblyStitchWeldAuto | interface | 7 | 15 |
| _IAssemblyStitchWeldsAuto | interface | 2 | 3 |
| _IAssemblyThreadAuto | interface | 8 | 11 |
| _IAssemblyThreadsAuto | interface | 2 | 3 |
| _IAxialRelation3dAuto | interface | 11 | 21 |
| _IBundleAuto | interface | 13 | 18 |
| _IBundlesAuto | interface | 2 | 4 |
| _ICableAuto | interface | 13 | 27 |
| _ICablesAuto | interface | 2 | 4 |
| _ICamFollowerRelation3dAuto | interface | 6 | 11 |
| _ICenterPlaneRelation3dAuto | interface | 11 | 9 |
| _IComponentLayoutAuto | interface | 1 | 8 |
| _IComponentLayoutsAuto | interface | 2 | 3 |
| _IConfigurationAuto | interface | 4 | 5 |
| _IConfigurationsAuto | interface | 6 | 4 |
| _ICoordinateSystemRelation3dAuto | interface | 10 | 11 |
| _ICurveSegmentAuto | interface | 6 | 10 |
| _ICurveSegmentsAuto | interface | 2 | 3 |
| _IDefaultCustomOccurrencePropertiesAuto | interface | 1 | 3 |
| _IEndCapAuto | interface | 6 | 8 |
| _IEndCapsAuto | interface | 3 | 2 |
| _IFastenerSystemAuto | interface | 7 | 4 |
| _IFastenerSystemsAuto | interface | 5 | 3 |
| _IGearRelation3dAuto | interface | 11 | 13 |
| _IGroundRelation3dAuto | interface | 6 | 11 |
| _IHarnessAuto | interface | 6 | 6 |
| _IHarnessesAuto | interface | 3 | 3 |
| _IInternalComponentAuto | interface | 20 | 16 |
| _IInternalComponentsAuto | interface | 3 | 4 |
| _IItemNumbersAuto | interface | 5 | 3 |
| _ILayoutAuto | interface | 1 | 11 |
| _ILayoutsAuto | interface | 3 | 4 |
| _ILineSegmentAuto | interface | 5 | 5 |
| _ILineSegmentsAuto | interface | 2 | 3 |
| _IOccurrenceAuto | interface | 66 | 73 |
| _IOccurrencesAuto | interface | 13 | 6 |
| _IPartAuto | interface | 12 | 23 |
| _IPartsAuto | interface | 4 | 3 |
| _IPathAuto | interface | 12 | 10 |
| _IPathRelation3dAuto | interface | 6 | 11 |
| _IPathsAuto | interface | 2 | 3 |
| _IPhysicalPropertiesAuto | interface | 9 | 9 |
| _IPipeAuto | interface | 9 | 7 |
| _IPipesAuto | interface | 2 | 3 |
| _IPlanarRelation3dAuto | interface | 10 | 19 |
| _IPointRelation3dAuto | interface | 10 | 16 |
| _IQueriesAuto | interface | 6 | 5 |
| _IQueryAuto | interface | 5 | 8 |
| _IRelations3dAuto | interface | 16 | 3 |
| _IRigidSetRelation3dAuto | interface | 8 | 12 |
| _ISegmentAngularRelation3dAuto | interface | 4 | 12 |
| _ISegmentDirectionRelation3dAuto | interface | 4 | 8 |
| _ISegmentDistanceRelation3dAuto | interface | 5 | 10 |
| _ISegmentPointRelation3dAuto | interface | 4 | 7 |
| _ISegmentRadiusRelation3dAuto | interface | 3 | 10 |
| _ISegmentRelations3dAuto | interface | 7 | 3 |
| _ISegmentTangentRelation3dAuto | interface | 4 | 7 |
| _ISegmentsAuto | interface | 1 | 3 |
| _ISimplifiedAssembliesAuto | interface | 1 | 5 |
| _ISimplifiedAssemblyAuto | interface | 5 | 6 |
| _ISpliceAuto | interface | 10 | 15 |
| _ISplicesAuto | interface | 2 | 4 |
| _IStructuralFrameAuto | interface | 35 | 9 |
| _IStructuralFramesAuto | interface | 9 | 3 |
| _ISubOccurrenceAuto | interface | 31 | 49 |
| _ISubOccurrencesAuto | interface | 1 | 3 |
| _ISubassemblyBodiesAuto | interface | 1 | 5 |
| _ISubassemblyBodyAuto | interface | 3 | 12 |
| _ISuppressComponentAuto | interface | 6 | 5 |
| _ITangentRelation3dAuto | interface | 10 | 16 |
| _ITopologyReferenceAuto | interface | 3 | 4 |
| _ITubeAuto | interface | 17 | 20 |
| _IVirtualComponentAuto | interface | 5 | 11 |
| _IVirtualComponentOccurrenceAuto | interface | 17 | 10 |
| _IVirtualComponentOccurrencesAuto | interface | 4 | 3 |
| _IWireAuto | interface | 12 | 26 |
| _IWirePathAuto | interface | 6 | 18 |
| _IWirePathCableMembersAuto | interface | 1 | 3 |
| _IWirePathSegmentsAuto | interface | 1 | 3 |
| _IWirePathsAuto | interface | 3 | 3 |
| _IWireRunAuto | interface | 7 | 6 |
| _IWireRunPathsAuto | interface | 1 | 3 |
| _IWireRunsAuto | interface | 3 | 3 |
| _IWiresAuto | interface | 2 | 4 |
| _IZoneAuto | interface | 11 | 4 |
| _IZonesAuto | interface | 9 | 3 |

---
## Program/constant.tlb
**Solid Edge Constants Type Library** (GUID: `{C467A6F5-27ED-11D2-BE30-080036B4D502}`, v1.0)

### Enums (745)

- **AcceleratorTypeConstants** [7]: seExecutable=1, seEmbeded=2, seServerInPlace=3, seContainerInPlace=4, seMainFrame=5, ... (7 total)
- **ActivatePartsOnFileOpenConstants** [2]: seActivatePartsOnFileOpenPrompt=0, seActivatePartsOnFileAutomatic=1
- **AddBodyTypeConstants** [7]: igPartType=1, igSheetMetalType=2, igSubdivisionType=3, igSubdivisionControlCageType=4, igConstructionPartType=5, ... (7 total)
- **AlignBodyFaceType** [6]: seAlignBodyFaceTypeFront=0, seAlignBodyFaceTypeBack=1, seAlignBodyFaceTypeTop=2, seAlignBodyFaceTypeBottom=3, seAlignBodyFaceTypeLeft=4, ... (6 total)
- **AlignBodyPointTypeOnFace** [9]: seAlignBodyPointTypeOnFaceLeftBottom=0, seAlignBodyPointTypeOnFaceLeftMiddle=1, seAlignBodyPointTypeOnFaceLeftTop=2, seAlignBodyPointTypeOnFaceCenterBottom=3, seAlignBodyPointTypeOnFaceCenterMiddle=4, ... (9 total)
- **AlternateAssemblyTypeConstants** [2]: seAlternateAssemblyType_Family=1, seAlternateAssemblyType_AlternatePosition=2
- **AnchorPointLocationConstants** [9]: igAnchorPointTopLeft=0, igAnchorPointTopCenter=1, igAnchorPointTopRight=2, igAnchorPointMiddleLeft=3, igAnchorPointMiddleCenter=4, ... (9 total)
- **AnglePrecisionConstants** [14]: igAnglePrecisionOnes=0, igAnglePrecisionTenths=1, igAnglePrecisionHundredths=2, igAnglePrecisionThousandths=3, igAnglePrecisionTenThousandths=4, ... (14 total)
- **AngularAccelerationPrecisionConstants** [8]: seAngularAccelerationPrecisionOnes=0, seAngularAccelerationPrecisionTenths=1, seAngularAccelerationPrecisionHundredths=2, seAngularAccelerationPrecisionThousandths=3, seAngularAccelerationPrecisionTenThousandths=4, ... (8 total)
- **AngularDimensionQuadrantConstants** [5]: igFirstQuadrant=0, igSecondQuadrant=1, igThirdQuadrant=2, igFourthQuadrant=3, igMajorQuadrant=4
- **AngularVelocityPrecisionConstants** [12]: seAngularVelocityPrecisionOnes=0, seAngularVelocityPrecisionTenths=1, seAngularVelocityPrecisionHundredths=2, seAngularVelocityPrecisionThousandths=3, seAngularVelocityPrecisionTenThousandths=4, ... (12 total)
- **AnimationEventConstants** [4]: BeforeTimelineFrameUpdate=1, AfterTimelineFrameUpdate=2, BeforeDragComponentFrameUpdate=3, AfterDragComponentFrameUpdate=4
- **ApplicationCommandConstants** [11]: ApplicationSoldEdgePortal=11675, ApplicationSoldEdgeFacebook=11793, ApplicationSoldEdgeCommunityBlog=11794, ApplicationSolidEdgeUserCommunity=11797, ApplicationTeamcenterUserCommunity=11798, ... (11 total)
- **ApplicationDisplayConstants** [5]: seAutomaticSelectionApplicationDisplay=0, seBackingStoreApplicationDisplay=1, seGraphicsCardDrivenApplicationDisplay=2, seSoftwareDrivenApplicationDisplay=3, seGraphicsCardDrivenAdvancedApplicationDisplay=4
- **ApplicationGlobalAntiAliasLevelConstants** [4]: seGlobalAntiAliasLevelUseViewStyle=0, seGlobalAntiAliasLevelLow=1, seGlobalAntiAliasLevelMedium=2, seGlobalAntiAliasLevelHigh=3
- **ApplicationGlobalAntiAliasStateConstants** [8]: seGlobalAntiAliasStateUseViewStyle=0, seGlobalAntiAliasStateLow=1, seGlobalAntiAliasStateMedium=2, seGlobalAntiAliasStateHigh=3, seGlobalAntiAliasStatePendingUseViewStyle=16, ... (8 total)
- **ApplicationGlobalConstants** [497]: seApplicationGlobalDisplayQuality=0, seApplicationGlobalDisplayArcQuality=1, seApplicationGlobalColorActive=2, seApplicationGlobalColorBackground=3, seApplicationGlobalColorConstruction=4, ... (497 total)
- **ApplicationGlobalFloorReflectionIntensityConstants** [4]: seGlobalFloorReflectionIntensity25=25, seGlobalFloorReflectionIntensity50=50, seGlobalFloorReflectionIntensity75=75, seGlobalFloorReflectionIntensity100=100
- **ArcSmoothnessConstants** [10]: seArcSmoothnessConstantsOne=6, seArcSmoothnessConstantsTwo=8, seArcSmoothnessConstantsThree=12, seArcSmoothnessConstantsFour=16, seArcSmoothnessConstantsFive=24, ... (10 total)
- **AreaPrecisionConstants** [14]: igAreaPrecisionOnes=0, igAreaPrecisionTenths=1, igAreaPrecisionHundredths=2, igAreaPrecisionThousandths=3, igAreaPrecisionTenThousandths=4, ... (14 total)
- **ArrangeWindowsStyles** [4]: igWindowsTiled=1, igWindowsHorizontal=2, igWindowsVertical=4, igWindowsCascade=8
- **AssemblyBaseStylesConstants** [6]: seAssemblyBaseStyle=0, seAssemblyConstructionStyle=1, seAssemblyThreadedCylindersStyle=2, seAssemblyCurveStyle=3, seAssemblyWeldBeadStyle=4, ... (6 total)
- **AssemblyChangeEventsConstants** [12]: seAssemblyOccurrenceRename=1, seAssemblyFeatureRename=2, seAssemblyComponentShow=3, seAssemblyComponentHide=4, seAssemblyOccurrenceAdd=5, ... (12 total)
- **AssemblyCommandConstants** [132]: AssemblyEnvironmentsExit=10231, AssemblyFenceSelectParts=10281, AssemblySelectAllIdenticalParts=10282, AssemblySelectAllIdenticalSubassemblyParts=10283, AssemblySelectSmallParts=10284, ... (132 total)
- **AssemblyComponentTypeConstants** [7]: seAssemblyComponentTypeAll=0, seAssemblyComponentTypeReference=1, seAssemblyComponentTypeFramePart=2, seAssemblyComponentTypeEndCapPart=3, seAssemblyComponentTypePatterns=4, ... (7 total)
- **AssemblyCopyActionConstants** [6]: seAssemblyCopyActionInclude=0, seAssemblyCopyActionExclude=1, seAssemblyCopyActionPending=2, seAssemblyCopyActionMirror=3, seAssemblyCopyActionRotate=4, ... (6 total)
- **AssemblyCopyComponentConstants** [4]: seAssemblyCopyComponentsIncludeAll=0, seAssemblyCopyComponentsExcludeAll=1, seAssemblyCopyComponentsIncludeSpecified=2, seAssemblyCopyComponentsExcludeSpecified=3
- **AssemblyCopyPlaneConstants** [7]: seAssemblyPlaneXY=0, seAssemblyPlaneYZ=1, seAssemblyPlaneZX=2, seAssemblyPlanePrinciple1=3, seAssemblyPlanePrinciple2=4, ... (7 total)
- **AssemblyCopyStatusConstants** [7]: seAssemblyCopyStatusOK=0, seAssemblyCopyStatusOutOfDate=1, seAssemblyCopyStatusFrozen=2, seAssemblyCopyStatusPending=3, seAssemblyCopyStatusMirrorPlaneMissing=4, ... (7 total)
- **AssemblyCopyTypeConstants** [3]: seAssemblyCopyTypeDefault=0, seAssemblyCopyTypeMirror=1, seAssemblyCopyTypeMultiBodyPart=2
- **AssemblyCopyUserConstants** [2]: seAssemblyCopyDefault=0, seAssemblyCopyUserDefined=1
- **AssemblyDrawingViewTypeConstants** [3]: seAssemblyDesignedView=0, seAssemblySimplifiedView=1, seAssemblyConfigurationSimplifiedView=2
- **AssemblyEventConstants** [1]: seAssemblyOccurrenceReplace=1
- **AssemblyFaceStyleOverrideConstants** [3]: UseNoneStyle=0, UsePartStyle=1, UseValidStyle=2
- **AssemblyFamilyMemberPropertyConstants** [3]: seAssemblyFamilyMemberPropertyDocumentNumber=0, seAssemblyFamilyMemberPropertyRevisionNumber=1, seAssemblyFamilyMemberPropertyProjectName=2
- **AssemblyFamilyMemberStatusConstants** [3]: seAssemblyFamilyMemberStatusUpToDate=0, seAssemblyFamilyMemberStatusNotPopulated=1, seAssemblyFamilyMemberStatusPopulatedAndOutOfDate=2
- **AssemblyFeaturePresenceConstants** [3]: AssemblyFeaturePresence_None=0, AssemblyFeaturePresence_Legacy=1, AssemblyFeaturePresence_Enhanced=2
- **AssemblyFileOpenActivateChangedPartOptions** [3]: seAssemblyFileOpenActivateChangedPart_Prompt=0, seAssemblyFileOpenActivateChangedPart_Activate=1, seAssemblyFileOpenActivateChangedPart_Inactivate=1
- **AssemblyFileOpenPartActivationOptions** [3]: seAssemblyFileOpenPartActivation_ActivateAll=0, seAssemblyFileOpenPartActivation_InactivateAll=1, seAssemblyFileOpenPartActivation_LastSaved=2
- **AssemblyFileOpenSimplificationOptions** [3]: seAssemblyFileOpenSimplification_AllSimplified=0, seAssemblyFileOpenSimplification_AllDesigned=1, seAssemblyFileOpenSimplification_LastSaved=2
- **AssemblyGlobalConstants** [21]: seAssemblyGlobalTubeWallThickness=1, seAssemblyGlobalTubeBendRadius=2, seAssemblyGlobalTubeOuterDiameter=3, seAssemblyGlobalTubeMinimumFlatLength=4, seAssemblyGlobalTubeEndTreatmentOutsideDiameter=5, ... (21 total)
- **AssemblyOpenModeConstants** [8]: seAssemblyOpenModeAutoSelect=0, seAssemblyOpenModeSmall=1, seAssemblyOpenModeMedium=2, seAssemblyOpenModeLarge=3, seAssemblyOpenModeLastSaved=4, ... (8 total)
- **AssemblyPathfinderUpdateConstants** [6]: seUpdate=1, seRebuild=2, seSuspend=3, seResume=4, seExpandAll=5, ... (6 total)
- **AssemblyPatternTypeConstants** [3]: seAssemblyPatternType=1, seAssemblyDuplicatePatternType=2, seAssemblyPatternAlongCurveType=3
- **AssemblyReportConstants** [6]: seAssemblyReportWirePathName=1, seAssemblyReportWirePathType=2, seAssemblyReportWirePathDescription=4, seAssemblyReportWirePathStartConnector=8, seAssemblyReportWirePathEndConnector=16, ... (6 total)
- **AssemblyReportTypeConstants** [2]: seAssemblyWireReportAtomic=0, seAssemblyWireReportExpanded=1
- **AssemblyWeldmentOccurrencesOptionsConstants** [3]: seIncludeAllOccurrences=1, seIncludeInputOccurrences=2, seExcludeInputOccurrences=3
- **AssemblyWireHarnessBOMPropertiesConstants** [20]: seWireHarnessBOMPropertyAuthor=1, seWireHarnessBOMPropertyFileName=2, seWireHarnessBOMPropertyDocNameFormula=3, seWireHarnessBOMPropertyKeywords=4, seWireHarnessBOMPropertyComments=5, ... (20 total)
- **AssemblyWireHarnessComponentPropertiesConstants** [16]: seWireHarnessComponentPropertyAuthor=1, seWireHarnessComponentPropertyFileName=2, seWireHarnessComponentPropertyKeywords=3, seWireHarnessComponentPropertyComments=4, seWireHarnessComponentPropertyTemplate=5, ... (16 total)
- **AssemblyWireHarnessConnectionPropertiesConstants** [15]: seWireHarnessConnectionPropertyWireId=1, seWireHarnessConnectionPropertyFromComponentId=2, seWireHarnessConnectionPropertyFromComponentTerminal=3, seWireHarnessConnectionPropertyToComponentId=4, seWireHarnessConnectionPropertyToComponentTerminal=5, ... (15 total)
- **AssemblyWireHarnessJustificationConstants** [3]: seWireHarnessReportLeft=1, seWireHarnessReportCenter=2, seWireHarnessReportRight=3
- **AssemblyWireHarnessReportOnConstants** [3]: seAssemblyWireHarnessReportOnAll=1, seAssemblyWireHarnessReportOnCurrentlySelected=2, seAssemblyWireHarnessReportOnCurrentlyVisible=3
- **AssemblyWireHarnessReportTypeConstants** [3]: seAssemblyWireHarnessReportComponents=1, seAssemblyWireHarnessReportConnections=2, seAssemblyWireHarnessReportHBom=3
- **AssemblyWireHarnessSortOrderConstants** [2]: seWireHarnessReportAscending=1, seWireHarnessReportDescending=2
- **AttachedStatusConstants** [8]: seStatusOK=0, seStatusMissingPropertyObject=1, seStatusMissingPropertyTable=2, seStatusMissingAttachedEntites=3, seStatusDuplicateProperties=4, ... (8 total)
- **AttributeTypeConstants** [11]: seInteger=2, seLong=3, seSingle=4, seDouble=5, seCurrency=6, ... (11 total)
- **AutoConstrainDimPlacementOptionConstants** [3]: seAutoConstrainDimChain=0, seAutoConstrainDimCoordinate=1, seAutoConstrainDimStack=2
- **AutoConstrainLinearDimOptionConstants** [3]: seAutoConstrainLinearDimDistanceBetween=0, seAutoConstrainLinearDimLineLength=1, seAutoConstrainLinearDimAll=2
- **AutoExplodeSelectionTypeConstants** [2]: seTopLevelAssembly=0, seSubassembly=1
- **AutoExplodeTechniqueConstants** [2]: seBySubassemblyLevel=0, seByIndividualPart=1
- **AutoSharpenConstants** [4]: seAutoSharpenConstantsOff=0, seAutoSharpenConstantsLow=1, seAutoSharpenConstantsStandard=2, seAutoSharpenConstantsHigh=3
- **BendCalculationMethodConstants** [3]: BendCalculationMethodNeutralFactor=0, BendCalculationMethodBendDeduction=1, BendCalculationMethodBendAllowance=2
- **BendDirectionConstants** [3]: seBendDirectionUnknown=0, seBendDirectionUp=1, seBendDirectionDown=2
- **BendFeatureConstants** [20]: seBendOnlyCornerRelief=1, seBendAndFaceCornerRelief=2, seBendExtendMoldlines=3, seBendNoExtendMoldines=4, seBendMoveRight=5, ... (20 total)
- **BlendShapeConstants** [6]: igBlendShapeConstantRadius=1, igBlendShapeConstantWidth=2, igBlendShapeChamfer=3, igBlendShapeRatioChamfer=4, igBlendShapeConic=5, ... (6 total)
- **BlockLabelOriginLocationConstants** [12]: igBlockLabelTopLeft=0, igBlockLabelTopCenter=1, igBlockLabelTopRight=2, igBlockLabelMiddleLeft=3, igBlockLabelMiddleCenter=4, ... (12 total)
- **BlockTableType** [2]: igBlockOnlyList=0, igBlockViewList=1
- **BooleanFeatureConstants** [5]: seBooleanIntersect=1, seBooleanSubtract=2, seBooleanUnite=3, seBooleanPlaneFront=4, seBooleanPlaneBack=5
- **Boundary2dStateConstants** [3]: igBoundary2dUndefined=0, igBoundary2dUpToDate=1, igBoundary2dUnableToCompute=2
- **BreakLinePairDirConstants** [2]: igBreakLinePairDirConstants_Vertical=0, igBreakLinePairDirConstants_Horizontal=1
- **BreakLinePairOrientConstants** [2]: igBreakLinePairOrientConstants_Default=0, igBreakLinePairOrientConstants_Explicit=1
- **BreakLinePairTypeConstants** [5]: igBreakLinePairTypeConstants_Straight=0, igBreakLinePairTypeConstants_Cylindrical=1, igBreakLinePairTypeConstants_ShortBreak=2, igBreakLinePairTypeConstants_LongBreak=3, igBreakLinePairTypeConstants_ShortCurvedBreak=4
- **BulkMigrationTypeConstants** [6]: igNoBulkMigration=0, igTDMBulkMigration=1, igProEBulkMigration=2, igNX2DBulkMigration=3, igMDTBulkMigration=4, ... (6 total)
- **CageOffsetTypes** [2]: CageOffsetTypeTip=1, CageOffsetTypeLift=2
- **CapturedRelationshipOffsetTypeConstants** [3]: seFixed=0, seFloating=1, seOffsetNotSupported=2
- **CapturedRelationshipTypeConstants** [6]: seMate=0, sePlanarAlign=1, seAxialAlign=2, seTangent=3, seConnect=4, ... (6 total)
- **ChangedPartActivationOption** [3]: seChangedPartActivationOptionActive=1, seChangedPartActivationOptionInactive=2, seChangedPartActivationOptionPrompt=3
- **CheckInOptions** [2]: DoNotCheckInOption=0, UploadAndCheckInOption=1
- **CleanProfileOptions** [2]: igCleanProfileDelete=1, igCleanProfileMove=2
- **CloneComponentOptions** [3]: seRepairUnsatisfiedRelationships=0, seDoNotCreateRelationships=2, seCreateGroundRelationships=3
- **CloneMatchTypeOptions** [2]: CloneMatchTypeAutomatic=0, CloneMatchTypeExact=1
- **CloseCornerFeatureConstants** [9]: seCloseCornerCloseFaces=1, seCloseCornerOverlapFaces=2, seCloseCornerTreatmentOff=3, seCloseCornerTreatmentIntersect=4, seCloseCornerTreatmentCircularCutout=5, ... (9 total)
- **CoefOfThermalExpansionPrecisionConstants** [8]: seCoefOfThermalExpansionPrecisionOnes=0, seCoefOfThermalExpansionPrecisionTenths=1, seCoefOfThermalExpansionPrecisionHundredths=2, seCoefOfThermalExpansionPrecisionThousandths=3, seCoefOfThermalExpansionPrecisionTenThousandths=4, ... (8 total)
- **ColorConstants** [16]: seColorBlack=0, seColorDarkRed=128, seColorRed=255, seColorDarkGreen=32768, seColorDarkYellow=32896, ... (16 total)
- **ColorSchemeConstants** [4]: seColorSchemeConstantsAqua=0, seColorSchemeConstantsBlac=1, seColorSchemeConstantsBlue=2, seColorSchemeConstantsSilver=3
- **CommandUserInterfaceConstants** [2]: CommandUserInterfaceVertical=0, CommandUserInterfaceHorizontal=1
- **ComponentImageCreationModeConstants** [2]: seAllVisible=0, seExplicit=1
- **ConfigForForeignFileType** [1]: seAutoCADConfigFile=1067709598
- **ConfigResetType** [2]: seResetGroup=-1957181463, seResetAll=-1801520595
- **ConfigurationTypeConstants** [2]: seConfigurationType_Display=0, seConfigurationType_Explode=1
- **ConnectorTypeConstants** [5]: seLineConnector=0, seJumpConnector=1, seCornerConnector=2, seStepConnector=3, seGapConnector=4
- **ConstraintReplacementConstants** [3]: seConstraintReplacementNone=0, seConstraintReplacementSuppress=1, seConstraintReplacementDelete=2
- **ConstraintTypeConstants** [8]: igRelationConcentric=1, igRelationCoincident=2, igRelationParallel=3, igRelationPerpendicular=4, igRelationTangent=5, ... (8 total)
- **CookieDataToGet** [1]: GET_REVISION_RULE=0
- **CoordinateSystem2dAxisConstants** [2]: seCoordinateSystem2dAxisLow=0, seCoordinateSystem2dAxisHigh=1
- **CoordinateSystemFeatureConstants** [6]: seCoordSysXAxis=1, seCoordSysYAxis=2, seCoordSysZAxis=3, seCoordSysXYPlane=4, seCoordSysYZPlane=5, ... (6 total)
- **CoordinateSystemOffsetTypeConstants** [2]: seCoordSysOffsetGlobal=1, seCoordSysOffsetRelative=2
- **CoordinateSystemRotationTypeConstants** [2]: seCoordSysRotateAboutSelf=1, seCoordSysRotateAboutParent=2
- **CoordinateSystemTypeConstants** [3]: seCoordSysGeometryBased=1, seCoordSysNonGeometryBased=2, seCoordSysNonGeometricRelativeTo=3
- **CopySketchErrorStatusConstants** [10]: seCopySketchErrorStatus_success_no_error=0, seCopySketchErrorStatus_failure_unknown_error=1, seCopySketchErrorStatus_warning_profile_text_not_copied=2, seCopySketchErrorStatus_failure_no_valid_elements_copied=3, seCopySketchErrorStatus_failure_checkout_for_writeaccess=4, ... (10 total)
- **CopySurfaceExternalBoundaryConstants** [2]: igCopySurfaceRemoveExternalBoundaries=1, igCopySurfaceCopyExternalBoundaries=2
- **CopySurfaceInternalBoundaryConstants** [2]: igCopySurfaceRemoveInternalBoundaries=1, igCopySurfaceCopyInternalBoundaries=2
- **CurveFitTypeConstants** [3]: igLinestringFit=0, igDirectFit=1, igLeastSquareFit=2
- **CurveSegmentPathAdditionStatusConstants** [9]: seCurveSegmentPathAdditionStatusSucceeded=0, seCurveSegmentPathAdditionStatusFailedUnknownReason=1, seCurveSegmentPathAdditionStatusFailedBreak=2, seCurveSegmentPathAdditionStatusFailedDuplicate=3, seCurveSegmentPathAdditionStatusFailedFork=4, ... (9 total)
- **CurveSegmentPathRemovalStatusConstants** [6]: seCurveSegmentPathRemovalStatusSucceeded=0, seCurveSegmentPathRemovalStatusFailedUnknownReason=1, seCurveSegmentPathRemovalStatusFailedBreak=2, seCurveSegmentPathRemovalStatusFailedNotInPath=3, seCurveSegmentPathRemovalStatusFailedSingle=4, ... (6 total)
- **CurveSegmentValidationConstants** [15]: seCurveSegmentValidation_valid=0, seCurveSegmentValidation_break=1, seCurveSegmentValidation_angle=2, seCurveSegmentValidation_length=4, seCurveSegmentValidation_intersection=8, ... (15 total)
- **CurveSegmentWhichKeypointsConstants** [3]: seCurveSegmentWhichKeypoints_mid_points=1, seCurveSegmentWhichKeypoints_end_points=2, seCurveSegmentWhichKeypoints_all_points=3
- **CuttingPlaneLineCommandConstants** [33]: CuttingPlaneLineEditUndoList=10112, CuttingPlaneLineEditRedoList=10113, CuttingPlaneLineViewPreviousView=10200, CuttingPlaneLineViewZoomArea=10201, CuttingPlaneLineViewFit=10202, ... (33 total)
- **CuttingPlaneLineDisplayStyleConstants** [3]: seThick=1, seThickCornersOnly=2, seThickThin=3
- **DVThreadDisplayModeConstants** [5]: seDVThreadDisplayModeANSI=0, seDVThreadDisplayModeISO=1, seDVThreadDisplayModeJIS=2, seDVThreadDisplayModeJISISO=3, seDVThreadDisplayModeESKD=4
- **DecalMappingType** [2]: seLabel=1, sePlanarProjection=2
- **DeleteFaceConstants** [2]: igDeleteFaceApplyHeal=1, igDeleteFaceApplyNoHeal=2
- **DeleteTopologyHealConstants** [1]: seDeleteTopologyNoHeal=0
- **DeleteTopologyOptionsConstants** [2]: seDeleteTopologyNoOptions=0, seDeleteTopologyIncludeFirstLevelBlendFaces=1
- **DensityPrecisionConstants** [12]: igDensityPrecisionOnes=0, igDensityPrecisionTenths=1, igDensityPrecisionHundredths=2, igDensityPrecisionThousandths=3, igDensityPrecisionTenThousandths=4, ... (12 total)
- **DerivedCurveTypeConstants** [2]: igDCComposite=1, igDCCurve=2
- **DetailCommandConstants** [157]: DetailFileSheetSetup=10002, DetailViewDeleteSheet=10106, DetailEditGoToSheet=10107, DetailEditProperties=10108, DetailEditCopytoSymbolLibrary=10114, ... (157 total)
- **DetailEnvelopConstants** [3]: seDetailEnvelopConstantsANSI=0, seDetailEnvelopConstantsISO=1, seDetailEnvelopConstantsESKD=2
- **DetailEnvelopeStandardConstants** [3]: seDetailEnvelopeANSI=0, seDetailEnvelopeISO=1, seDetailEnvelopeESKD=2
- **DimAngularCoordnateOrientationConstants** [2]: igDimAngCoordOrientClockwise=0, igDimAngCoordOrientCounterClockwise=1
- **DimAngularUnitConstants** [3]: igDimStyleAngularDegMinSec=1, igDimStyleAngularRadians=2, igDimStyleAngularDegrees=3
- **DimAxisModeConstants** [4]: igDimAxisModeDefault=1, igDimAxisModeImplied=2, igDimAxisModeExplicit=3, igDimAxisModeCoordinate=4
- **DimBalloonDirTypeConstants** [4]: igDimBalloonDirectionLeft=1, igDimBalloonDirectionRight=2, igDimBalloonDirectionTop=3, igDimBalloonDirectionBottom=4
- **DimBalloonTypeConstants** [14]: igDimBalloonNone=0, igDimBalloonCircle=1, igDimBalloonNSided=2, igDimBalloonSquare=3, igDimBalloonSquareRotated=4, ... (14 total)
- **DimBreakPositionConstants** [4]: igDimBreakRight=1, igDimBreakCenter=2, igDimBreakLeft=3, igDimBreakAltCenter=4
- **DimCalloutBalloonBreaklineDirectionConstants** [4]: igDimCalloutBalloonBreaklineDirectionWest=0, igDimCalloutBalloonBreaklineDirectionNorth=1, igDimCalloutBalloonBreaklineDirectionEast=2, igDimCalloutBalloonBreaklineDirectionSouth=3
- **DimCalloutLeaderTextConnectionPointConstants** [10]: igDimCalloutLeaderTextConnectionPointDefaultLeft=0, igDimCalloutLeaderTextConnectionPointTopLeft=1, igDimCalloutLeaderTextConnectionPointTopCenter=2, igDimCalloutLeaderTextConnectionPointTopRight=3, igDimCalloutLeaderTextConnectionPointDefaultRight=4, ... (10 total)
- **DimCalloutTextWidthModeConstants** [3]: igDimCalloutFitToContent=1, igDimCalloutFixedAutoAspectRatio=2, igDimCalloutFixedWrapText=3
- **DimCenterlineTypeConstants** [4]: igDimCenterlineNormal=1, igDimCenterlineMidway=2, igDimCenterArcByCenterPoint=3, igDimCenterArcBy2Arcs=4
- **DimChamferModeConstants** [4]: igDimChamferModeAlongAxis=0, igDimChamferModePerpendicular=1, igDimChamferModeParallel=2, igDimChamferModeNotApplicable=3
- **DimCommonOriginTypeConstants** [3]: igDimStyleCommonOrigNone=6, igDimStyleCommonOrigDot=7, igDimStyleCommonOrigCircle=8
- **DimCoordTextPositionConstants** [2]: igDimStyleCoordTextAbove=1, igDimStyleCoordTextInLine=2
- **DimDMSRoundOffTypeConstants** [6]: igDimStyleAngular10Degree=1, igDimStyleAngular1Degree=2, igDimStyleAngular10Minute=3, igDimStyleAngular1Minute=4, igDimStyleAngular10Second=5, ... (6 total)
- **DimDatumPointTypeConstants** [3]: igDimDatumPointCross=1, igDimDatumPointCircle=2, igDimDatumPointRectangle=3
- **DimDatumTargetLeaderTypeConstants** [2]: igDimDatumTargetNearSide=1, igDimDatumTargetFarSide=2
- **DimDatumTargetTermTypeConstants** [4]: igDimStyleDatumTargetTermHollow=1, igDimStyleDatumTargetTermFilled=2, igDimStyleDatumTargetTermOpen=3, igDimStyleDatumTargetTermBlank=4
- **DimDatumTargetTypeConstants** [3]: igDimDatumTargetRegular=1, igDimDatumTargetMovable=2, igDimDatumTargetAlignedMovable=3
- **DimDatumTermTypeConstants** [4]: igDimStyleDatumTermNormal=1, igDimStyleDatumTermAnchor=2, igDimStyleDatumTermLine=3, igDimStyleDatumTermAnchorHollow=4
- **DimDecimalRoundOffTypeConstants** [9]: igDimStyleDecimal10=1, igDimStyleDecimal1=2, igDimStyleDecimal_1=3, igDimStyleDecimal_2=4, igDimStyleDecimal_3=5, ... (9 total)
- **DimDelimiterTypeConstants** [3]: igDimStyleDelimiterDot=1, igDimStyleDelimiterComma=2, igDimStyleDelimiterSpace=3
- **DimDispTypeConstants** [14]: igDimDisplayTypeNominal=1, igDimDisplayTypeTolerance=2, igDimDisplayTypeClassfit=3, igDimDisplayTypeLimits=4, igDimDisplayTypeBasic=5, ... (14 total)
- **DimDualUnitPositionConstants** [2]: igDimStyleDualUnitPositionAsBelowPrimary=1, igDimStyleDualUnitPositionAsBesidePrimary=2
- **DimFCFGeometrySymbolTypeConstants** [14]: igDimGeomSymFlatness=1, igDimGeomSymStraightness=2, igDimGeomSymCircularity=3, igDimGeomSymCylindricity=4, igDimGeomSymPerpendicularity=5, ... (14 total)
- **DimFCFLeaderTextConnectionPointConstants** [9]: igDimFCFLeaderTextConnectionPointCenter=0, igDimFCFLeaderTextConnectionPointMiddleLeft=1, igDimFCFLeaderTextConnectionPointTopLeft=2, igDimFCFLeaderTextConnectionPointTopMiddle=3, igDimFCFLeaderTextConnectionPointTopRight=4, ... (9 total)
- **DimFCFMaterialConditionTypeConstants** [5]: igDimMaterialConditionNone=0, igDimMaterialConditionMaximum=2, igDimMaterialConditionRegular=3, igDimMaterialConditionLeast=4, igDimMaterialConditionReciprocity=5
- **DimFCFOrientationConstants** [4]: igDimFCFOrientationVertical=0, igDimFCFOrientationHorizontal=1, igDimFCFOrientationPerpendicular=2, igDimFCFOrientationParallel=3
- **DimFractionRoundOffTypeConstants** [7]: igDimStyleFraction_1=1, igDimStyleFraction_2=2, igDimStyleFraction_4=3, igDimStyleFraction_8=4, igDimStyleFraction_16=5, ... (7 total)
- **DimGostWeldPermanentJointTypeConstants** [5]: igDimGostWeldPermJointAdhesive=0, igDimGostWeldPermJointSolder=1, igDimGostWeldPermJointStitch=2, igDimGostWeldPermJointBracket=3, igDimGostWeldPermJointAngled=4
- **DimGostWeldTerminatorTypeConstants** [3]: igDimGostWeldTerminatorSameSide=0, igDimGostWeldTerminatorOtherSide=1, igDimGostWeldTerminatorFullArrow=2
- **DimGroupMemberTypeConstants** [4]: seDimNotAGroupMember=1, seDimStackGroupMember=2, seDimChainGroupMember=3, seDimCoordinateGroupMember=4
- **DimHoleShaftSeparatorTypeConstants** [3]: igDimStyleShowHoleShaftSeparatorTypeAsSlash=1, igDimStyleShowHoleShaftSeparatorTypeAsSeparator=2, igDimStyleShowHoleShaftSeparatorTypeAsSpace=3
- **DimItemNumDirConstants** [3]: igDimItemNumberDirectionNone=0, igDimItemNumberDirectionClockwise=1, igDimItemNumberDirectionCounterClockwise=2
- **DimLimitTextArrangmentConstants** [2]: igDimStyleLimitTextHorizontal=1, igDimStyleLimitTextVertical=2
- **DimLineDisplayTypeConstants** [4]: igDimStyleDimLineNone=0, igDimStyleDimLineOrig=1, igDimStyleDimLineMeas=2, igDimStyleDimLineBoth=3
- **DimLinearUnitConstants** [6]: igDimStyleLinearFtIn=1, igDimStyleLinearMeters=2, igDimStyleLinearMM=3, igDimStyleLinearCM=4, igDimStyleLinearInches=5, ... (6 total)
- **DimNTSTypeConstants** [3]: igDimStyleNTSNone=1, igDimStyleNTSUnderline=2, igDimStyleNTSZigzag=3
- **DimOffsetLeaderTypeConstants** [1]: igDimStyleOffsetLeaderLine=1
- **DimProjArcConstants** [3]: igDimProjArcNone=1, igDimProjArcStart=2, igDimProjArcEnd=3
- **DimProjDisplayTypeConstants** [4]: igDimStyleProjLineNone=0, igDimStyleProjLineOrig=1, igDimStyleProjLineMeas=2, igDimStyleProjLineBoth=3
- **DimProjTolZonePositionConstants** [2]: igDimStyleProjTolZoneInLine=1, igDimStyleProjTolZoneBelow=2
- **DimReattachStatusConstants** [2]: igDimReattachSucceeded=0, igDimReattachFailed=1
- **DimRoundOffTypeConstants** [2]: igDimStyleDecimal=1, igDimStyleFraction=2
- **DimRoundUpTypeConstants** [2]: igDimStyleRoundUpAll=1, igDimStyleRoundUpOdd=2
- **DimScaleModeConstants** [2]: igDimStyleScaleManual=0, igDimStyleScaleAutomatic=1
- **DimStackFractionSizeConstants** [8]: igDimStyleFractSize50=1, igDimStyleFractSize60=2, igDimStyleFractSize66=3, igDimStyleFractSize70=4, igDimStyleFractSize75=5, ... (8 total)
- **DimStackFractionTypeConstants** [3]: igDimStyleFractionStacked=1, igDimStyleFractionSkewed=2, igDimStyleFractionLinear=3
- **DimStatusConstants** [6]: seDimStatusDetached=1, seDimStatusError=2, seDimStatusDriving=3, seDimStatusDriven=4, seOneEndDetached=5, ... (6 total)
- **DimStyleDatumFrameShapeConstants** [2]: igDimStyleDatumFrameShapeRectangle=1, igDimStyleDatumFrameShapeCircle=2
- **DimStyleSecondaryUnitSeparatorConstants** [3]: igDimStyleSecondaryUnitSeparatorNothing=0, igDimStyleSecondaryUnitSeparatorParenthesis=1, igDimStyleSecondaryUnitSeparatorBrackets=2
- **DimStyleSymbolFontConstants** [2]: igDimStyleSymbolFontANSI=1, igDimStyleSymbolFontISO=2
- **DimSurfTextureLaySymTypeConstants** [9]: igDimSurfaceFinishLayNone=1, igDimSurfaceFinishLayPerpendicular=2, igDimSurfaceFinishLayVtParallel=3, igDimSurfaceFinishLayHzParallel=4, igDimSurfaceFinishLayCrossed=5, ... (9 total)
- **DimSurfTextureSymTypeConstants** [23]: igDimSurfaceFinishBasic=1, igDimSurfaceFinishMachined=2, igDimSurfaceFinishNoMaterialRemoval=3, igDimSurfaceFinishBasicHz=4, igDimSurfaceFinishMachinedHz=5, ... (23 total)
- **DimSymbolPositionConstants** [3]: igDimStyleSymbolNone=1, igDimStyleSymbolBefore=2, igDimStyleSymbolAfter=3
- **DimTermDisplayTypeConstants** [4]: igDimStyleTermNone=0, igDimStyleTermOrig=1, igDimStyleTermMeas=2, igDimStyleTermBoth=3
- **DimTermTypeConstants** [16]: igDimStyleTermHollow=1, igDimStyleTermFilled=2, igDimStyleTermOpen=3, igDimStyleTermSlash=4, igDimStyleTermBackSlash=5, ... (16 total)
- **DimTextFontStyleConstants** [4]: igDimStyleFontNormal=1, igDimStyleFontBold=2, igDimStyleFontItalic=3, igDimStyleFontItalicBold=4
- **DimTextOrientationConstants** [4]: igDimStyleTextHorizontal=1, igDimStyleTextVertical=2, igDimStyleTextParallel=3, igDimStyleTextPerpendicular=4
- **DimTextPositionConstants** [2]: igDimStyleTextAbove=1, igDimStyleTextEmbedded=2
- **DimToleranceTextHorizontalAlignOptionsConstants** [2]: igDimStyleToleranceTextHorizontalAlignBySign=1, igDimStyleToleranceTextHorizontalAlignByDecimalPoint=2
- **DimToleranceZoneTypeConstants** [6]: igDimToleranceZoneNone=0, igDimToleranceZoneProjected=1, igDimToleranceZoneTangentPlane=2, igDimToleranceZoneFreeState=3, igDimToleranceZoneEnvelope=4, ... (6 total)
- **DimTypeConstants** [12]: igDimTypeLinear=1, igDimTypeRadial=2, igDimTypeAngular=3, igDimTypeRDiameter=4, igDimTypeCDiameter=5, ... (12 total)
- **DimViewCPLCaptionLocationConstants** [4]: igDimViewCPLCaptionLocationFrom=1, igDimViewCPLCaptionLocationOn=2, igDimViewCPLCaptionLocationTo=3, igDimViewCPLCaptionLocationOutsideOpenEnd=4
- **DimViewCaptionLocationConstants** [2]: igDimViewCaptionLocationTop=1, igDimViewCaptionLocationBottom=2
- **DimViewCuttingPlaneDisplayTypeConstants** [2]: igDimViewCuttingPlaneLineDisplayTo=1, igDimViewCuttingPlaneLineDisplayFrom=2
- **DimViewPlaneDisplayTypeConstants** [2]: igDimViewPlaneLineDisplaySingle=1, igDimViewPlaneLineDisplayDouble=2
- **DimWeldBeadWeldImportConstants** [3]: igDimWeldBeadWeldImportUnknown=0, igDimWeldBeadWeldImportLocal=1, igDimWeldBeadWeldImportImported=2
- **DimWeldBeadWeldStandardConstants** [4]: igDimWeldBeadWeldStandardUnknown=0, igDimWeldBeadWeldStandardANSI=1, igDimWeldBeadWeldStandardISO=2, igDimWeldBeadWeldStandardDIN=3
- **DimWeldBeadWeldTypeConstants** [3]: igDimWeldBeadWeldTypeUnknown=0, igDimWeldBeadWeldTypeContinuous=1, igDimWeldBeadWeldTypeStitch=2
- **DimWeldBeadWeldmentShapeConstants** [4]: igDimWeldBeadWeldmentShapeUnknown=0, igDimWeldBeadWeldmentShapeFill=1, igDimWeldBeadWeldmentShapeConcave=2, igDimWeldBeadWeldmentShapeConvex=3
- **DimWeldBeadWeldmentTypeConstants** [4]: igDimWeldBeadWeldmentTypeUnknown=0, igDimWeldBeadWeldmentTypeFillet=1, igDimWeldBeadWeldmentTypeFill=2, igDimWeldBeadWeldmentTypeLabel=3
- **DimWeldDashLineTypeConstants** [3]: igDimWeldDashLineNone=0, igDimWeldDashLineAbove=1, igDimWeldDashLineBelow=2
- **DimWeldLabelImportConstants** [3]: igDimWeldLabelImportUnknown=0, igDimWeldLabelLocal=1, igDimWeldLabelImported=2
- **DimWeldModifierConstants** [3]: igDimWeldModifierNone=0, igDimWeldTopThreeSided=1, igDimWeldBottomThreeSided=2
- **DimWeldTailTypeConstants** [3]: igDimWeldTailNone=0, igDimWeldTailOpen=1, igDimWeldTailClosed=2
- **DimWeldTreatmentTypeConstants** [7]: igDimWeldTreatmentNone=0, igDimWeldTreatmentFlush=1, igDimWeldTreatmentConcave=2, igDimWeldTreatmentConvex=3, igDimWeldTreatmentSmoothBlend=4, ... (7 total)
- **DimWeldTypeConstants** [84]: igDimWeldTypeNone=0, igDimWeldTopFillet=1, igDimWeldTopSpot=2, igDimWeldTopSeam=3, igDimWeldTopBevel=4, ... (84 total)
- **DimensionOrientationConstants** [2]: igOrientationHorizontal=0, igOrientationVertical=1
- **DimensionTrackerReasonCode** [10]: igDTRC_Unknown=0, igDTRC_ValueChanged=1, igDTRC_TerminatorMoved=2, igDTRC_DetachedRebindFailure=3, igDTRC_DetachedNoEdgeInformation=4, ... (10 total)
- **DimpleFeatureConstants** [12]: seDimpleDepthLeft=1, seDimpleDepthRight=2, seDimpleDimensionOffset=3, seDimpleDimensionFull=4, seDimpleProfileLeft=5, ... (12 total)
- **DisableBuilInDataMgmt** [1]: DisableBuilInDM=0
- **DisplayArcQualityConstants** [13]: seMinimumDisplayArcQuality=1, seDisplayArcQualityOne=1, seDisplayArcQualityTwo=2, seDefaultDisplayArcQuality=3, seDisplayArcQualityThree=3, ... (13 total)
- **DisplayQualityConstants** [2]: seMinimumDisplayQuality=0, seMaximumDisplayQuality=48
- **DisplayTypeConstant** [3]: igNotSpecifiedDisplay=-1, igContentsDisplay=0, igIconDisplay=1
- **DisplayTypeConstants** [3]: igDisplayTypeContents=1, igDisplayTypeIcon=2, igDisplayTypeThumbnail=3
- **DistancePrecisionConstants** [14]: igDistancePrecisionOnes=0, igDistancePrecisionTenths=1, igDistancePrecisionHundredths=2, igDistancePrecisionThousandths=3, igDistancePrecisionTenThousandths=4, ... (14 total)
- **DividedPartCutDirectionConstants** [2]: seDividedPartCutNormal=0, seDividedPartCutReverseNormal=1
- **DividedPartStatusConstants** [4]: seDividedPartStatusNotCreated=0, seDividedStatusUpToDate=1, seDividedStatusOutOfDate=2, seDividedStatusLinkBroken=3
- **DocumentAccess** [3]: igReadWrite=0, igReadOnly=1, igReadExclusive=2
- **DocumentDownloadLevel** [3]: SEECDownloadAllLevel=0, SEECDownloadFirstLevel=1, SEECDownloadTopLevel=2
- **DocumentStatus** [7]: igStatusAvailable=0, igStatusInWork=1, igStatusInReview=2, igStatusReleased=3, igStatusBaselined=4, ... (7 total)
- **DocumentTypeConstants** [13]: igPartDocument=1, igDraftDocument=2, igAssemblyDocument=3, igSheetMetalDocument=4, igUnknownDocument=5, ... (13 total)
- **DraftGlobalConstants** [7]: seDraftSelectToolWireFrameFilter=1, seDraftSelectToolRelationHandleFilter=2, seDraftSelectToolDimensionAnnotationFilter=3, seDraftSelectToolTextFilter=4, seDraftSelectToolDrawingViewFilter=5, ... (7 total)
- **DraftPrintOrientationConstants** [2]: igDraftPrintPortrait=0, igDraftPrintLandscape=1
- **DraftPrintPaperSizeConstants** [115]: igDraftPrintPaperSize_Custom=0, igDraftPrintPaperSize_LETTER=1, igDraftPrintPaperSize_LETTERSMALL=2, igDraftPrintPaperSize_TABLOID=3, igDraftPrintPaperSize_LEDGER=4, ... (115 total)
- **DraftPrintScaleTooLargeActionConstants** [2]: igDraftPrintScaleToFit=0, igDraftSkipDocument=1
- **DraftPrintSheetsPerPageConstants** [2]: igSingleSheet=0, igMultipleSheets=1
- **DraftPrintUnitsConstants** [2]: igDraftPrintMillimeters=0, igDraftPrintInches=1
- **DraftSaveAsPDFPrintQualityDPIConstants** [8]: seDraftSaveAsPDFPrintQualityDPIConstants_72=72, seDraftSaveAsPDFPrintQualityDPIConstants_96=96, seDraftSaveAsPDFPrintQualityDPIConstants_144=144, seDraftSaveAsPDFPrintQualityDPIConstants_150=150, seDraftSaveAsPDFPrintQualityDPIConstants_300=300, ... (8 total)
- **DraftSaveAsPDFSheetOptionsConstants** [3]: seDraftSaveAsPDFSheetOptionsConstantsActiveSheet=0, seDraftSaveAsPDFSheetOptionsConstantsAllSheets=1, seDraftSaveAsPDFSheetOptionsConstantsSelectedSheets=2
- **DraftSectionViewType** [2]: seDraftSectionViewTypeStandard=0, seDraftSectionViewTypeRevolved=1
- **DraftSideConstants** [3]: seDraftInside=4, seDraftOutside=5, seDraftNone=44
- **DragComponentAnalysisOptionConstants** [2]: seNoAnalysis=0, seDetectCollisions=1
- **DragComponentCollisionOptionConstants** [2]: seDetectCollisionsEncounteredBySelectedPartOrSubassemblyOnly=0, seDetectCollisionsAmongAllAnalyzedPartsOrSubassemblies=1
- **DrawingStandardConstants** [2]: seDrawingStandardRadioButtonUpper=0, seDrawingStandardRadioButtonLower=1
- **DrawingViewAnnotationTypeConstants** [3]: seCuttingPlane=1, seViewingPlane=2, seDetailEnvelope=3
- **DrawingViewBsplineSimplificationConstants** [3]: igAlwaysSimplify=0, igSimplifyNonPlanarOnly=1, igNeverSimplify=2
- **DrawingViewCaptionTextAlignment** [3]: seTextAlignmentLeft=1, seTextAlignmentCenter=2, seTextAlignmentRight=3
- **DrawingViewCaptionTypeConstants** [6]: sePrincipalView=1, seSectionView=2, seAuxiliaryView=3, seDetailView=4, se2DModelView=5, ... (6 total)
- **DrawingViewDefaultsConstants** [2]: seDrawingViewDefaultsPrincipal=0, seDrawingViewDefaultsPictorial=1
- **DrawingViewEdgeStyleMappingEdgeType** [7]: seDVEdgeStyleMapping_VisibleEdge=0, seDVEdgeStyleMapping_HiddenEdge=1, seDVEdgeStyleMapping_TangentEdge=2, seDVEdgeStyleMapping_CoordinateSystemEdge=3, seDVEdgeStyleMapping_ReferenceVisibleEdge=4, ... (7 total)
- **DrawingViewEditCommandConstants** [134]: DrawingViewEditFileSheetSetup=10002, DrawingViewEditEditDelete=10100, DrawingViewEditViewDeleteSheet=10106, DrawingViewEditEditProperties=10108, DrawingViewEditEditCopytoSymbolLibrary=10114, ... (134 total)
- **DrawingViewIntersectionProcessingConstants** [4]: igNoIntersectionProcessing=0, igNoInterferenceEdges=1, igInterferenceEdgesThreadedPartsOnly=2, igInterferenceEdgesAllParts=3
- **DrawingViewProjectionAngleConstants** [2]: ProjectionAngleFirst=0, ProjectionAngleThird=1
- **DrawingViewShadingQualityConstants** [4]: igShadingQualityLevel1=1, igShadingQualityLevel2=2, igShadingQualityLevel3=3, igShadingQualityLevel4=4
- **DrawingViewSimplifiedAssemblyOptionConstants** [4]: seDrawingViewSimplifiedAssemblyOptionNone=0, seDrawingViewSimplifiedAssemblyOptionAllSubassemblies=1, seDrawingViewSimplifiedAssemblyOptionByConfiguration=2, seDrawingViewSimplifiedAssemblyOptionTopAssembly=3
- **DrawingViewSimplifiedPartOptionConstants** [3]: seDrawingViewSimplifiedPartOptionNone=0, seDrawingViewSimplifiedPartOptionAllParts=1, seDrawingViewSimplifiedPartOptionByConfiguration=2
- **DrawingViewSnapShotQualityConstants** [6]: igViewIsNotSnapShot=-1, igSnapShotQualityLevel1=1, igSnapShotQualityLevel2=2, igSnapShotQualityLevel3=3, igSnapShotQualityLevel4=4, ... (6 total)
- **DrawingViewStyleMappingElementType** [10]: seDVStyleMapping_PrincipalAndPictorialViews=0, seDVStyleMapping_2DmodelViews=1, seDVStyleMapping_SectionViews=2, seDVStyleMapping_AuxiliaryViews=3, seDVStyleMapping_DetailViews=4, ... (10 total)
- **DrawingViewStyleSheetNumberLocationConstants** [3]: seLeftArrow=1, seRightArrow=2, seBothArrows=3
- **DrawingViewTypeConstants** [11]: igNullView=0, igPrincipleView=1, igIsometricView=2, igAuxiliaryView=3, igXSectionView=4, ... (11 total)
- **DrawingViewVHL_ToleranceOverrideQualityConstants** [7]: igViewNotVHL=-1, igVHL_Tolerance_Use_SE_Default=0, igVHL_ToleranceOverrideQualityLevel1=1, igVHL_ToleranceOverrideQualityLevel2=2, igVHL_ToleranceOverrideQualityLevel3=3, ... (7 total)
- **DrawnCutoutFeatureConstants** [10]: seDrawnCutoutDepthLeft=1, seDrawnCutoutDepthRight=2, seDrawnCutoutMaterialInside=3, seDrawnCutoutMaterialOutside=4, seDrawnCutoutProfileLeft=5, ... (10 total)
- **DynamicGridSpacingConstants** [3]: igDynamicGridFine=0, igDynamicGridNormal=1, igDynamicGridCoarse=2
- **EdgeBarConstant** [6]: NO_RESIZE_CHILD=1, DONOT_MAKE_ACTIVE=2, TRACK_CLOSE_GLOBALLY=4, TRACK_CLOSE_BYDOCUMENT=8, UPDATE_ON_PANE_SLIDING=16, ... (6 total)
- **EnableDynamicEditProfilesSketches** [3]: seDynamicEditDisableWindow=0, seDynamicEditRecomputeDuringEdit=1, seDynamicEditRecomputeAfterEdit=2
- **EnclosureTypeConstant** [3]: igEnclosureTypeBox=0, igEnclosureTypeInsideCylinder=1, igEnclosureTypeOutsideCylinder=2
- **EndCapTreatmentConstants** [3]: NoCornerTreatment=0, ApplyChamfer=1, ApplyFillet=2
- **EndCapTypeConstants** [2]: Inward=0, Outward=1
- **EnergyDensityPrecisionConstants** [8]: seEnergyDensityPrecisionOnes=0, seEnergyDensityPrecisionTenths=1, seEnergyDensityPrecisionHundredths=2, seEnergyDensityPrecisionThousandths=3, seEnergyDensityPrecisionTenThousandths=4, ... (8 total)
- **EnergyPrecisionConstants** [8]: seEnergyPrecisionOnes=0, seEnergyPrecisionTenths=1, seEnergyPrecisionHundredths=2, seEnergyPrecisionThousandths=3, seEnergyPrecisionTenThousandths=4, ... (8 total)
- **EquationDrivenCurveErrorCode** [5]: seEquationDrivenCurveErrorCodeUnknownError=-1, seEquationDrivenCurveErrorCodeNoError=0, seEquationDrivenCurveErrorCodeInvalidExpression=1, seEquationDrivenCurveErrorCodeSelfIntersecting=2, seEquationDrivenCurveErrorCodeDiscontinuous=3
- **ExpandSelectionOptions** [2]: IncludeComponentsFromAssemblies=1, IncludeComponentsFromPartCopy=2
- **ExplodeCommandConstants** [85]: ExplodeAssemblyToolsMacro=25040, ExplodeAssemblyToolsOptions=25042, ExplodeAssemblyToolsReports=25043, ExplodeViewPreviousView=25046, ExplodeViewNamedViews=25053, ... (85 total)
- **ExtendSurfaceExtentTypeConstants** [6]: igESNatural=1, igESLinear=2, igESLinearTangentContinuous=3, igESLinearCurvatureContinuous=4, igESReflective=5, ... (6 total)
- **FEABoltConnGeomTypeEnum_Auto** [5]: eBoltConnGeomTypeNone_Auto=0, eBoltConnGeomTypeHole_Auto=1, eBoltConnGeomTypePlane_Auto=2, eBoltConnGeomTypeBolt_Auto=3, eBoltConnGeomTypeFastnerSys_Auto=4
- **FEABoltConnHoleTypeEnum_Auto** [4]: eBoltConnHoleTypeNone_Auto=0, eBoltConnHoleTypeAutomatic_Auto=1, eBoltConnHoleTypeThreaded_Auto=2, eBoltConnHoleTypeLooseFit_Auto=3
- **FEAConnectorTypeEnum_Auto** [8]: eConnectorTypeNone_Auto=0, eConnectorTypeLinear_Auto=1, eConnectorTypeGlue_Auto=2, eConnectorTypeBoltConnection_Auto=3, eConnectorTypeEdgeConnector_Auto=4, ... (8 total)
- **FEAConstraintTypeEnum_Auto** [7]: eCnstrTypeNone_Auto=0, eCnstrTypeFixed_Auto=1, eCnstrTypePinned_Auto=2, eCnstrTypeNoRotation_Auto=3, eCnstrTypeSlidingAlongSurface_Auto=4, ... (7 total)
- **FEADesBoundType_Auto** [2]: eFEADesBoundTypeValue_Auto=0, eFEADesBoundTypeNone_Auto=1
- **FEADesObjAction_Auto** [4]: eDesObjActionNone_Auto=0, eDesObjActionMin_Auto=1, eDesObjActionMax_Auto=2, eDesObjActionTarget_Auto=3
- **FEADesObjType_Auto** [7]: eDesObjTypeNone_Auto=0, eDesObjTypeMass_Auto=1, eDesObjTypeVloume_Auto=2, eDesObjTypeSurfArea_Auto=3, eDesObjTypeResComp_Auto=4, ... (7 total)
- **FEADesObjValueType_Auto** [3]: eDesObjValueTyeNone_Auto=0, eDesObjValueTypeMin_Auto=1, eDesObjValueypeMax_Auto=2
- **FEADesOptResultFlags_Auto** [6]: eOptResNoConvergence_Auto=0, eOptResSmallChngDesConv_Auto=1, eOptResSmallChngNoBetterDes_Auto=2, eOptResMaxNoOfIterReached_Auto=3, eOptResProcessCancelledByUser_Auto=4, ... (6 total)
- **FEADesignVarType_Auto** [4]: eFEADesignVarTypeNone_Auto=0, eFEADesignVarTypeDim_Auto=1, eFEADesignVarTypeVar_Auto=2, eFEADesignVarTypeSimVar_Auto=3
- **FEAFileType_Auto** [2]: eFEAModFile_Auto=0, eFEANastranFile_Auto=1
- **FEAFunctionType_Auto** [4]: eFunctionTypeNone_Auto=0, eFunctionTypeFreqVsFactor_Auto=1, eFunctionTypeTimeVsFactor_Auto=2, eFunctionTypeFreqVsStructDamping_Auto=3
- **FEAInitialPenetrationTypeEnum_Auto** [3]: eCalculatedType_Auto=0, eCalculatedOrZeroType_Auto=1, eZeroGapType_Auto=2
- **FEALoadTypeEnum_Auto** [19]: eLoadTypeNone_Auto=0, eLoadTypeForce_Auto=1, eLoadTypePressure_Auto=2, eLoadTypeTorque_Auto=3, eLoadTypeGravity_Auto=4, ... (19 total)
- **FEAMeshTypeEnum_Auto** [5]: eMeshTypeNone_Auto=0, eMeshTypeTetrahedral_Auto=1, eMeshType2D_Auto=2, eMeshTypeMixed_Auto=3, eMeshTypeBeam_Auto=4
- **FEAMesherType_Auto** [2]: eFEAMesherTypeLegacy_Auto=0, eFEAMesherTypeBody_Auto=1
- **FEAPlotsOwnerTypeEnum_Auto** [17]: ePlotsOwnerTypeNone_Auto=0, ePlotsOwnerTypeDisplacement_Auto=1, ePlotsOwnerTypeRotation_Auto=2, ePlotsOwnerTypeAppliedForce_Auto=3, ePlotsOwnerTypeAppliedMoment_Auto=4, ... (17 total)
- **FEAResultOptions_Auto** [20]: eDisplacement_Auto=1, eAppliedForce_Auto=2, eConstraintForce_Auto=4, eFEAEquationForce_Auto=8, eFEAForceBalance_Auto=16, ... (20 total)
- **FEAStudyGeomTypeEnum_Auto** [5]: eStudyGeomTypeNone_Auto=0, eStudyGeomTypeSync_Auto=1, eStudyGeomTypeOrdered_Auto=2, eStudyGeomTypeSimplify_Auto=3, eStudyGeomTypeDesigned_Auto=4
- **FEAStudyStatusEnum_Auto** [5]: eStudyStatusNone_Auto=0, eStudyStatusGeometry_Auto=1, eStudyStatusLoadsConstr_Auto=2, eStudyStatusMesh_Auto=3, eStudyStatusResults_Auto=4
- **FEAStudyTypeEnum_Auto** [9]: eStudyTypeNone_Auto=0, eStudyTypeLinearStatic_Auto=1, eStudyTypeNormalModal_Auto=2, eStudyTypeLinearBuckling_Auto=3, eStudyTypeSSHT_Auto=4, ... (9 total)
- **FaceMoveConstants** [13]: igFaceMoveNone=0, igFaceMoveAlong2PointVector=1, igFaceMoveAlongFaceNormal=2, igFaceMoveAlongEdge=3, igFaceMoveInPlane=4, ... (13 total)
- **FaceOffsetConstants** [3]: igFaceOffsetNone=0, igFaceOffsetBySynchronousOffset=1, igFaceOffsetByOffset=2
- **FaceRotateConstants** [8]: igFaceRotateNone=0, igFaceRotateByPoints=1, igFaceRotateByGeometry=2, igFaceRotateAxisStart=3, igFaceRotateAxisEnd=4, ... (8 total)
- **FamilyMemberStatusConstants** [6]: seStatusUnknown=0, seStatusNotCreated=1, seStatusUpToDate=2, seStatusOutOfDate=3, seStatusLinkBroken=4, ... (6 total)
- **FeatureLoopType** [3]: eIncludeInternalLoop=1, eExcludeInternalLoop=2, eUseOnlyInternalLoop=3
- **FeaturePropertyConstants** [258]: igNullConstant=0, igLeft=1, igRight=2, igSymmetric=3, igInside=4, ... (258 total)
- **FeatureStatusConstants** [5]: igFeatureOK=1216476310, igFeatureFailed=1216476311, igFeatureWarned=1216476312, igFeatureSuppressed=1216476313, igFeatureRolledBack=1216476314
- **FeatureTopologyQueryTypeConstants** [10]: igQueryAll=1, igQueryRoundable=2, igQueryStraight=3, igQueryEllipse=4, igQuerySpline=5, ... (10 total)
- **FeatureTypeConstants** [129]: igEmbossFeatureObject=-2101998503, igSweptProtrusionFeatureObject=-2101194894, igBeadFeatureObject=-2099521208, igWeldPatternFeatureObject=-1994967864, igUnitedBodyObject=-1974090952, ... (129 total)
- **FileTranslationMode** [2]: seExport=-1720541218, seImport=1493142125
- **FillHoleType** [4]: seFillHoleTypeLinear=0, seFillHoleTypeRefined=1, seFillHoleTypeTangent=2, seFillHoleTypeCurvature=3
- **FillPatternMethodConstants** [6]: seRectangularFillMethod=1, seStaggerPolarFillMethod=2, seStaggerLinearOffsetFillMethod=3, seRadialTargetSpacingFillMethod=4, seRadialInstanceCountFillMethod=5, ... (6 total)
- **FilletWeldSetbackConstants** [3]: seFilletWeldEqualSetback=0, seFilletWeldUnequalSetback=1, seFilletWeldThickness=2
- **FindWhereUsedDocuments** [1]: NoOfDocsFound=0
- **FlangeFeatureConstants** [10]: seFlangeBendOnlyCornerRelief=1, seFlangeBendAndFaceCornerRelief=2, seFlangeBendAndFaceChainRelief=3, seFlangeMaterialInside=4, seFlangeMaterialOutside=5, ... (10 total)
- **FlattenPatternModelTypeConstants** [3]: igFlattenPatternModelTypeDevelopable=0, igFlattenPatternModelTypeNonDevelopable=1, igFlattenPatternModelTypeFlattenAnything=2
- **FoldTypeConstants** [9]: igNullFold=0, igFoldUp=1, igFoldDown=2, igFoldRight=3, igFoldLeft=4, ... (9 total)
- **ForcePerAreaPrecisionConstants** [12]: igForcePerAreaPrecisionOnes=0, igForcePerAreaPrecisionTenths=1, igForcePerAreaPrecisionHundredths=2, igForcePerAreaPrecisionThousandths=3, igForcePerAreaPrecisionTenThousandths=4, ... (12 total)
- **ForcePrecisionConstants** [12]: igForcePrecisionOnes=0, igForcePrecisionTenths=1, igForcePrecisionHundredths=2, igForcePrecisionThousandths=3, igForcePrecisionTenThousandths=4, ... (12 total)
- **FrameShapeConstants** [2]: igRectangularFrame=1, igEllipticalFrame=2
- **FrequencyPrecisionConstants** [12]: igFrequencyPrecisionOnes=0, igFrequencyPrecisionTenths=1, igFrequencyPrecisionHundredths=2, igFrequencyPrecisionThousandths=3, igFrequencyPrecisionTenThousandths=4, ... (12 total)
- **GNTTypePropertyConstants** [30]: igMesh=-2071771273, igPlane=-1909484335, igParamBSplineCurve=-1811952078, igCurveBody=-1020639371, igCurvePath=-1020639369, ... (30 total)
- **GenerateMasterImportListError** [1]: NoDocsFound=1
- **GenerateSourceImportListError** [1]: GenerateSourceImportListError_NoDocsFound=1
- **GenerativeConstraintTypeConstants** [5]: seGenerativeDesignUnknownConstraint=0, seGenerativeDesignFixedConstraint=1, seGenerativeDesignPinnedConstraint=2, seGenerativeDesignDisplacementConstraint=3, seGenerativeDesignMaximumDisplacementConstraint=4
- **GenerativeDirectionTypeConstants** [8]: seGenerativeDesignDirectionTypeUnknown=0, seGenerativeDesignDirectionTypeNormalToFace=1, seGenerativeDesignDirectionTypeAlongVector=2, seGenerativeDesignDirectionTypeByXYZComponents=3, seGenerativeDesignDirectionTypeAbsoluteMagnitude=4, ... (8 total)
- **GenerativeLoadTypeConstants** [4]: seGenerativeDesignUnknownLoad=0, seGenerativeDesignForceLoad=1, seGenerativeDesignPressureLoad=2, seGenerativeDesignTorqueLoad=3
- **GenerativeMaterialExtrusionAxisConstants** [4]: seGenerativeMaterialExtrusionAxisConstantsNone=0, seGenerativeMaterialExtrusionAxisConstantsX=1, seGenerativeMaterialExtrusionAxisConstantsY=2, seGenerativeMaterialExtrusionAxisConstantsZ=3
- **GenerativeMaterialExtrusionDirectionConstants** [3]: seGenerativeMaterialExtrusionDirectionConstantsPositive=0, seGenerativeMaterialExtrusionDirectionConstantsNegative=1, seGenerativeMaterialExtrusionDirectionConstantsBoth=2
- **GenerativeOverhangDraftAngleDirectionConstants** [4]: seGenerativeOverhangDraftAngleDirectionConstantsNone=0, seGenerativeOverhangDraftAngleDirectionConstantsX=1, seGenerativeOverhangDraftAngleDirectionConstantsY=2, seGenerativeOverhangDraftAngleDirectionConstantsZ=3
- **GenerativePlanarSymmetryTypeConstants** [3]: seGenerativePlanarSymmetryTypeHalf=1, seGenerativePlanarSymmetryTypeQuarter=2, seGenerativePlanarSymmetryTypeOneEighth=3
- **GenerativeStudyNotReadyForSolveReasons** [6]: seGenerativeDesignStudyNotReadyForSolveUnknownReason=0, seGenerativeDesignStudyNotReadyForSolveDesignSpaceUndefined=1, seGenerativeDesignStudyNotReadyForSolveMaterialNotDefined=2, seGenerativeDesignStudyNotReadyForSolveDoesNotHaveAtLeastOneValidLoadCase=3, seGenerativeDesignStudyNotReadyForSolveAllLoadCasesSuppressed=4, ... (6 total)
- **GenerativeStudyOptimizationType** [3]: seGenerativeStudyOptimizationTypeUnknown=0, seGenerativeStudyOptimizationTypeReduceMassByPercentage=1, seGenerativeStudyOptimizationTypeFactorOfSafety=2
- **Geom2dFormConstants** [7]: igGeom2dFormUnknown=0, igGeom2dFormOpen=1, igGeom2dFormClosed=2, igGeom2dFormClosedWithTangents=3, igGeom2dFormClosedWithCurvature=4, ... (7 total)
- **Geom2dOrientationConstants** [2]: igGeom2dOrientClockwise=0, igGeom2dOrientCounterClockwise=1
- **Geom2dScopeConstants** [5]: igGeom2dScopeUnknown=0, igGeom2dScopePlaner=1, igGeom2dScopeColinear=2, igGeom2dScopeDegenerate=3, igGeom2dScopeNonplaner=4
- **GetFileOpenOptions** [7]: HideReadOnlyOptions=1, OpenFromCompareDrawing=2, OpenWithReadOnly=4, OpenAssemblyWithAllLevelsReadOnly=8, OpenDraftWithInactiveDrawingViews=16, ... (7 total)
- **GraphicMemberEdgeTypeConstants** [8]: seUnknownEdgeType=0, seModelEdgeType=1, seSilhouetteEdgeType=2, seSectionEdgeType=3, seSnapshotEdgeType=4, ... (8 total)
- **GridDisplayOptionsConstants** [2]: igGridDisplayedAsLines=0, igGridDisplayedAsPoints=1
- **GridSnapOptionsConstants** [2]: igGridSnapUsingLines=0, igGridSnapUsingPoints=1
- **GridTypeConstants** [2]: igGridDynamic=0, igGridStatic=1
- **GussetConstants** [9]: igGussetNone=0, igAutomaticProfile=1, igUserDrawnProfile=2, igRoundShape=3, igSquareShape=4, ... (9 total)
- **GussetPlateAlignmentConstants** [3]: GussetPlateAlignType_Center=0, GussetPlateAlignType_Right=1, GussetPlateAlignType_Left=2
- **GussetPlateErrorCode** [6]: GussetPlateErrorCodeUnknownError=-1, GussetPlateErrorCodeNoError=0, GussetPlateErrorCodeMissingParameter=1, GussetPlateErrorCodeInvalidParameter=2, GussetPlateErrorCodeNoReferencePlane=3, ... (6 total)
- **GussetPlateNamingFormat** [5]: igNamingFormatParameter=0, igNamingFormatThickness=1, igNamingFormatMaterial=2, igNamingFormatNumber=3, igNamingFormatNone=4
- **GussetPlateThicknessDirConstants** [3]: GussetPlateDir_Center=0, GussetPlateDir_Right=1, GussetPlateDir_Left=2
- **GussetPlateUniquenessCriteria** [2]: igUniquenessCriteriaGussetParameter=0, igUniquenessCriteriaCuttingStock=1
- **HTHoleTypeConstants** [9]: seHTOther=0, seHTSimple=1, seHTCounterbore=2, seHTCountersink=3, seHTSimpleThreaded=4, ... (9 total)
- **HandleType** [7]: igHandleNone=0, igHandleReadOnly=1, igHandleWriteable=2, igHandleInvisible=4, igHandleRotate=8, ... (7 total)
- **HarnessSaveAsEcadStatusConstants** [11]: seHarnessSaveAsEcadStatus_Success=0, seHarnessSaveAsEcadStatus_Failed=1, seHarnessSaveAsEcadStatus_FailedBadArgs=2, seHarnessSaveAsEcadStatus_FailedNoComps=3, seHarnessSaveAsEcadStatus_FailedNoConns=4, ... (11 total)
- **HarnessTypeConstants** [8]: seHarnessType_Wire=1, seHarnessType_Cable=2, seHarnessType_Bundle=3, seHarnessType_Wires=4, seHarnessType_Cables=5, ... (8 total)
- **HatchElementType** [3]: igHatchElementTypeUnknown=0, igHatchElementTypeLinear=1, igHatchElementTypeRadial=2
- **HeatFluxPerDistancePrecisionConstants** [8]: seHeatFluxPerDistancePrecisionOnes=0, seHeatFluxPerDistancePrecisionTenths=1, seHeatFluxPerDistancePrecisionHundredths=2, seHeatFluxPerDistancePrecisionThousandths=3, seHeatFluxPerDistancePrecisionTenThousandths=4, ... (8 total)
- **HeatFluxPrecisionConstants** [8]: seHeatFluxPrecisionOnes=0, seHeatFluxPrecisionTenths=1, seHeatFluxPrecisionHundredths=2, seHeatFluxPrecisionThousandths=3, seHeatFluxPrecisionTenThousandths=4, ... (8 total)
- **HeatGenerationPrecisionConstants** [8]: seHeatGenerationPrecisionOnes=0, seHeatGenerationPrecisionTenths=1, seHeatGenerationPrecisionHundredths=2, seHeatGenerationPrecisionThousandths=3, seHeatGenerationPrecisionTenThousandths=4, ... (8 total)
- **HeatTransferCoefficientPrecisionConstants** [8]: seHeatTransferCoefficientPrecisionOnes=0, seHeatTransferCoefficientPrecisionTenths=1, seHeatTransferCoefficientPrecisionHundredths=2, seHeatTransferCoefficientPrecisionThousandths=3, seHeatTransferCoefficientPrecisionTenThousandths=4, ... (8 total)
- **HelicalCurveMethodType** [3]: igHelicalCurveMethodPitchAndHeight=0, igHelicalCurveMethodPitchAndTurns=1, igHelicalCurveMethodHeightAndTurns=2
- **HelicalCurveTaperByType** [3]: igHelicalCurveTaperNone=0, igHelicalCurveTaperByAngle=1, igHelicalCurveTaperByDiameter=2
- **HemFeatureConstants** [15]: seHemTypeClosed=1, seHemTypeOpen=2, seHemTypeSFlange=3, seHemTypeCurl=4, seHemTypeOpenLoop=5, ... (15 total)
- **HideAllcomponentsConstants** [2]: seHideAllcomponentsConstantsNo=0, seHideAllcomponentsConstantsYes=1
- **HoleDataUnitsConstants** [2]: igHoleDataUnitsInches=0, igHoleDataUnitsMillimeters=1
- **HoleTable2AngularUnit** [3]: igHoleTable2AngularDegrees=0, igHoleTable2AngularDegMinSec=1, igHoleTable2AngularRadians=2
- **HoleTable2DMSRoundOffTypeConstants** [6]: igHoleTable2Angular10Degree=1, igHoleTable2Angular1Degree=2, igHoleTable2Angular10Minute=3, igHoleTable2Angular1Minute=4, igHoleTable2Angular10Second=5, ... (6 total)
- **HoleTable2DecimalRoundOffTypeConstants** [8]: igHoleTable2Decimal1=0, igHoleTable2Decimal_1=1, igHoleTable2Decimal_2=2, igHoleTable2Decimal_3=3, igHoleTable2Decimal_4=4, ... (8 total)
- **HoleTable2PrimaryLinearUnit** [2]: igHoleTable2LinearMM=0, igHoleTable2LinearInches=1
- **HoleTableAnnotPosition** [4]: igAnnotPosTopLeft=0, igAnnotPosTopRight=1, igAnnotPosBottomLeft=2, igAnnotPosBottomRight=3
- **HoleTableCalloutType** [4]: igHoleCallout1=1, igHoleCallout2=2, igHoleCallout3=3, igHoleCallout4=4
- **HoleTableDelimiterType** [4]: igDelimiterTypeNone=0, igDelimiterTypeDot=1, igDelimiterTypeComma=2, igDelimiterTypeSpace=3
- **HoleTableType** [3]: igByDrawingView=0, igByUserSelection=1, igByFeature=2
- **HoleToleranceTypeConstants** [2]: seStandardFit_Tolerance=0, seUnit_Tolerance=1
- **HoleTypeToDeleteConstants** [3]: seHoleTypeToDeleteFeaturesOnly=0, seHoleTypeToDeleteCylindersAndConesOnly=1, seHoleTypeToDeleteAll=2
- **InsightSPUserRights** [23]: seViewListItems=1, seAddListItems=2, seEditListItems=4, seDeleteListItems=8, seCancelCheckout=256, ... (23 total)
- **InterDocumentUpdateMode** [2]: seActiveLevel=0, seAllOpenDocuments=1
- **InterPartLinkOption** [4]: eInterPartLinkUnknown=0, eCopyAllLinkedDocs=1, eUpdateLinksToNewDoc=2, eOutOfContextWithNewDoc=3
- **InterferenceComparisonConstants** [4]: seInterferenceComparisonSet1vsSet2=1, seInterferenceComparisonSet1vsAllOther=2, seInterferenceComparisonSet1vsVisible=3, seInterferenceComparisonSet1vsItself=4
- **InterferenceOptionsConstants** [2]: seIntfOptIgnoreSameNominalDia=1, seIntfOptIgnoreThreadVsNonThreaded=2
- **InterferenceReportConstants** [4]: seInterferenceReportPartNames=1, seInterferenceReportPartCentersOfGravity=2, seInterferenceReportInterferenceCenterOfGravity=4, seInterferenceReportInterferenceVolume=8
- **InterferenceStatusConstants** [5]: seInterferenceStatusNoInterference=1, seInterferenceStatusConfirmedInterference=2, seInterferenceStatusProbableInterference=3, seInterferenceStatusConfirmedAndProbableInterference=4, seInterferenceStatusIncompleteAnalysis=5
- **InternalComponentTypeConstant** [4]: InternalComponentTypeConstant_Unknown=0, InternalComponentTypeConstant_Part=1, InternalComponentTypeConstant_Assembly=2, InternalComponentTypeConstant_SheetMetal=3
- **IsoclineDirectionConstants** [2]: igIsoclineleft=1, igIsoclineRight=2
- **ItemNumberGenerationModeConstants** [4]: seItemNumberGenerationModeGenerationDisabled=0, seItemNumberGenerationModeTopLevelOnlyMode=1, seItemNumberGenerationModeAtomicMode=2, seItemNumberGenerationModeExplodedMode=3
- **ItemNumberModeConstants** [5]: seItemNumber_None=0, seItemNumber_Toplevel=1, seItemNumber_Atomic=2, seItemNumber_Exploded=3, seItemNumber_LevelBased=4
- **JogFeatureConstants** [19]: seJogBendNFT=1, seJogBendEqn=2, seJogBRRectangular=3, seJogBRFillet=4, seJogBendOnlyCR=5, ... (19 total)
- **KeyPointExtentConstants** [4]: igTangentNormal=1, igReverseTangentNormal=2, igInteriorTangentNormal=3, igInteriorReverseTangentNormal=4
- **KeyPointType** [13]: igKeyPointStart=1, igKeyPointEnd=2, igKeyPointCenter=4, igKeyPointMajorAxis=8, igKeyPointMinorAxis=16, ... (13 total)
- **KeypointEndConditionConstants** [5]: seKeypointEndConditionNatural=1, seKeypointEndConditionPeriodic=2, seKeypointEndConditionTangent=3, seKeypointEndConditionNormalToFace=4, seKeypointEndConditionCurvatureContinuous=5
- **KeypointIndexConstants** [39]: igArcCenter=0, igCircleCenter=0, igEllipseArcCenter=0, igEllipseCenter=0, igLineStart=0, ... (39 total)
- **LayoutCommandConstants** [129]: LayoutEditDelete=10100, LayoutFileProperties=10146, LayoutViewZoom=10194, LayoutViewZoomArea=10201, LayoutViewFit=10202, ... (129 total)
- **LayoutElementTypeConstants** [4]: igTemplateEditor3DView=1, igTemplateEditorViewCarousel=2, igTemplateEditorBOMTable=3, igTemplateEditorPDFText=4
- **LayoutInPartCommandConstants** [140]: LayoutInPartEditDelete=10100, LayoutInPartFileProperties=10146, LayoutInPartViewZoom=10194, LayoutInPartViewZoomArea=10201, LayoutInPartViewFit=10202, ... (140 total)
- **LayoutStatusConstants** [3]: seLayoutAddedNewLayout=0, seLayoutReturnedExistingLayout=1, seLayoutFailedBecauseOfExisting=2
- **LinearAccelerationPrecisionConstants** [8]: seLinearAccelerationPrecisionOnes=0, seLinearAccelerationPrecisionTenths=1, seLinearAccelerationPrecisionHundredths=2, seLinearAccelerationPrecisionThousandths=3, seLinearAccelerationPrecisionTenThousandths=4, ... (8 total)
- **LinearDensityPrecisionConstants** [12]: seLinearDensityPrecisionOnes=0, seLinearDensityPrecisionTenths=1, seLinearDensityPrecisionHundredths=2, seLinearDensityPrecisionThousandths=3, seLinearDensityPrecisionTenThousandths=4, ... (12 total)
- **LinearVelocityPrecisionConstants** [12]: seLinearVelocityPrecisionOnes=0, seLinearVelocityPrecisionTenths=1, seLinearVelocityPrecisionHundredths=2, seLinearVelocityPrecisionThousandths=3, seLinearVelocityPrecisionTenThousandths=4, ... (12 total)
- **LineupTextAlignOptionConstants** [8]: igAlignLeft=0, igAlignRight=1, igAlignCenter=2, igAlignBottom=3, igAlignTop=4, ... (8 total)
- **LinksUpdateOption** [3]: igNoLinksUpdate=0, igLinksUpdateWithDefpath=1, igLinksUpdateWithAltPath=2
- **LipFeatureConstants** [2]: seLipTypeLip=1, seLipTypeGroove=2
- **LiveRulesConstants** [18]: igConcentricLiveRule=1, igCoplanarLiveRule=2, igTangentEdgeLiveRule=3, igTangentTouchingLiveRule=4, igParallelLiveRule=5, ... (18 total)
- **LoadSymbDirOptsEnum_Auto** [10]: eLoadDirDefault_Auto=0, eLoadDirAlongVec_Auto=1, eLoadDirNormalToFace_Auto=2, eLoadDirTorque_Auto=3, eLoadDirGravity_Auto=4, ... (10 total)
- **LoftedFlangeFeatureAutoReliefConstants** [2]: igLoftedFlangeAutoReliefSpherical=251, igLoftedFlangeAutoReliefLinear=252
- **LoftedFlangeFeatureAutoReliefTrimConstants** [2]: igLoftedFlangeAutoReliefTrimEndPlates=253, igLoftedFlangeAutoReliefTrimNone=254
- **LoftedFlangeFeatureBendingMethodConstants** [4]: igLoftedFlangeFeatureBendingMethodNone=1, igLoftedFlangeFeatureBendingMethodGraphicBends=2, igLoftedFlangeFeatureBendingMethodRealBends=3, igLoftedFlangeFeatureBendingMethodFormedBends=4
- **LoftedFlangeFeatureDivideBendConstants** [4]: igLoftedFlangeDivideBendByCount=255, igLoftedFlangeDivideBendByMaximumChordHeight=256, igLoftedFlangeDivideBendByMaximumSegmentLength=257, igLoftedFlangeDivideBendByMaximumSegmentAngle=258
- **LouverFeatureConstants** [10]: seLouverDepthDirectionLeft=1, seLouverDepthDirectionRight=2, seLouverDimensionOffset=3, seLouverDimensionFull=4, seLouverFormedEnd=5, ... (10 total)
- **MassPrecisionConstants** [12]: igMassPrecisionOnes=0, igMassPrecisionTenths=1, igMassPrecisionHundredths=2, igMassPrecisionThousandths=3, igMassPrecisionTenThousandths=4, ... (12 total)
- **MatTablePropIndexConstants** [13]: seMaterialName=3, seFaceStyle=20, seFillStyle=21, seVSPlusStyle=22, seDensity=23, ... (13 total)
- **MeasureDistanceTypeConstants** [3]: MeasureDistanceTypeConstants_MinimumDistance=1, MeasureDistanceTypeConstants_MaximumDistance=2, MeasureDistanceTypeConstants_SmartDistance=3
- **MeasureVariableTypeConstants** [4]: MeasureVariableTypeConstants_Distance=1, MeasureVariableTypeConstants_MinimumDistance=2, MeasureVariableTypeConstants_NormalDistance=3, MeasureVariableTypeConstants_Angle=4
- **MeasureVariableValueConstants** [1]: MeasureVariableValueConstants_TrueMeasure=1
- **MeshControlType_Auto** [4]: eNoneMeshControl_Auto=0, eBodyMeshControl_Auto=1, eSurfaceMeshControl_Auto=2, eEdgeMeshControl_Auto=3
- **MirrorOptionConstants** [4]: MirrorOptionNormal=1, MirrorOptionDetach=2, MirrorOptionPersist=4, MirrorOptionRemoveOriginal=8
- **ModelLinkTypeConstants** [3]: igPartLink=0, igAssemblyLink=1, igWeldmentLink=2
- **ModelMemberComponentTypeConstants** [12]: seAssemblyMemberType=0, sePartMemberType=1, seConstructionMemberType=2, seWeldmentMemberType=3, seWeldPartMemberType=4, ... (12 total)
- **ModelMemberDisplayTypeConstants** [4]: seShowPart=0, seHidePart=1, seSectionPart=2, seUndefinedDisplay=3
- **ModelMemberTypeConstants** [3]: seAssemblyMember=0, sePartMember=1, seConstructionMember=2
- **ModelNodeTypeConstants** [2]: igPartNode=0, igAssemblyNode=1
- **ModelingModeConstants** [2]: seModelingModeSynchronous=1, seModelingModeOrdered=2
- **ModellingEnvironmentConstants** [2]: ModellingEnvironmentConstantsSynchronous=1, ModellingEnvironmentConstantsOrdered=2
- **MotionCommandConstants** [58]: MotionAssemblyToolsPhysicalProperties=25038, MotionAssemblyToolsCheckInterference=25039, MotionAssemblyToolsMacro=25040, MotionAssemblyToolsOptions=25042, MotionViewPreviousView=25046, ... (58 total)
- **MoveConnectedFaceTypes** [3]: seMoveConnectedFaceTypeExtendTrim=0, seMoveConnectedFaceTypeTip=1, seMoveConnectedFaceTypeLift=2
- **MoveMultipleMoveTypeConstants** [2]: seMoveMultipleMove=1, seMoveMultipleCopy=2
- **MoveMultipleRelationshipConstants** [3]: seMoveMultipleMaintainInternalRelationships=1, seMoveMultipleDropInternalRelationships=2, seMoveMultipleDropInternalRelationshipsAndGround=3
- **MovePrecedenceConstants** [2]: igSelectSetMovePrecedence=1, igModelMovePredecence=2
- **MultiBodyPublishStatusConstants** [7]: seMBPStatusUnknown=0, seMBPStatusNotCreated=1, seMBPStatusUpToDate=2, seMBPStatusOutOfDate=3, seMBPStatusFailed=4, ... (7 total)
- **NewWindowOptionConstants** [8]: igNewWindowContainer=1, igNewWindowServer=2, igNewWindowLocalServer=4, igNewWindowVisible=8, igNewWindowInvisible=16, ... (8 total)
- **NotifyOption** [5]: igNotifyWhenReadable=0, igNotifyWhenWriteable=1, igNotifyWhenAvailable=2, igNoNotify=3, igNotifyWhenExclusive=4
- **OLEInsertionTypeConstant** [5]: igUseSymbolPreferences=-1, igOLELinked=0, igOLEEmbedded=1, igOLENone=3, igOLESharedEmbedded=4
- **OLEUpdateOptionConstant** [3]: igOLEAutomatic=0, igOLEFrozen=1, igOLEManual=2
- **ObjectType** [130]: seDVCircle2d=-2074243498, igPlanarRelation3d=-2058948880, igSketch3D=-2054330988, seAssemblyGroups=-2004545918, igDividedPart=-1940558319, ... (130 total)
- **OccurrenceSectionedFacetDataConstants** [3]: seOccurrenceSectionedFacetDataPresent=0, seOccurrenceSectionedFacetDataNotPresent=1, seOccurrenceNotSectioned=2
- **OccurrenceStatusConstants** [8]: seOccurrenceStatusWellDefined=1, seOccurrenceStatusFixed=2, seOccurrenceStatusUnderDefined=4, seOccurrenceStatusOverDefined=32776, seOccurrenceStatusNotConsistent=32784, ... (8 total)
- **OffsetEditDirectionConstants** [3]: seEditSourceFace=1, seEditTargetFace=2, seEditSymmetric=3
- **OffsetSideConstants** [3]: seOffsetLeft=1, seOffsetRight=2, seOffsetNone=44
- **OpenNonSolidEdgeFileContext** [9]: OpenImage=1, OpenPointCloud=2, OpenDecal=3, OpenViewBackground=4, OpenViewReflection=5, ... (9 total)
- **OrientXpressSizeConstants** [3]: seOrientXpressSizeConstantSmall=0, seOrientXpressSizeConstantMedium=1, sOrientXpressSizeConstantssHigh=2
- **OverWriteFilesOption** [2]: NoToAll=0, YesToAll=1
- **OverlayColorModeConstants** [2]: seOverlayColorModeAbsolute=1, seOverlayColorModeRelative=2
- **PCFFilePermissions** [9]: NoPermissions=0, PMIPermissions=2, CrossSectionPermissions=8, MeasurePermissions=80, MarkupPermissions=768, ... (9 total)
- **PMIEditDirectionConstants** [3]: seMoveOriginParent=1, seMoveMeasureParent=2, seMoveParentsSymmetrically=3
- **PMIModelStateConstants** [3]: seDesignModelState=1, seFlatModelState=2, seSimplifyModelState=3
- **PMIModelViewStandardOrientationConstants** [9]: sePMIModelViewFront=0, sePMIModelViewBack=1, sePMIModelViewLeft=2, sePMIModelViewRight=3, sePMIModelViewTop=4, ... (9 total)
- **PMIRenderModeConstants** [5]: sePMIModelViewRenderModeNone=0, sePMIModelViewRenderModeVisibleEdges=1, sePMIModelViewRenderModeVisibleAndHiddenEdges=2, sePMIModelViewRenderModeShaded=3, sePMIModelViewRenderModeShadedWithVisibleEdges=4
- **PMISectionDisplayModeConstants** [4]: sePMISectionDisplayShowOnlyCutFaces=0, sePMISectionDisplayShowCutFacesAndCutBodies=1, sePMISectionDisplayShowCutFacesWithOriginalBodies=2, sePMISectionDisplayShowOnlyOriginalBodies=3
- **PaperSizeConstants** [50]: igCustomSheetSize=-2, igSameAsPrintSetup=-1, igEngFolioTall=0, igEngFolioWide=1, igEngLegalTall=2, ... (50 total)
- **PaperToModelScaleConstants** [47]: igDefault1To1=-1, igCustomScale=0, igMetric50To1=1, igMetric20To1=2, igMetric10To1=3, ... (47 total)
- **PaperUnitConstants** [3]: igUnitInches=0, igUnitMillimeters=1, igUnitCentimeters=2
- **ParasolidVersionConstants** [13]: seParasolidCurrentVersion=0, seParasolidVersion70=70, seParasolidVersion71=71, seParasolidVersion80=80, seParasolidVersion90=90, ... (13 total)
- **PartActivationAssemblyConstants** [3]: sePartActivationAssemblyLastSaved=0, sePartActivationAssemblyAllInActive=1, sePartActivationAssemblyAllActive=2
- **PartBaseStylesConstants** [6]: sePartBaseStyle=0, seConstructionBaseStyle=1, seThreadedCylindersBaseStyle=2, seCurveBaseStyle=3, seWeldBeadBaseStyle=4, ... (6 total)
- **PartCommandConstants** [183]: PartEnvironmentsExit=10231, PartTransformToSyncSheetmetal=10640, PartConstructionUnitedBody=10855, PartConstructionRecoveredBody=10856, PartFormatStyle=25030, ... (183 total)
- **PartCopyUpdateModeConstants** [3]: igPartCopyUpdatePrompt=0, igPartCopyUpdateAutomatic=1, igPartCopyUpdateManual=2
- **PartDrawingViewTypeConstants** [2]: sePartDesignedView=0, sePartSimplifiedView=1
- **PartGlobalConstants** [8]: sePartGlobalDensity=1, sePartGlobalAccuracyForDensity=2, sePartGlobalMaterial=3, sePartGlobalCombMaximumDensity=4, sePartGlobalCombMaximumMagnitude=5, ... (8 total)
- **PartIntersectionsConstants** [2]: sePartIntersectionsDoNotProcess=0, sePartIntersectionsProcessIntersections=1
- **PartListEndAngleRepresentationType** [3]: igDefaultRepresentation=0, igSignRepresentation=1, igClockwiseRepresentation=2
- **PartSimplificationAssemblyConstants** [3]: sePartSimplificationAssemblyLastSaved=0, sePartSimplificationnAssemblySimplified=1, sePartSimplificationAssemblyDesigned=2
- **PartStatusConstants** [8]: igPartStatusWellDefined=1, igPartStatusFixed=2, igPartStatusUnderDefined=4, igPartStatusOverDefined=32776, igPartStatusNotConsistent=32784, ... (8 total)
- **PartsListComponentType** [5]: igPartsListComponentType_Parts=0, igPartsListComponentType_Pipes=1, igPartsListComponentType_PipeFittings=2, igPartsListComponentType_FrameMembers=3, igPartsListComponentType_Tubes=4
- **PartsListType** [3]: igTopLevel=0, igAtomic=1, igExploded=2
- **PatternCurveAnchorSideConstants** [2]: sePatternCurveLeftSide=1, sePatternCurveRightSide=2
- **PatternOffsetTypeConstants** [4]: sePatternFitOffset=0, sePatternFillOffset=1, sePatternFixedOffset=2, sePatternChordLengthOffset=3
- **PatternTransformRotateTypeConstants** [2]: sePatternTransformRotateOnCurvePosition=0, sePatternTransformRotateOnFeaturePosition=1
- **PatternTransformTypeConstants** [4]: sePatternTransformLinear=0, sePatternTransformFullRotation=1, sePatternTransformProjectedRotation=2, sePatternTransformFullRotationFromSurface=3
- **PatternTypeConstants** [2]: seSmartPattern=0, seFastPattern=1
- **PhysicalPropertiesStatusConstants** [3]: sePhysicalPropertiesStatus_None=0, sePhysicalPropertiesStatus_Model=1, sePhysicalPropertiesStatus_User=2
- **PhysicalThreadClearanceTypeConstants** [2]: sePhysicalThreadClearanceTypePercentage=0, sePhysicalThreadClearanceTypeAbsolute=1
- **PhysicalThreadErrorCode** [8]: sePhysicalThreadNoError=0, sePhysicalThreadUnknownError=1, sePhysicalThreadProfileCreationError=2, sePhysicalThreadHelixCreationError=3, sePhysicalThreadBooleanOperationError=4, ... (8 total)
- **PipeFittingEndTreatmentConstants** [6]: sePipeFittingEndTreatmentNone=0, sePipeFittingEndTreatmentSocketWeld=1, sePipeFittingEndTreatmentButtWeld=2, sePipeFittingEndTreatmentFlange=3, sePipeFittingEndTreatmentThread=4, ... (6 total)
- **PipeFittingTypeConstants** [10]: sePipeFittingTypeNone=0, sePipeFittingTypeElbow=1, sePipeFittingTypeY=2, sePipeFittingTypeTee=3, sePipeFittingTypeCoupling=4, ... (10 total)
- **PlacementMethodConstants** [4]: igByOrigin=1, igByFrameBoundaries=2, igByCascadeMethod=3, igByDefaultStateData=4
- **PointTypeConstants** [4]: igSpacePoint=0, igKeyPoint=1, igCylinderStartPoint=2, igCylinderEndPoint=3
- **PowerPrecisionConstants** [8]: sePowerPrecisionOnes=0, sePowerPrecisionTenths=1, sePowerPrecisionHundredths=2, sePowerPrecisionThousandths=3, sePowerPrecisionTenThousandths=4, ... (8 total)
- **PrecisionConstants** [10]: igPrecisionOnes=0, igPrecisionTenths=1, igPrecisionHundredths=2, igPrecisionThousandths=3, igPrecisionTenThousandths=4, ... (10 total)
- **PredefineRelationGroupPolarityConstants** [4]: MagneticGroup=0, SPoleGroup=1, NPoleGroup=2, CaptureFitGroup=3
- **PressurePrecisionConstants** [8]: igPressurePrecisionOnes=0, igPressurePrecisionTenths=1, igPressurePrecisionHundredths=2, igPressurePrecisionThousandths=3, igPressurePrecisionTenThousandths=4, ... (8 total)
- **Print3DFileType** [2]: e3DPrint_STL=1, e3DPrint_3MF=2
- **PrintRangeConstants** [4]: igPrintAll=1, igPrintSelected=2, igPrintSpecified=3, igPrintCurrentDisplay=4
- **ProfileCommandConstants** [129]: ProfileEditDelete=10100, ProfileFileProperties=10146, ProfileViewZoom=10194, ProfileViewZoomArea=10201, ProfileViewFit=10202, ... (129 total)
- **ProfileHoleCommandConstants** [129]: ProfileHoleEditDelete=10100, ProfileHoleFileProperties=10146, ProfileHoleViewZoom=10194, ProfileHoleViewZoomArea=10201, ProfileHoleViewFit=10202, ... (129 total)
- **ProfilePatternCommandConstants** [129]: ProfilePatternEditDelete=10100, ProfilePatternFileProperties=10146, ProfilePatternViewZoom=10194, ProfilePatternViewZoomArea=10201, ProfilePatternViewFit=10202, ... (129 total)
- **ProfileRevolvedCommandConstants** [131]: ProfileRevolvedEditDelete=10100, ProfileRevolvedFileProperties=10146, ProfileRevolvedViewZoom=10194, ProfileRevolvedViewZoomArea=10201, ProfileRevolvedViewFit=10202, ... (131 total)
- **ProfileValidationStatus** [2]: igProfileStatusInvalid=-1, igProfileStatusValid=0
- **ProfileValidationType** [7]: igProfileClosed=1, igProfileSingle=4, igProfileNoSelfIntersect=8, igProfileRefAxisRequired=16, igProfileNoRefAxisIntersect=32, ... (7 total)
- **PropertyFilterTypeConstants** [7]: sePropertyFilterTypeFace=1, sePropertyFilterTypeFaceChain=2, sePropertyFilterTypeFeatureEdges=3, sePropertyFilterTypeFeatureFaces=4, sePropertyFilterTypeEdge=5, ... (7 total)
- **PropertyTableConstants** [3]: seCustomPropertyQueryAllProperties=1, seCustomPropertyQueryByTable=2, seCustomPropertyQueryByNameAndValue=3
- **PropertyTextErrorConstants** [3]: sePropertyTextDoNotShowError=0, sePropertyTextSolidEdgeError=1, sePropertyTextMyError=2
- **PropertyTypeConstants** [3]: sePropertyTypeDouble=1, sePropertyTypeString=2, sePropertyTypeInteger=3
- **QueryConditionConstants** [3]: seQueryConditionContains=0, seQueryConditionIs=1, seQueryConditionIsNot=2
- **QueryPropertyConstants** [17]: seQueryPropertyName=0, seQueryPropertyTitle=1, seQueryPropertySubject=2, seQueryPropertyAuthor=3, seQueryPropertyManager=4, ... (17 total)
- **QueryReferenceConstants** [7]: seQueryReferenceExcludedFromBOM=0, seQueryReferenceHiddenInDrawing=1, seQueryReferenceHiddenNextLevel=2, seQueryReferenceExcludedFromPhysProps=3, seQueryReferenceNotSelectable=4, ... (7 total)
- **QueryScopeConstants** [4]: seQueryScopeAllParts=0, seQueryScopeShownParts=1, seQueryScopeHiddenParts=2, seQueryScopeSelectedParts=3
- **QueryStatusConstants** [4]: seQueryStatusAvailable=0, seQueryStatusInWork=1, seQueryStatusInReview=2, seQueryStatusReleased=3
- **RadialHatchElementCenterLocation** [10]: igRadialHatchElementCenterUnknown=0, igRadialHatchElementCenterTopLeft=1, igRadialHatchElementCenterTopMid=2, igRadialHatchElementCenterTopRight=3, igRadialHatchElementCenterMidLeft=4, ... (10 total)
- **RayIntersectionEntityConstants** [3]: seFace=1, seEdge=2, seVertex=3
- **RayIntersectionTypeConstants** [4]: seTypeUnknown=0, seSilhouette=1, seEnter=2, seExit=3
- **RecomputeAsmSketchEditConstants** [3]: seRecomputeAsmSketchEditDisableWindow=0, seRecomputeAsmSketchEditRecomputeDuringEdit=1, seRecomputeAsmSketchEditecomputeAfterEdit=2
- **RedefineFaceTangencyType** [4]: igRedefineFaceNormalToPlane=20, igRedefineFaceTangentContinuous=50, igRedefineFaceNatural=113, igRedefineFaceCurvatureContinuous=171
- **ReferenceElementConstants** [29]: igRefEleInit=0, igReverseNormalSide=1, igNormalSide=2, igPivotStart=3, igPivotEnd=4, ... (29 total)
- **ReferencePointCloudDensity** [4]: seMaximumDensity=1, seMediumDensity=2, seLowDensity=3, seMinimumDensity=4
- **ReferencePointTypeEnumForFromPointOption** [2]: sePatternReferenceTypeFromCoOrdinateSystem=0, sePatternReferenceTypeFromKeyPoint=1
- **ReferencePointTypeEnumForToPointOption** [2]: sePatternReferenceTypeToKeyPoint=0, sePatternReferenceTypeToExcelFirstRow=1
- **ReferencedObjectTypeConstants** [11]: igReferencedObjectTypeNone=0, igReferencedObjectTypeCallout=1, igReferencedObjectTypeBalloon=2, igReferencedObjectTypeDatumFrame=3, igReferencedObjectTypeDatumTarget=4, ... (11 total)
- **ReflectivePlaneConstants** [9]: igReflectivePlane=1, igTopPlane=2, igRightPlane=3, igFrontPlane=4, igTopPlaneDistance=5, ... (9 total)
- **Relation3dDetailedStatusConstants** [7]: igRelation3dDetailedStatusUnknown=0, igRelation3dDetailedStatusSolved=1, igRelation3dDetailedStatusSuppressed=2, igRelation3dDetailedStatusBetweenSetMembers=3, igRelation3dDetailedStatusBetweenFixed=4, ... (7 total)
- **Relation3dGearRatioTypeConstants** [2]: igRelation3dGearRatioTypeNumberOfTurns=0, igRelation3dGearRatioTypeNumberOfTeeth=1
- **Relation3dGearTypeConstants** [3]: igRelation3dGearTypeRotaryRotary=0, igRelation3dGearTypeRotaryLinear=1, igRelation3dGearTypeLinearLinear=2
- **Relation3dGeometryConstants** [12]: igRelation3dGeometryPlane=1, igRelation3dGeometryLine=2, igRelation3dGeometryPoint=3, igRelation3dStartPoint=4, igRelation3dMidPoint=5, ... (12 total)
- **Relation3dOrientationConstants** [3]: igRelation3dOrientationNotspecified=0, igRelation3dOrientationAlign=1, igRelation3dOrientationAntialign=2
- **Relation3dStatusConstants** [2]: igRelation3dStatusUnsolved=0, igRelation3dStatusSolved=1
- **RevisionManagerAction** [14]: UnknownAction=0, CopyAction=1, CopyAllAction=2, ReviseAction=3, ReviseAllAction=4, ... (14 total)
- **RevisionRuleType** [5]: LastSavedType=0, LatestReleasedRevision=1, LatestRevision=2, ExternalBOM=3, VersionFromCache=4
- **RibbonBarConstants** [1]: seWM_ACCELERATORSELECTED=4226
- **RibbonBarControlSize** [3]: seRibbonBarControlSizeDefault=0, seRibbonBarControlSizeSmall=1, seRibbonBarControlSizeLarge=2
- **RibbonBarControlText** [3]: seRibbonBarControlTextDefault=0, seRibbonBarControlTextOn=1, seRibbonBarControlTextOff=2
- **RibbonBarInsertMode** [6]: seRibbonBarInsertCopy=0, seRibbonBarInsertMove=1, seRibbonBarInsertCreate=2, seRibbonBarInsertCreateButton=3, seRibbonBarInsertCreatePopup=4, ... (6 total)
- **RoundTypeConstants** [2]: igConstantRadius=1, igVariableRadius=2
- **RouteStatus** [4]: igInvalidSlip=0, igRouteComplete=1, igNotYetRouted=2, igRouteInProgress=3
- **RouteType** [2]: igOneAfterAnother=0, igAllAtOnce=1
- **RuledSurfaceDirectionConstants** [2]: igRuledSurfaceleft=1, igRuledSurfacRight=2
- **RuledSurfaceSideConstants** [2]: igRuledSurfaceInside=1, igRuledSurfaceOutside=2
- **RuledSurfaceTypeConstants** [5]: igRuledTangentContinuous=1, igRuledNormalToPlane=2, igRuledNatural=3, igRuledTaperedToPlane=4, igRuledAlongAnAxis=5
- **SEBlendRadiusType** [3]: igBlendRadiusAutomatic=0, igBlendRadiusFixAxis=1, igBlendRadiusFixUnders=2
- **SECommandActivation** [8]: seCmdActive_Enabled=1, seCmdActive_Checked=2, seCmdActive_ChangeText=4, seCmdActive_UseDotMark=8, seCmdActive_UseBitmap=16, ... (8 total)
- **SECommandBarModeConstants** [2]: seApplicationGlobalShowCommandBarMode=1, seApplicationGlobalShowQuickBarMode=2
- **SEECOptions** [2]: SEEC_eUnknownOption=0, SEEC_SearchLimit=1
- **SEFamilyOfPartsOptionConstants** [7]: SEFamilyOfPartsOptionFlatPattern=1, SEFamilyOfPartsOptionSimplify=2, SEFamilyOfPartsOptionCoordinateSystems=4, SEFamilyOfPartsOptionReferencePlanes=8, SEFamilyOfPartsOptionSketches=16, ... (7 total)
- **SEFenceMode** [2]: SEFenceModeRectangular=0, SEFenceModePolygonLasso=1
- **SEFenceOption** [3]: SEFenceOptionDirectional=0, SEFenceOptionOverlap=1, SEFenceOptionInside=2
- **SEFixedLengthConstraintDirection** [6]: igConstraintDirectionNone=0, igConstraintDirectionNoAxis=1, igConstraintDirectionXAxis=2, igConstraintDirectionYAxis=3, igConstraintDirectionZAxis=4, ... (6 total)
- **SELicenseCheck** [3]: SELicenserConsume=1, SELicenserReturn=2, SELicenserIsPresent=3
- **SEPatternRecognitionLevel** [3]: igFeaturesPattern=0, igLevelTwoPattern=1, igLevelThreePattern=2
- **SESubtractDirection** [3]: igSubtractDirectionNone=0, igSubtractDirectionRight=1, igSubtractDirectionLeft=2
- **SETargetConstructionBodyOption** [2]: igCreateMultipleConstructionBodiesOnNonManifoldOption=0, igCreateSingleConstructionGeneralBodyOnNonManifoldOption=1
- **SETargetDesignBodyOption** [3]: igCreateMultipleDesignBodiesOnNonManifoldOption=0, igFailOnNonManifoldOption=1, igCreateSingleDesignBodyOnNonManifoldOption=2
- **SEUserTypeConstants** [3]: seApplicationGlobalSEUsertypeMixed=1, seApplicationGlobalSEUsertypeTrad=2, seApplicationGlobalSEUsertypeSync=3
- **SPServerType** [6]: SERVER_TYPE_NOT_SHAREPOINT=0, SHAREPOINT_V1_SERVER=1, SHAREPOINT_V2_SERVER=2, SHAREPOINT_V3_SERVER=3, SHAREPOINT_V4_SERVER=4, ... (6 total)
- **SaveAsFlatFileTypes** [3]: igAutoCAD=0, igPart_Document=1, igSheet_Metal_Document=2
- **SaveAsHarnessFileFormats** [3]: HarnessFileFormatHX2ML=0, HarnessFileFormatDSI=1, HarnessFileFormatX2ML=2
- **SaveAsHarnessTopologyStatusConstants** [2]: seSaveAsHarnessTopologyStatus_Success=0, seSaveAsHarnessTopologyStatus_FailedBadArgs=1
- **SaveBodyConstants** [4]: seSaveBodyAsPartDocument=0, seSaveBodyAsSheetMetalDocument=1, seSaveBodyAsParasolidText=2, seSaveBodyAsParasolidBinary=3
- **SaveOptions** [2]: SaveAs=0, SaveCopyAs=1
- **SeAnalysisModeType** [6]: seAnalysisModeDefault=0, seAnalysisModeZebraStripeLinear=1, seAnalysisModeZebraStripeSpherical=2, seAnalysisModeZebraStripeReflection=3, seAnalysisModeCurvatureColor=4, ... (6 total)
- **SeAnalysisStateType** [3]: seAnalysisStateNone=0, seAnalysisStateGlobal=1, seAnalysisStateLocal=2
- **SeAntiAliasLevel** [4]: seAntiAliasLevelNone=0, seAntiAliasLevelLow=2, seAntiAliasLevelMedium=4, seAntiAliasLevelHigh=8
- **SeBackgroundType** [6]: seBackgroundTypeSolid=0, seBackgroundTypeGradient=1, seBackgroundTypeImage=2, seBackgroundTypeImageReference=3, seBackgroundTypeStaticEnvironment=4, ... (6 total)
- **SeBarPosition** [5]: seBarTop=1, seBarBottom=2, seBarLeft=3, seBarRight=4, seBarFloating=5
- **SeBarType** [3]: seBarTypeMenuBar=1, seBarTypeNormal=2, seBarTypePopup=3
- **SeButtonState** [3]: seButtonDown=1, seButtonMixed=2, seButtonUp=3
- **SeButtonStyle** [9]: seButtonAutomatic=1, seButtonCaption=2, seButtonIcon=3, seButtonIconAndCaption=4, seButtonIconAndCaptionBelow=5, ... (9 total)
- **SeConnectMode** [3]: seConnectAtStartup=1, seConnectByUser=2, seConnectExternally=3
- **SeControlType** [3]: seControlPopup=1, seControlButton=2, seControlSeparator=3
- **SeDisconnectMode** [3]: seDisconnectAtShutdown=1, seDisconnectByUser=2, seDisconnectExternally=3
- **SeFeatureAddFlag** [5]: seNew=1, seUnSuppress=2, seUnSuppressUpTo=3, seNewPatternItem=4, seUnSuppressPatternItem=5
- **SeFeatureDeleteFlag** [5]: sePermanent=1, seSuppress=2, seSuppressDownTo=3, sePermanentPatternItem=4, seSuppressPatternItem=5
- **SeFeatureModifyFlag** [3]: seSchemaChanged=1, seDirectInputsChanged=2, seReordered=3
- **SeGradientType** [7]: seGradientTypeHorizontal=1, seGradientTypeVertical=2, seGradientTypeDiagonalUp=3, seGradientTypeDiagonalDown=4, seGradientTypeSquareSpot=5, ... (7 total)
- **SeHiddenLineMode** [3]: seHiddenLineModeOff=0, seHiddenLineModeDim=1, seHiddenLineModeDashed=2
- **SeImageQualityType** [3]: seImageQualityLow=1, seImageQualityMedium=2, seImageQualityHigh=3
- **SeModifySketchFlag** [3]: seInsertEntity=1, seRemoveEntity=2, seModifyEntity=3
- **SeObjectType** [3]: seObjectNamedViews=1, seObjectViewStyles=2, seObjectFaceStyles=3
- **SeRenderColorType** [4]: seRenderColorRGB=0, seRenderColorRGBA=1, seRenderColorColorIndex=2, seRenderColorCOLORREF=3
- **SeRenderFillMode** [3]: seRenderFillSolid=1, seRenderFillBorder=2, seRenderFillSolidBorder=3
- **SeRenderMaterialGetMode** [2]: seGetModeExisting=0, seGetModeCreateOnDemand=1
- **SeRenderMaterialSetMode** [4]: seSetModeDetach=0, seSetModeAttach=1, seSetModeUpdate=2, seSetModeAttachAndUpdate=3
- **SeRenderModeType** [12]: seRenderModeUndefined=0, seRenderModeWireframe=1, seRenderModeWiremesh=2, seRenderModeOutline=3, seRenderModeBoundary=4, ... (12 total)
- **SeRenderShadeMode** [2]: seRenderShadeModeFlat=1, seRenderShadeModeSmooth=2
- **SeRenderShapeType** [2]: seRenderShapeSquare=1, seRenderShapeRound=2
- **SeRenderSpaceType** [3]: seRenderSpaceDevice=0, seRenderSpacePaper=1, seRenderSpaceWorld=2
- **SeSkyboxSide** [6]: seSkyboxSideFront=0, seSkyboxSideRight=1, seSkyboxSideBack=2, seSkyboxSideLeft=3, seSkyboxSideBottom=4, ... (6 total)
- **SeSkyboxType** [5]: seSkyboxTypeUndefined=-1, seSkyboxTypeSkybox=0, seSkyboxTypeSingleImage=1, seSkyboxTypeSpheremap=2, seSkyboxTypePanoramic=3
- **SearchType** [2]: ShallowSearch=0, DeepSearch=1
- **SectionSketchesErrorCode** [4]: seSectionSketchesUnknownError=-1, seSectionSketchesNoError=0, seSectionSketchesNotPlaneIntersecting=1, seSectionSketchesSomePlaneIntersecting=2
- **SectionSketchesPlanesDirection** [3]: seSectionSketchesPlaneReverseNormalSide=-1, seSectionSketchesPlaneNormalSide=0, seSectionSketchesPlaneBothSide=1
- **SectionViewExtentSide** [6]: igLeftExtent=1, igRightExtent=2, igFiniteSymmetricExtent=3, igInfiniteLeftExtent=4, igInfiniteRightExtent=5, ... (6 total)
- **SectionViewPlaneExtentTypeConstant** [2]: SectionViewPlaneExtentTypeConstant_Bounded=1, SectionViewPlaneExtentTypeConstant_UnBounded=2
- **SectionViewPlaneType** [2]: igDynamic=1, igAssociative=2
- **SectionViewProfileSide** [4]: igLeftProfileSide=1, igRightProfileSide=2, igInsideProfileSide=3, igOutsideProfileSide=4
- **SeedOptionConstants** [2]: igSeedSingle=1, igSeedAll=2
- **SegmentRelation3dDirectionConstants** [3]: seSegmentRelation3dDirectionParallel=0, seSegmentRelation3dDirectionPerpendicular=1, seSegmentRelation3dDirectionCoincident=2
- **SegmentRelation3dDistanceConstants** [3]: seSegmentRelation3dDistanceNormal=0, seSegmentRelation3dDistanceReverse=1, seSegmentRelation3dDistanceTrueLength=2
- **SegmentRelation3dGeometryConstants** [9]: seSegmentRelation3dStartPoint=1, seSegmentRelation3dEndPoint=2, seSegmentRelation3dUnbounded=3, seSegmentRelation3dArcCenter=4, seSegmentRelation3dEllipseCenter=5, ... (9 total)
- **SegmentRelation3dStatusConstants** [2]: seSegmentRelation3dStatusUnsolved=0, seSegmentRelation3dStatusSolved=1
- **SensorDisplayTypeConstants** [3]: seSensorDisplayTypeInvalid=0, seSensorDisplayTypeHorizontalRange=1, seSensorDisplayTypeTrueFalse=2
- **SensorOperatorConstants** [7]: seSensorOperatorInvalid=0, seSensorOperatorGreaterThan=1, seSensorOperatorLessThan=2, seSensorOperatorEqualTo=3, seSensorOperatorNotEqualTo=4, ... (7 total)
- **SensorStatusConstants** [3]: seSensorStatusUpToDate=0, seSensorStatusOutOfDate=1, seSensorStatusInError=2
- **SensorTypeConstants** [4]: seSensorTypeInvalid=0, seSensorTypeVariable=1, seSensorTypeMinimumDistance=6, seSensorTypeUser=7
- **SensorUpdateMechanismConstants** [3]: seSensorUpdateMechanismInvalid=0, seSensorUpdateMechanismAutomatic=1, seSensorUpdateMechanismManual=2
- **SetColorConstants** [21]: seColorConstantsBlack=0, seColorConstantsDKRed=128, seColorConstantsRed=255, seColorConstantsDKGreen=32768, seColorConstantsDKYellow=32896, ... (21 total)
- **SheetFitConstants** [5]: igFitWorkingGraphicsOnly=0, igFitAll=1, igFitWorkingAndBackgroundGraphics=2, igFitBackgroundGraphicsOnly=3, igFitSheet=4
- **SheetMetalCommandConstants** [174]: SheetMetalConstructionUnitedBody=10855, SheetMetalConstructionRecoveredBody=10856, SheetMetalFormatStyle=25030, SheetMetalToolsVariables=25036, SheetMetalToolsPhysicalProperties=25038, ... (174 total)
- **SheetMetalDrawingViewTypeConstants** [3]: seSheetMetalDesignedView=0, seSheetMetalSimplifiedView=1, seSheetMetalFlatView=2
- **SheetMetalGlobalConstants** [26]: seSheetMetalGlobalDensity=1, seSheetMetalGlobalAccuracyForDensity=2, seSheetMetalGlobalMaterial=3, seSheetMetalGlobalMaterialThickness=4, seSheetMetalGlobalBendRadius=5, ... (26 total)
- **SheetMetalGlobalConstantsBendEquationType** [3]: seSheetMetalGlobalBendEquationStandard=1, seSheetMetalGlobalBendEquationCustom=2, seSheetMetalNeutralFactroFromExcel=3
- **SheetMetalGlobalConstantsFlatPatternCornerTreatmentType** [3]: seSheetMetalGlobalFlatPatternCornerTreatmentChamfer=1, seSheetMetalGlobalFlatPatternCornerTreatmentNone=2, seSheetMetalGlobalFlatPatternCornerTreatmentRadius=3
- **SheetMetalSensorFeatureTypeConstants** [8]: seSheetMetalSensorFeatureTypeExteriorEdges=0, seSheetMetalSensorFeatureTypeInteriorEdges=1, seSheetMetalSensorFeatureTypeCutouts=2, seSheetMetalSensorFeatureTypeHoles=3, seSheetMetalSensorFeatureTypeDimples=4, ... (8 total)
- **SheetSectionTypeConstants** [6]: igUnknownSection=-1, igWorkingSection=0, igBackgroundSection=1, igDrawingViewSection=2, ig2dModelSection=3, ... (6 total)
- **ShortCutMenuContextConstants** [7]: seShortCutForGraphicLocate=1, seShortCutForView=2, seShortCutForFeaturePathFinder=3, seShortCutForFeaturePathFinderDocument=4, seShortCutNone=5, ... (7 total)
- **SimplifiedAssemblyMode** [3]: seSimplifiedAssemblyModeUnknown=0, seSimplifiedAssemblyModeModeled=1, seSimplifiedAssemblyModeVisibleFaces=2
- **SimplifyBSplineEdgesConstants** [3]: seSimplifyBSplineEdgesAlways=0, seSimplifyBSplineEdgesOnlyEdgesOutside=1, seSimplifyBSplineEdgesNever=2
- **SimplifyCommandConstants** [82]: SimplifyFormatStyle=25030, SimplifyToolsVariables=25036, SimplifyToolsMacro=25040, SimplifyToolsOptions=25042, SimplifyViewPreviousView=25046, ... (82 total)
- **SizeModeConstants** [3]: igFrameCrops=1, igFrameChangesSize=2, igObjectScaled=3
- **Sketch3DCurveEndConditionConstants** [3]: seSketch3DCurveEndConditionNatural=1, seSketch3DCurveEndConditionNormalToFace=2, seSketch3DCurveEndConditionCurvatureContinuous=3
- **Sketch3DKeypointType** [9]: igSketch3DUnknown=0, igSketch3DStartPoint=1, igSketch3DEndPoint=2, igSketch3DMidPoint=4, igSketch3DCenter=5, ... (9 total)
- **Sketch3DRelationTypeConstants** [16]: igSketch3DConnect=0, igSketch3DParallel=1, igSketch3DPerpendicular=2, igSketch3DPointOn=3, igSketch3DInclude=4, ... (16 total)
- **SmartCollectionTypeConstants** [14]: seRoundableEdgesAtVertex=1, seRoundableSmoothEdgeChain=2, seRoundableEdgesOfFace=3, seRoundableEdgesOfLoop=4, seRoundableEdgesOfFeature=5, ... (14 total)
- **SolidEdgeCommandConstants** [9]: seConvertCommand=10452, seSurfaceVisualCommand=11129, seAssemblyPlacePartCommand=32791, seRefreshViewCommand=32876, sePartInsertPartCommand=40254, ... (9 total)
- **SolveTypeConstants** [2]: igSimple=1, igAdvanced=2
- **SpecificHeatPrecisionConstants** [8]: seSpecificHeatPrecisionOnes=0, seSpecificHeatPrecisionTenths=1, seSpecificHeatPrecisionHundredths=2, seSpecificHeatPrecisionThousandths=3, seSpecificHeatPrecisionTenThousandths=4, ... (8 total)
- **SpiralCurveMethodType** [3]: igSpiralCurveMethodEndDiameterAndTurns=0, igSpiralCurveMethodEndDiameterAndRadialPitch=1, igSpiralCurveMethodRadialPitchAndTurns=2
- **StaggerTypeConstants** [3]: seNoStagger=0, seRowStagger=1, seColumnStagger=2
- **StandardOLEVerbConstants** [7]: igOLEDiscardUndoState=-6, igOLEInPlaceActivate=-5, igOLEUIActivate=-4, igOLEHide=-3, igOLEOpen=-2, ... (7 total)
- **StartUsingTemplateConstants** [6]: seStartUsingTemplateNone=1, seStartUsingTemplatePart=2, seStartUsingTemplateSheetMetal=3, seStartUsingTemplateAssembly=4, seStartUsingTemplateWeldment=5, ... (6 total)
- **StitchWeldAnnotationFormat** [3]: seLengthPitch=1, seNXL=2, seNXL_E=3
- **StitchWeldType** [3]: seStitchOnly=1, seStitchPlusOffsets=2, seOffsetsOnly=3
- **StreeringWheelSizeConstants** [3]: seStreeringWheelSizeConstantsSmall=0, seStreeringWheelSizeConstantsMedium=1, sStreeringWheelSizeConstantsHigh=2
- **StructuralFrameEndConditionConstants** [12]: seMiter=0, seButt1=1, seButt2=2, seNone=3, seRadius=4, ... (12 total)
- **StructuralFrameExtendTrimPositionConstants** [2]: startPosition=0, endPosition=1
- **StructuralFrameOrientationConstants** [3]: seOrientXY=0, seOrientYZ=1, seOrientXZ=2
- **StudioCommandConstants** [64]: StudioAssemblyToolsMacro=25040, StudioAssemblyToolsOptions=25042, StudioViewPreviousView=25046, StudioViewNamedViews=25053, StudioHelpTipoftheDay=25062, ... (64 total)
- **StudyStatusType_Auto** [11]: eNoneStatus_Auto=0, eStudyGeomInError_Auto=1, eStudyMeshInError_Auto=2, eStudyResultsInError_Auto=3, eStudyReadyForMesh_Auto=4, ... (11 total)
- **StudyTypeConstants** [6]: seStudyTypeConstantsLinearStatic=1, seStudyTypeConstantsNormalModes=2, seStudyTypeConstantsLinearBuckling=3, seStudyTypeConstantsHeatTransfer=4, seStudyTypeConstantsHeatTransferLinearStatic=5, ... (6 total)
- **StyleConstants** [11]: seStyleConstantsVisibleReference=1, seStyleConstantsCenter=2, seStyleConstantsCuttingPlane=3, seStyleConstantsDotted=4, seStyleConstantsHidden=5, ... (11 total)
- **StyleUnitsConstant** [3]: PAPER_STYLEUNITS=11, DESIGN_STYLEUNITS=12, VIEW_STYLEUNITS=13
- **SubdivisionDragTypeConstants** [2]: igLinearMoveType=1, igRotateType=2
- **SubfixAlignmentConstants** [3]: seSubfixAlignLeft=0, seSubfixAlignCenter=1, seSubfixAlignRight=2
- **SuppressRegionsConstants** [2]: seSuppressRegionInside=4, seSuppressRegionOutside=5
- **SurfaceAreaSensorAreaTypeConstants** [2]: seSurfaceAreaSensorAreaTypeNeg=0, seSurfaceAreaSensorAreaTypePos=1
- **SurfaceAreaSensorSelectionTypeConstants** [2]: seSurfaceAreaSensorSelectFace=0, seSurfaceAreaSensorSelectFaceChain=1
- **SurfaceByBoundaryConstants** [2]: igSurfaceByBoundaryPreferPlanar=1, igSurfaceByBoundaryTangent=2
- **SurfaceByBoundaryFillPreference** [4]: igSurfaceByBoundaryFillSmooth=1, igSurfaceByBoundaryFillNonSmooth=2, igSurfaceByBoundaryFillPreferPlane=3, igSurfaceByBoundaryFillPlaneOnly=4
- **SurfaceByBoundaryInternalSmoothness** [2]: igSurfaceByBoundarySharp=1, igSurfaceByBoundarySmooth=2
- **SurfaceByBoundaryOptimise** [2]: igSurfaceByBoundaryQuality=1, igSurfaceByBoundaryPerformance=2
- **SurfaceByBoundaryPatchTopology** [3]: igSurfaceByBoundaryMinimal=1, igSurfaceByBoundarySingle=2, igSurfaceByBoundaryMultiple=3
- **SurfaceByBoundaryTangencyType** [3]: igSurfaceByBoundaryTangential=50, igSurfaceByBoundaryNatural=113, igSurfaceByBoundaryCurvatureContinuous=171
- **SyncOption** [2]: SEECSyncAll=0, SEECSyncOne=1
- **TCDownloadOptions** [13]: COImplicit=1, DoNotShowUnableToExportDlg=2, DoNotContinue=4, RevisionReplace=8, DoNotExpandAllGRMs=16, ... (13 total)
- **TCESETypes** [5]: TCE_SEPart=0, TCE_SEAssembly=1, TCE_SEWeldment=2, TCE_SESheetmetal=3, TCE_SEDraft=4
- **TabAndSlotExtentTypeConstants** [3]: TabAndSlotExtentTypeFinite=13, TabAndSlotExtentTypeFromTo=15, TabAndSlotExtentTypeToKeyPoint=72
- **TabAndSlotGapTypeConstants** [2]: SlotGapTypeSingle=0, SlotGapTypeMultiple=1
- **TabAndSlotPatternOffsetTypeConstants** [2]: TabAndSlotPatternOffsetTypeFit=0, TabAndSlotPatternOffsetTypeFill=1
- **TabAndSlotTreatmentTypeConstants** [3]: TabAndSlotTreatmentTypeNone=0, TabAndSlotTreatmentTypeRound=1, TabAndSlotTreatmentTypeChamfer=2
- **TableAnchorPoint** [4]: igUpperLeft=0, igUpperRight=1, igLowerLeft=2, igLowerRight=3
- **TableStyleLineTypeConstants** [7]: seBorder=0, seTitleSeparator=1, seTitleHeaderSeparator=2, seHeaderDataSeparator=3, seHeaderSeparator=4, ... (7 total)
- **TableTextOrientation** [3]: igHorizontal=0, igRotated=1, igVertical=2
- **TemperatureGradientPrecisionConstants** [8]: seTemperatureGradientPrecisionOnes=0, seTemperatureGradientPrecisionTenths=1, seTemperatureGradientPrecisionHundredths=2, seTemperatureGradientPrecisionThousandths=3, seTemperatureGradientPrecisionTenThousandths=4, ... (8 total)
- **TemperaturePrecisionConstants** [8]: igTemperaturePrecisionOnes=0, igTemperaturePrecisionTenths=1, igTemperaturePrecisionHundredths=2, igTemperaturePrecisionThousandths=3, igTemperaturePrecisionTenThousandths=4, ... (8 total)
- **TemplatesListType** [4]: eUnknownTemplateList=0, eStandardTemplateList=1, eUserTemplateList=2, eCustomTemplateList=3
- **TextBorderTypeConstants** [2]: igTextBorderNone=0, igTextBorderRectangle=1
- **TextBulletTypeConstants** [8]: igFilledRound=0, igHollowRound=1, igFilledSquare=2, igHollowSquare=3, igStar=4, ... (8 total)
- **TextControlTypeConstants** [3]: igTextFitToContent=0, igTextAdjustAspectRatio=1, igTextWrap=2
- **TextFlowDirectionConstants** [2]: igTextLeftToRight=0, igTextRightToLeft=1
- **TextFlowOrientationConstants** [2]: igTextHorizontal=0, igTextVertical=1
- **TextFractionAlignConstants** [3]: igUpper=1, igMiddle=2, igLower=3
- **TextFractionSizeConstants** [10]: ig10=0, ig20=1, ig30=2, ig40=3, ig50=4, ... (10 total)
- **TextFractionTypeConstants** [4]: igStacked=1, igTolerance=2, igSkewed=3, igLinearFraction=4
- **TextHorizontalAlignmentConstants** [5]: igTextHzAlignLeft=0, igTextHzAlignCenter=1, igTextHzAlignRight=2, igTextHzAlignIndent=3, igTextHzAlignJustify=16
- **TextJustificationConstants** [8]: igTextJustifyTop=0, igTextJustifyLeft=0, igTextJustifyCenter=1, igTextJustifyRight=2, igTextJustifyVCenter=4, ... (8 total)
- **TextLineSpacingTypeConstants** [6]: igSingle=0, igOneAndHalf=1, igDouble=2, igAtLeast=3, igExactly=4, ... (6 total)
- **TextNumberFormatConstants** [4]: igNoFormat=0, igPeriod=1, igBracket=2, igDoubleBrackets=3
- **TextNumberJustificationConstants** [3]: igLeftJustification=0, igCenterJustification=1, igRightJustification=2
- **TextNumberTypeConstants** [5]: igPlain=0, igCapitalRoman=1, igSmallRoman=2, igCapitalLatinAlpha=3, igSmallLatinAlpha=4
- **TextPlacementTypeConstants** [2]: igTextBoxType=1, igTextStringType=2
- **TextSelectConstants** [4]: seTextSelectRange=0, seTextSelectWord=1, seTextSelectParagraph=2, seTextSelectAll=5
- **TextSpecialIndentTypeConstants** [3]: igIndentNone=0, igFirstline=1, igHanging=2
- **TextStyleNumberJustificationConstants** [3]: igLeftJustificationStyle=0, igCenterJustificationStyle=1, igRightJustificationStyle=2
- **TextTabTypeConstants** [4]: igTextTabFlushLeft=1, igTextTabFlushRight=2, igTextTabFlushCentered=3, igTextTabFlushDecimal=4
- **TextVerticalAlignmentConstants** [3]: igTextVtAlignTop=0, igTextHzAlignVCenter=1, igTextHzAlignBottom=8
- **ThermalConductivityPrecisionConstants** [8]: seThermalConductivityPrecisionOnes=0, seThermalConductivityPrecisionTenths=1, seThermalConductivityPrecisionHundredths=2, seThermalConductivityPrecisionThousandths=3, seThermalConductivityPrecisionTenThousandths=4, ... (8 total)
- **ThreadDiameterOptionConstants** [4]: seTapDrillDiameter=0, seInternalMinorDiameter=1, seNominalDiameter=2, seInsidePipeDiameter=3
- **ThreadDisplayModeConstants** [4]: seThreadDisplayModeANSI=0, seThreadDisplayModeISO=1, seThreadDisplayModeJIS=3, seThreadDisplayModeJISISO=4
- **TitlePosition** [4]: igHeader=0, igFooter=1, igFooterAndHeader=2, igNeither=3
- **TopologyCollectionTypeConstants** [3]: seFaceCollection=1, seEdgeCollection=2, seVertexCollection=3
- **TorquePrecisionConstants** [8]: seTorquePrecisionOnes=0, seTorquePrecisionTenths=1, seTorquePrecisionHundredths=2, seTorquePrecisionThousandths=3, seTorquePrecisionTenThousandths=4, ... (8 total)
- **TreatmentCrownCurvatureSideConstants** [3]: seTreatmentCrownCurvatureInside=4, seTreatmentCrownCurvatureOutside=5, seTreatmentCrownCurvatureNone=44
- **TreatmentCrownSideConstants** [3]: seTreatmentCrownSideInside=4, seTreatmentCrownSideOutside=5, seTreatmentCrownSideNone=44
- **TreatmentCrownTypeConstants** [5]: seTreatmentCrownNone=0, seTreatmentCrownByRadius=1, seTreatmentCrownByRadiusAndTakeOffAngle=2, seTreatmentCrownByOffset=3, seTreatmentCrownByOffsetAndTakeOffAngle=4
- **TreatmentTypeConstants** [3]: seTreatmentNone=44, seTreatmentDraft=173, seTreatmentCrown=174
- **TrimExtendErrorCode** [6]: TrimExtendErrorCodeUnknownError=-1, TrimExtendErrorCodeNoError=0, TrimExtendErrorCodeMissingParameter=1, TrimExtendErrorCodeInvalidParameter=2, TrimExtendErrorCodeNoReferencePlane=3, ... (6 total)
- **TrimSurfaceAreaSideConstants** [2]: igTSLeft=1, igTSRight=2
- **TubeEndTreatmentTypeConstants** [5]: seTubeEndTreatmentTypeNone=1, seTubeEndTreatmentTypeExpand=2, seTubeEndTreatmentTypeFlange=3, seTubeEndTreatmentTypeClose=4, seTubeEndTreatmentTypeReduce=5
- **TubePropertyPidConstants** [9]: seTubePropertyPid_TubeBendRadius=1508, seTubePropertyPid_TubeOuterDiameter=1509, seTubePropertyPid_TubeMinimumFlatLength=1510, seTubePropertyPid_TubeWallThickness=1511, seTubePropertyPid_TubeFlatLength=1512, ... (9 total)
- **TubeSegmentAdditionStatusConstants** [4]: seTubeSegmentAdditionStatusSucceeded=1, seTubeSegmentAdditionStatusFailedSplit=2, seTubeSegmentAdditionStatusFailedDisjoint=3, seTubeSegmentAdditionStatusFailedUnknownReason=4
- **TubeSegmentRemovalStatusConstants** [4]: seTubeSegmentRemovalStatusSucceeded=1, seTubeSegmentRemovalStatusFailedNotPartOfTube=2, seTubeSegmentRemovalStatusFailedDueToDisjoint=3, seTubeSegmentRemovalStatusFailedUnknownReason=4
- **TubingCommandConstants** [107]: TubingXpresRouteRelationshipHandles=10210, TubingAssemblyToolsVariables=25036, TubingAssemblyToolsPhysicalProperties=25038, TubingAssemblyToolsCheckInterference=25039, TubingAssemblyToolsMacro=25040, ... (107 total)
- **UnitOfMeasureAngleReadoutConstants** [10]: seAngleRadian=0, seAngleDegree=1, seAngleMinute=2, seAngleSecond=3, seAngleGradient=4, ... (10 total)
- **UnitOfMeasureAngularAccelerationReadoutConstants** [9]: seradpersecondsq=0, seradperminutesq=1, seradperhoursq=2, sedegpersecondsq=3, sedegperminutesq=4, ... (9 total)
- **UnitOfMeasureAngularVelocityReadoutConstants** [9]: seRadianPerSecond=0, seRadianPerMinute=1, seRadianPerHour=2, seCyclePerSecond=3, seCyclePerMinute=4, ... (9 total)
- **UnitOfMeasureAreaReadoutConstants** [9]: seAreaInchSquared=0, seAreaFootSquared=1, seAreaYardSquared=2, seAreaMileSquared=3, seAreaAcre=4, ... (9 total)
- **UnitOfMeasureCoefOfThermalExpansionReadoutConstants** [4]: sePerFahrenheit=0, sePerKelvin=1, sePerRankine=2, sePerCelsius=3
- **UnitOfMeasureDensityReadoutConstants** [13]: seDensityPoundMassPerFootCubed=0, seDensityPoundMassPerInchCubed=1, seDensitySlugPerFootCubed=2, seDensitySlinchPerFootCubed=3, seDensityKilogramPerMeterCubed=4, ... (13 total)
- **UnitOfMeasureEnergyDensityReadoutConstants** [14]: seJoulepermetercu=0, secentijoulepercentimetercu=1, semillijoulepermillimetercu=2, semicrojoulepermetercu=3, sekilojoulepermetercu=4, ... (14 total)
- **UnitOfMeasureEnergyReadoutConstants** [13]: seEnergyJoule=0, seEnergycentijoule=1, seEnergymillijoule=2, seEnergymicrojoule=3, seEnergykilojoule=4, ... (13 total)
- **UnitOfMeasureForcePerAreaReadoutConstants** [13]: seForcePerAreaPascal=0, seForcePerAreaMilliPascal=1, seForcePerAreaKiloPascal=2, seForcePerAreaKiloNewton=3, seForcePerAreaMegaPascal=4, ... (13 total)
- **UnitOfMeasureForceReadoutConstants** [7]: seForceNewton=0, seForceNanoNewton=1, seForceMilliNewton=2, seForceKiloNewton=3, seForcePoundForce=4, ... (7 total)
- **UnitOfMeasureFrequencyReadoutConstants** [5]: seFrequencyPerSecond=0, seFrequencyPerMinute=1, seFrequencyPerHour=2, seFrequencyHertz=3, seFrequencyMegaHertz=4
- **UnitOfMeasureHeatFluxPerDistanceReadoutConstants** [14]: seWattsPerMeter=0, seKiloWattPerMeter=1, seWattsPerCentiMeter=2, seWattsPerMilliMeter=3, seWattsPerInch=4, ... (14 total)
- **UnitOfMeasureHeatFluxReadoutConstants** [14]: seWattsPerSqMeter=0, seKiloWattPerSqMeter=1, seWattsPerSqCentiMeter=2, seWattsPerSqMilliMeter=3, seWattsPerSqInch=4, ... (14 total)
- **UnitOfMeasureHeatGenerationReadoutConstants** [12]: seWattPerCuMeter=0, seKiloWattPerCuMeter=1, seWattPerCuCentiMeter=2, seWattPerCuMilliMeter=3, seWattPerCuInch=4, ... (12 total)
- **UnitOfMeasureHeatTransferCoefficientReadoutConstants** [10]: seWattsPerSqMeterKelvin=0, seKiloWattsPerSqMeterKelvin=1, seWattsPerSqCentiMeterKelvin=2, seWattsPerSqMeterCelcious=3, seBTUPerSqFootHourFahrenheit=4, ... (10 total)
- **UnitOfMeasureLengthReadoutConstants** [20]: seLengthInch=0, seLengthFoot=1, seLengthInchAbbr=2, seLengthFootAbbr=3, seLengthFootInch=4, ... (20 total)
- **UnitOfMeasureLinearAccelerationReadoutConstants** [9]: semillimeterspersecondsq=0, secentimeterspersecondsq=1, semeterspersecondsq=2, sekilometerspersecondsq=3, sekilometersperhoursq=4, ... (9 total)
- **UnitOfMeasureLinearDensityReadoutConstants** [9]: seSlugPerInch=0, seSlugPerFoot=1, seSlinchPerInch=2, sePoundPerInch=3, sePoundPerFoot=4, ... (9 total)
- **UnitOfMeasureLinearVelocityReadoutConstants** [9]: seMillimeterPerSecond=0, seCentimeterPerSecond=1, seMeterPerSecond=2, seKilometerPerSecond=3, seKilometerPerHour=4, ... (9 total)
- **UnitOfMeasureMassReadoutConstants** [9]: seMassSlug=0, seMassSlinch=1, seMassPoundMass=2, seMassTon=3, seMassNetTon=4, ... (9 total)
- **UnitOfMeasurePowerReadoutConstants** [19]: seWatt=0, seMilliWatt=1, seKiloWatt=2, seMegaWatt=3, seErgPerSecond=4, ... (19 total)
- **UnitOfMeasurePressureReadoutConstants** [12]: sePressurePascal=0, sePressureMilliPascal=1, sePressureKiloPascal=2, sePressureMegaPascal=3, sePressurePoundForcePerSqInch=4, ... (12 total)
- **UnitOfMeasureSpecificHeatReadoutConstants** [3]: seBTUPerPoundFahrenheit=0, seJoulePerKilogramKelvin=1, seJoulePerKilogramCelsius=2
- **UnitOfMeasureTemperatureGradientReadoutConstants** [10]: seKelvinPerMeter=0, seKelvinPerCentiMeter=1, seKelvinPerMilliMeter=2, seCelciousPerMeter=3, seCelciousPerCentiMeter=4, ... (10 total)
- **UnitOfMeasureTemperatureReadoutConstants** [4]: seKelvin=0, seCelcius=1, seRankine=2, seFahrenheit=3
- **UnitOfMeasureThermalConductivityReadoutConstants** [4]: seBTUPerHourFootFahrenheit=0, seInchPoundForcePerSecondInchFarhrenheit=1, seWattPerMeterCelsius=2, seKiloWattPerMeterCelsius=3
- **UnitOfMeasureTorqueReadoutConstants** [16]: seNewtonMeter=0, seNewtonMiliMeter=1, seNewtonCentiMeter=2, seKiloNewtonMeter=3, seDynesMeter=4, ... (16 total)
- **UnitOfMeasureVolumeReadoutConstants** [12]: seVolumeInchCubed=0, seVolumeFootCubed=1, seVolumeYardCubed=2, seVolumeGallon=3, seVolumeQuart=4, ... (12 total)
- **UnitTypeConstants** [63]: igUnitDistance=1, igUnitAngle=2, igUnitMass=3, igUnitTime=4, igUnitTemperature=5, ... (63 total)
- **UpdateOptionConstants** [3]: igUpdateAutomatic=1, igUpdateOnSave=2, igUpdateManual=3
- **UpdateStructureCacheConstants** [2]: seUseOpenDocuments=1, seWalkFilesOnDisk=2
- **UploadType** [2]: DeepUploadType=0, ShallowUploadType=1
- **VariableLimitValueConstant** [3]: igVariableLimitNone=0, igDiscreteList=1, igMinMaxLimit=2
- **VariableNameBy** [3]: seVariableNameByUser=0, seVariableNameBySystem=1, seVariableNameByBoth=2
- **VariableVarType** [7]: SeVariableVarTypeDimension=1, SeVariableVarTypeVariable=2, SeVariableVarTypeBoth=3, SeVariableVarTypePMIDimension=4, SeVariableVarSimulationVariable=8, ... (7 total)
- **VentDraftSideConstants** [2]: seVentDraftSideInward=4, seVentDraftSideOutward=5
- **VentExtentSideConstants** [2]: seVentReverseSketchPlaneNormalSide=1, seVentSketchPlaneNormalSide=2
- **VentExtentTypeConstants** [4]: seVentExtentTypeFinite=13, seVentExtentTypeThroughNext=14, seVentExtentTypeThroughAll=16, seVentExtentToKeyPoint=72
- **ViewAttributeConstants** [8]: seDisplayStatistics=1, seDisplaySectionCaps=2, seSoftwareVHL=3, seDynamicTransition=4, seApplicationDisplay=5, ... (8 total)
- **ViewOrientationConstants** [30]: igTopView=1, igRightView=2, igLeftView=3, igFrontView=4, igBottomView=5, ... (30 total)
- **VirtualComponentPublishConstants** [4]: seVCPublishOn_FrontView=1, seVCPublishOn_TopView=2, seVCPublishOn_RightView=3, seVCPublishOn_SketchView=4
- **VirtualComponentStatusConstants** [11]: seVCStatus_Success=1, seVCStatus_Fail=2, seVCStatus_AddUnManagedToManaged=3, seVCStatus_AddManagedToUnManaged=4, seVCStatus_ReplaceConflictWithVirtualComponent=5, ... (11 total)
- **VirtualComponentTypeConstants** [4]: seVirtualComponentType_Unknown=1, seVirtualComponentType_Assembly=2, seVirtualComponentType_Part=3, seVirtualComponentType_Sheetmetal=4
- **VisibilityBasedSimplifiedAssemblyCopyType** [2]: seVisibilityBasedSimplifiedAssemblyCopyTypeFaces=0, seVisibilityBasedSimplifiedAssemblyCopyTypeBodies=1
- **VolumePrecisionConstants** [8]: igVolumePrecisionOnes=0, igVolumePrecisionTenths=1, igVolumePrecisionHundredths=2, igVolumePrecisionThousandths=3, igVolumePrecisionTenThousandths=4, ... (8 total)
- **WallThicknessDisplayResolution** [3]: DisplayResolutionCoarse=0, DisplayResolutionStandard=1, DisplayResolutionFine=2
- **WebNetworkFeatureConstants** [6]: seWebNormal=1, seWebReverseNormal=2, seWebExtendToNext=3, seWebExtendFinite=4, seWebProfileExtend=5, ... (6 total)
- **WeldSymbolFlagDirectionConstants** [2]: igRightFlag=0, igLeftFlag=1
- **WeldmentCommandConstants** [134]: WeldmentFormatStyle=25030, WeldmentToolsVariables=25036, WeldmentToolsPhysicalProperties=25038, WeldmentToolsMacro=25040, WeldmentToolsOptions=25042, ... (134 total)
- **WeldmentDrawingViewTypeConstants** [3]: seWeldmentMachinedView=0, seWeldmentWeldedView=1, seWeldmentAssembledView=2
- **WeldmentGlobalConstants** [7]: seWeldmentGlobalDensity=1, seWeldmentGlobalAccuracyForDensity=2, seWeldmentGlobalBeadsDensity=3, seWeldmentGlobalMaterial=4, seWeldmentGlobalBeadMaterial=5, ... (7 total)
- **WeldmentLinkStatusConstants** [3]: seLinkOK=1, seLinkOutOfDate=2, seLinkBroken=3
- **WeldmentSectionTypeConstants** [4]: seWeldmentSectionTypeComponent=0, seWeldmentSectionTypeSurfacePrep=1, seWeldmentSectionTypeBead=2, seWeldmentSectionTypeMachining=3
- **WirePathConstants** [3]: seSingleWirePath=0, seCableWirePathMaster=1, seCableWirePathMember=2
- **WirePathConstantsEx** [3]: seSingleWirePathEx=0, seCableWirePathSource=1, seCableWirePathMemberEx=2
- **WorkflowAction** [4]: Initiate=0, Delegate=1, Accept=2, Reject=3
- **WorkflowType** [2]: OneStepRelease=0, QuickRelease=1
- **ZoomToolClickOptionsConstants** [6]: seZoomToolClickOptions2xZoomOut=1, seZoomToolClickOptions2xZoomIn=2, seZoomToolClickOptionsZoomArea=3, seZoomToolClickOptionsPan=4, seZoomToolClickOptionsSimplified=5, ... (6 total)
- **ZoomToolDragConstants** [3]: seZoomToolDragZoomArea=1, seZoomToolDragDynamicZoom=2, seZoomToolDragDynamicPan=3
- **__MIDL___MIDL_itf_constant_0001_0000_0001** [4]: DVShowHideEdgeOverrideIndeterminant=-1, DVShowHideEdgeOverrideNone=0, DVShowHideEdgeOverrideShow=1, DVShowHideEdgeOverrideHide=2
- **eCPDMode** [4]: CPD_NEW_FILE=1, CPD_UPLOAD_FILE=2, CPD_SAVEAS_FILE=3, CPD_REVISE_FILE=4
- **eSaveAllOption** [4]: saveAll_Select=1, saveAll_SaveAll=2, saveAll_DiscardAll=3, saveAll_Cancel=4
- **seActionProp** [3]: ReadProperties=0, WriteProperties=1, RemoveProperties=2
- **seAssemblyBodyTypeConstants** [3]: seAssemblyBodyType_WeldBeadBody=1, seAssemblyBodyType_HarnessBody=2, seAssemblyBodyType_GenericAssemblyBody=3
- **seButton** [3]: seLEFT=1, seRIGHT=2, seMIDDLE=4
- **seCmdFlag** [2]: seTerminateAfterActivation=1, seNoDeactivate=2
- **seCopytoPMIConstants** [3]: seCopytoPMIConstantsDimension=1, seCopytoPMIConstantsAnnotation=2, seCopytoPMIConstantsAll=3
- **seDynamicsModes** [4]: seDynamicsOff=0, seDynamicsLine=1, seDynamicsCircleByCenter=2, seDynamicsRectangle=3
- **seKey** [3]: seSHIFT=1, seCONTROL=2, seALT=4
- **seLocateFilterConstants** [77]: seLocateGeometry2d=0, seLocateArc2d=1, seLocateBspCurve2d=2, seLocateCircle2d=3, seLocateComplexString2d=4, ... (77 total)
- **seLocateModes** [4]: seSmartLocate=0, seLocateSimple=1, seLocateQuickPick=2, seLocateOff=3
- **seMouseAction** [4]: seDOWN=0, seUP=1, seMOVE=2, seDBLCLICK=3
- **seMouseDragState** [3]: seMouseEnterDrag=0, seMouseDrag=1, seMouseExitDrag=2
- **seMovieFormatConstants** [2]: seMovieFormatAVI=0, seMovieFormatWMV=1
- **seMovieStandardResolutionConstants** [5]: seMovieStandardResolutionNTSC=0, seMovieStandardResolutionPAL=1, seMovieStandardResolutionHD=2, seMovieStandardResolutionFullHD=3, seMovieStandardResolutionCurrentView=4
- **sePropValidationTypes** [2]: TCServerValidation=0, StorageValidation=1
- **seRefreshViewConstants** [3]: seRefreshAll=-1, seRefreshView=0, seRefreshGraphics=1
- **seSectionPlanesOptionsConstants** [5]: seSectionPlanesOptionsConvexResults=0, seSectionPlanesOptionsEnabled=1, seSectionPlanesOptionsConcaveResults=16, seSectionPlanesOptionsComplexResults=32, seSectionPlanesOptionsResultsMask=240
- **seSharpenLevelConstants** [9]: seSharpenDefault=0, seSharpenCoarse=1, seSharpenNormal=2, seSharpenFine=3, seSharpenExtraFine=4, ... (9 total)
- **seSteeringWheelConstants** [3]: seSteeringWheelConstantsXAxis=1, seSteeringWheelConstantsYAxis=2, seSteeringWheelConstantsZAxis=3
- **seStyleShaderConstant** [21]: seStyleShaderAutomatic=0, seStyleShaderGeneral=1, seStyleShaderAdvanced=2, seStyleShaderDiffuse=5, seStyleShaderEmissive=6, ... (21 total)
- **seStyleTypeConstants** [7]: igDimensionStyle=0, igDrawingViewStyle=1, igFillStyle=2, igHatchStyle=3, igLineStyle=4, ... (7 total)
- **seStyleVersionConstant** [5]: seStyleVersion=0, seStyleVersionEx=1, seStyleVersionCreated=2, seStyleVersionLastModified=3, seStyleVersionLastSaved=4
- **seUnitsTypeConstants** [2]: seUnitsType_DataBase=-730794371, seUnitsType_Document=1886781498
- **seVariableTypeConstants** [4]: seVariableType_Text=-170730141, seVariableType_Simulation=215773802, seVariableType_UserDefined=1560616706, seVariableType_Dimension=1661573600
- **uomPrecisionConstants** [18]: uomPrecisionOnes=0, uomPrecisionTenths=1, uomPrecisionHundredths=2, uomPrecisionThousandths=3, uomPrecisionTenThousandths=4, ... (18 total)

### Aliases (8)

- DVShowHideEdgeOverrideType = __MIDL___MIDL_itf_constant_0001_0000_0001
- MatTablePropIndex = MatTablePropIndexConstants
- SheetMetalGlobalBendEquationConstants = SheetMetalGlobalConstantsBendEquationType
- SheetMetalGlobalFlatPatternCornerTreatmentConstants = SheetMetalGlobalConstantsFlatPatternCornerTreatmentType
- seAssemblyChangeEventsConstants = AssemblyChangeEventsConstants
- seAssemblyEventConstants = AssemblyEventConstants
- seStyleShaderConstants = seStyleShaderConstant
- seStyleVersionConstants = seStyleVersionConstant

---
## Program/ddmseapi.tlb
**Dynamic Designer Motion Solid Edge Type Library** (GUID: `{5FC1B7D8-1CDE-4784-B1C1-DA062DEE7FAD}`, v1.0)

### Enums (17)

- **DDMAutoMapParts** [4]: MapOff=0, MapOn=1, MapAsk=2, MapDefault=3
- **DDMDlgTestTypes** [17]: DDMJoint=1, DDMContact=2, DDMMotion=3, DDMSpring=4, DDMDamper=5, ... (17 total)
- **DDMElementType** [23]: DDMElement_part=1, DDMElement_joint=2, DDMElement_constrainedJoint=3, DDMElement_pointCurve=4, DDMElement_curveCurve=5, ... (23 total)
- **DDMForceUnits** [10]: DDMForce_kilogram=1, DDMForce_newton=2, DDMForce_kilonewton=3, DDMForce_pound=4, DDMForce_kilopound=5, ... (10 total)
- **DDMFunctionType** [5]: DDMFunction_constant=1, DDMFunction_step=2, DDMFunction_harmonic=3, DDMFunction_dataPoints=4, DDMFunction_expression=5
- **DDMIntegratorType** [3]: DDMIntegrator_GSTIFF=1, DDMIntegrator_WSTIFF=2, DDMIntegrator_SI2_GSTIFF=3
- **DDMJointType** [55]: DDMJoint_revolute=1, DDMJoint_cylindrical=2, DDMJoint_translational=3, DDMJoint_spherical=4, DDMJoint_planar=5, ... (55 total)
- **DDMMessageType** [4]: DDMMessageType_ErrorsAndWarnings=1, DDMMessageType_ErrorsOnly=2, DDMMessageType_AllMessages=3, DDMMessageType_NoMessages=4
- **DDMMotionType** [5]: DDMMotion_fixed=1, DDMMotion_free=2, DDMMotion_displacement=3, DDMMotion_velocity=4, DDMMotion_acceleration=5
- **DDMPartMotionType** [3]: DDMPart_excluded=1, DDMPart_moving=2, DDMPart_grounded=3
- **DDMPartParameterSource** [3]: DDMPart_useUserSettings=1, DDMPart_useMaterial=2, DDMPart_usePart=3
- **DDMPlotResult** [28]: DDMPlot_TranslationalDisplacement=1, DDMPlot_TranslationalVelocity=2, DDMPlot_TranslationalAcceleration=3, DDMPlot_AngularVelocity=4, DDMPlot_AngularAcceleration=5, ... (28 total)
- **DDMPlotXAxis** [3]: DDMPlot_vsTime=1, DDMPlot_vsFrame=2, DDMPlot_vsResult=3
- **DDMProductId** [3]: DDMProduct_SimplyMotion=1, DDMProduct_Motion=2, DDMProduct_MotionProfessional=3
- **DDMResultsComponent** [4]: DDMComponent_x=1, DDMComponent_y=2, DDMComponent_z=3, DDMComponent_magnitude=4
- **DDMStatusType** [3]: DDMSolveFailed=1, DDMSaveFailed=2, DDMSucceeded=3
- **DDMTimeUnits** [4]: DDMTime_hour=1, DDMTime_minute=2, DDMTime_second=3, DDMTime_millisecond=4

### Interfaces (47)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| IDDMADisplacement | dispatch | 2 | 12 |
| IDDMActionOnlyForce | dispatch | 3 | 16 |
| IDDMActionReactionForce | dispatch | 3 | 17 |
| IDDMAddin | dispatch | 14 | 2 |
| IDDMAssembly | dispatch | 5 | 6 |
| IDDMBushing | dispatch | 2 | 33 |
| IDDMConnector | dispatch | 3 | 12 |
| IDDMConnectors | dispatch | 1 | 1 |
| IDDMConstrainedJoint | dispatch | 4 | 19 |
| IDDMContact3D | dispatch | 3 | 8 |
| IDDMContactPair | dispatch | 2 | 12 |
| IDDMContactProperties | dispatch | 0 | 13 |
| IDDMCoupler | dispatch | 0 | 11 |
| IDDMCurve | dispatch | 4 | 6 |
| IDDMCurveCurve | dispatch | 3 | 16 |
| IDDMDamper | dispatch | 3 | 17 |
| IDDMElement | dispatch | 0 | 5 |
| IDDMElements | dispatch | 1 | 1 |
| IDDMFea | dispatch | 1 | 0 |
| IDDMFunction | dispatch | 11 | 2 |
| IDDMGravity | dispatch | 2 | 2 |
| IDDMImpact | dispatch | 3 | 17 |
| IDDMIntegrator | dispatch | 0 | 8 |
| IDDMJoint | dispatch | 3 | 20 |
| IDDMJointFriction | dispatch | 2 | 7 |
| IDDMJoints | dispatch | 2 | 1 |
| IDDMLDisplacement | dispatch | 2 | 11 |
| IDDMLinearAcceleration | dispatch | 2 | 12 |
| IDDMLinearVelocity | dispatch | 2 | 12 |
| IDDMLocation | dispatch | 2 | 4 |
| IDDMMechanism | dispatch | 41 | 22 |
| IDDMMotion | dispatch | 0 | 5 |
| IDDMMotions | dispatch | 0 | 6 |
| IDDMOrientation | dispatch | 2 | 5 |
| IDDMPart | dispatch | 10 | 18 |
| IDDMPartMotion | dispatch | 3 | 16 |
| IDDMParts | dispatch | 1 | 1 |
| IDDMPlot | dispatch | 7 | 9 |
| IDDMPlots | dispatch | 1 | 1 |
| IDDMPointCurve | dispatch | 3 | 14 |
| IDDMReactionForce | dispatch | 0 | 10 |
| IDDMReactionForces | dispatch | 1 | 1 |
| IDDMSimulation | dispatch | 29 | 6 |
| IDDMSourceObjects | dispatch | 1 | 1 |
| IDDMSpring | dispatch | 3 | 24 |
| IDDMTracePath | dispatch | 5 | 14 |
| _IDDMAddinEvents | dispatch | 1 | 0 |

### CoClasses (46)

- **DDMADisplacement** (`{4708EF36-C224-48E4-844F-12EC4BDE66EA}`): IDDMADisplacement
- **DDMActionOnlyForce** (`{B6FF1306-FCF0-440D-BDC6-6934BE2DC038}`): IDDMActionOnlyForce
- **DDMActionReactionForce** (`{8343703F-BCFE-4FB1-BED9-2DBC770BFEA9}`): IDDMActionReactionForce
- **DDMAssembly** (`{3C9688ED-BDF7-4C40-9134-35C2F3F18EEF}`): IDDMAssembly
- **DDMBushing** (`{1385EC95-9D9C-11D6-BFEF-009027DFCC3E}`): IDDMBushing
- **DDMConnector** (`{488C8F51-ADC2-40D6-9E55-51792B3B9AA7}`): IDDMConnector
- **DDMConnectors** (`{9EE7F3EF-8804-4FA8-81F8-B644070E078C}`): IDDMConnectors
- **DDMConstrainedJoint** (`{07372BDC-6652-49A9-A54E-D59ECFAACBB3}`): IDDMConstrainedJoint
- **DDMContact3D** (`{D1C90A2D-768E-41C6-93D2-CDB8BCB80157}`): IDDMContact3D
- **DDMContactPair** (`{FED40896-F3C8-465C-9053-126A8452E6A5}`): IDDMContactPair
- **DDMContactProperties** (`{5D0D266D-D217-4ADB-BAE6-83F40B1F6E68}`): IDDMContactProperties
- **DDMCoupler** (`{7BA7D548-22D1-49AF-95E9-AF0C6D21D48E}`): IDDMCoupler
- **DDMCurve** (`{90204DAD-B33A-432F-9C8A-E0C8F72BE414}`): IDDMCurve
- **DDMCurveCurve** (`{63096A88-5362-4EA8-9793-59B3F7A01C94}`): IDDMCurveCurve
- **DDMDamper** (`{0FCB68FC-D5F0-41DB-9D1D-8B85501EFA0F}`): IDDMDamper
- **DDMElement** (`{3EF442EF-F972-4CA1-8F98-C7E581453AA6}`): IDDMElement
- **DDMElements** (`{F5C6F209-2BCE-41B6-B275-7A1C03557A89}`): IDDMElements
- **DDMFea** (`{6E108803-2AC4-49EE-A18E-49CDF301AE9D}`): IDDMFea
- **DDMFunction** (`{E8EFCE78-270F-4122-9902-BDE1C1D9CB92}`): IDDMFunction
- **DDMGravity** (`{96BC1AD2-809F-4FCA-88AC-4558A95293F3}`): IDDMGravity
- **DDMImpact** (`{DD370474-D0AB-454D-9328-CCBF7B526B07}`): IDDMImpact
- **DDMIntegrator** (`{DF34AC41-EE79-452D-A984-DBDC5E14C591}`): IDDMIntegrator
- **DDMJoint** (`{188810D8-E461-4554-98A4-6123DB99D6AC}`): IDDMJoint
- **DDMJointFriction** (`{5B64E3F3-85E8-49A4-943B-AEA3C56C4595}`): IDDMJointFriction
- **DDMJoints** (`{308E19E8-1B91-402D-B637-86D4CF95EB75}`): IDDMJoints
- **DDMLDisplacement** (`{55C22E35-2688-4E68-AED1-925B189A9CAC}`): IDDMLDisplacement
- **DDMLinearAcceleration** (`{102EBC53-3B1D-4486-8EF3-D20EDD0A319C}`): IDDMLinearAcceleration
- **DDMLinearVelocity** (`{D29A2734-B1FD-43C6-B187-ED9DD4A91509}`): IDDMLinearVelocity
- **DDMLocation** (`{F2C655A3-A809-4E1E-92D0-950B87B0E0E1}`): IDDMLocation
- **DDMMechanism** (`{4E740AED-5959-427B-8A01-F184F6FCCBCC}`): IDDMMechanism
- **DDMMotion** (`{1F87A4DE-DBE8-492E-B6A7-479D44D0215D}`): IDDMMotion
- **DDMMotions** (`{64AB3E63-EEED-459A-8EAE-B595D147FCA6}`): IDDMMotions
- **DDMOrientation** (`{7493454E-2E41-40B3-B710-62C55485CB68}`): IDDMOrientation
- **DDMPart** (`{CE9C859D-51B3-485E-84C8-471EA63734D0}`): IDDMPart
- **DDMPartMotion** (`{5F0583D9-9312-464D-9291-B94EED314468}`): IDDMPartMotion
- **DDMParts** (`{8F57334C-4B70-4857-BC03-C097343E1EE1}`): IDDMParts
- **DDMPlot** (`{997B37C6-B537-41F2-BE4C-6EDCC076F129}`): IDDMPlot
- **DDMPlots** (`{9786FB68-0E48-4404-8BEC-24BB7A9ECB41}`): IDDMPlots
- **DDMPointCurve** (`{C00CAF43-A88E-4769-9989-F23701EAA91B}`): IDDMPointCurve
- **DDMReactionForce** (`{4E77FF12-4AA2-4801-A636-89BEF619195A}`): IDDMReactionForce
- **DDMReactionForces** (`{3E32DBF7-9860-48EF-98EC-1410C4776FB0}`): IDDMReactionForces
- **DDMSEAddin** (`{EBCF41F8-2492-4CFB-AA28-2A57D02EDE62}`): IDDMAddin
- **DDMSimulation** (`{034CC4E4-BC54-475D-96A6-8541E494B9D5}`): IDDMSimulation
- **DDMSourceObjects** (`{5E7195FA-23DB-4660-8CF3-2BD9B6D8BB82}`): IDDMSourceObjects
- **DDMSpring** (`{E778C5E1-FD2F-47EF-90C0-C9F1055A7006}`): IDDMSpring
- **DDMTracePath** (`{95E88A08-A1C6-4254-9CE5-664C566E0C03}`): IDDMTracePath

---
## Program/draft.tlb
**Solid Edge Draft Type Library** (GUID: `{3E2B3BDC-F0B9-11D1-BDFD-080036B4D502}`, v1.0)

### Enums (78)

- **AssemblyDrawingViewTypeConstants** [3]: seAssemblyDesignedView=0, seAssemblySimplifiedView=1, seAssemblyConfigurationSimplifiedView=2
- **BlockLabelOriginLocationConstants** [12]: igBlockLabelTopLeft=0, igBlockLabelTopCenter=1, igBlockLabelTopRight=2, igBlockLabelMiddleLeft=3, igBlockLabelMiddleCenter=4, ... (12 total)
- **BlockTableType** [2]: igBlockOnlyList=0, igBlockViewList=1
- **BreakLinePairDirConstants** [2]: igBreakLinePairDirConstants_Vertical=0, igBreakLinePairDirConstants_Horizontal=1
- **BreakLinePairOrientConstants** [2]: igBreakLinePairOrientConstants_Default=0, igBreakLinePairOrientConstants_Explicit=1
- **BreakLinePairTypeConstants** [5]: igBreakLinePairTypeConstants_Straight=0, igBreakLinePairTypeConstants_Cylindrical=1, igBreakLinePairTypeConstants_ShortBreak=2, igBreakLinePairTypeConstants_LongBreak=3, igBreakLinePairTypeConstants_ShortCurvedBreak=4
- **CleanProfileOptions** [2]: igCleanProfileDelete=1, igCleanProfileMove=2
- **CollectDataFlag** [8]: PartData=0, SheetSizeData=1, DrawingViewScaleData=2, OrthogonalViewData=4, IsoMetricViewData=8, ... (8 total)
- **CoordinateSystem2dAxisConstants** [2]: seCoordinateSystem2dAxisLow=0, seCoordinateSystem2dAxisHigh=1
- **DVThreadDisplayModeConstants** [5]: seDVThreadDisplayModeANSI=0, seDVThreadDisplayModeISO=1, seDVThreadDisplayModeJIS=2, seDVThreadDisplayModeJISISO=3, seDVThreadDisplayModeESKD=4
- **DetailEnvelopeStandardConstants** [3]: seDetailEnvelopeANSI=0, seDetailEnvelopeISO=1, seDetailEnvelopeESKD=2
- **DimWeldBeadWeldImportConstants** [3]: igDimWeldBeadWeldImportUnknown=0, igDimWeldBeadWeldImportLocal=1, igDimWeldBeadWeldImportImported=2
- **DimWeldBeadWeldStandardConstants** [4]: igDimWeldBeadWeldStandardUnknown=0, igDimWeldBeadWeldStandardANSI=1, igDimWeldBeadWeldStandardISO=2, igDimWeldBeadWeldStandardDIN=3
- **DimWeldBeadWeldTypeConstants** [3]: igDimWeldBeadWeldTypeUnknown=0, igDimWeldBeadWeldTypeContinuous=1, igDimWeldBeadWeldTypeStitch=2
- **DimWeldBeadWeldmentShapeConstants** [4]: igDimWeldBeadWeldmentShapeUnknown=0, igDimWeldBeadWeldmentShapeFill=1, igDimWeldBeadWeldmentShapeConcave=2, igDimWeldBeadWeldmentShapeConvex=3
- **DimWeldBeadWeldmentTypeConstants** [4]: igDimWeldBeadWeldmentTypeUnknown=0, igDimWeldBeadWeldmentTypeFillet=1, igDimWeldBeadWeldmentTypeFill=2, igDimWeldBeadWeldmentTypeLabel=3
- **DimWeldLabelImportConstants** [3]: igDimWeldLabelImportUnknown=0, igDimWeldLabelLocal=1, igDimWeldLabelImported=2
- **DimensionTrackerReasonCode** [10]: igDTRC_Unknown=0, igDTRC_ValueChanged=1, igDTRC_TerminatorMoved=2, igDTRC_DetachedRebindFailure=3, igDTRC_DetachedNoEdgeInformation=4, ... (10 total)
- **DraftGlobalConstants** [7]: seDraftSelectToolWireFrameFilter=1, seDraftSelectToolRelationHandleFilter=2, seDraftSelectToolDimensionAnnotationFilter=3, seDraftSelectToolTextFilter=4, seDraftSelectToolDrawingViewFilter=5, ... (7 total)
- **DraftPrintOrientationConstants** [2]: igDraftPrintPortrait=0, igDraftPrintLandscape=1
- **DraftPrintPaperSizeConstants** [115]: igDraftPrintPaperSize_Custom=0, igDraftPrintPaperSize_LETTER=1, igDraftPrintPaperSize_LETTERSMALL=2, igDraftPrintPaperSize_TABLOID=3, igDraftPrintPaperSize_LEDGER=4, ... (115 total)
- **DraftPrintScaleTooLargeActionConstants** [2]: igDraftPrintScaleToFit=0, igDraftSkipDocument=1
- **DraftPrintSheetsPerPageConstants** [2]: igSingleSheet=0, igMultipleSheets=1
- **DraftPrintUnitsConstants** [2]: igDraftPrintMillimeters=0, igDraftPrintInches=1
- **DraftSectionViewType** [2]: seDraftSectionViewTypeStandard=0, seDraftSectionViewTypeRevolved=1
- **DrawingViewBsplineSimplificationConstants** [3]: igAlwaysSimplify=0, igSimplifyNonPlanarOnly=1, igNeverSimplify=2
- **DrawingViewDefaultsConstants** [2]: seDrawingViewDefaultsPrincipal=0, seDrawingViewDefaultsPictorial=1
- **DrawingViewEdgeStyleMappingEdgeType** [7]: seDVEdgeStyleMapping_VisibleEdge=0, seDVEdgeStyleMapping_HiddenEdge=1, seDVEdgeStyleMapping_TangentEdge=2, seDVEdgeStyleMapping_CoordinateSystemEdge=3, seDVEdgeStyleMapping_ReferenceVisibleEdge=4, ... (7 total)
- **DrawingViewIntersectionProcessingConstants** [4]: igNoIntersectionProcessing=0, igNoInterferenceEdges=1, igInterferenceEdgesThreadedPartsOnly=2, igInterferenceEdgesAllParts=3
- **DrawingViewProjectionAngleConstants** [2]: ProjectionAngleFirst=0, ProjectionAngleThird=1
- **DrawingViewShadingQualityConstants** [4]: igShadingQualityLevel1=1, igShadingQualityLevel2=2, igShadingQualityLevel3=3, igShadingQualityLevel4=4
- **DrawingViewSimplifiedAssemblyOptionConstants** [4]: seDrawingViewSimplifiedAssemblyOptionNone=0, seDrawingViewSimplifiedAssemblyOptionAllSubassemblies=1, seDrawingViewSimplifiedAssemblyOptionByConfiguration=2, seDrawingViewSimplifiedAssemblyOptionTopAssembly=3
- **DrawingViewSimplifiedPartOptionConstants** [3]: seDrawingViewSimplifiedPartOptionNone=0, seDrawingViewSimplifiedPartOptionAllParts=1, seDrawingViewSimplifiedPartOptionByConfiguration=2
- **DrawingViewSnapShotQualityConstants** [6]: igViewIsNotSnapShot=-1, igSnapShotQualityLevel1=1, igSnapShotQualityLevel2=2, igSnapShotQualityLevel3=3, igSnapShotQualityLevel4=4, ... (6 total)
- **DrawingViewStyleMappingElementType** [10]: seDVStyleMapping_PrincipalAndPictorialViews=0, seDVStyleMapping_2DmodelViews=1, seDVStyleMapping_SectionViews=2, seDVStyleMapping_AuxiliaryViews=3, seDVStyleMapping_DetailViews=4, ... (10 total)
- **DrawingViewTypeConstants** [11]: igNullView=0, igPrincipleView=1, igIsometricView=2, igAuxiliaryView=3, igXSectionView=4, ... (11 total)
- **DrawingViewVHL_ToleranceOverrideQualityConstants** [7]: igViewNotVHL=-1, igVHL_Tolerance_Use_SE_Default=0, igVHL_ToleranceOverrideQualityLevel1=1, igVHL_ToleranceOverrideQualityLevel2=2, igVHL_ToleranceOverrideQualityLevel3=3, ... (7 total)
- **FoldTypeConstants** [9]: igNullFold=0, igFoldUp=1, igFoldDown=2, igFoldRight=3, igFoldLeft=4, ... (9 total)
- **GraphicMemberEdgeTypeConstants** [8]: seUnknownEdgeType=0, seModelEdgeType=1, seSilhouetteEdgeType=2, seSectionEdgeType=3, seSnapshotEdgeType=4, ... (8 total)
- **GridDisplayOptionsConstants** [2]: igGridDisplayedAsLines=0, igGridDisplayedAsPoints=1
- **GridSnapOptionsConstants** [2]: igGridSnapUsingLines=0, igGridSnapUsingPoints=1
- **GussetPlateNamingFormat** [5]: igNamingFormatParameter=0, igNamingFormatThickness=1, igNamingFormatMaterial=2, igNamingFormatNumber=3, igNamingFormatNone=4
- **GussetPlateUniquenessCriteria** [2]: igUniquenessCriteriaGussetParameter=0, igUniquenessCriteriaCuttingStock=1
- **HTHoleTypeConstants** [9]: seHTOther=0, seHTSimple=1, seHTCounterbore=2, seHTCountersink=3, seHTSimpleThreaded=4, ... (9 total)
- **HoleTable2AngularUnit** [3]: igHoleTable2AngularDegrees=0, igHoleTable2AngularDegMinSec=1, igHoleTable2AngularRadians=2
- **HoleTable2DMSRoundOffTypeConstants** [6]: igHoleTable2Angular10Degree=1, igHoleTable2Angular1Degree=2, igHoleTable2Angular10Minute=3, igHoleTable2Angular1Minute=4, igHoleTable2Angular10Second=5, ... (6 total)
- **HoleTable2DecimalRoundOffTypeConstants** [8]: igHoleTable2Decimal1=0, igHoleTable2Decimal_1=1, igHoleTable2Decimal_2=2, igHoleTable2Decimal_3=3, igHoleTable2Decimal_4=4, ... (8 total)
- **HoleTable2PrimaryLinearUnit** [2]: igHoleTable2LinearMM=0, igHoleTable2LinearInches=1
- **HoleTableAnnotPosition** [4]: igAnnotPosTopLeft=0, igAnnotPosTopRight=1, igAnnotPosBottomLeft=2, igAnnotPosBottomRight=3
- **HoleTableCalloutType** [4]: igHoleCallout1=1, igHoleCallout2=2, igHoleCallout3=3, igHoleCallout4=4
- **HoleTableDelimiterType** [4]: igDelimiterTypeNone=0, igDelimiterTypeDot=1, igDelimiterTypeComma=2, igDelimiterTypeSpace=3
- **HoleTableType** [3]: igByDrawingView=0, igByUserSelection=1, igByFeature=2
- **KeypointIndexConstants** [39]: igArcCenter=0, igCircleCenter=0, igEllipseArcCenter=0, igEllipseCenter=0, igLineStart=0, ... (39 total)
- **LineupTextAlignOptionConstants** [8]: igAlignLeft=0, igAlignRight=1, igAlignCenter=2, igAlignBottom=3, igAlignTop=4, ... (8 total)
- **ModelLinkTypeConstants** [3]: igPartLink=0, igAssemblyLink=1, igWeldmentLink=2
- **ModelMemberComponentTypeConstants** [12]: seAssemblyMemberType=0, sePartMemberType=1, seConstructionMemberType=2, seWeldmentMemberType=3, seWeldPartMemberType=4, ... (12 total)
- **ModelMemberDisplayTypeConstants** [4]: seShowPart=0, seHidePart=1, seSectionPart=2, seUndefinedDisplay=3
- **ModelMemberTypeConstants** [3]: seAssemblyMember=0, sePartMember=1, seConstructionMember=2
- **ModelNodeTypeConstants** [2]: igPartNode=0, igAssemblyNode=1
- **PaperSizeConstants** [50]: igCustomSheetSize=-2, igSameAsPrintSetup=-1, igEngFolioTall=0, igEngFolioWide=1, igEngLegalTall=2, ... (50 total)
- **PaperToModelScaleConstants** [47]: igDefault1To1=-1, igCustomScale=0, igMetric50To1=1, igMetric20To1=2, igMetric10To1=3, ... (47 total)
- **PaperUnitConstants** [3]: igUnitInches=0, igUnitMillimeters=1, igUnitCentimeters=2
- **PartDrawingViewTypeConstants** [2]: sePartDesignedView=0, sePartSimplifiedView=1
- **PartListEndAngleRepresentationType** [3]: igDefaultRepresentation=0, igSignRepresentation=1, igClockwiseRepresentation=2
- **PartsListComponentType** [5]: igPartsListComponentType_Parts=0, igPartsListComponentType_Pipes=1, igPartsListComponentType_PipeFittings=2, igPartsListComponentType_FrameMembers=3, igPartsListComponentType_Tubes=4
- **PartsListType** [3]: igTopLevel=0, igAtomic=1, igExploded=2
- **PrecisionConstants** [10]: igPrecisionOnes=0, igPrecisionTenths=1, igPrecisionHundredths=2, igPrecisionThousandths=3, igPrecisionTenThousandths=4, ... (10 total)
- **ProfileValidationStatus** [2]: igProfileStatusInvalid=-1, igProfileStatusValid=0
- **SheetFitConstants** [5]: igFitWorkingGraphicsOnly=0, igFitAll=1, igFitWorkingAndBackgroundGraphics=2, igFitBackgroundGraphicsOnly=3, igFitSheet=4
- **SheetMetalDrawingViewTypeConstants** [3]: seSheetMetalDesignedView=0, seSheetMetalSimplifiedView=1, seSheetMetalFlatView=2
- **SheetSectionTypeConstants** [6]: igUnknownSection=-1, igWorkingSection=0, igBackgroundSection=1, igDrawingViewSection=2, ig2dModelSection=3, ... (6 total)
- **StyleConstants** [11]: seStyleConstantsVisibleReference=1, seStyleConstantsCenter=2, seStyleConstantsCuttingPlane=3, seStyleConstantsDotted=4, seStyleConstantsHidden=5, ... (11 total)
- **TableAnchorPoint** [4]: igUpperLeft=0, igUpperRight=1, igLowerLeft=2, igLowerRight=3
- **TableTextOrientation** [3]: igHorizontal=0, igRotated=1, igVertical=2
- **TitlePosition** [4]: igHeader=0, igFooter=1, igFooterAndHeader=2, igNeither=3
- **ViewOrientationConstants** [30]: igTopView=1, igRightView=2, igLeftView=3, igFrontView=4, igBottomView=5, ... (30 total)
- **WeldmentDrawingViewTypeConstants** [3]: seWeldmentMachinedView=0, seWeldmentWeldedView=1, seWeldmentAssembledView=2
- **__MIDL___MIDL_itf_draft_0002_0028_0001** [4]: DVShowHideEdgeOverrideIndeterminant=-1, DVShowHideEdgeOverrideNone=0, DVShowHideEdgeOverrideShow=1, DVShowHideEdgeOverrideHide=2

### Interfaces (197)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| Block | dispatch | 1 | 9 |
| BlockLabel | dispatch | 16 | 18 |
| BlockLabelOccurrence | dispatch | 2 | 15 |
| BlockLabelOccurrences | dispatch | 1 | 3 |
| BlockLabels | dispatch | 2 | 3 |
| BlockOccurrence | dispatch | 19 | 17 |
| BlockOccurrences | dispatch | 2 | 3 |
| BlockTable | dispatch | 8 | 54 |
| BlockTables | dispatch | 4 | 3 |
| BlockView | dispatch | 5 | 39 |
| BlockViews | dispatch | 2 | 4 |
| Blocks | dispatch | 5 | 3 |
| BreakLinePair | dispatch | 2 | 11 |
| BreakLinePairs | dispatch | 3 | 3 |
| BrokenOutSectionProfile | dispatch | 0 | 7 |
| BrokenOutSectionProfiles | dispatch | 2 | 3 |
| ConductorTable | dispatch | 4 | 38 |
| ConductorTables | dispatch | 2 | 3 |
| ConnectorTable | dispatch | 7 | 40 |
| ConnectorTables | dispatch | 2 | 3 |
| CoordinateSystem2d | dispatch | 2 | 7 |
| CoordinateSystems2d | dispatch | 1 | 3 |
| CuttingPlane | dispatch | 4 | 29 |
| CuttingPlanes | dispatch | 2 | 3 |
| DVArc2d | dispatch | 8 | 22 |
| DVArcs2d | dispatch | 3 | 3 |
| DVBSplineCurve2d | dispatch | 8 | 25 |
| DVBSplineCurves2d | dispatch | 3 | 3 |
| DVCircle2d | dispatch | 6 | 22 |
| DVCircles2d | dispatch | 3 | 3 |
| DVEllipse2d | dispatch | 7 | 25 |
| DVEllipses2d | dispatch | 3 | 3 |
| DVEllipticalArc2d | dispatch | 9 | 24 |
| DVEllipticalArcs2d | dispatch | 3 | 3 |
| DVLine2d | dispatch | 6 | 21 |
| DVLineString2d | dispatch | 7 | 18 |
| DVLineStrings2d | dispatch | 3 | 3 |
| DVLines2d | dispatch | 3 | 3 |
| DVPoint2d | dispatch | 5 | 16 |
| DVPoints2d | dispatch | 1 | 3 |
| DetailEnvelope | dispatch | 13 | 33 |
| DetailEnvelopes | dispatch | 1 | 3 |
| DraftBendTable | dispatch | 5 | 38 |
| DraftBendTables | dispatch | 2 | 3 |
| DraftDocument | dispatch | 42 | 75 |
| DraftFilePreferences | dispatch | 0 | 58 |
| DraftPrintUtility | dispatch | 10 | 28 |
| DraftProfile | dispatch | 3 | 10 |
| DrawingView | dispatch | 59 | 155 |
| DrawingViews | dispatch | 20 | 3 |
| FOPTable | dispatch | 3 | 37 |
| FOPTables | dispatch | 2 | 3 |
| GraphicMembers | dispatch | 1 | 3 |
| HTHole | dispatch | 0 | 20 |
| HTHoles | dispatch | 1 | 3 |
| HighlightDrawingViewMembers | dispatch | 2 | 0 |
| HoleTable | dispatch | 2 | 4 |
| HoleTable2 | dispatch | 17 | 69 |
| HoleTables | dispatch | 1 | 3 |
| HoleTables2 | dispatch | 2 | 3 |
| ModelLink | dispatch | 7 | 14 |
| ModelLinks | dispatch | 3 | 3 |
| ModelMember | dispatch | 2 | 45 |
| ModelMembers | dispatch | 1 | 3 |
| ModelNode | dispatch | 1 | 12 |
| ModelNodes | dispatch | 1 | 3 |
| ModelWeld | dispatch | 0 | 43 |
| ModelWelds | dispatch | 1 | 3 |
| PartsList | dispatch | 18 | 73 |
| PartsLists | dispatch | 5 | 3 |
| Section | dispatch | 3 | 6 |
| SectionBoundaries2d | dispatch | 1 | 3 |
| SectionSheets | dispatch | 1 | 3 |
| Sections | dispatch | 2 | 6 |
| SelectedSheets | dispatch | 1 | 3 |
| Sheet | dispatch | 23 | 63 |
| SheetGroup | dispatch | 1 | 5 |
| SheetGroupSheets | dispatch | 1 | 3 |
| SheetGroups | dispatch | 1 | 3 |
| SheetSetup | dispatch | 7 | 16 |
| SheetWindow | dispatch | 24 | 37 |
| Sheets | dispatch | 4 | 4 |
| Table | dispatch | 3 | 37 |
| TableCell | dispatch | 0 | 12 |
| TableColumn | dispatch | 1 | 32 |
| TableColumns | dispatch | 2 | 3 |
| TableGroup | dispatch | 0 | 9 |
| TableGroups | dispatch | 2 | 3 |
| TablePage | dispatch | 2 | 7 |
| TablePages | dispatch | 1 | 3 |
| TableRow | dispatch | 1 | 6 |
| TableRows | dispatch | 2 | 3 |
| TableTitle | dispatch | 1 | 12 |
| TableTitles | dispatch | 2 | 3 |
| Tables | dispatch | 2 | 3 |
| ToleranceTable | dispatch | 8 | 40 |
| ToleranceTables | dispatch | 4 | 3 |
| ViewPlane | dispatch | 14 | 31 |
| ViewPlanes | dispatch | 0 | 0 |
| _IBlockAuto | interface | 1 | 9 |
| _IBlockLabelAuto | interface | 16 | 18 |
| _IBlockLabelOccurrenceAuto | interface | 2 | 15 |
| _IBlockLabelOccurrencesAuto | interface | 1 | 3 |
| _IBlockLabelsAuto | interface | 2 | 3 |
| _IBlockOccurrenceAuto | interface | 19 | 17 |
| _IBlockOccurrencesAuto | interface | 2 | 3 |
| _IBlockTableAuto | interface | 8 | 54 |
| _IBlockTablesAuto | interface | 4 | 3 |
| _IBlockViewAuto | interface | 5 | 39 |
| _IBlockViewsAuto | interface | 2 | 4 |
| _IBlocksAuto | interface | 5 | 3 |
| _IBreakLinePairAuto | interface | 2 | 11 |
| _IBreakLinePairsAuto | interface | 3 | 3 |
| _IBrokenOutSectionProfileAuto | interface | 0 | 7 |
| _IBrokenOutSectionProfilesAuto | interface | 2 | 3 |
| _IConductorTableAuto | interface | 4 | 38 |
| _IConductorTablesAuto | interface | 2 | 3 |
| _IConnectorTableAuto | interface | 7 | 40 |
| _IConnectorTablesAuto | interface | 2 | 3 |
| _ICoordinateSystem2dAuto | interface | 2 | 7 |
| _ICoordinateSystems2dAuto | interface | 1 | 3 |
| _ICuttingPlaneAuto | interface | 4 | 29 |
| _ICuttingPlanesAuto | interface | 2 | 3 |
| _IDVArc2dAuto | interface | 8 | 22 |
| _IDVArcs2dAuto | interface | 3 | 3 |
| _IDVBSplineCurve2dAuto | interface | 8 | 25 |
| _IDVBSplineCurves2dAuto | interface | 3 | 3 |
| _IDVCircle2dAuto | interface | 6 | 22 |
| _IDVCircles2dAuto | interface | 3 | 3 |
| _IDVEllipArc2dAuto | interface | 9 | 24 |
| _IDVEllipArcs2dAuto | interface | 3 | 3 |
| _IDVEllipse2dAuto | interface | 7 | 25 |
| _IDVEllipses2dAuto | interface | 3 | 3 |
| _IDVLine2dAuto | interface | 6 | 21 |
| _IDVLineString2dAuto | interface | 7 | 18 |
| _IDVLineStrings2dAuto | interface | 3 | 3 |
| _IDVLines2dAuto | interface | 3 | 3 |
| _IDVPoint2dAuto | interface | 5 | 16 |
| _IDVPoints2dAuto | interface | 1 | 3 |
| _IDetailEnvelopeAuto | interface | 13 | 33 |
| _IDetailEnvelopesAuto | interface | 1 | 3 |
| _IDraftBendTableAuto | interface | 5 | 38 |
| _IDraftBendTablesAuto | interface | 2 | 3 |
| _IDraftDocumentAuto | interface | 42 | 75 |
| _IDraftFilePreferencesAuto | interface | 0 | 58 |
| _IDraftPrintUtilityAuto | interface | 10 | 28 |
| _IDraftProfileAuto | interface | 3 | 10 |
| _IDrawingViewAuto | interface | 59 | 155 |
| _IDrawingViewsAuto | interface | 20 | 3 |
| _IFOPTableAuto | interface | 3 | 37 |
| _IFOPTablesAuto | interface | 2 | 3 |
| _IGraphicMembersAuto | interface | 1 | 3 |
| _IHTHoleAuto | interface | 0 | 20 |
| _IHTHolesAuto | interface | 1 | 3 |
| _IHighlightDrawingViewMembersAuto | interface | 2 | 0 |
| _IHoleTable2Auto | interface | 17 | 69 |
| _IHoleTableAuto | interface | 2 | 4 |
| _IHoleTables2Auto | interface | 2 | 3 |
| _IHoleTablesAuto | interface | 1 | 3 |
| _IModelLinkAuto | interface | 7 | 14 |
| _IModelLinksAuto | interface | 3 | 3 |
| _IModelMemberAuto | interface | 2 | 45 |
| _IModelMembersAuto | interface | 1 | 3 |
| _IModelNodeAuto | interface | 1 | 12 |
| _IModelNodesAuto | interface | 1 | 3 |
| _IModelWeldAuto | interface | 0 | 43 |
| _IModelWeldsAuto | interface | 1 | 3 |
| _IPartsListAuto | interface | 18 | 73 |
| _IPartsListsAuto | interface | 5 | 3 |
| _ISectionAuto | interface | 3 | 6 |
| _ISectionBoundaries2dAuto | interface | 1 | 3 |
| _ISectionSheetsAuto | interface | 1 | 3 |
| _ISectionsAuto | interface | 2 | 6 |
| _ISelectedSheetsAuto | interface | 1 | 3 |
| _ISheetAuto | interface | 23 | 63 |
| _ISheetGroupAuto | interface | 1 | 5 |
| _ISheetGroupSheetsAuto | interface | 1 | 3 |
| _ISheetGroupsAuto | interface | 1 | 3 |
| _ISheetSetupAuto | interface | 7 | 16 |
| _ISheetWindowAuto | interface | 24 | 37 |
| _ISheetsAuto | interface | 4 | 4 |
| _ITableAuto | interface | 3 | 37 |
| _ITableCellAuto | interface | 0 | 12 |
| _ITableColumnAuto | interface | 1 | 32 |
| _ITableColumnsAuto | interface | 2 | 3 |
| _ITableGroupAuto | interface | 0 | 9 |
| _ITableGroupsAuto | interface | 2 | 3 |
| _ITablePageAuto | interface | 2 | 7 |
| _ITablePagesAuto | interface | 1 | 3 |
| _ITableRowAuto | interface | 1 | 6 |
| _ITableRowsAuto | interface | 2 | 3 |
| _ITableTitleAuto | interface | 1 | 12 |
| _ITableTitlesAuto | interface | 2 | 3 |
| _ITablesAuto | interface | 2 | 3 |
| _IToleranceTableAuto | interface | 8 | 40 |
| _IToleranceTablesAuto | interface | 4 | 3 |
| _IViewPlaneAuto | interface | 14 | 31 |

### Aliases (1)

- DVShowHideEdgeOverrideType = __MIDL___MIDL_itf_draft_0002_0028_0001

---
## Program/framewrk.tlb
**Solid Edge Framework Type Library** (GUID: `{8A7EFA3A-F000-11D1-BDFC-080036B4D502}`, v1.0)

### Enums (113)

- **AcceleratorTypeConstants** [7]: seExecutable=1, seEmbeded=2, seServerInPlace=3, seContainerInPlace=4, seMainFrame=5, ... (7 total)
- **AnimationEventConstants** [4]: BeforeTimelineFrameUpdate=1, AfterTimelineFrameUpdate=2, BeforeDragComponentFrameUpdate=3, AfterDragComponentFrameUpdate=4
- **ApplicationActiveFrameSwitchingEvent** [2]: ApplicationSwitchingToMainFrame=1, ApplicationSwitchingToFloatingFrame=2
- **ApplicationBeforeDocumentOpenEvent** [6]: OpenFromUnknown=1, OpenFromMRU=2, OpenDropTagetApplication=3, OpenDropTargetDocumentView=4, OpenFromAutomation=5, ... (6 total)
- **ApplicationDocumentLoadingEvent** [1]: ApplicationWaitingForNextLevel=1
- **ApplicationGlobalConstants** [497]: seApplicationGlobalDisplayQuality=0, seApplicationGlobalDisplayArcQuality=1, seApplicationGlobalColorActive=2, seApplicationGlobalColorBackground=3, seApplicationGlobalColorConstruction=4, ... (497 total)
- **ApplicationLicenseEvent** [6]: ApplicationLicenseCheckin=1, ApplicationLicenseCheckout=2, ApplicationLicenseTransfer=721082, ApplicationLicenseOffline=721083, ApplicationLicenseOnline=721084, ... (6 total)
- **ApplicationReadyEvent** [3]: ApplicationIsUIReady=1, ActiveDocumentIsUIReady=2, ActiveEnvironmentIsUIReady=3
- **ArrangeWindowsStyles** [4]: igWindowsTiled=1, igWindowsHorizontal=2, igWindowsVertical=4, igWindowsCascade=8
- **AssemblyChangeEventsConstants** [12]: seAssemblyOccurrenceRename=1, seAssemblyFeatureRename=2, seAssemblyComponentShow=3, seAssemblyComponentHide=4, seAssemblyOccurrenceAdd=5, ... (12 total)
- **AssemblyEventConstants** [1]: seAssemblyOccurrenceReplace=1
- **AttributeTypeConstants** [11]: seInteger=2, seLong=3, seSingle=4, seDouble=5, seCurrency=6, ... (11 total)
- **BulkMigrationTypeConstants** [6]: igNoBulkMigration=0, igTDMBulkMigration=1, igProEBulkMigration=2, igNX2DBulkMigration=3, igMDTBulkMigration=4, ... (6 total)
- **CapturedRelationshipOffsetTypeConstants** [3]: seFixed=0, seFloating=1, seOffsetNotSupported=2
- **CapturedRelationshipTypeConstants** [6]: seMate=0, sePlanarAlign=1, seAxialAlign=2, seTangent=3, seConnect=4, ... (6 total)
- **CheckInOptions** [2]: DoNotCheckInOption=0, UploadAndCheckInOption=1
- **CommandBarHeaderDialogControlIDs** [2]: CommandBarHeaderDoitButton=1073, CommandBarHeaderOptionsButton=1074
- **ConfigForForeignFileType** [1]: seAutoCADConfigFile=1067709598
- **ConfigResetType** [2]: seResetGroup=-1957181463, seResetAll=-1801520595
- **CookieDataToGet** [1]: GET_REVISION_RULE=0
- **DisplayTypeConstant** [3]: igNotSpecifiedDisplay=-1, igContentsDisplay=0, igIconDisplay=1
- **DocumentAccess** [3]: igReadWrite=0, igReadOnly=1, igReadExclusive=2
- **DocumentDownloadLevel** [3]: SEECDownloadAllLevel=0, SEECDownloadFirstLevel=1, SEECDownloadTopLevel=2
- **DocumentStatus** [7]: igStatusAvailable=0, igStatusInWork=1, igStatusInReview=2, igStatusReleased=3, igStatusBaselined=4, ... (7 total)
- **DocumentTypeConstants** [13]: igPartDocument=1, igDraftDocument=2, igAssemblyDocument=3, igSheetMetalDocument=4, igUnknownDocument=5, ... (13 total)
- **FileTranslationMode** [2]: seExport=-1720541218, seImport=1493142125
- **GenerateMasterImportListError** [1]: NoDocsFound=1
- **GenerateSourceImportListError** [1]: GenerateSourceImportListError_NoDocsFound=1
- **HatchElementType** [3]: igHatchElementTypeUnknown=0, igHatchElementTypeLinear=1, igHatchElementTypeRadial=2
- **InsightSPUserRights** [23]: seViewListItems=1, seAddListItems=2, seEditListItems=4, seDeleteListItems=8, seCancelCheckout=256, ... (23 total)
- **InterDocumentUpdateMode** [2]: seActiveLevel=0, seAllOpenDocuments=1
- **KeyPointType** [13]: igKeyPointStart=1, igKeyPointEnd=2, igKeyPointCenter=4, igKeyPointMajorAxis=8, igKeyPointMinorAxis=16, ... (13 total)
- **LinksUpdateOption** [3]: igNoLinksUpdate=0, igLinksUpdateWithDefpath=1, igLinksUpdateWithAltPath=2
- **MatTablePropIndexConstants** [13]: seMaterialName=3, seFaceStyle=20, seFillStyle=21, seVSPlusStyle=22, seDensity=23, ... (13 total)
- **NotifyOption** [5]: igNotifyWhenReadable=0, igNotifyWhenWriteable=1, igNotifyWhenAvailable=2, igNoNotify=3, igNotifyWhenExclusive=4
- **OLEInsertionTypeConstant** [5]: igUseSymbolPreferences=-1, igOLELinked=0, igOLEEmbedded=1, igOLENone=3, igOLESharedEmbedded=4
- **OLEUpdateOptionConstant** [3]: igOLEAutomatic=0, igOLEFrozen=1, igOLEManual=2
- **ObjectType** [130]: seDVCircle2d=-2074243498, igPlanarRelation3d=-2058948880, igSketch3D=-2054330988, seAssemblyGroups=-2004545918, igDividedPart=-1940558319, ... (130 total)
- **OpenNonSolidEdgeFileContext** [9]: OpenImage=1, OpenPointCloud=2, OpenDecal=3, OpenViewBackground=4, OpenViewReflection=5, ... (9 total)
- **OverWriteFilesOption** [2]: NoToAll=0, YesToAll=1
- **PMISectionDisplayModeConstants** [4]: sePMISectionDisplayShowOnlyCutFaces=0, sePMISectionDisplayShowCutFacesAndCutBodies=1, sePMISectionDisplayShowCutFacesWithOriginalBodies=2, sePMISectionDisplayShowOnlyOriginalBodies=3
- **PredefineRelationGroupPolarityConstants** [4]: MagneticGroup=0, SPoleGroup=1, NPoleGroup=2, CaptureFitGroup=3
- **RadialHatchElementCenterLocation** [10]: igRadialHatchElementCenterUnknown=0, igRadialHatchElementCenterTopLeft=1, igRadialHatchElementCenterTopMid=2, igRadialHatchElementCenterTopRight=3, igRadialHatchElementCenterMidLeft=4, ... (10 total)
- **RevisionRuleType** [5]: LastSavedType=0, LatestReleasedRevision=1, LatestRevision=2, ExternalBOM=3, VersionFromCache=4
- **RibbonBarControlSize** [3]: seRibbonBarControlSizeDefault=0, seRibbonBarControlSizeSmall=1, seRibbonBarControlSizeLarge=2
- **RibbonBarControlText** [3]: seRibbonBarControlTextDefault=0, seRibbonBarControlTextOn=1, seRibbonBarControlTextOff=2
- **RibbonBarInsertMode** [6]: seRibbonBarInsertCopy=0, seRibbonBarInsertMove=1, seRibbonBarInsertCreate=2, seRibbonBarInsertCreateButton=3, seRibbonBarInsertCreatePopup=4, ... (6 total)
- **RouteStatus** [4]: igInvalidSlip=0, igRouteComplete=1, igNotYetRouted=2, igRouteInProgress=3
- **RouteType** [2]: igOneAfterAnother=0, igAllAtOnce=1
- **SEColorTheme** [4]: SEColorThemeLight=0, SEColorThemeMedium=1, SEColorThemeDark=2, SEColorThemeFramed=3
- **SEECOptions** [2]: SEEC_eUnknownOption=0, SEEC_SearchLimit=1
- **SELicenseCheck** [3]: SELicenserConsume=1, SELicenserReturn=2, SELicenserIsPresent=3
- **SPServerType** [6]: SERVER_TYPE_NOT_SHAREPOINT=0, SHAREPOINT_V1_SERVER=1, SHAREPOINT_V2_SERVER=2, SHAREPOINT_V3_SERVER=3, SHAREPOINT_V4_SERVER=4, ... (6 total)
- **SeAnalysisModeType** [6]: seAnalysisModeDefault=0, seAnalysisModeZebraStripeLinear=1, seAnalysisModeZebraStripeSpherical=2, seAnalysisModeZebraStripeReflection=3, seAnalysisModeCurvatureColor=4, ... (6 total)
- **SeAnalysisStateType** [3]: seAnalysisStateNone=0, seAnalysisStateGlobal=1, seAnalysisStateLocal=2
- **SeAntiAliasLevel** [4]: seAntiAliasLevelNone=0, seAntiAliasLevelLow=2, seAntiAliasLevelMedium=4, seAntiAliasLevelHigh=8
- **SeBackgroundType** [6]: seBackgroundTypeSolid=0, seBackgroundTypeGradient=1, seBackgroundTypeImage=2, seBackgroundTypeImageReference=3, seBackgroundTypeStaticEnvironment=4, ... (6 total)
- **SeBarPosition** [5]: seBarTop=1, seBarBottom=2, seBarLeft=3, seBarRight=4, seBarFloating=5
- **SeBarType** [3]: seBarTypeMenuBar=1, seBarTypeNormal=2, seBarTypePopup=3
- **SeButtonState** [3]: seButtonDown=1, seButtonMixed=2, seButtonUp=3
- **SeButtonStyle** [9]: seButtonAutomatic=1, seButtonCaption=2, seButtonIcon=3, seButtonIconAndCaption=4, seButtonIconAndCaptionBelow=5, ... (9 total)
- **SeConnectMode** [3]: seConnectAtStartup=1, seConnectByUser=2, seConnectExternally=3
- **SeControlType** [3]: seControlPopup=1, seControlButton=2, seControlSeparator=3
- **SeDisconnectMode** [3]: seDisconnectAtShutdown=1, seDisconnectByUser=2, seDisconnectExternally=3
- **SeFeatureAddFlag** [5]: seNew=1, seUnSuppress=2, seUnSuppressUpTo=3, seNewPatternItem=4, seUnSuppressPatternItem=5
- **SeFeatureDeleteFlag** [5]: sePermanent=1, seSuppress=2, seSuppressDownTo=3, sePermanentPatternItem=4, seSuppressPatternItem=5
- **SeFeatureModifyFlag** [3]: seSchemaChanged=1, seDirectInputsChanged=2, seReordered=3
- **SeGradientType** [7]: seGradientTypeHorizontal=1, seGradientTypeVertical=2, seGradientTypeDiagonalUp=3, seGradientTypeDiagonalDown=4, seGradientTypeSquareSpot=5, ... (7 total)
- **SeHiddenLineMode** [3]: seHiddenLineModeOff=0, seHiddenLineModeDim=1, seHiddenLineModeDashed=2
- **SeImageQualityType** [3]: seImageQualityLow=1, seImageQualityMedium=2, seImageQualityHigh=3
- **SeModifySketchFlag** [3]: seInsertEntity=1, seRemoveEntity=2, seModifyEntity=3
- **SeObjectType** [3]: seObjectNamedViews=1, seObjectViewStyles=2, seObjectFaceStyles=3
- **SeRenderFillMode** [3]: seRenderFillSolid=1, seRenderFillBorder=2, seRenderFillSolidBorder=3
- **SeRenderMaterialGetMode** [2]: seGetModeExisting=0, seGetModeCreateOnDemand=1
- **SeRenderMaterialSetMode** [4]: seSetModeDetach=0, seSetModeAttach=1, seSetModeUpdate=2, seSetModeAttachAndUpdate=3
- **SeRenderModeType** [12]: seRenderModeUndefined=0, seRenderModeWireframe=1, seRenderModeWiremesh=2, seRenderModeOutline=3, seRenderModeBoundary=4, ... (12 total)
- **SeRenderShadeMode** [2]: seRenderShadeModeFlat=1, seRenderShadeModeSmooth=2
- **SeRenderShapeType** [2]: seRenderShapeSquare=1, seRenderShapeRound=2
- **SeRenderSpaceType** [3]: seRenderSpaceDevice=0, seRenderSpacePaper=1, seRenderSpaceWorld=2
- **SeSkyboxType** [5]: seSkyboxTypeUndefined=-1, seSkyboxTypeSkybox=0, seSkyboxTypeSingleImage=1, seSkyboxTypeSpheremap=2, seSkyboxTypePanoramic=3
- **SectionViewExtentSide** [6]: igLeftExtent=1, igRightExtent=2, igFiniteSymmetricExtent=3, igInfiniteLeftExtent=4, igInfiniteRightExtent=5, ... (6 total)
- **SectionViewPlaneExtentTypeConstant** [2]: SectionViewPlaneExtentTypeConstant_Bounded=1, SectionViewPlaneExtentTypeConstant_UnBounded=2
- **SectionViewPlaneType** [2]: igDynamic=1, igAssociative=2
- **SectionViewProfileSide** [4]: igLeftProfileSide=1, igRightProfileSide=2, igInsideProfileSide=3, igOutsideProfileSide=4
- **SensorDisplayTypeConstants** [3]: seSensorDisplayTypeInvalid=0, seSensorDisplayTypeHorizontalRange=1, seSensorDisplayTypeTrueFalse=2
- **SensorOperatorConstants** [7]: seSensorOperatorInvalid=0, seSensorOperatorGreaterThan=1, seSensorOperatorLessThan=2, seSensorOperatorEqualTo=3, seSensorOperatorNotEqualTo=4, ... (7 total)
- **SensorStatusConstants** [3]: seSensorStatusUpToDate=0, seSensorStatusOutOfDate=1, seSensorStatusInError=2
- **SensorTypeConstants** [4]: seSensorTypeInvalid=0, seSensorTypeVariable=1, seSensorTypeMinimumDistance=6, seSensorTypeUser=7
- **SensorUpdateMechanismConstants** [3]: seSensorUpdateMechanismInvalid=0, seSensorUpdateMechanismAutomatic=1, seSensorUpdateMechanismManual=2
- **SheetMetalSensorFeatureTypeConstants** [8]: seSheetMetalSensorFeatureTypeExteriorEdges=0, seSheetMetalSensorFeatureTypeInteriorEdges=1, seSheetMetalSensorFeatureTypeCutouts=2, seSheetMetalSensorFeatureTypeHoles=3, seSheetMetalSensorFeatureTypeDimples=4, ... (8 total)
- **ShortCutMenuContextConstants** [7]: seShortCutForGraphicLocate=1, seShortCutForView=2, seShortCutForFeaturePathFinder=3, seShortCutForFeaturePathFinderDocument=4, seShortCutNone=5, ... (7 total)
- **SolidEdgeCommandConstants** [9]: seConvertCommand=10452, seSurfaceVisualCommand=11129, seAssemblyPlacePartCommand=32791, seRefreshViewCommand=32876, sePartInsertPartCommand=40254, ... (9 total)
- **StyleUnitsConstant** [3]: PAPER_STYLEUNITS=11, DESIGN_STYLEUNITS=12, VIEW_STYLEUNITS=13
- **SurfaceAreaSensorAreaTypeConstants** [2]: seSurfaceAreaSensorAreaTypeNeg=0, seSurfaceAreaSensorAreaTypePos=1
- **SurfaceAreaSensorSelectionTypeConstants** [2]: seSurfaceAreaSensorSelectFace=0, seSurfaceAreaSensorSelectFaceChain=1
- **SyncOption** [2]: SEECSyncAll=0, SEECSyncOne=1
- **TCESETypes** [5]: TCE_SEPart=0, TCE_SEAssembly=1, TCE_SEWeldment=2, TCE_SESheetmetal=3, TCE_SEDraft=4
- **TemplatesListType** [4]: eUnknownTemplateList=0, eStandardTemplateList=1, eUserTemplateList=2, eCustomTemplateList=3
- **TextStyleNumberJustificationConstants** [3]: igLeftJustificationStyle=0, igCenterJustificationStyle=1, igRightJustificationStyle=2
- **UnitTypeConstants** [63]: igUnitDistance=1, igUnitAngle=2, igUnitMass=3, igUnitTime=4, igUnitTemperature=5, ... (63 total)
- **UploadType** [2]: DeepUploadType=0, ShallowUploadType=1
- **VariableLimitValueConstant** [3]: igVariableLimitNone=0, igDiscreteList=1, igMinMaxLimit=2
- **WorkflowAction** [4]: Initiate=0, Delegate=1, Accept=2, Reject=3
- **WorkflowType** [2]: OneStepRelease=0, QuickRelease=1
- **eCPDMode** [4]: CPD_NEW_FILE=1, CPD_UPLOAD_FILE=2, CPD_SAVEAS_FILE=3, CPD_REVISE_FILE=4
- **eSaveAllOption** [4]: saveAll_Select=1, saveAll_SaveAll=2, saveAll_DiscardAll=3, saveAll_Cancel=4
- **seMovieFormatConstants** [2]: seMovieFormatAVI=0, seMovieFormatWMV=1
- **seMovieStandardResolutionConstants** [5]: seMovieStandardResolutionNTSC=0, seMovieStandardResolutionPAL=1, seMovieStandardResolutionHD=2, seMovieStandardResolutionFullHD=3, seMovieStandardResolutionCurrentView=4
- **seSharpenLevelConstants** [9]: seSharpenDefault=0, seSharpenCoarse=1, seSharpenNormal=2, seSharpenFine=3, seSharpenExtraFine=4, ... (9 total)
- **seSteeringWheelConstants** [3]: seSteeringWheelConstantsXAxis=1, seSteeringWheelConstantsYAxis=2, seSteeringWheelConstantsZAxis=3
- **seStyleTypeConstants** [7]: igDimensionStyle=0, igDrawingViewStyle=1, igFillStyle=2, igHatchStyle=3, igLineStyle=4, ... (7 total)
- **seUnitsTypeConstants** [2]: seUnitsType_DataBase=-730794371, seUnitsType_Document=1886781498
- **seVariableTypeConstants** [4]: seVariableType_Text=-170730141, seVariableType_Simulation=215773802, seVariableType_UserDefined=1560616706, seVariableType_Dimension=1661573600

### Interfaces (301)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| Accelerator | dispatch | 6 | 3 |
| Accelerators | dispatch | 1 | 2 |
| AddIn | dispatch | 3 | 9 |
| AddIns | dispatch | 2 | 2 |
| Application | dispatch | 81 | 76 |
| Attribute | dispatch | 0 | 3 |
| AttributeQuery | dispatch | 1 | 2 |
| AttributeSet | dispatch | 3 | 2 |
| AttributeSets | dispatch | 3 | 1 |
| CPDInitializer | dispatch | 6 | 0 |
| CPDInitializerBiDM | dispatch | 4 | 0 |
| CPDInitializerInsightXT | dispatch | 6 | 0 |
| CommandBar | dispatch | 4 | 15 |
| CommandBarButton | dispatch | 4 | 27 |
| CommandBarControl | dispatch | 4 | 24 |
| CommandBarControls | dispatch | 2 | 3 |
| CommandBarPopup | dispatch | 4 | 26 |
| CommandBars | dispatch | 3 | 6 |
| CommandCategories | dispatch | 1 | 2 |
| CommandCategory | dispatch | 1 | 2 |
| CommandInfo | dispatch | 1 | 6 |
| Customization | dispatch | 2 | 5 |
| DISEAddInEvents | dispatch | 3 | 0 |
| DISEAddInEventsEx | dispatch | 4 | 0 |
| DISEAddInEventsEx2 | dispatch | 4 | 0 |
| DISEAnimationEvents | dispatch | 1 | 0 |
| DISEApplicationEvents | dispatch | 16 | 0 |
| DISEApplicationWindowEvents | dispatch | 1 | 0 |
| DISEAssemblyChangeEvents | dispatch | 2 | 0 |
| DISEAssemblyConfigurationChangeEvents | dispatch | 2 | 0 |
| DISEAssemblyFamilyEvents | dispatch | 6 | 0 |
| DISEAssemblyFamilyEvents2 | dispatch | 8 | 0 |
| DISEAssemblyPhysicalPropertiesChangeEvents | dispatch | 2 | 0 |
| DISEAssemblyRecomputeEvents | dispatch | 5 | 0 |
| DISEBeforeFileSaveAsEvents | dispatch | 1 | 0 |
| DISEBendTableEvents | dispatch | 4 | 0 |
| DISECommand | dispatch | 1 | 5 |
| DISECommandBarButtonEvents | dispatch | 3 | 0 |
| DISECommandEvents | dispatch | 7 | 0 |
| DISECommandWindowEvents | dispatch | 1 | 0 |
| DISEDocumentEvents | dispatch | 4 | 0 |
| DISEFeatureSelectedFromPFEvents | dispatch | 1 | 0 |
| DISEFileUIEvents | dispatch | 6 | 0 |
| DISEMouse | dispatch | 3 | 35 |
| DISEMouseEvents | dispatch | 6 | 0 |
| DISESketchRecomputeEvents | dispatch | 4 | 0 |
| DISEViewEvents | dispatch | 3 | 0 |
| DISEhDCDisplayEvents | dispatch | 4 | 0 |
| DashStyle | dispatch | 2 | 7 |
| DashStyles | dispatch | 3 | 3 |
| Documents | dispatch | 9 | 6 |
| DynamicVisualization | dispatch | 1 | 0 |
| Environment | dispatch | 0 | 12 |
| Environments | dispatch | 1 | 3 |
| FaceStyle | dispatch | 49 | 69 |
| FaceStyles | dispatch | 4 | 3 |
| FillStyle | dispatch | 0 | 13 |
| FillStyles | dispatch | 3 | 4 |
| HatchPatternStyle | dispatch | 34 | 11 |
| HatchPatternStyles | dispatch | 3 | 3 |
| HighlightSet | dispatch | 9 | 2 |
| HighlightSets | dispatch | 2 | 3 |
| IBiDMEvents | interface | 2 | 0 |
| ISEAccelerator | interface | 6 | 3 |
| ISEAccelerators | interface | 1 | 2 |
| ISEAddIn | interface | 3 | 9 |
| ISEAddInEdgeBarEvents | interface | 3 | 0 |
| ISEAddInEdgeBarEventsEx | interface | 3 | 0 |
| ISEAddInEvents | interface | 3 | 0 |
| ISEAddInEventsEx | interface | 1 | 0 |
| ISEAddInEventsEx2 | interface | 4 | 0 |
| ISEAddInEx | interface | 1 | 1 |
| ISEAddInEx2 | interface | 1 | 0 |
| ISEAddInSaveAsTranslator | interface | 1 | 1 |
| ISEAddInSaveAsTranslatorEvents | interface | 3 | 0 |
| ISEAddIns | interface | 2 | 2 |
| ISEAnimationEvents | interface | 1 | 0 |
| ISEApplicationActiveFrameSwitchingEvents | interface | 1 | 0 |
| ISEApplicationDocumentLoadingEvents | interface | 1 | 0 |
| ISEApplicationEvents | interface | 16 | 0 |
| ISEApplicationEventsEx | interface | 1 | 0 |
| ISEApplicationEventsEx2 | interface | 1 | 0 |
| ISEApplicationLicenseEvents | interface | 1 | 0 |
| ISEApplicationReadyEvents | interface | 1 | 0 |
| ISEApplicationV8AfterDocumentOpenEvent | interface | 1 | 0 |
| ISEApplicationWindowEvents | interface | 1 | 0 |
| ISEAssemblyChangeEvents | interface | 2 | 0 |
| ISEAssemblyConfigurationChangeEvents | interface | 2 | 0 |
| ISEAssemblyFamilyEvents | interface | 6 | 0 |
| ISEAssemblyFamilyEvents2 | interface | 8 | 0 |
| ISEAssemblyPhysicalPropertiesChangeEvents | interface | 2 | 0 |
| ISEAssemblyRecomputeEvents | interface | 5 | 0 |
| ISEBeforeFileSaveAsEvents | interface | 1 | 0 |
| ISEBendTableEvents | interface | 4 | 0 |
| ISEBlockTableEvents | interface | 1 | 0 |
| ISECommand | interface | 1 | 5 |
| ISECommandBar | interface | 4 | 15 |
| ISECommandBarButton | interface | 0 | 3 |
| ISECommandBarButtonEvents | interface | 3 | 0 |
| ISECommandBarControl | interface | 4 | 24 |
| ISECommandBarControls | interface | 2 | 3 |
| ISECommandBarPopup | interface | 0 | 2 |
| ISECommandBars | interface | 3 | 6 |
| ISECommandCategories | interface | 1 | 2 |
| ISECommandCategory | interface | 1 | 2 |
| ISECommandEvents | interface | 7 | 0 |
| ISECommandEx | interface | 1 | 0 |
| ISECommandEx2 | interface | 2 | 0 |
| ISECommandInfo | interface | 1 | 6 |
| ISECommandInfoEx | interface | 0 | 1 |
| ISECommandWindowEvents | interface | 1 | 0 |
| ISEConnectorTableEvents | interface | 1 | 0 |
| ISEDividePartEvents | interface | 3 | 0 |
| ISEDocumentEvents | interface | 4 | 0 |
| ISEDocumentEventsEx | interface | 2 | 0 |
| ISEDraftBendTableEvents | interface | 1 | 0 |
| ISEDrawingViewEvents | interface | 1 | 0 |
| ISEDynamicEditEvents | interface | 2 | 0 |
| ISEECEvents | interface | 3 | 0 |
| ISEECEventsEx | interface | 1 | 0 |
| ISEFamilyOfPartsEvents | interface | 3 | 0 |
| ISEFamilyOfPartsExEvents | interface | 3 | 0 |
| ISEFeatureLibraryEvents | interface | 3 | 0 |
| ISEFeatureSelectedFromPFEvents | interface | 1 | 0 |
| ISEFileUIEvents | interface | 6 | 0 |
| ISEIGLDisplayEvents | interface | 4 | 0 |
| ISEKeyBinding | interface | 0 | 5 |
| ISELocateFilterEvents | interface | 1 | 0 |
| ISEModelRecomputeEvents | interface | 6 | 0 |
| ISEMouse | interface | 2 | 32 |
| ISEMouseEvents | interface | 6 | 0 |
| ISEMouseEx | interface | 1 | 1 |
| ISEMouseEx2 | interface | 0 | 1 |
| ISEMouseEx3 | interface | 0 | 1 |
| ISENewFileUIEvents | interface | 1 | 0 |
| ISEOpenNonSolidEdgeFileUIEvents | interface | 1 | 0 |
| ISEPartsListEvents | interface | 1 | 0 |
| ISEPhysicalPropertiesChangeEvents | interface | 2 | 0 |
| ISERenderEvents | interface | 3 | 0 |
| ISESPEvents | interface | 3 | 0 |
| ISEShortCutMenuEvents | interface | 1 | 0 |
| ISESketchRecomputeEvents | interface | 4 | 0 |
| ISEViewEvents | interface | 3 | 0 |
| ISEhDCDisplayEvents | interface | 4 | 0 |
| ISolidEdgeAddIn | interface | 3 | 0 |
| ISolidEdgeBar | interface | 3 | 0 |
| ISolidEdgeBarEx | interface | 1 | 0 |
| ISolidEdgeBarEx2 | interface | 3 | 0 |
| ISolidEdgeCommandBar | interface | 20 | 0 |
| ISolidEdgeRibbonBar | interface | 9 | 0 |
| ISolidEdgeRibbonBarEx | interface | 1 | 0 |
| Insight | dispatch | 57 | 0 |
| InterDocumentUpdate | dispatch | 5 | 0 |
| InterpartLink | dispatch | 5 | 0 |
| InterpartLinks | dispatch | 1 | 3 |
| KeyBinding | dispatch | 0 | 5 |
| Layer | dispatch | 15 | 10 |
| Layers | dispatch | 2 | 4 |
| LinearStyle | dispatch | 2 | 10 |
| LinearStyles | dispatch | 3 | 4 |
| MatTable | dispatch | 59 | 0 |
| NamedView | dispatch | 4 | 3 |
| NamedViews | dispatch | 5 | 2 |
| PredefineRelationProducer | dispatch | 22 | 2 |
| Properties | dispatch | 4 | 4 |
| Property | dispatch | 2 | 3 |
| PropertyEx | dispatch | 3 | 3 |
| PropertySets | dispatch | 2 | 3 |
| QueryObjects | dispatch | 1 | 3 |
| RadialMenu | dispatch | 11 | 3 |
| Reference | dispatch | 2 | 8 |
| RibbonBar | dispatch | 0 | 4 |
| RibbonBarControl | dispatch | 0 | 9 |
| RibbonBarControls | dispatch | 3 | 4 |
| RibbonBarGroup | dispatch | 0 | 6 |
| RibbonBarGroups | dispatch | 3 | 3 |
| RibbonBarTab | dispatch | 1 | 6 |
| RibbonBarTabs | dispatch | 3 | 3 |
| RibbonBarTheme | dispatch | 0 | 7 |
| RibbonBarThemes | dispatch | 5 | 3 |
| RibbonBars | dispatch | 1 | 3 |
| RoutingSlip | dispatch | 4 | 15 |
| SEGenericCollection | dispatch | 1 | 3 |
| SectionView | dispatch | 6 | 15 |
| SectionViews | dispatch | 4 | 3 |
| SelectSet | dispatch | 13 | 4 |
| Sensor | dispatch | 2 | 15 |
| Sensors | dispatch | 4 | 3 |
| SheetMetalSensors | dispatch | 5 | 3 |
| SolidEdgeDocument | dispatch | 22 | 31 |
| SolidEdgeInsightXT | dispatch | 50 | 0 |
| SolidEdgeTCE | dispatch | 103 | 0 |
| SteeringWheel | dispatch | 5 | 0 |
| SummaryInfo | dispatch | 0 | 22 |
| SwitchWindowCust | dispatch | 7 | 3 |
| Symbol2d | dispatch | 24 | 31 |
| SymbolProperties | dispatch | 0 | 5 |
| Symbols | dispatch | 3 | 3 |
| TemplateManager | dispatch | 1 | 2 |
| TextCharStyle | dispatch | 2 | 13 |
| TextCharStyles | dispatch | 3 | 3 |
| TextStyle | dispatch | 2 | 13 |
| TextStyles | dispatch | 3 | 4 |
| UnitOfMeasure | dispatch | 0 | 3 |
| UnitsOfMeasure | dispatch | 3 | 3 |
| VariableList | dispatch | 3 | 1 |
| Variables | dispatch | 13 | 3 |
| View | dispatch | 60 | 33 |
| ViewStyle | dispatch | 32 | 38 |
| ViewStyles | dispatch | 5 | 3 |
| Window | dispatch | 8 | 25 |
| Windows | dispatch | 1 | 3 |
| _IApplicationAuto | interface | 81 | 76 |
| _IAttributeAuto | interface | 0 | 3 |
| _IAttributeQueryAuto | interface | 1 | 2 |
| _IAttributeSetAuto | interface | 3 | 2 |
| _IAttributeSetsAuto | interface | 3 | 1 |
| _ICPDInitializerAuto | interface | 6 | 0 |
| _ICPDInitializerBiDMAuto | interface | 4 | 0 |
| _ICPDInitializerInsightXTAuto | interface | 6 | 0 |
| _ICustomizationAuto | interface | 2 | 5 |
| _IDashStyleAuto | interface | 2 | 7 |
| _IDashStylesAuto | interface | 3 | 3 |
| _IDocumentsAuto | interface | 9 | 6 |
| _IDynamicVisualization | interface | 0 | 0 |
| _IDynamicVisualizationAuto | interface | 1 | 0 |
| _IEnvironmentAuto | interface | 0 | 12 |
| _IEnvironmentsAuto | interface | 1 | 3 |
| _IFaceStyleAuto | interface | 49 | 69 |
| _IFaceStylesAuto | interface | 4 | 3 |
| _IFillStyleAuto | interface | 0 | 13 |
| _IFillStylesAuto | interface | 3 | 4 |
| _IHatchPatternStyleAuto | interface | 34 | 11 |
| _IHatchPatternStylesAuto | interface | 3 | 3 |
| _IHighlightSetAuto | interface | 9 | 2 |
| _IHighlightSetsAuto | interface | 2 | 3 |
| _IInsightAuto | interface | 57 | 0 |
| _IInterDocumentUpdateAuto | interface | 5 | 0 |
| _IInterpartLinkAuto | interface | 5 | 0 |
| _IInterpartLinksAuto | interface | 1 | 3 |
| _ILayerAuto | interface | 15 | 10 |
| _ILayersAuto | interface | 2 | 4 |
| _ILinearStyleAuto | interface | 2 | 10 |
| _ILinearStylesAuto | interface | 3 | 4 |
| _IMatTableAuto | interface | 59 | 0 |
| _INamedViewAuto | interface | 4 | 3 |
| _INamedViewsAuto | interface | 5 | 2 |
| _IPredefineRelationProducerAuto | interface | 22 | 2 |
| _IPropertiesAuto | interface | 4 | 4 |
| _IPropertyAuto | interface | 2 | 3 |
| _IPropertyExAuto | interface | 1 | 0 |
| _IPropertySetsAuto | interface | 2 | 3 |
| _IQueryObjectsAuto | interface | 1 | 3 |
| _IRadialMenuAuto | interface | 11 | 3 |
| _IReferenceAuto | interface | 2 | 8 |
| _IRibbonBarAuto | interface | 0 | 4 |
| _IRibbonBarControlAuto | interface | 0 | 9 |
| _IRibbonBarControlsAuto | interface | 3 | 4 |
| _IRibbonBarGroupAuto | interface | 0 | 6 |
| _IRibbonBarGroupsAuto | interface | 3 | 3 |
| _IRibbonBarTabAuto | interface | 1 | 6 |
| _IRibbonBarTabsAuto | interface | 3 | 3 |
| _IRibbonBarThemeAuto | interface | 0 | 7 |
| _IRibbonBarThemesAuto | interface | 5 | 3 |
| _IRibbonBarsAuto | interface | 1 | 3 |
| _IRoutingSlipAuto | interface | 4 | 15 |
| _ISEGenericCollectionAuto | interface | 1 | 3 |
| _ISEInsight | interface | 0 | 0 |
| _ISectionViewAuto | interface | 6 | 15 |
| _ISectionViewsAuto | interface | 4 | 3 |
| _ISelectSetAuto | interface | 13 | 4 |
| _ISensorAuto | interface | 2 | 15 |
| _ISensorsAuto | interface | 4 | 3 |
| _ISheetMetalSensorsAuto | interface | 5 | 3 |
| _ISolidEdgeDocumentAuto | interface | 22 | 31 |
| _ISolidEdgeInsightXT | interface | 0 | 0 |
| _ISolidEdgeInsightXTAuto | interface | 50 | 0 |
| _ISolidEdgeTCE | interface | 0 | 0 |
| _ISolidEdgeTCEAuto | interface | 103 | 0 |
| _ISteeringWheelAuto | interface | 5 | 0 |
| _ISummaryInfoAuto | interface | 0 | 22 |
| _ISwitchWindowCustAuto | interface | 7 | 3 |
| _ISymbol2dAuto | interface | 24 | 31 |
| _ISymbolPropertiesAuto | interface | 0 | 5 |
| _ISymbolsAuto | interface | 3 | 3 |
| _ITemplateManagerAuto | interface | 1 | 2 |
| _ITextCharStyleAuto | interface | 2 | 13 |
| _ITextCharStylesAuto | interface | 3 | 3 |
| _ITextStyleAuto | interface | 2 | 13 |
| _ITextStylesAuto | interface | 3 | 4 |
| _IUnitOfMeasureAuto | interface | 0 | 3 |
| _IUnitsOfMeasureAuto | interface | 3 | 3 |
| _IVariableAuto | interface | 35 | 16 |
| _IVariableListAuto | interface | 3 | 1 |
| _IVariablesAuto | interface | 13 | 3 |
| _IViewAuto | interface | 60 | 33 |
| _IViewStyleAuto | interface | 32 | 38 |
| _IViewStylesAuto | interface | 5 | 3 |
| _IWindowAuto | interface | 8 | 25 |
| _IWindowsAuto | interface | 1 | 3 |
| variable | dispatch | 35 | 16 |

### CoClasses (44)

- **AddInEdgeBarEvents** (`{57C5D6DB-10B7-4904-BDCE-3162EAFE393B}`): IUnknown, ISEAddInEdgeBarEvents
- **AddInEvents** (`{0F539243-4816-11D2-B5AC-080036E8B802}`): IUnknown, ISEAddInEvents, DISEAddInEvents
- **AddInSaveAsTranslatorEvents** (`{611EDD20-8236-4733-9D70-4E15D5DA7488}`): IUnknown, ISEAddInSaveAsTranslatorEvents
- **AnimationEvents** (`{F21AE4BC-6EFD-4FC3-9B6E-FB090E4CD5D0}`): IUnknown, DISEAnimationEvents, ISEAnimationEvents
- **ApplicationEvents** (`{EB4193C7-8C5A-11D1-BA85-080036230602}`): IUnknown, DISEApplicationEvents, ISEApplicationEvents
- **ApplicationV8DocumentOpenEvent** (`{3ADAF821-EF13-41B6-A7F6-D3A2F297C0E6}`): IUnknown, ISEApplicationV8AfterDocumentOpenEvent
- **ApplicationWindowEvents** (`{25045F7E-965C-11D1-BA90-080036230602}`): IUnknown, DISEApplicationWindowEvents, ISEApplicationWindowEvents
- **AssemblyChangeEvents** (`{5D00D4E3-AF48-4A81-848E-BA85A1E7DA54}`): IUnknown, ISEAssemblyChangeEvents, DISEAssemblyChangeEvents
- **AssemblyConfigurationChangeEvents** (`{653FE660-47DB-4C5A-9FCA-E9C971218C65}`): IUnknown, ISEAssemblyConfigurationChangeEvents, DISEAssemblyConfigurationChangeEvents
- **AssemblyFamilyEvents** (`{EF8B9F76-70ED-4A9A-88DA-3B76869D8E78}`): IUnknown, DISEAssemblyFamilyEvents, ISEAssemblyFamilyEvents
- **AssemblyFamilyEvents2** (`{96C93307-1AAA-4E6F-937C-AC6C726B56E5}`): IUnknown, DISEAssemblyFamilyEvents2, ISEAssemblyFamilyEvents2
- **AssemblyPhysicalPropertiesChangeEvents** (`{F4B15DBB-C4B2-4F8F-8B1C-C3EF3429EB53}`): IUnknown, ISEAssemblyPhysicalPropertiesChangeEvents, DISEAssemblyPhysicalPropertiesChangeEvents
- **AssemblyRecomputeEvents** (`{03CFED71-8E07-11D3-A3E6-0004AC969A5D}`): IUnknown, ISEAssemblyRecomputeEvents, DISEAssemblyRecomputeEvents
- **BeforeFileSaveAsEvents** (`{18B5C96E-71A3-417B-BDAA-97923794ACAC}`): IUnknown, DISEBeforeFileSaveAsEvents, ISEBeforeFileSaveAsEvents
- **BendTableEvents** (`{30837272-1899-4F51-8969-0AA3BD1DC3E4}`): IUnknown, DISEBendTableEvents, ISEBendTableEvents
- **BiDMEvents** (`{31B7689B-B25C-4AE8-8A4E-96F1130FA4A6}`): IUnknown, IBiDMEvents
- **BlockTableEvents** (`{395A16D6-0075-4D64-AEC1-F9E08CB09CF0}`): IUnknown, ISEBlockTableEvents
- **Command** (`{3B77DE42-6B3E-11D1-919E-08003601BE21}`): DISECommand, DISECommandEvents, ISECommand, ISECommandEvents
- **CommandBarButtonEvents** (`{59DE95A1-9CA6-11D1-BA97-080036230602}`): IUnknown, ISECommandBarButtonEvents, DISECommandBarButtonEvents
- **CommandWindow** (`{3B77DE46-6B3E-11D1-919E-08003601BE21}`): IUnknown, DISECommandWindowEvents, ISECommandWindowEvents
- **ConnectorTableEvents** (`{EEEF65B9-ECC4-4157-BFD1-C4D2075FA285}`): IUnknown, ISEConnectorTableEvents
- **DisplayEvents** (`{791849E0-A4AA-11D1-AECC-08003616CE02}`): IUnknown, DISEhDCDisplayEvents, ISEhDCDisplayEvents
- **DividePartEvents** (`{03A58A84-9CFB-11D3-A3F0-0004AC969A5D}`): IUnknown, ISEDividePartEvents
- **DocumentEvents** (`{0EA0D1F0-A199-11D1-AECC-08003616CE02}`): IUnknown, DISEDocumentEvents, ISEDocumentEvents
- **DraftBendTableEvents** (`{E8371752-4A37-4BBA-8EE8-9F68337FE5AC}`): IUnknown, ISEDraftBendTableEvents
- **DrawingViewEvents** (`{2D93AEED-3B14-11D4-A4D3-0004AC9695CB}`): IUnknown, ISEDrawingViewEvents
- **FamilyOfPartsEvents** (`{A054F88C-9C75-11D3-A3F0-0004AC969A5D}`): IUnknown, ISEFamilyOfPartsEvents
- **FamilyOfPartsExEvents** (`{80E1310F-C681-4FEC-8F5C-9449D8B33AFF}`): IUnknown, ISEFamilyOfPartsExEvents
- **FeatureLibraryEvents** (`{EBF71668-ACF0-11D3-A3F3-0004AC969A5D}`): IUnknown, ISEFeatureLibraryEvents
- **FeatureSelectedFromPFEvents** (`{215C74C1-EC59-4DC1-9888-B806B9BAB3A3}`): IUnknown, DISEFeatureSelectedFromPFEvents, ISEFeatureSelectedFromPFEvents
- **FileUIEvents** (`{ECC667A0-A4AA-11D1-AECC-08003616CE02}`): IUnknown, DISEFileUIEvents, ISEFileUIEvents
- **GLDisplayEvents** (`{2A11B897-CCC5-11D2-9231-00C04F79BE98}`): IUnknown, ISEIGLDisplayEvents
- **ModelRecomputeEvents** (`{6A89DFD0-9E7D-11D1-AECC-08003616CE02}`): IUnknown, ISEModelRecomputeEvents
- **Mouse** (`{3B77DE44-6B3E-11D1-919E-08003601BE21}`): DISEMouse, DISEMouseEvents, ISEMouse, ISEMouseEx, ISEMouseEvents
- **NewFileUIEvents** (`{206AF232-E02E-4F19-9101-B28C2A565100}`): IUnknown, ISENewFileUIEvents
- **OpenNonSolidEdgeFileUIEvents** (`{DD0C475C-D9B3-4150-935E-6E556444882C}`): IUnknown, ISEOpenNonSolidEdgeFileUIEvents
- **PartsListEvents** (`{21EE3695-5BCC-4815-8A40-209EF7D3EEE4}`): IUnknown, ISEPartsListEvents
- **PhysicalPropertiesChangeEvents** (`{2D10AE62-4DE5-4EEC-9124-0ED3067B7574}`): IUnknown, ISEPhysicalPropertiesChangeEvents
- **RenderEvents** (`{2A11B898-CCC5-11D2-9231-00C04F79BE98}`): IUnknown, ISERenderEvents
- **SEECEvents** (`{9CB472ED-39B7-44D5-B8AA-AC9A4EAA30A0}`): IUnknown, ISEECEvents
- **SESPEvents** (`{1CEC80A4-3FDD-493E-9F33-56A96077099A}`): IUnknown, ISESPEvents
- **ShortcutMenuEvents** (`{FEFB7665-5732-4BF0-8E46-D1E158ED20D3}`): IUnknown, ISEShortCutMenuEvents
- **SketchRecomputeEvents** (`{15264F78-B291-4587-95DB-B35979CADD23}`): IUnknown, DISESketchRecomputeEvents, ISESketchRecomputeEvents
- **ViewEvents** (`{5BDAAD30-966B-11D1-AECB-08003616CE02}`): IUnknown, DISEViewEvents, ISEViewEvents

### Aliases (5)

- LONG_PTR = VT_I8
- MatTablePropIndex = MatTablePropIndexConstants
- UINT_PTR = VT_UI8
- seAssemblyChangeEventsConstants = AssemblyChangeEventsConstants
- seAssemblyEventConstants = AssemblyEventConstants

---
## Program/fwksupp.tlb
**Solid Edge FrameworkSupport Type Library** (GUID: `{943AC5C6-F4DB-11D1-BE00-080036B4D502}`, v1.0)

### Enums (120)

- **AnchorPointLocationConstants** [9]: igAnchorPointTopLeft=0, igAnchorPointTopCenter=1, igAnchorPointTopRight=2, igAnchorPointMiddleLeft=3, igAnchorPointMiddleCenter=4, ... (9 total)
- **AngularDimensionQuadrantConstants** [5]: igFirstQuadrant=0, igSecondQuadrant=1, igThirdQuadrant=2, igFourthQuadrant=3, igMajorQuadrant=4
- **Boundary2dStateConstants** [3]: igBoundary2dUndefined=0, igBoundary2dUpToDate=1, igBoundary2dUnableToCompute=2
- **ComponentImageCreationModeConstants** [2]: seAllVisible=0, seExplicit=1
- **ConnectorTypeConstants** [5]: seLineConnector=0, seJumpConnector=1, seCornerConnector=2, seStepConnector=3, seGapConnector=4
- **CurveFitTypeConstants** [3]: igLinestringFit=0, igDirectFit=1, igLeastSquareFit=2
- **CuttingPlaneLineDisplayStyleConstants** [3]: seThick=1, seThickCornersOnly=2, seThickThin=3
- **DimAngularCoordnateOrientationConstants** [2]: igDimAngCoordOrientClockwise=0, igDimAngCoordOrientCounterClockwise=1
- **DimAngularUnitConstants** [3]: igDimStyleAngularDegMinSec=1, igDimStyleAngularRadians=2, igDimStyleAngularDegrees=3
- **DimAxisModeConstants** [4]: igDimAxisModeDefault=1, igDimAxisModeImplied=2, igDimAxisModeExplicit=3, igDimAxisModeCoordinate=4
- **DimBalloonDirTypeConstants** [4]: igDimBalloonDirectionLeft=1, igDimBalloonDirectionRight=2, igDimBalloonDirectionTop=3, igDimBalloonDirectionBottom=4
- **DimBalloonTypeConstants** [14]: igDimBalloonNone=0, igDimBalloonCircle=1, igDimBalloonNSided=2, igDimBalloonSquare=3, igDimBalloonSquareRotated=4, ... (14 total)
- **DimBreakPositionConstants** [4]: igDimBreakRight=1, igDimBreakCenter=2, igDimBreakLeft=3, igDimBreakAltCenter=4
- **DimCalloutBalloonBreaklineDirectionConstants** [4]: igDimCalloutBalloonBreaklineDirectionWest=0, igDimCalloutBalloonBreaklineDirectionNorth=1, igDimCalloutBalloonBreaklineDirectionEast=2, igDimCalloutBalloonBreaklineDirectionSouth=3
- **DimCalloutLeaderTextConnectionPointConstants** [10]: igDimCalloutLeaderTextConnectionPointDefaultLeft=0, igDimCalloutLeaderTextConnectionPointTopLeft=1, igDimCalloutLeaderTextConnectionPointTopCenter=2, igDimCalloutLeaderTextConnectionPointTopRight=3, igDimCalloutLeaderTextConnectionPointDefaultRight=4, ... (10 total)
- **DimCalloutTextWidthModeConstants** [3]: igDimCalloutFitToContent=1, igDimCalloutFixedAutoAspectRatio=2, igDimCalloutFixedWrapText=3
- **DimCenterlineTypeConstants** [4]: igDimCenterlineNormal=1, igDimCenterlineMidway=2, igDimCenterArcByCenterPoint=3, igDimCenterArcBy2Arcs=4
- **DimChamferModeConstants** [4]: igDimChamferModeAlongAxis=0, igDimChamferModePerpendicular=1, igDimChamferModeParallel=2, igDimChamferModeNotApplicable=3
- **DimCommonOriginTypeConstants** [3]: igDimStyleCommonOrigNone=6, igDimStyleCommonOrigDot=7, igDimStyleCommonOrigCircle=8
- **DimCoordTextPositionConstants** [2]: igDimStyleCoordTextAbove=1, igDimStyleCoordTextInLine=2
- **DimDMSRoundOffTypeConstants** [6]: igDimStyleAngular10Degree=1, igDimStyleAngular1Degree=2, igDimStyleAngular10Minute=3, igDimStyleAngular1Minute=4, igDimStyleAngular10Second=5, ... (6 total)
- **DimDatumPointTypeConstants** [3]: igDimDatumPointCross=1, igDimDatumPointCircle=2, igDimDatumPointRectangle=3
- **DimDatumTargetLeaderTypeConstants** [2]: igDimDatumTargetNearSide=1, igDimDatumTargetFarSide=2
- **DimDatumTargetTermTypeConstants** [4]: igDimStyleDatumTargetTermHollow=1, igDimStyleDatumTargetTermFilled=2, igDimStyleDatumTargetTermOpen=3, igDimStyleDatumTargetTermBlank=4
- **DimDatumTargetTypeConstants** [3]: igDimDatumTargetRegular=1, igDimDatumTargetMovable=2, igDimDatumTargetAlignedMovable=3
- **DimDatumTermTypeConstants** [4]: igDimStyleDatumTermNormal=1, igDimStyleDatumTermAnchor=2, igDimStyleDatumTermLine=3, igDimStyleDatumTermAnchorHollow=4
- **DimDecimalRoundOffTypeConstants** [9]: igDimStyleDecimal10=1, igDimStyleDecimal1=2, igDimStyleDecimal_1=3, igDimStyleDecimal_2=4, igDimStyleDecimal_3=5, ... (9 total)
- **DimDelimiterTypeConstants** [3]: igDimStyleDelimiterDot=1, igDimStyleDelimiterComma=2, igDimStyleDelimiterSpace=3
- **DimDispTypeConstants** [14]: igDimDisplayTypeNominal=1, igDimDisplayTypeTolerance=2, igDimDisplayTypeClassfit=3, igDimDisplayTypeLimits=4, igDimDisplayTypeBasic=5, ... (14 total)
- **DimDualUnitPositionConstants** [2]: igDimStyleDualUnitPositionAsBelowPrimary=1, igDimStyleDualUnitPositionAsBesidePrimary=2
- **DimFCFLeaderTextConnectionPointConstants** [9]: igDimFCFLeaderTextConnectionPointCenter=0, igDimFCFLeaderTextConnectionPointMiddleLeft=1, igDimFCFLeaderTextConnectionPointTopLeft=2, igDimFCFLeaderTextConnectionPointTopMiddle=3, igDimFCFLeaderTextConnectionPointTopRight=4, ... (9 total)
- **DimFCFOrientationConstants** [4]: igDimFCFOrientationVertical=0, igDimFCFOrientationHorizontal=1, igDimFCFOrientationPerpendicular=2, igDimFCFOrientationParallel=3
- **DimFractionRoundOffTypeConstants** [7]: igDimStyleFraction_1=1, igDimStyleFraction_2=2, igDimStyleFraction_4=3, igDimStyleFraction_8=4, igDimStyleFraction_16=5, ... (7 total)
- **DimGostWeldPermanentJointTypeConstants** [5]: igDimGostWeldPermJointAdhesive=0, igDimGostWeldPermJointSolder=1, igDimGostWeldPermJointStitch=2, igDimGostWeldPermJointBracket=3, igDimGostWeldPermJointAngled=4
- **DimGostWeldTerminatorTypeConstants** [3]: igDimGostWeldTerminatorSameSide=0, igDimGostWeldTerminatorOtherSide=1, igDimGostWeldTerminatorFullArrow=2
- **DimGroupMemberTypeConstants** [4]: seDimNotAGroupMember=1, seDimStackGroupMember=2, seDimChainGroupMember=3, seDimCoordinateGroupMember=4
- **DimHoleShaftSeparatorTypeConstants** [3]: igDimStyleShowHoleShaftSeparatorTypeAsSlash=1, igDimStyleShowHoleShaftSeparatorTypeAsSeparator=2, igDimStyleShowHoleShaftSeparatorTypeAsSpace=3
- **DimItemNumDirConstants** [3]: igDimItemNumberDirectionNone=0, igDimItemNumberDirectionClockwise=1, igDimItemNumberDirectionCounterClockwise=2
- **DimLimitTextArrangmentConstants** [2]: igDimStyleLimitTextHorizontal=1, igDimStyleLimitTextVertical=2
- **DimLineDisplayTypeConstants** [4]: igDimStyleDimLineNone=0, igDimStyleDimLineOrig=1, igDimStyleDimLineMeas=2, igDimStyleDimLineBoth=3
- **DimLinearUnitConstants** [6]: igDimStyleLinearFtIn=1, igDimStyleLinearMeters=2, igDimStyleLinearMM=3, igDimStyleLinearCM=4, igDimStyleLinearInches=5, ... (6 total)
- **DimNTSTypeConstants** [3]: igDimStyleNTSNone=1, igDimStyleNTSUnderline=2, igDimStyleNTSZigzag=3
- **DimOffsetLeaderTypeConstants** [1]: igDimStyleOffsetLeaderLine=1
- **DimProjArcConstants** [3]: igDimProjArcNone=1, igDimProjArcStart=2, igDimProjArcEnd=3
- **DimProjDisplayTypeConstants** [4]: igDimStyleProjLineNone=0, igDimStyleProjLineOrig=1, igDimStyleProjLineMeas=2, igDimStyleProjLineBoth=3
- **DimProjTolZonePositionConstants** [2]: igDimStyleProjTolZoneInLine=1, igDimStyleProjTolZoneBelow=2
- **DimReattachStatusConstants** [2]: igDimReattachSucceeded=0, igDimReattachFailed=1
- **DimRoundOffTypeConstants** [2]: igDimStyleDecimal=1, igDimStyleFraction=2
- **DimRoundUpTypeConstants** [2]: igDimStyleRoundUpAll=1, igDimStyleRoundUpOdd=2
- **DimScaleModeConstants** [2]: igDimStyleScaleManual=0, igDimStyleScaleAutomatic=1
- **DimStackFractionSizeConstants** [8]: igDimStyleFractSize50=1, igDimStyleFractSize60=2, igDimStyleFractSize66=3, igDimStyleFractSize70=4, igDimStyleFractSize75=5, ... (8 total)
- **DimStackFractionTypeConstants** [3]: igDimStyleFractionStacked=1, igDimStyleFractionSkewed=2, igDimStyleFractionLinear=3
- **DimStatusConstants** [6]: seDimStatusDetached=1, seDimStatusError=2, seDimStatusDriving=3, seDimStatusDriven=4, seOneEndDetached=5, ... (6 total)
- **DimStyleDatumFrameShapeConstants** [2]: igDimStyleDatumFrameShapeRectangle=1, igDimStyleDatumFrameShapeCircle=2
- **DimStyleSecondaryUnitSeparatorConstants** [3]: igDimStyleSecondaryUnitSeparatorNothing=0, igDimStyleSecondaryUnitSeparatorParenthesis=1, igDimStyleSecondaryUnitSeparatorBrackets=2
- **DimStyleSymbolFontConstants** [2]: igDimStyleSymbolFontANSI=1, igDimStyleSymbolFontISO=2
- **DimSurfTextureLaySymTypeConstants** [9]: igDimSurfaceFinishLayNone=1, igDimSurfaceFinishLayPerpendicular=2, igDimSurfaceFinishLayVtParallel=3, igDimSurfaceFinishLayHzParallel=4, igDimSurfaceFinishLayCrossed=5, ... (9 total)
- **DimSurfTextureSymTypeConstants** [23]: igDimSurfaceFinishBasic=1, igDimSurfaceFinishMachined=2, igDimSurfaceFinishNoMaterialRemoval=3, igDimSurfaceFinishBasicHz=4, igDimSurfaceFinishMachinedHz=5, ... (23 total)
- **DimSymbolPositionConstants** [3]: igDimStyleSymbolNone=1, igDimStyleSymbolBefore=2, igDimStyleSymbolAfter=3
- **DimTermDisplayTypeConstants** [4]: igDimStyleTermNone=0, igDimStyleTermOrig=1, igDimStyleTermMeas=2, igDimStyleTermBoth=3
- **DimTermTypeConstants** [16]: igDimStyleTermHollow=1, igDimStyleTermFilled=2, igDimStyleTermOpen=3, igDimStyleTermSlash=4, igDimStyleTermBackSlash=5, ... (16 total)
- **DimTextFontStyleConstants** [4]: igDimStyleFontNormal=1, igDimStyleFontBold=2, igDimStyleFontItalic=3, igDimStyleFontItalicBold=4
- **DimTextOrientationConstants** [4]: igDimStyleTextHorizontal=1, igDimStyleTextVertical=2, igDimStyleTextParallel=3, igDimStyleTextPerpendicular=4
- **DimTextPositionConstants** [2]: igDimStyleTextAbove=1, igDimStyleTextEmbedded=2
- **DimToleranceTextHorizontalAlignOptionsConstants** [2]: igDimStyleToleranceTextHorizontalAlignBySign=1, igDimStyleToleranceTextHorizontalAlignByDecimalPoint=2
- **DimTypeConstants** [12]: igDimTypeLinear=1, igDimTypeRadial=2, igDimTypeAngular=3, igDimTypeRDiameter=4, igDimTypeCDiameter=5, ... (12 total)
- **DimViewCPLCaptionLocationConstants** [4]: igDimViewCPLCaptionLocationFrom=1, igDimViewCPLCaptionLocationOn=2, igDimViewCPLCaptionLocationTo=3, igDimViewCPLCaptionLocationOutsideOpenEnd=4
- **DimViewCaptionLocationConstants** [2]: igDimViewCaptionLocationTop=1, igDimViewCaptionLocationBottom=2
- **DimViewCuttingPlaneDisplayTypeConstants** [2]: igDimViewCuttingPlaneLineDisplayTo=1, igDimViewCuttingPlaneLineDisplayFrom=2
- **DimViewPlaneDisplayTypeConstants** [2]: igDimViewPlaneLineDisplaySingle=1, igDimViewPlaneLineDisplayDouble=2
- **DimWeldDashLineTypeConstants** [3]: igDimWeldDashLineNone=0, igDimWeldDashLineAbove=1, igDimWeldDashLineBelow=2
- **DimWeldModifierConstants** [3]: igDimWeldModifierNone=0, igDimWeldTopThreeSided=1, igDimWeldBottomThreeSided=2
- **DimWeldTailTypeConstants** [3]: igDimWeldTailNone=0, igDimWeldTailOpen=1, igDimWeldTailClosed=2
- **DimWeldTreatmentTypeConstants** [7]: igDimWeldTreatmentNone=0, igDimWeldTreatmentFlush=1, igDimWeldTreatmentConcave=2, igDimWeldTreatmentConvex=3, igDimWeldTreatmentSmoothBlend=4, ... (7 total)
- **DimWeldTypeConstants** [84]: igDimWeldTypeNone=0, igDimWeldTopFillet=1, igDimWeldTopSpot=2, igDimWeldTopSeam=3, igDimWeldTopBevel=4, ... (84 total)
- **DimensionOrientationConstants** [2]: igOrientationHorizontal=0, igOrientationVertical=1
- **DisplayTypeConstants** [3]: igDisplayTypeContents=1, igDisplayTypeIcon=2, igDisplayTypeThumbnail=3
- **DrawingViewAnnotationTypeConstants** [3]: seCuttingPlane=1, seViewingPlane=2, seDetailEnvelope=3
- **DrawingViewCaptionTextAlignment** [3]: seTextAlignmentLeft=1, seTextAlignmentCenter=2, seTextAlignmentRight=3
- **DrawingViewCaptionTypeConstants** [6]: sePrincipalView=1, seSectionView=2, seAuxiliaryView=3, seDetailView=4, se2DModelView=5, ... (6 total)
- **DrawingViewStyleSheetNumberLocationConstants** [3]: seLeftArrow=1, seRightArrow=2, seBothArrows=3
- **DynamicGridSpacingConstants** [3]: igDynamicGridFine=0, igDynamicGridNormal=1, igDynamicGridCoarse=2
- **FrameShapeConstants** [2]: igRectangularFrame=1, igEllipticalFrame=2
- **Geom2dFormConstants** [7]: igGeom2dFormUnknown=0, igGeom2dFormOpen=1, igGeom2dFormClosed=2, igGeom2dFormClosedWithTangents=3, igGeom2dFormClosedWithCurvature=4, ... (7 total)
- **Geom2dOrientationConstants** [2]: igGeom2dOrientClockwise=0, igGeom2dOrientCounterClockwise=1
- **Geom2dScopeConstants** [5]: igGeom2dScopeUnknown=0, igGeom2dScopePlaner=1, igGeom2dScopeColinear=2, igGeom2dScopeDegenerate=3, igGeom2dScopeNonplaner=4
- **GridTypeConstants** [2]: igGridDynamic=0, igGridStatic=1
- **HandleType** [7]: igHandleNone=0, igHandleReadOnly=1, igHandleWriteable=2, igHandleInvisible=4, igHandleRotate=8, ... (7 total)
- **LayoutElementTypeConstants** [4]: igTemplateEditor3DView=1, igTemplateEditorViewCarousel=2, igTemplateEditorBOMTable=3, igTemplateEditorPDFText=4
- **PMIEditDirectionConstants** [3]: seMoveOriginParent=1, seMoveMeasureParent=2, seMoveParentsSymmetrically=3
- **PMIModelViewStandardOrientationConstants** [9]: sePMIModelViewFront=0, sePMIModelViewBack=1, sePMIModelViewLeft=2, sePMIModelViewRight=3, sePMIModelViewTop=4, ... (9 total)
- **PMIRenderModeConstants** [5]: sePMIModelViewRenderModeNone=0, sePMIModelViewRenderModeVisibleEdges=1, sePMIModelViewRenderModeVisibleAndHiddenEdges=2, sePMIModelViewRenderModeShaded=3, sePMIModelViewRenderModeShadedWithVisibleEdges=4
- **PatternOffsetTypeConstants** [4]: sePatternFitOffset=0, sePatternFillOffset=1, sePatternFixedOffset=2, sePatternChordLengthOffset=3
- **PlacementMethodConstants** [4]: igByOrigin=1, igByFrameBoundaries=2, igByCascadeMethod=3, igByDefaultStateData=4
- **ReferencedObjectTypeConstants** [11]: igReferencedObjectTypeNone=0, igReferencedObjectTypeCallout=1, igReferencedObjectTypeBalloon=2, igReferencedObjectTypeDatumFrame=3, igReferencedObjectTypeDatumTarget=4, ... (11 total)
- **SizeModeConstants** [3]: igFrameCrops=1, igFrameChangesSize=2, igObjectScaled=3
- **StaggerTypeConstants** [3]: seNoStagger=0, seRowStagger=1, seColumnStagger=2
- **SubfixAlignmentConstants** [3]: seSubfixAlignLeft=0, seSubfixAlignCenter=1, seSubfixAlignRight=2
- **TableStyleLineTypeConstants** [7]: seBorder=0, seTitleSeparator=1, seTitleHeaderSeparator=2, seHeaderDataSeparator=3, seHeaderSeparator=4, ... (7 total)
- **TextBorderTypeConstants** [2]: igTextBorderNone=0, igTextBorderRectangle=1
- **TextBulletTypeConstants** [8]: igFilledRound=0, igHollowRound=1, igFilledSquare=2, igHollowSquare=3, igStar=4, ... (8 total)
- **TextControlTypeConstants** [3]: igTextFitToContent=0, igTextAdjustAspectRatio=1, igTextWrap=2
- **TextFlowDirectionConstants** [2]: igTextLeftToRight=0, igTextRightToLeft=1
- **TextFlowOrientationConstants** [2]: igTextHorizontal=0, igTextVertical=1
- **TextFractionAlignConstants** [3]: igUpper=1, igMiddle=2, igLower=3
- **TextFractionSizeConstants** [10]: ig10=0, ig20=1, ig30=2, ig40=3, ig50=4, ... (10 total)
- **TextFractionTypeConstants** [4]: igStacked=1, igTolerance=2, igSkewed=3, igLinearFraction=4
- **TextHorizontalAlignmentConstants** [5]: igTextHzAlignLeft=0, igTextHzAlignCenter=1, igTextHzAlignRight=2, igTextHzAlignIndent=3, igTextHzAlignJustify=16
- **TextJustificationConstants** [8]: igTextJustifyTop=0, igTextJustifyLeft=0, igTextJustifyCenter=1, igTextJustifyRight=2, igTextJustifyVCenter=4, ... (8 total)
- **TextLineSpacingTypeConstants** [6]: igSingle=0, igOneAndHalf=1, igDouble=2, igAtLeast=3, igExactly=4, ... (6 total)
- **TextNumberFormatConstants** [4]: igNoFormat=0, igPeriod=1, igBracket=2, igDoubleBrackets=3
- **TextNumberJustificationConstants** [3]: igLeftJustification=0, igCenterJustification=1, igRightJustification=2
- **TextNumberTypeConstants** [5]: igPlain=0, igCapitalRoman=1, igSmallRoman=2, igCapitalLatinAlpha=3, igSmallLatinAlpha=4
- **TextPlacementTypeConstants** [2]: igTextBoxType=1, igTextStringType=2
- **TextSelectConstants** [4]: seTextSelectRange=0, seTextSelectWord=1, seTextSelectParagraph=2, seTextSelectAll=5
- **TextSpecialIndentTypeConstants** [3]: igIndentNone=0, igFirstline=1, igHanging=2
- **TextTabTypeConstants** [4]: igTextTabFlushLeft=1, igTextTabFlushRight=2, igTextTabFlushCentered=3, igTextTabFlushDecimal=4
- **TextVerticalAlignmentConstants** [3]: igTextVtAlignTop=0, igTextHzAlignVCenter=1, igTextHzAlignBottom=8
- **UpdateOptionConstants** [3]: igUpdateAutomatic=1, igUpdateOnSave=2, igUpdateManual=3
- **WeldSymbolFlagDirectionConstants** [2]: igRightFlag=0, igLeftFlag=1

### Interfaces (228)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| AnnotAlignmentShape | dispatch | 13 | 16 |
| AnnotAlignmentShapes | dispatch | 2 | 3 |
| AnnotInitData | dispatch | 15 | 1 |
| Arc2d | dispatch | 34 | 23 |
| Arcs2d | dispatch | 5 | 3 |
| AreaProperties | dispatch | 18 | 11 |
| AreaPropertiesCollection | dispatch | 2 | 3 |
| BSplineCurve2d | dispatch | 43 | 28 |
| BSplineCurves2d | dispatch | 4 | 3 |
| BackDrop | dispatch | 0 | 11 |
| Balloon | dispatch | 41 | 58 |
| Balloons | dispatch | 6 | 6 |
| BoltHoleCircle | dispatch | 18 | 20 |
| BoltHoleCircles | dispatch | 5 | 4 |
| Boundaries2d | dispatch | 3 | 3 |
| Boundary2d | dispatch | 19 | 17 |
| BoundaryStyle2d | dispatch | 1 | 10 |
| BoundingObjects2d | dispatch | 1 | 3 |
| CenterLine | dispatch | 29 | 18 |
| CenterLines | dispatch | 14 | 6 |
| CenterMark | dispatch | 25 | 21 |
| CenterMarks | dispatch | 8 | 7 |
| ChamferGeometry2d | dispatch | 3 | 3 |
| Circle2d | dispatch | 28 | 21 |
| Circles2d | dispatch | 3 | 3 |
| CircularPattern2d | dispatch | 2 | 10 |
| CircularPatterns2d | dispatch | 5 | 3 |
| ComplexString2d | dispatch | 26 | 18 |
| ComplexStrings2d | dispatch | 2 | 3 |
| ComponentImage2d | dispatch | 1 | 7 |
| ComponentImages2d | dispatch | 2 | 3 |
| Conic2d | dispatch | 28 | 13 |
| Conics2d | dispatch | 2 | 3 |
| Connector | dispatch | 31 | 14 |
| Connectors | dispatch | 3 | 3 |
| CornerAnnotation | dispatch | 31 | 34 |
| CornerAnnotations | dispatch | 6 | 6 |
| Curve2d | dispatch | 30 | 21 |
| Curves2d | dispatch | 2 | 3 |
| DatumFrame | dispatch | 32 | 26 |
| DatumFrames | dispatch | 6 | 6 |
| DatumPoint | dispatch | 29 | 21 |
| DatumPoints | dispatch | 6 | 7 |
| DatumTarget | dispatch | 34 | 30 |
| DatumTargets | dispatch | 6 | 6 |
| DimInitData | dispatch | 17 | 1 |
| DimStyle | dispatch | 1 | 188 |
| Dimension | dispatch | 59 | 86 |
| DimensionStyle | dispatch | 0 | 198 |
| DimensionStyles | dispatch | 5 | 4 |
| Dimensions | dispatch | 25 | 10 |
| DisplayData | dispatch | 17 | 0 |
| DrawingObjects | dispatch | 1 | 3 |
| DrawingViewStyle | dispatch | 0 | 52 |
| DrawingViewStyles | dispatch | 3 | 4 |
| Ellipse2d | dispatch | 30 | 24 |
| Ellipses2d | dispatch | 2 | 3 |
| EllipticalArc2d | dispatch | 36 | 23 |
| EllipticalArcs2d | dispatch | 3 | 3 |
| FeatureControlFrame | dispatch | 33 | 47 |
| FeatureControlFrameDataSet | dispatch | 0 | 21 |
| FeatureControlFrameDataSets | dispatch | 3 | 3 |
| FeatureControlFrames | dispatch | 7 | 7 |
| FilletGeometry2d | dispatch | 1 | 0 |
| Frame | dispatch | 0 | 7 |
| GeometryStyle2d | dispatch | 3 | 8 |
| GostWeldSymbol | dispatch | 31 | 36 |
| GostWeldSymbols | dispatch | 5 | 6 |
| Group | dispatch | 22 | 49 |
| GroupStyle | dispatch | 3 | 8 |
| Groups | dispatch | 4 | 3 |
| Image2d | dispatch | 7 | 22 |
| Images2d | dispatch | 3 | 3 |
| Leader | dispatch | 36 | 25 |
| Leaders | dispatch | 8 | 6 |
| Line2d | dispatch | 30 | 21 |
| LineString2d | dispatch | 33 | 18 |
| LineStrings2d | dispatch | 2 | 3 |
| Lines2d | dispatch | 4 | 3 |
| PMI | dispatch | 2 | 25 |
| PMIModelView | dispatch | 11 | 11 |
| PMIModelViews | dispatch | 3 | 3 |
| Point2d | dispatch | 24 | 17 |
| Points2d | dispatch | 2 | 3 |
| RectangularPattern2d | dispatch | 2 | 17 |
| RectangularPatterns2d | dispatch | 3 | 3 |
| Relation2d | dispatch | 5 | 10 |
| Relations2d | dispatch | 27 | 1 |
| Relationships2d | dispatch | 1 | 3 |
| SmartFrame2d | dispatch | 26 | 37 |
| SmartFrame2dDefaults | dispatch | 2 | 10 |
| SmartFrame2dStyle | dispatch | 2 | 29 |
| SmartFrame2dStyles | dispatch | 2 | 4 |
| SmartFrames2d | dispatch | 3 | 3 |
| SurfaceFinishSymbol | dispatch | 32 | 39 |
| SurfaceFinishSymbolDataSet | dispatch | 0 | 14 |
| SurfaceFinishSymbolDataSets | dispatch | 3 | 3 |
| SurfaceFinishSymbols | dispatch | 6 | 7 |
| SymbolicPMI | dispatch | 3 | 10 |
| SymbolicPMIGroup | dispatch | 1 | 3 |
| TableStyle | dispatch | 0 | 9 |
| TableStyles | dispatch | 3 | 3 |
| TechnicalRequirement | dispatch | 6 | 5 |
| TechnicalRequirements | dispatch | 2 | 3 |
| TextBox | dispatch | 23 | 43 |
| TextBoxes | dispatch | 6 | 3 |
| TextEdit | dispatch | 22 | 30 |
| TextProfile | dispatch | 15 | 12 |
| TextProfiles | dispatch | 1 | 3 |
| VFSet | dispatch | 5 | 2 |
| WeldSymbol | dispatch | 36 | 59 |
| WeldSymbolDataSet | dispatch | 0 | 22 |
| WeldSymbolDataSets | dispatch | 3 | 3 |
| WeldSymbols | dispatch | 7 | 7 |
| _IAnnotAlignmentShapeAuto | interface | 13 | 16 |
| _IAnnotAlignmentShapesAuto | interface | 2 | 3 |
| _IAnnotInitDataAuto | interface | 15 | 1 |
| _IArc2dAuto | interface | 34 | 23 |
| _IArcs2dAuto | interface | 5 | 3 |
| _IAreaPropertiesAuto | interface | 18 | 11 |
| _IAreaPropertiesCollectionAuto | interface | 2 | 3 |
| _IBackDropAuto | interface | 0 | 11 |
| _IBalloonAuto | interface | 41 | 58 |
| _IBalloonsAuto | interface | 6 | 6 |
| _IBoltHoleCircleAuto | interface | 18 | 20 |
| _IBoltHoleCirclesAuto | interface | 5 | 4 |
| _IBoundaries2dAuto | interface | 3 | 3 |
| _IBoundary2dAuto | interface | 19 | 17 |
| _IBoundaryStyle2dAuto | interface | 1 | 10 |
| _IBoundingObjects2dAuto | interface | 1 | 3 |
| _IBspCurve2dAuto | interface | 43 | 28 |
| _IBspCurves2dAuto | interface | 4 | 3 |
| _ICenterLineAuto | interface | 29 | 18 |
| _ICenterLinesAuto | interface | 14 | 6 |
| _ICenterMarkAuto | interface | 25 | 21 |
| _ICenterMarksAuto | interface | 8 | 7 |
| _IChamferGeometry2dAuto | interface | 3 | 3 |
| _ICircle2dAuto | interface | 28 | 21 |
| _ICircles2dAuto | interface | 3 | 3 |
| _ICircularPattern2dAuto | interface | 2 | 10 |
| _ICircularPatterns2dAuto | interface | 5 | 3 |
| _IComplexString2dAuto | interface | 26 | 18 |
| _IComplexStrings2dAuto | interface | 2 | 3 |
| _IComponentImage2dAuto | interface | 1 | 7 |
| _IComponentImages2dAuto | interface | 2 | 3 |
| _IConic2dAuto | interface | 28 | 13 |
| _IConics2dAuto | interface | 2 | 3 |
| _IConnectorAuto | interface | 31 | 14 |
| _IConnectorsAuto | interface | 3 | 3 |
| _ICornerAnnotationAuto | interface | 31 | 34 |
| _ICornerAnnotationsAuto | interface | 6 | 6 |
| _ICurve2dAuto | interface | 30 | 21 |
| _ICurves2dAuto | interface | 2 | 3 |
| _IDatumFrameAuto | interface | 32 | 26 |
| _IDatumFramesAuto | interface | 6 | 6 |
| _IDatumPointAuto | interface | 29 | 21 |
| _IDatumPointsAuto | interface | 6 | 7 |
| _IDatumTargetAuto | interface | 34 | 30 |
| _IDatumTargetsAuto | interface | 6 | 6 |
| _IDimInitDataAuto | interface | 17 | 1 |
| _IDimStyleAuto | interface | 1 | 188 |
| _IDimensionAuto | interface | 59 | 86 |
| _IDimensionStyleAuto | interface | 0 | 198 |
| _IDimensionStylesAuto | interface | 5 | 4 |
| _IDimensionsAuto | interface | 25 | 10 |
| _IDisplayDataAuto | interface | 17 | 0 |
| _IDrawingObjectsAuto | interface | 1 | 3 |
| _IDrawingViewStyleAuto | interface | 0 | 52 |
| _IDrawingViewStylesAuto | interface | 3 | 4 |
| _IEllipArc2dAuto | interface | 36 | 23 |
| _IEllipArcs2dAuto | interface | 3 | 3 |
| _IEllipse2dAuto | interface | 30 | 24 |
| _IEllipses2dAuto | interface | 2 | 3 |
| _IFeatureControlFrameAuto | interface | 33 | 47 |
| _IFeatureControlFrameDataSetAuto | interface | 0 | 21 |
| _IFeatureControlFrameDataSetsAuto | interface | 3 | 3 |
| _IFeatureControlFramesAuto | interface | 7 | 7 |
| _IFilletGeom2dAuto | interface | 1 | 0 |
| _IFrameAuto | interface | 0 | 7 |
| _IGeometryStyle2dAuto | interface | 3 | 8 |
| _IGostWeldSymbolAuto | interface | 31 | 36 |
| _IGostWeldSymbolsAuto | interface | 5 | 6 |
| _IGroupAuto | interface | 22 | 49 |
| _IGroupStyleAuto | interface | 3 | 8 |
| _IGroupsAuto | interface | 4 | 3 |
| _IImage2dAuto | interface | 7 | 22 |
| _IImages2dAuto | interface | 3 | 3 |
| _ILeaderAuto | interface | 36 | 25 |
| _ILeadersAuto | interface | 8 | 6 |
| _ILine2dAuto | interface | 30 | 21 |
| _ILineString2dAuto | interface | 33 | 18 |
| _ILineStrings2dAuto | interface | 2 | 3 |
| _ILines2dAuto | interface | 4 | 3 |
| _IPMIAuto | interface | 2 | 25 |
| _IPMIModelViewAuto | interface | 11 | 11 |
| _IPMIModelViewsAuto | interface | 3 | 3 |
| _IPoint2dAuto | interface | 24 | 17 |
| _IPoints2dAuto | interface | 2 | 3 |
| _IRectangularPattern2dAuto | interface | 2 | 17 |
| _IRectangularPatterns2dAuto | interface | 3 | 3 |
| _IRelation2dAuto | interface | 5 | 10 |
| _IRelations2dAuto | interface | 27 | 1 |
| _IRelationships2dAuto | interface | 1 | 3 |
| _ISmartFrame2dAuto | interface | 26 | 37 |
| _ISmartFrame2dDefaultsAuto | interface | 2 | 10 |
| _ISmartFrame2dStyleAuto | interface | 2 | 29 |
| _ISmartFrame2dStylesAuto | interface | 2 | 4 |
| _ISmartFrames2dAuto | interface | 3 | 3 |
| _ISurfaceFinishSymbolAuto | interface | 32 | 39 |
| _ISurfaceFinishSymbolDataSetAuto | interface | 0 | 14 |
| _ISurfaceFinishSymbolDataSetsAuto | interface | 3 | 3 |
| _ISurfaceFinishSymbolsAuto | interface | 6 | 7 |
| _ISymbolicPMIAuto | interface | 3 | 10 |
| _ISymbolicPMIGroupAuto | interface | 1 | 3 |
| _ITableStyleAuto | interface | 0 | 9 |
| _ITableStylesAuto | interface | 3 | 3 |
| _ITechnicalRequirementAuto | interface | 6 | 5 |
| _ITechnicalRequirementsAuto | interface | 2 | 3 |
| _ITextBoxAuto | interface | 23 | 43 |
| _ITextBoxesAuto | interface | 6 | 3 |
| _ITextEditAuto | interface | 22 | 30 |
| _ITextProfileAuto | interface | 15 | 12 |
| _ITextProfilesAuto | interface | 1 | 3 |
| _IVFSetAuto | interface | 5 | 2 |
| _IWeldSymbolAuto | interface | 36 | 59 |
| _IWeldSymbolDataSetAuto | interface | 0 | 22 |
| _IWeldSymbolDataSetsAuto | interface | 3 | 3 |
| _IWeldSymbolsAuto | interface | 7 | 7 |

---
## Program/geometry.tlb
**Solid Edge Geometry Type Library** (GUID: `{3E2B3BE1-F0B9-11D1-BDFD-080036B4D502}`, v1.0)

### Enums (5)

- **FeatureTopologyQueryTypeConstants** [10]: igQueryAll=1, igQueryRoundable=2, igQueryStraight=3, igQueryEllipse=4, igQuerySpline=5, ... (10 total)
- **GNTTypePropertyConstants** [30]: igMesh=-2071771273, igPlane=-1909484335, igParamBSplineCurve=-1811952078, igCurveBody=-1020639371, igCurvePath=-1020639369, ... (30 total)
- **SmartCollectionTypeConstants** [14]: seRoundableEdgesAtVertex=1, seRoundableSmoothEdgeChain=2, seRoundableEdgesOfFace=3, seRoundableEdgesOfLoop=4, seRoundableEdgesOfFeature=5, ... (14 total)
- **TopologyCollectionTypeConstants** [3]: seFaceCollection=1, seEdgeCollection=2, seVertexCollection=3
- **WallThicknessDisplayResolution** [3]: DisplayResolutionCoarse=0, DisplayResolutionStandard=1, DisplayResolutionFine=2

### Interfaces (68)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| BSplineCurve | dispatch | 7 | 5 |
| BSplineSurface | dispatch | 7 | 5 |
| Body | dispatch | 17 | 22 |
| Circle | dispatch | 3 | 4 |
| Cone | dispatch | 3 | 6 |
| Curve | dispatch | 14 | 11 |
| CurveBody | dispatch | 3 | 11 |
| CurvePath | dispatch | 2 | 10 |
| CurvePaths | dispatch | 1 | 3 |
| CurveVertex | dispatch | 2 | 7 |
| CurveVertices | dispatch | 1 | 3 |
| Curves | dispatch | 1 | 3 |
| Cylinder | dispatch | 3 | 4 |
| Edge | dispatch | 18 | 17 |
| EdgeUse | dispatch | 9 | 12 |
| EdgeUses | dispatch | 1 | 4 |
| Edges | dispatch | 4 | 5 |
| Ellipse | dispatch | 4 | 4 |
| Face | dispatch | 19 | 20 |
| Faces | dispatch | 4 | 5 |
| Line | dispatch | 3 | 3 |
| Loop | dispatch | 2 | 12 |
| Loops | dispatch | 1 | 4 |
| MeshSurface | dispatch | 3 | 3 |
| PLine | dispatch | 4 | 3 |
| ParamBSplineCurve | dispatch | 7 | 4 |
| Plane | dispatch | 4 | 3 |
| Shell | dispatch | 3 | 13 |
| Shells | dispatch | 1 | 4 |
| Sphere | dispatch | 2 | 4 |
| Torus | dispatch | 3 | 5 |
| Vertex | dispatch | 2 | 12 |
| Vertices | dispatch | 4 | 5 |
| _Collection | dispatch | 4 | 5 |
| _IDMDBSplineCurve | interface | 7 | 5 |
| _IDMDBSplineSurface | interface | 7 | 5 |
| _IDMDBody | interface | 17 | 22 |
| _IDMDCircle | interface | 3 | 4 |
| _IDMDCollection | interface | 4 | 5 |
| _IDMDCone | interface | 3 | 6 |
| _IDMDCurve | interface | 14 | 11 |
| _IDMDCurveBody | interface | 3 | 11 |
| _IDMDCurvePath | interface | 2 | 10 |
| _IDMDCurvePaths | interface | 1 | 3 |
| _IDMDCurves | interface | 1 | 3 |
| _IDMDCylinder | interface | 3 | 4 |
| _IDMDEdge | interface | 18 | 17 |
| _IDMDEdgeUse | interface | 9 | 12 |
| _IDMDEdgeUses | interface | 1 | 4 |
| _IDMDEdges | interface | 4 | 5 |
| _IDMDEllipse | interface | 4 | 4 |
| _IDMDFace | interface | 19 | 20 |
| _IDMDFaces | interface | 4 | 5 |
| _IDMDLine | interface | 3 | 3 |
| _IDMDLoop | interface | 2 | 12 |
| _IDMDLoops | interface | 1 | 4 |
| _IDMDMesh | interface | 3 | 3 |
| _IDMDPLine | interface | 4 | 3 |
| _IDMDParamBSplineCurve | interface | 7 | 4 |
| _IDMDPlane | interface | 4 | 3 |
| _IDMDShell | interface | 3 | 13 |
| _IDMDShells | interface | 1 | 4 |
| _IDMDSphere | interface | 2 | 4 |
| _IDMDTorus | interface | 3 | 5 |
| _IDMDVertex | interface | 2 | 12 |
| _IDMDVertices | interface | 4 | 5 |
| _ISEDCurveVertex | interface | 2 | 7 |
| _ISEDCurveVertices | interface | 1 | 3 |

---
## Program/iCnct.tlb
**Solid Edge View And Markup Object Library** (GUID: `{0E6AA0AE-9E97-4440-B6E0-41E3FF654FFE}`, v1.0)

### Enums (1)

- **PCFFilePermission** [9]: NoPermission=0, PMIPermission=2, CrossSectionPermission=8, MeasurePermission=80, MarkupPermission=768, ... (9 total)

### Interfaces (1)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| IVMApp | dispatch | 7 | 0 |

### CoClasses (1)

- **VMApplication** (`{1E3809BB-BC66-4646-AF41-0AADAC68EF92}`): IVMApp

---
## Program/onnxML.tlb
**** (GUID: `{D7F93D90-36B2-4F3C-84A3-2F6C6CC34864}`, v226.0)

### Interfaces (1)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| IMLPrediction | interface | 1 | 0 |

### CoClasses (1)

- **onnxClass** (`{62321166-C532-45AA-89F5-D0769624689C}`): _Object, IMLPrediction

---
## Program/partattr.tlb
**Part Dynamic Attributes Type Library** (GUID: `{6D683D60-FA27-11D1-A271-0800362BDC02}`, v1.0)

### Interfaces (3)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| Identification | dispatch | 0 | 0 |
| Identification2 | dispatch | 0 | 0 |
| _PhysicalProperties | dispatch | 0 | 0 |

---
## Simulation/x64/femap.tlb
**Simcenter™ Femap™ v2506.0 Type Library** (GUID: `{08F336B3-E668-11D4-9441-001083FFF11C}`, v25.60)

### Enums (216)

- **CTRLDEF** [4]: CTRLDEF_BLANK=0, CTRLDEF_QLINEAR=1, CTRLDEF_MILDLY=2, CTRLDEF_SEVERLY=3
- **NLSTEP_LOAD_STEPPING** [3]: NLSTEP_LOAD_FIXED=0, NLSTEP_LOAD_ADAPT=1, NLSTEP_LOAD_ARCLEN=2
- **bolt_pl_type** [3]: Load_bp=0, Strain_bp=1, Disp_bp=2
- **elar_criteria_type** [3]: ELAR_CRITERIA_TIME=0, ELAR_CRITERIA_RINELE=1, ELAR_CRITERIA_RMECHE=2
- **elar_type** [3]: ELAR_TYPE_ELAR=0, ELAR_TYPE_ELAR2=1, ELAR_TYPE_ELARADD=2
- **flxsli_driver_type** [4]: FLXSLI_DRIVER_UNKNOWN=-1, FLXSLI_DRIVER_FORC=0, FLXSLI_DRIVER_DISP=1, FLXSLI_DRIVER_SENSOR=2
- **flxsli_friction_type** [5]: FLXSLI_FRICTION_UNKNOWN=-1, FLXSLI_FRICTION_NONE=0, FLXSLI_FRICTION_INF=1, FLXSLI_FRICTION_VELO=2, FLXSLI_FRICTION_DISP=3
- **flxsli_type** [5]: FLXSLI_TYPE_UNKNOWN=-1, FLXSLI_TYPE_FLEX=0, FLXSLI_TYPE_CYLF=1, FLXSLI_TYPE_PRIF=2, FLXSLI_TYPE_TWIF=3
- **joint_attachment_selection** [7]: JOINT_ATTACH_UNKNOWN=0, JOINT_ATTACH_POINTS=1, JOINT_ATTACH_SURFACES=2, JOINT_ATTACH_CURVES=3, JOINT_ATTACH_NODES=4, ... (7 total)
- **joint_behavior** [12]: JOINT_UNKNOWN=0, JOINT_REVOLUTE=1, JOINT_INLINE=2, JOINT_SLIDER=3, JOINT_SPHERE=4, ... (12 total)
- **joint_connection_geom_expansion** [3]: EXPAND_BOUNDARY=0, EXPAND_INTERIOR=1, EXPAND_BOTH=2
- **joint_connection_nas_expansion** [2]: EXPAND_CJOINT_RBE2=0, EXPAND_CJOINT_RBE3=1
- **kinematic_type** [3]: KINEMATIC_UNKNOWN=0, KINEMATIC_JOINT=1, KINEMATIC_CONNECTION=2
- **omega_type** [3]: OMEGA_TYPE_OMEGA=0, OMEGA_TYPE_OMEGA1=1, OMEGA_TYPE_OMEGA2=2
- **outmgt_res** [9]: OUTMGT_RES_DISP=0, OUTMGT_RES_VELOC=1, OUTMGT_RES_ACCEL=2, OUTMGT_RES_REAC=3, OUTMGT_RES_ORBITP=4, ... (9 total)
- **outmgt_type** [2]: OUTMGT_TYPE_GRP=0, OUTMGT_TYPE_NODE_ELEM=1
- **zAeroPanelType** [4]: AERO_PNL_SURF=0, AERO_PNL_BODY=1, AERO_PNL_ZSURF=2, AERO_PNL_ZBODY=4
- **zAlignment** [3]: FAL_LEFT=0, FAL_CENTER=1, FAL_RIGHT=2
- **zAnalysisAssignForm** [5]: AAF_NONE=0, AAF_FORMATTED=1, AAF_UNFORMATTED=2, AAF_LITTLEENDIAN=3, AAF_BIGENDIAN=4
- **zAnalysisExtSEOutTo** [3]: EXTSEOUTTO_DMIGPCH=0, EXTSEOUTTO_DMIGOP2=1, EXTSEOUTTO_MATOP4=2
- **zAnalysisExtSERef** [3]: EXTSEREF_TYPE_OP2=0, EXTSEREF_TYPE_OP4=1, EXTSEREF_TYPE_PCH=2
- **zAnalysisMgrProgram** [9]: FAM_UNKNOWN=0, FAM_MSC_NASTRAN=4, FAM_ANSYS=5, FAM_ABAQUS=16, FAM_LS_DYNA=28, ... (9 total)
- **zAnalysisProgram** [37]: FAP_UNKNOWN=0, FAP_FEMAP_GEN=1, FAP_PAL=2, FAP_PAL2=3, FAP_MSC_NASTRAN=4, ... (37 total)
- **zAnalysisTranslator** [55]: FTR_NONE=-1, FTR_MSC_NASTRAN=0, FTR_PC_NASTRAN=1, FTR_PAL_2=2, FTR_STARDYNE=3, ... (55 total)
- **zAnalysisType** [35]: FAT_UNKNOWN=0, FAT_STATIC=1, FAT_MODES=2, FAT_TRANSIENT=3, FAT_FREQUENCY_RESPONSE=4, ... (35 total)
- **zAnalyticSurfaceType** [3]: FARS_CYLINDER=0, FARS_SEGMENTS=1, FARS_REVOLUTION=2
- **zApiWarningLevel** [4]: APIWARN_EVERY=0, APIWARN_ONCEPERITEM=1, APIWARN_ONCEPERSESSION=2, APIWARN_NEVER=3
- **zAttachStatus** [5]: FRA_UNLOADED=0, FRA_OPEN=1, FRA_OPEN_CHECK=2, FRA_ERROR=3, FRA_UNLOAD_CHECK=4
- **zBCGeomType** [6]: FBG_DOF=0, FBG_GENERAL=1, FBG_SURFSLIDING=2, FBG_SURFNONSLIDING=3, FBG_SURFDIRSLIDING=4, ... (6 total)
- **zBeamCalculatorStressComponent** [9]: FBMC_SC_ALL=-1, FBMC_SC_VONMISES=0, FBMC_SC_MAXSHEAR=1, FBMC_SC_MAXPRIN=2, FBMC_SC_MINPRIN=3, ... (9 total)
- **zCSysType** [3]: FCS_RECTANGULAR=0, FCS_CYLINDRICAL=1, FCS_SPHERICAL=2
- **zChartAxisStyle** [2]: FCH_AXISSTYLE_LINEAR=0, FCH_AXISSTYLE_LOG=1
- **zChartComplexLocation** [3]: FCCL_OFF=0, FCCL_TOP=1, FCCL_BOTTOM=2
- **zChartLegendDirection** [2]: FCH_LEGEND_DIRECTION_TOPTOBOTTOM=0, FCH_LEGEND_DIRECTION_LEFTTORIGHT=1
- **zChartLegendLocation** [5]: FCH_LEGEND_LOCATION_NEAROUTSIDE=0, FCH_LEGEND_LOCATION_NEAR=1, FCH_LEGEND_LOCATION_CENTER=2, FCH_LEGEND_LOCATION_FAR=3, FCH_LEGEND_LOCATION_FAROUTSIDE=4
- **zChartMarkerStyle** [7]: FCH_MARKERSTYLE_CIRCLE=0, FCH_MARKERSTYLE_SQUARE=1, FCH_MARKERSTYLE_DIAMOND=2, FCH_MARKERSTYLE_TRIANGLE=3, FCH_MARKERSTYLE_PENTAGON=4, ... (7 total)
- **zChartNumberFormat** [3]: FCH_FORMAT_STANDARD=0, FCH_FORMAT_SCIENTIFIC=1, FCH_FORMAT_PERCENTAGE=2
- **zChartPalette** [9]: FCH_PALETTE_CUSTOM=0, FCH_PALETTE_FEMAP=1, FCH_PALETTE_GRAY=2, FCH_PALETTE_OFFICE=3, FCH_PALETTE_VIBRANT=4, ... (9 total)
- **zChartSeriesCombination** [4]: FCSC_ADD=0, FCSC_SUBTRACT=1, FCSC_MULTIPLY=2, FCSC_DIVIDE=3
- **zChartSeriesComplexMethod** [4]: FCSCM_NONE=0, FCSCM_MATCHMODEL=1, FCSCM_MATCHVIEW=2, FCSCM_SYNC=3
- **zChartSeriesType** [9]: FCHD_TYPE_ID=0, FCHD_TYPE_SET=1, FCHD_TYPE_SETVAL=2, FCHD_TYPE_POSITION=3, FCHD_TYPE_FUNCTION=4, ... (9 total)
- **zChartStyle** [6]: FCH_STYLE_POINT=0, FCH_STYLE_LINE=1, FCH_STYLE_LINEFAST=2, FCH_STYLE_LINESTEP=3, FCH_STYLE_AREA=4, ... (6 total)
- **zChartTextJustification** [3]: FCH_TEXT_JUSTIFICATION_LEFT=0, FCH_TEXT_JUSTIFICATION_CENTER=1, FCH_TEXT_JUSTIFICATION_RIGHT=2
- **zChartTitleLocation** [4]: FCH_TITLE_LOCATION_TOP=0, FCH_TITLE_LOCATION_LEFT=1, FCH_TITLE_LOCATION_RIGHT=2, FCH_TITLE_LOCATION_BOTTOM=3
- **zColor** [198]: FCL_BLACK=0, FPF_SOLID=0, FPL_SOLID=0, FCL_SEPIA=1, FCL_DARKRED=2, ... (198 total)
- **zColorMatch** [4]: FCOM_COLOR=1, FCOM_PATTERN=2, FCOM_LINESTYLE=4, FCOM_ALL=7
- **zCombinedMode** [3]: FCC_OFF=0, FCC_ON=1, FCC_BOTH=2
- **zConnectionPropType** [2]: FCPT_CONTACT=0, FCPT_GLUED=1
- **zConnectionRegionType** [5]: FRT_CONNECTION=0, FRT_FLUID=1, FRT_BOLT=2, FRT_ROTOR=3, FRT_NSM=4
- **zContourFormat** [8]: FCF_NONE=0, FCF_MODEL_COLOR=0, FCF_CONTOUR=1, FCF_CRITERIA=2, FCF_BEAM_DIAGRAM=3, ... (8 total)
- **zCoordPick** [5]: FPC_ABOVE_MAX=0, FPC_BELOW_MIN=1, FPC_OUTSIDE=2, FPC_BETWEEN=3, FPC_AT=4
- **zCopyPropApproach** [4]: FCPPR_KEEP=0, FCPPR_DUP_PROP=1, FCPPR_DUP_MATL=2, FCPPR_OVERRIDE=3
- **zCopyRenumMethod** [3]: FCPRNM_DEFAULT=0, FCPRNM_BLOCK=1, FCPRNM_OFFSET=2
- **zCurveManifoldType** [5]: FCMT_UNKNOWN=-1, FCMT_WIREEDGE=0, FCMT_FREEEDGE=1, FCMT_MANIFOLD=2, FCMT_NONMANIFOLD=3
- **zCurveOffsetType** [3]: FCO_VECTOR=0, FCO_RADIAL=1, FCO_POINT=2
- **zCurveOrientType** [4]: FCR_BY_VECTOR=0, FCR_BY_LOCATION=1, FCR_BY_VECTOR_REV=2, FCR_BY_LOCATION_REV=3
- **zCurveRemoveOption** [3]: FCRO_NORMAL=0, FCRO_AGGRESSIVE=1, FCRO_COMBINE=2
- **zCurveType** [7]: FCU_LINE=0, FCU_ARC=1, FCU_CIRCLE=2, FCU_SPLINE=3, FCU_BSPLINE=4, ... (7 total)
- **zDataConvert** [11]: FMDC_VU=0, FMDC_AVG=1, FMDC_MAX=2, FMDC_MIN=3, FMDC_AVG_SKIP_CORNER=4, ... (11 total)
- **zDataTableColumnType** [4]: FCT_BOOL=0, FCT_INT=1, FCT_DOUBLE=2, FCT_STRING=3
- **zDataTableSaveFormat** [4]: FSF_TEXT=0, FSF_CSV=1, FSF_RTF=2, FSF_HTML=3
- **zDataType** [84]: FT_POINT=3, FT_CURVE=4, FT_SURFACE=5, FT_VOLUME=6, FT_NODE=7, ... (84 total)
- **zDeformedFormat** [8]: FDF_NONE=0, FDF_MODEL_UNDEF=0, FDF_DEFORMED=1, FDF_ANIMATE=2, FDF_ANIMATE_MULTICASE=3, ... (8 total)
- **zElementType** [46]: FET_NONE=0, FET_L_ROD=1, FET_L_BAR=2, FET_L_TUBE=3, FET_L_LINK=4, ... (46 total)
- **zEventCode** [18]: FEVENT_INITIALIZE=1, FEVENT_NEWMODEL=2, FEVENT_ENDMODEL=3, FEVENT_SHUTDOWN=4, FEVENT_COMMAND=5, ... (18 total)
- **zExistState** [2]: FEX_EXISTING=0, FEX_NONEXISTING=1
- **zFbdComponent** [6]: FBC_FX=0, FBC_FY=1, FBC_FZ=2, FBC_MX=3, FBC_MY=4, ... (6 total)
- **zFbdContribution** [8]: FBL_APPLIED=0, FBL_SPC=1, FBL_MPC=2, FBL_EL_FB=3, FBL_EL_PER=4, ... (8 total)
- **zFbdDisplayMode** [3]: FBD_DISPLAYMODE_FREEBODY=0, FBD_DISPLAYMODE_INTERFACE=1, FBD_DISPLAYMODE_SECTION=2
- **zFbdSectionMode** [4]: FBD_SECTMODE_PLANENORMAL=0, FBD_SECTMODE_PLANEVECTOR=1, FBD_SECTMODE_VECTOR=2, FBD_SECTMODE_CURVE=3
- **zFbdSectionSumLoc** [3]: FBD_SECTION_SUMLOC_BASE=0, FBD_SECTION_SUMLOC_CENTROID=1, FBD_SECTION_SUMLOC_LOCATION=2
- **zFbdVecMode** [3]: FBD_VEC_MODE_OFF=0, FBD_VEC_MODE_COMPONENT=1, FBD_VEC_MODE_RESULTANT=2
- **zFeatureType** [20]: FEAT_NX_NASTRAN_BASIC=0, FEAT_NX_NASTRAN_NONLINEAR=1, FEAT_NX_NASTRAN_DYNAMICS=2, FEAT_NX_NASTRAN_DMAP=3, FEAT_NX_NASTRAN_SUPERELEMENTS=4, ... (20 total)
- **zFemapLanguage** [6]: FLNG_AUTO=0, FLNG_EN=1, FLNG_DE=2, FLNG_JP=3, FLNG_TW=4, ... (6 total)
- **zFreqType** [6]: FREQ=0, FREQ1=1, FREQ2=2, FREQ3=3, FREQ4=4, ... (6 total)
- **zFunctionType** [50]: FTB_NONE=0, FTB_TIME=1, FTB_TEMP=2, FTB_FREQ=3, FTB_STRESSSTRAIN=4, ... (50 total)
- **zGFXArrowMode** [2]: GAM_ABSOLUTE=0, GAM_SCALED=1
- **zGFXArrowStyle** [6]: GAS_LINE=0, GAS_SOLID=1, GAS_DOUBLE_LINE=2, GAS_DOUBLE_SOLID=3, GAS_REV_DOUBLE_LINE=4, ... (6 total)
- **zGFXEdgeFlags** [6]: GEF_NONE=0, GEF_EDGE1=1, GEF_EDGE2=2, GEF_EDGE3=4, GEF_EDGE4=8, ... (6 total)
- **zGFXPointSymbol** [11]: GPS_POINT=0, GPS_SQUARE=1, GPS_SQUARE_FILLED=2, GPS_DIAMOND=3, GPS_X=4, ... (11 total)
- **zGeomInterfaceColorMode** [3]: GICM_ACTIVE=0, GICM_SINGLE=1, GICM_FILE=2
- **zGeometryExportInterface** [10]: FGXI_NONE=-1, FGXI_PARASOLID=0, FGXI_ACIS=1, FGXI_SLA=2, FGXI_VRML=3, ... (10 total)
- **zGeometryImportBodyType** [6]: FGITY_ALL=0, FGITY_DESIGN=1, FGITY_SIMPLE_OR_DESIGN=2, FGITY_SIMPLE=3, FGITY_CONSTRUCTION=4, ... (6 total)
- **zGeometryInterface** [17]: FGI_NONE=-1, FGI_DXF=10, FGI_IGES=11, FGI_SLA=27, FGI_ACIS=29, ... (17 total)
- **zGifColorOpt** [3]: GIFC_NET=0, GIFC_OCTREE=1, GIFC_DITHER=2
- **zGroupBooleanOp** [6]: FGB_ADD=0, FGB_SUBTRACT=1, FGB_INALL=2, FGB_ONLYINONE=3, FGB_NOTINANY=4, ... (6 total)
- **zGroupDataType** [28]: FGR_CSYS=0, FGR_POINT=1, FGR_CURVE=2, FGR_SURFACE=3, FGR_VOLUME=4, ... (28 total)
- **zGroupDefinitionType** [173]: FGD_CSYS_ID=0, FGD_CSYS_BYDEFCSYS=1, FGD_CSYS_BYTYPE=2, FGD_POINT_ID=3, FGD_POINT_BYDEFCSYS=4, ... (173 total)
- **zInvariantResultType** [6]: FIVT_MAX_PRIN=0, FIVT_MIN_PRIN=1, FIVT_MID_PRIN=2, FIVT_MEAN_PRIN=3, FIVT_MAX_SHEAR=4, ... (6 total)
- **zJT_FileUnits** [12]: JT_UNIT_UNKNOWN=0, JT_UNIT_MICRO=1, JT_UNIT_MILLI=2, JT_UNIT_CENTI=3, JT_UNIT_DECI=4, ... (12 total)
- **zJT_FileVersion** [19]: JT_V_8_0=80, JT_V_8_1=81, JT_V_8_2=82, JT_V_9_0=90, JT_V_9_1=91, ... (19 total)
- **zJT_SetOption** [5]: JT_SETS_NONE=0, JT_SETS_VISIBLE=1, JT_SETS_ACTIVE=2, JT_SETS_ALL=3, JT_SETS_SELECT=4
- **zLibraryFile** [4]: FLIB_DIALOG=0, FLIB_PERSONAL=1, FLIB_SHARED=2, FLIB_SYSTEM=3
- **zLinkedSolver** [3]: FS_INTEGRATED=0, FS_LINKED=1, FS_VISQ=2
- **zListDestination** [7]: FDST_SCREEN=1, FDST_PRINTER=16, FDST_SCR_PRINT=17, FDST_FILE=256, FDST_SCR_FILE=257, ... (7 total)
- **zLoadDirection** [5]: FLD_NONE=0, FLD_VECTOR=1, FLD_ALONGCURVE=2, FLD_NORMALTOPLANE=3, FLD_NORMALTOSURFACE=4
- **zLoadSelectType** [25]: FLS_ANY=-1, FLS_NONE=0, FLS_BODY=1, FLS_NHTGEN=2, FLS_NHTFLUX=4, ... (25 total)
- **zLoadType** [132]: FLT_NBODY=0, FLT_NFORCE=1, FLT_NMOMENT=2, FLT_NDISPLACEMENT=3, FLT_NROTDISPLACEMENT=4, ... (132 total)
- **zLoadVariation** [5]: FLV_NONE=0, FLV_EQUATION=1, FLV_FUNCTION=2, FLV_INTERPOLATION=3, FLV_DATASURFACE=4
- **zLocateOption** [4]: FLO_AFTER=1, FLO_BEFORE=2, FLO_AFTER_EQUAL=3, FLO_BEFORE_EQUAL=4
- **zMDCType** [52]: FVMDC_NONE_SELECTED=0, FVMDC_MATL_E=1, FVMDC_MATL_TABLE=2, FVMDC_PROP_PLATE_THICKNESS=3, FVMDC_PROP_LINE_AREA=4, ... (52 total)
- **zManageResultsAttach** [4]: FMRA_LOAD=0, FMRA_UNLOAD=1, FMRA_DETACH=2, FMRA_UPDATE_PATH=3
- **zMapLoadType** [14]: FMLT_NFORCE=1, FMLT_NMOMENT=2, FMLT_NDISPLACEMENT=3, FMLT_NROTDISPLACEMENT=4, FMLT_NVELOCITY=5, ... (14 total)
- **zMapOption** [5]: FMO_ZERO=0, FMO_VALUE=1, FMO_EXTEND=2, FMO_INTERP=3, FMO_NONE=4
- **zMapType** [3]: FMP_STANDARD=0, FMP_NODE=1, FMP_ELEMENT=2
- **zMatCplxForm** [2]: MAT_REAL_IMAG=0, MAT_AMP_PHASE=1
- **zMatFileForm** [2]: MAT_PCH=0, MAT_OP2=1
- **zMatIOType** [5]: MAT_MACHPRES=0, MAT_REAL_SINGLE=1, MAT_REAL_DOUBLE=2, MAT_CPLX_SINGLE=3, MAT_CPLX_DOUBLE=4
- **zMatInputForm** [4]: MAT_SQUARE=0, MAT_SYMMETRIC=1, MAT_RECT2=2, MAT_RECT9=3
- **zMatSrcForm** [3]: MAT_INT=0, MAT_EXT=1, MAT_COMB=2
- **zMatchOpt** [6]: FMTCH_ANY=0, FMTCH_ALL=1, FMTCH_ANY_TRUE=2, FMTCH_ALL_TRUE=3, FMTCH_ANY_CONSTRAINED=4, ... (6 total)
- **zMaterialType** [8]: FMT_ISOTROPIC=0, FMT_ORTHOTROPIC_2D=1, FMT_ORTHOTROPIC_3D=2, FMT_ANISOTROPIC_2D=3, FMT_ANISOTROPIC_3D=4, ... (8 total)
- **zMergeRenumMethod** [5]: FMRRNM_NONE=0, FMRRNM_MINIMAL=1, FMRRNM_BLOCK=2, FMRRNM_OFFSET=3, FMRRNM_COMPRESS=4
- **zMeshApproach** [9]: FMAP_NONE=0, FMAP_FREE_PARAMETRIC=1, FMAP_FREE_PLANAR=2, FMAP_MAP_4CORNER=3, FMAP_MAP_3CORNER=4, ... (9 total)
- **zMeshBodyAssoc** [3]: MBAS_ALL=0, MBAS_REQD=1, MBAS_SELECT=2
- **zMeshBodyMidsideMode** [2]: MBMM_NONE=0, MBMM_ASSOCIATED=1
- **zMeshEditingSplitMode** [6]: MESM_QUAD_TO_2QUADS=0, MESM_QUAD_TO_4QUADS=1, MESM_QUAD_TO_2TRIS=2, MESM_QUAD_TO_3TRIS=3, MESM_TRI_TO_4TRIS=4, ... (6 total)
- **zMeshOffsetFrom** [3]: FMOF_CENTERLINE=0, FMOF_TOP=1, FMOF_BOTTOM=2
- **zMeshSizePropEdgeMode** [4]: MSPE_OFF=0, MSPE_FREEONLY=1, MSPE_FREEPLUS=2, MSPE_ALL=3
- **zMeshSizePropSelMode** [2]: MSPS_ALL=0, MSPS_MESHED=1
- **zMesherType** [4]: FMSH_AUTO=0, FMSH_SUBDIVISION=1, FMSH_FASTTRI=2, FMSH_3DTRI=3
- **zMessageColor** [5]: FCM_NORMAL=0, FCM_HIGHLIGHT=1, FCM_WARNING=2, FCM_ERROR=3, FCM_COMMAND=4
- **zMptComponent** [6]: MPT_FX=0, MPT_FY=1, MPT_FZ=2, MPT_MX=3, MPT_MY=4, ... (6 total)
- **zMptContribution** [4]: MPT_SPC=0, MPT_MPC=1, MPT_APPLIED=2, MPT_DMIG=3
- **zMptType** [5]: MPT_1_AEROPANEL=0, MPT_1_AEROMESH=1, MPT_1_STRUCT=2, MPT_3=3, MPT_2=4
- **zNasLicenseType** [2]: FSNAS_LIC_DESK=0, FSNAS_LIC_ENT=1
- **zNodeType** [4]: FND_NODE=0, FND_SPOINT=1, FND_EPOINT=2, FND_FLPOINT=3
- **zOptBoundtype** [3]: FOPBT_VALUES=0, FOPBT_RELATIVE=1, FOPBT_PCT=2
- **zOptGoal** [6]: FOG_NONE=0, FOG_DRESP=0, FOG_MINWEIGHT=1, FOG_WEIGHT=1, FOG_VOLUME=2, ... (6 total)
- **zOptLimit** [31]: FOL_NONE=0, FOL_NODXDISP=1, FOL_NODYDISP=2, FOL_NODZDISP=3, FOL_NODXRDISP=4, ... (31 total)
- **zOptMnConType** [8]: FOPMC_ADDM=0, FOPMC_CAST=1, FOPMC_CHECK=2, FOPMC_CSYM=3, FOPMC_EXTR=4, ... (8 total)
- **zOptRelType** [4]: FOPRT_PROPERTY=0, FOPRT_MATERIAL=1, FOPRT_TOPOLOGY=2, FOPRT_ELEM=3
- **zOptRespAttType** [4]: FOPATT_BLANK=0, FOPATT_CHAR=1, FOPATT_INT=2, FOPATT_REAL=3
- **zOptRespType** [14]: FOPRSP_CUSTOM=0, FOPRSP_NDISP=1, FOPRSP_SPCFORCE=2, FOPRSP_ELEM=3, FOPRSP_ESE=4, ... (14 total)
- **zOptType** [4]: FOP_NONE=0, FOP_GOAL=1, FOP_VARY=2, FOP_LIMIT=3
- **zOptVary** [8]: FOV_NONE=0, FOV_RODAREA=1, FOV_RODTORSION=2, FOV_BARAREA=3, FOV_BARI1=4, ... (8 total)
- **zOutputComplex** [5]: FOC_MAGNITUDE=0, FOC_PHASE=1, FOC_REAL=2, FOC_IMAGINARY=3, FOC_ANY=4
- **zOutputDestination** [9]: FOD_NONE=0, FOD_VECTOR_TO_CSYS=1, FOD_VECTOR_TO_NODE_OUTPUT_CSYS=2, FOD_PLATE_TO_MATL=3, FOD_PLATE_TO_CSYS=4, ... (9 total)
- **zOutputProcessCombine** [3]: FOPC_ALL=0, FOPC_IN_SET=1, FOPC_EACH_VECTOR=2
- **zOutputProcessEnvApproach** [3]: FOPA_ALL=0, FOPA_LOCATIONS=1, FOPA_EACH=2
- **zOutputProcessEnvType** [3]: FOPE_MAX=0, FOPE_MIN=1, FOPE_MAXABS=2
- **zOutputProcessErrorMethod** [6]: FOPM_MAXDIFF=0, FOPM_DIFFAVG=1, FOPM_PCTMAXDIFF=2, FOPM_PCTDIFFAVG=3, FOPM_NORMMAXDIFF=4, ... (6 total)
- **zOutputType** [7]: FOT_ANY=0, FOT_DISP=1, FOT_ACCEL=2, FOT_FORCE=3, FOT_STRESS=4, ... (7 total)
- **zPadAlignment** [3]: FPAD_AUTO=0, FPAD_VECTOR=1, FPAD_CURVE=2
- **zPadOffsetType** [2]: FPAD_SCALE=0, FPAD_DIST=1
- **zPictFormat** [12]: FPM_AVI_UNCOMPRESSED=-6, FPM_BMP=1, FPM_METAFILE=2, FPM_PLACEMF=3, FPM_JPEG=4, ... (12 total)
- **zPictFormat2** [5]: FPM2_BMP=1, FPM2_JPEG=4, FPM2_GIF=9, FPM2_TIF=11, FPM2_PNG=12
- **zPictRegion** [3]: FPRG_WINDOW=0, FPRG_LAYOUT=1, FPRG_DESKTOP=2
- **zPlaneDefinition** [12]: FPD_POSITION=0, FPD_USE_POINTS=1, FPD_USE_NODES=2, FPD_COMPONENTS=3, FPD_BISECT=4, ... (12 total)
- **zPlateThickOffsetMethod** [5]: FPTM_SETTOVALUE=0, FPTM_INCREMENT=1, FPTM_ADJUSTPCT=2, FPTM_TOPTONODE=3, FPTM_BOTTOMTONODE=4
- **zPlateThickOffsetOptions** [3]: FPTO_ELEM_THICKNESS=0, FPTO_PROP_THICKNESS=1, FPTO_ELEM_OFFSET=2
- **zPlyType** [11]: FPLT_PLY=0, FPLT_PLYMATERIAL=1, FPLT_LAYUP=2, FPLT_LAYUPSYMMETRIC=3, FPLT_LAYUPANTI=4, ... (11 total)
- **zPointDefinition** [19]: FCD_COORDINATES=0, FCD_WORKPLANE_COORDINATES=1, FCD_USE_POINTS=2, FCD_USE_NODES=3, FCD_OFFSET=4, ... (19 total)
- **zPointType** [2]: FPT_DEFAULT=0, FPT_SOLID=1
- **zPrefAnimateFormat** [4]: PAFM_BMP=0, PAFM_BMPSERIES=1, PAFM_AVI=2, PAFM_GIF=3
- **zPrefPictureFormat** [5]: PPFM_BMP=0, PPFM_JPEG=1, PPFM_PNG=2, PPFM_GIF=3, PPFM_TIF=4
- **zPrintSource** [10]: FPS_VIEW=0, FPS_DESKTOP=1, FPS_FILE=2, FPS_LAYOUT=3, FPS_MESSAGES=4, ... (10 total)
- **zProjectAlong** [4]: FPA_CLOSEST=0, FPA_VECTOR=1, FPA_RADIAL_VECTOR=2, FPA_RADIAL_POINT=3
- **zProjectOnto** [4]: FPO_CURVE=0, FPO_SURFACE=1, FPO_VECTOR=2, FPO_PLANE=3
- **zPublishAlign** [3]: PUBALN_LEFT=0, PUBALN_RIGHT=1, PUBALN_CENTER=2
- **zPublishFormat** [2]: PUB_RTF=0, PUB_HTML=1
- **zPublishImageFormat** [5]: PUBIF_BITMAP=0, PUBIF_JPEG=1, PUBIF_PNG=2, PUBIF_GIF=3, PUBIF_TIF=4
- **zRangeOpt** [5]: FRNG_ANY=0, FRNG_ABOVE=1, FRNG_BELOW=2, FRNG_BETWEEN=3, FRNG_OUTSIDE=4
- **zRankingApproach** [2]: FRKA_ALL=0, FRKA_EACH=1
- **zRankingMethod** [2]: FRKM_SETS=0, FRKM_ENTITY=1
- **zRankingType** [3]: FRKT_MAX=0, FRKT_MIN=1, FRKT_MAXABS=2
- **zRealFormat** [3]: FRFM_NORMAL=0, FRFM_EXPONENTIAL=1, FRFM_NASTRAN=2
- **zResultsConvert** [11]: FRC_NONE=-1, FRC_AVG=0, FRC_MAX=1, FRC_AVG_SKIP_CORNER=2, FRC_MAX_SKIP_CORNER=3, ... (11 total)
- **zResultsLocation** [9]: FRL_DB=1, FRL_OP2=2, FRL_FNO=3, FRL_XDB=5, FRL_CSV=6, ... (9 total)
- **zResultsProcessType** [9]: FRPROC_NONE=0, FRPROC_LINEAR=1, FRPROC_RSS=2, FRPROC_ENV_MAX=3, FRPROC_ENV_MIN=4, ... (9 total)
- **zReturnCode** [18]: FE_OK=-1, FE_FAIL=0, FE_CANCEL=2, FE_INVALID=3, FE_NOT_EXIST=4, ... (18 total)
- **zRigidMethod** [5]: FRIG_METHOD_AUTO=0, FRIG_METHOD_LAGRAN=1, FRIG_METHOD_LINEAR=2, FRIG_METHOD_STIFF=3, FRIG_METHOD_LGELIM=4
- **zRuledSurfaceType** [3]: FRST_RULED=0, FRST_TANGENT_SURF=1, FRST_VECTOR=2
- **zSelectorDrill** [3]: FSD_OFF=0, FSD_QUERY=1, FSD_FRONT=2
- **zSelectorType** [24]: FS_NONE=0, FS_POINT=3, FS_CURVE=4, FS_SURFACE=5, FS_NODE=7, ... (24 total)
- **zShapeEvaluator** [4]: FSEV_AUTO=0, FSEV_ORIG=1, FSEV_ALT=2, FSEV_PBEAML=3
- **zShapeOrient** [4]: FSOR_RIGHT=0, FSOR_UP=1, FSOR_LEFT=2, FSOR_DOWN=3
- **zShapeStandard** [34]: FSHP_RECT_BAR=1, FSHP_RECT_TUBE=2, FSHP_TRAP_BAR=3, FSHP_TRAP_TUBE=4, FSHP_CIRC_BAR=5, ... (34 total)
- **zSolidAlignVecMode** [3]: FSAV_VECAUTO=0, FSAV_VECINPUT=1, FSAV_VECASK=2
- **zSpringOffset** [4]: FESL_DEFAULT=0, FESL_ELLOC=1, FESL_PRLOC=2, FESL_OFFSET=3
- **zSpringOrient** [5]: FESO_NONE=0, FESO_NODE=1, FESO_VECTOR=2, FESO_ELCID=3, FESO_PRCID=4
- **zSurfaceType** [8]: FSU_BILINEAR=0, FSU_RULED=1, FSU_REVOLUTION=2, FSU_COONS=3, FSU_BEZIER=4, ... (8 total)
- **zSymmetryType** [4]: FPLS_ASIS=0, FPLS_SYMMETRIC=1, FPLS_ANTI=2, FPLS_ANTISYMMETRIC=3
- **zTableType** [5]: FTBL_NONE=0, FTBL_FUNCTION=1, FTBL_VECTORFUNCTION=2, FTBL_LOADSETCOMBINATION=3, FTBL_RESULTSETPROCESS=4
- **zTetPyrApproach** [3]: FTP_SURFACEONLY=0, FTP_TET=1, FTP_PYR=2
- **zTopologyType** [22]: FTO_LINE2=0, FTO_LINE3=1, FTO_TRIA3=2, FTO_TRIA6=3, FTO_QUAD4=4, ... (22 total)
- **zUpdateLineDirection** [3]: FULD_REVERSE=0, FULD_ELEM=1, FULD_VECTOR=2
- **zVecComplex** [4]: VCX_MAGNITUDE=0, VCX_PHASE=1, VCX_REAL=2, VCX_IMAGINARY=3
- **zVecElemOther** [38]: VEO_STRAIN_ENERGY=0, VEO_STRAIN_ENERGY_PERCENT=1, VEO_STRAIN_ENERGY_DENSITY=2, VEO_TEMP_GRADIENT_X=3, VEO_TEMP_GRADIENT_Y=4, ... (38 total)
- **zVecLineElemType** [3]: VLT_BAR=0, VLT_BEAM=1, VLT_WELD=2
- **zVecLineEnd** [3]: VLE_OVERALL=0, VLE_A=1, VLE_B=2
- **zVecLineLoc** [7]: VLL_OVERALL=0, VLL_MAX=1, VLL_MIN=2, VLL_1=3, VLL_2=4, ... (7 total)
- **zVecLineOther** [58]: VLO_SPRING_FORCE=0, VLO_SPRING_STRESS=1, VLO_SPRING_STRAIN=2, VLO_ROD_AXIAL_FORCE=3, VLO_ROD_TORQUE=4, ... (58 total)
- **zVecLineResult** [21]: VLV_AXIAL_FORCE=0, VLV_TORQUE=1, VLV_TORQUE_WARPING=2, VLV_MOMENT_PLANE1=3, VLV_MOMENT_PLANE2=4, ... (21 total)
- **zVecNodalResult** [35]: VNV_TRANSLATION=0, VNV_ROTATION=1, VNV_VELOCITY=2, VNV_ANG_VELOCITY=3, VNV_ACCELERATION=4, ... (35 total)
- **zVecNodalScalar** [24]: VNS_TEMPERATURE=0, VNS_THERMAL_CONSTRAINTFORCE=1, VNS_THERMAL_APPLIEDLOAD=2, VNS_PRESSURE=3, VNS_ENTHALPY=4, ... (24 total)
- **zVecNodalType** [4]: VNT_TOTAL_NONE=0, VNT_X=1, VNT_Y=2, VNT_Z=3
- **zVecPlateLoc** [5]: VPL_CENTROID=0, VPL_1=1, VPL_2=2, VPL_3=3, VPL_4=4
- **zVecPlatePly** [3]: VPP_TOP=0, VPP_MID=1, VPP_BOT=2
- **zVecPlateResult** [11]: VPV_FORCE=0, VPV_MOMENT=1, VPV_STRESS=2, VPV_STRAIN=3, VPV_ELASTIC_STRAIN=4, ... (11 total)
- **zVecPlateScalar** [113]: VPS_SHEAR_1FROM4=0, VPS_SHEAR_1FROM2=1, VPS_SHEAR_2FROM1=2, VPS_SHEAR_2FROM3=3, VPS_SHEAR_3FROM2=4, ... (113 total)
- **zVecPlateType** [13]: VPT_VON_MISES=0, VPT_MAX_PRIN=1, VPT_MIN_PRIN=2, VPT_MID_PRIN=3, VPT_MAX_SHEAR=4, ... (13 total)
- **zVecSolidLamLoc** [3]: VSLL_TOP=0, VSLL_MID=1, VSLL_BOT=2
- **zVecSolidLamResult** [4]: VSLV_STRESS=0, VSLV_STRAIN=1, VSLV_FAILURE=2, VSLV_STRENGTHRATIO=3
- **zVecSolidLamType** [19]: VSLT_X=0, VSLT_Y=1, VSLT_Z=2, VSLT_XY=3, VSLT_YZ=4, ... (19 total)
- **zVecSolidLoc** [9]: VSL_CENTROID=0, VSL_1=1, VSL_2=2, VSL_3=3, VSL_4=4, ... (9 total)
- **zVecSolidOther** [25]: VSO_BOLT_AXIALFORCE=0, VSO_BOLT_SHEARFORCE1=1, VSO_BOLT_SHEARFORCE2=2, VSO_BOLT_MOMENT1=3, VSO_BOLT_MOMENT2=4, ... (25 total)
- **zVecSolidResult** [4]: VSV_STRESS=0, VSV_STRAIN=1, VSV_NONLINEAR_STRESS=2, VSV_NONLINEAR_STRAIN=3
- **zVecSolidType** [16]: VST_X=0, VST_Y=1, VST_Z=2, VST_XY=3, VST_YZ=4, ... (16 total)
- **zVectorDefinition** [15]: FVD_POSITION=0, FVD_POSITION_LENGTH=1, FVD_USE_POINTS=2, FVD_USE_NODES=3, FVD_COMPONENTS=4, ... (15 total)
- **zVectorFunctionType** [6]: FTBV_NONE=0, FTBV_ACCELERATION=1, FTBV_SUNPLANET=2, FTBV_SUNPLANETALTITUDE=3, FTBV_SPHERICALVECTORSUNPLANET=4, ... (6 total)
- **zViewMode** [11]: FVM_DRAW=0, FVM_FEATURE=1, FVM_SORT=2, FVM_HIDE=3, FVM_FREE=4, ... (11 total)
- **zViewOptions** [130]: FVI_LABEL=0, FVI_CSYS=1, FVI_POINT=2, FVI_CURVE=3, FVI_SURFACE=4, ... (130 total)
- **zVisibilityType** [16]: FVIS_POINT=3, FVIS_CURVE=4, FVIS_SURFACE=5, FVIS_ELEM=8, FVIS_CSYS=9, ... (16 total)
- **zVolumeType** [4]: FVO_BRICK=0, FVO_WEDGE=1, FVO_PYRAMID=2, FVO_TETRA=3
- **zZaeroFixType** [4]: FZAF_FIXHATM=0, FZAF_FIXMACH=1, FZAF_FIXMATM=2, FZAF_FIXMDEN=3

### Interfaces (117)

| Interface | Kind | Methods | Properties |
|-----------|------|---------|------------|
| IAcoord | dispatch | 30 | 0 |
| IAeroPanel | dispatch | 45 | 2 |
| IAeroProp | dispatch | 52 | 0 |
| IAeroSpline | dispatch | 36 | 0 |
| IAeroSurf | dispatch | 36 | 0 |
| IAnalysisCase | dispatch | 91 | 10 |
| IAnalysisMgr | dispatch | 140 | 31 |
| IAnalysisStep | dispatch | 33 | 2 |
| IAnalysisStudy | dispatch | 39 | 0 |
| IBCDefinition | dispatch | 34 | 0 |
| IBCEqn | dispatch | 33 | 3 |
| IBCGeom | dispatch | 40 | 2 |
| IBCNode | dispatch | 36 | 2 |
| IBCSet | dispatch | 40 | 0 |
| IBeamCalculator | dispatch | 5 | 0 |
| IBearingSpeedDefinition | dispatch | 30 | 0 |
| IBodyMesher | dispatch | 10 | 0 |
| ICSys | dispatch | 33 | 0 |
| IChart | dispatch | 35 | 29 |
| IChartSeries | dispatch | 33 | 2 |
| IComputedResultsVectors | dispatch | 13 | 0 |
| IConnection | dispatch | 39 | 1 |
| IConnectionProp | dispatch | 32 | 4 |
| IContact | dispatch | 56 | 1 |
| ICopyTool | dispatch | 18 | 0 |
| ICurve | dispatch | 98 | 14 |
| IDBase | dispatch | 30 | 0 |
| IDataSurf | dispatch | 68 | 0 |
| IDataTable | dispatch | 47 | 0 |
| IDesignEquation | dispatch | 30 | 0 |
| IDiscreteValueSet | dispatch | 43 | 0 |
| IDrawErase | dispatch | 10 | 0 |
| IElem | dispatch | 70 | 9 |
| IElemAddRemove | dispatch | 41 | 0 |
| IElementQuality | dispatch | 85 | 0 |
| IFibersim | dispatch | 13 | 0 |
| IFlexibleSlider | dispatch | 33 | 0 |
| IFreebody | dispatch | 44 | 12 |
| IFreq | dispatch | 79 | 0 |
| IFunction | dispatch | 33 | 0 |
| IGFXArrow | dispatch | 34 | 2 |
| IGFXLine | dispatch | 34 | 1 |
| IGFXPoint | dispatch | 34 | 1 |
| IGFXQuad4 | dispatch | 35 | 2 |
| IGFXTria3 | dispatch | 35 | 2 |
| IGeometryInterface | dispatch | 3 | 0 |
| IGlobalPly | dispatch | 30 | 0 |
| IGlobalStep | dispatch | 33 | 2 |
| IGroup | dispatch | 57 | 4 |
| IInterpolate | dispatch | 37 | 2 |
| IJoint | dispatch | 36 | 4 |
| ILayer | dispatch | 41 | 0 |
| ILayup | dispatch | 59 | 16 |
| ILoadBolt | dispatch | 34 | 0 |
| ILoadDefinition | dispatch | 36 | 0 |
| ILoadETemp | dispatch | 34 | 0 |
| ILoadGeom | dispatch | 32 | 12 |
| ILoadMesh | dispatch | 37 | 7 |
| ILoadNTemp | dispatch | 34 | 0 |
| ILoadSet | dispatch | 41 | 8 |
| IMapData | dispatch | 21 | 0 |
| IMapOutput | dispatch | 19 | 0 |
| IMatl | dispatch | 39 | 5 |
| IMatrixInput | dispatch | 39 | 0 |
| IMergeTool | dispatch | 26 | 0 |
| IMeshHardPoint | dispatch | 41 | 1 |
| IMeshHardPointDefinition | dispatch | 33 | 0 |
| IMesher | dispatch | 11 | 0 |
| IMidFaceCentroidModel | dispatch | 38 | 0 |
| IMonitorPoint | dispatch | 42 | 3 |
| IMoveTool | dispatch | 11 | 0 |
| INode | dispatch | 42 | 1 |
| IOptMC | dispatch | 46 | 4 |
| IOptRel | dispatch | 39 | 1 |
| IOptResp | dispatch | 48 | 0 |
| IOptim | dispatch | 30 | 0 |
| IOutput | dispatch | 0 | 0 |
| IOutputSet | dispatch | 36 | 0 |
| IOutputTable | dispatch | 0 | 0 |
| IPlane | dispatch | 31 | 3 |
| IPlyMaterial | dispatch | 30 | 0 |
| IPoint | dispatch | 41 | 0 |
| IProp | dispatch | 52 | 5 |
| IPublishTable | dispatch | 15 | 0 |
| IPublishTool | dispatch | 17 | 0 |
| IRead | dispatch | 36 | 0 |
| IReference | dispatch | 31 | 0 |
| IReport | dispatch | 30 | 0 |
| IResults | dispatch | 123 | 0 |
| IResultsIDQuery | dispatch | 24 | 0 |
| IRotationalSpeedDefinition | dispatch | 30 | 0 |
| ISEReference | dispatch | 30 | 0 |
| IScratch | dispatch | 11 | 4 |
| ISelector | dispatch | 20 | 0 |
| ISet | dispatch | 122 | 0 |
| ISolid | dispatch | 58 | 2 |
| ISolidCleanupTool | dispatch | 3 | 0 |
| ISolidEdit | dispatch | 5 | 0 |
| ISortSet | dispatch | 35 | 0 |
| IStressLinear | dispatch | 4 | 0 |
| ISurface | dispatch | 106 | 7 |
| ITableData | dispatch | 51 | 0 |
| IText | dispatch | 32 | 2 |
| ITmgBC | dispatch | 34 | 4 |
| ITmgCtl | dispatch | 34 | 4 |
| ITmgInt | dispatch | 32 | 1 |
| ITmgOpt | dispatch | 32 | 3 |
| ITmgReal | dispatch | 32 | 2 |
| ITrackData | dispatch | 8 | 0 |
| IUserData | dispatch | 40 | 0 |
| IUserDefinedGraphics | dispatch | 89 | 0 |
| IVar | dispatch | 34 | 0 |
| IVector | dispatch | 31 | 2 |
| IView | dispatch | 55 | 42 |
| IViewOrient | dispatch | 48 | 3 |
| IXYPlotDefinition | dispatch | 30 | 0 |
| Imodel | dispatch | 747 | 43 |

### CoClasses (118)

- **Acoord** (`{66081583-5805-403B-9419-904DFD6D2F9B}`): IAcoord
- **AeroPanel** (`{923D4FF9-4C93-4DAA-8223-F275CC54C69F}`): IAeroPanel
- **AeroProp** (`{6C3881ED-8C68-4807-B69A-4430737F37B1}`): IAeroProp
- **AeroSpline** (`{39B680B4-1AD7-44BB-8C89-A699F3B191AE}`): IAeroSpline
- **AeroSurf** (`{61CFF171-CC7E-40BB-A20F-B1F065C36B29}`): IAeroSurf
- **AnalysisCase** (`{AB06C176-0E7E-11D5-9471-001083FFF11C}`): IAnalysisCase
- **AnalysisMgr** (`{00EF42FA-0E77-11D5-9471-001083FFF11C}`): IAnalysisMgr
- **AnalysisStep** (`{B49E120C-C070-4C6D-BB09-036D188F05A4}`): IAnalysisStep
- **AnalysisStudy** (`{589EAFBA-B3D0-42FB-B902-FE0A88B7EC80}`): IAnalysisStudy
- **BCDefinition** (`{F1704418-2455-4C38-8C0C-AE23E062D421}`): IBCDefinition
- **BCEqn** (`{56434B16-F392-11D4-9453-001083FFF11C}`): IBCEqn
- **BCGeom** (`{D7297E18-F305-11D4-9452-001083FFF11C}`): IBCGeom
- **BCNode** (`{D0E25458-F2FB-11D4-9452-001083FFF11C}`): IBCNode
- **BCSet** (`{5D2F5E16-F2F1-11D4-9452-001083FFF11C}`): IBCSet
- **BeamCalculator** (`{3A62FE4E-D156-4F16-9C1B-F81C6BB4089A}`): IBeamCalculator
- **BearingSpeedDefinition** (`{F5B85DA5-FA4D-447A-A50A-27C71A35D8AC}`): IBearingSpeedDefinition
- **BodyMesher** (`{F2509BC8-33D7-4DF8-BDE1-3CB362DB1ACD}`): IBodyMesher
- **CSys** (`{10CE53BA-F2E2-11D4-9452-001083FFF11C}`): ICSys
- **Chart** (`{7AADC5F1-400B-4984-9D12-314296952F1F}`): IChart
- **ChartSeries** (`{19988E83-F344-4944-82DE-AEBE26689F33}`): IChartSeries
- **ComputedResultsVectors** (`{AAA42219-5244-45C6-A6B4-4AD46D318C4D}`): IComputedResultsVectors
- **Connection** (`{1A8C9C55-6711-4498-BDD9-8BD54586842E}`): IConnection
- **ConnectionProp** (`{FA64FD81-5C92-425F-87B4-FC849D84898B}`): IConnectionProp
- **ConnectionRegion** (`{14057456-0382-11D5-9465-001083FFF11C}`): IContact
- **Contact** (`{14057454-0382-11D5-9465-001083FFF11C}`): IContact
- **CopyTool** (`{72722F0C-7881-406C-9ADE-AB1BD014068F}`): ICopyTool
- **Curve** (`{1F9F16D0-09D6-11D5-946C-001083FFF11C}`): ICurve
- **DBase** (`{90561A66-EB1F-11D4-9447-001083FFF11C}`): IDBase
- **DataSurf** (`{8F814532-166A-4092-BBD8-C37483772F1E}`): IDataSurf
- **DataTable** (`{473E5698-513B-4A26-BD0F-FDB36820E7B1}`): IDataTable
- **DesignEquation** (`{1CA3384F-4A57-4BB1-9C7F-BE32974ED31C}`): IDesignEquation
- **DiscreteValueSet** (`{C05A6065-9B64-4E95-BF20-EEAA0E741159}`): IDiscreteValueSet
- **DrawErase** (`{0BECB76B-5F94-4718-942B-9A2A866A59D1}`): IDrawErase
- **Elem** (`{1E6C2700-F16A-11D4-9450-001083FFF11C}`): IElem
- **ElemAddRemove** (`{65FADBB9-C7F0-4587-92DD-309E47A66F37}`): IElemAddRemove
- **ElementQuality** (`{DED875D6-7D90-445B-89C7-17D709DB45F9}`): IElementQuality
- **Fibersim** (`{F8E33640-CC4A-447D-BFFD-B70D8D6B51FB}`): IFibersim
- **FlexibleSlider** (`{AA0C28B6-A618-4ADD-B1AB-0C794A44CA27}`): IFlexibleSlider
- **Freebody** (`{F39A93F4-DFD9-42D5-B663-8F09A959DAFE}`): IFreebody
- **Frequency** (`{BC4680A6-7B1C-449B-B7F7-AAF21EC0ABD3}`): IFreq
- **Function** (`{14481C58-0767-11D5-9467-001083FFF11C}`): IFunction
- **GFXArrow** (`{1694667C-A6BD-4EA1-B1F0-6485588CDAEB}`): IGFXArrow
- **GFXLine** (`{72FA0DCF-21F2-4E55-9EDC-5D4F64ED7EC6}`): IGFXLine
- **GFXPoint** (`{90C90B36-D880-497A-9CD6-AAC2CADB7B7C}`): IGFXPoint
- **GFXQuad4** (`{5070769D-079C-46E2-BB16-57D7260F9C2B}`): IGFXQuad4
- **GFXTria3** (`{CAC6D4FB-4D32-42C5-910C-D73FBB9AEB62}`): IGFXTria3
- **GeometryInterface** (`{8E76D487-C2EE-4C57-A491-756662689141}`): IGeometryInterface
- **GlobalStep** (`{4DEBC496-8BC4-4B09-A866-FF3A324BA3B7}`): IGlobalStep
- **Interpolate** (`{60266D05-AF68-4B10-906C-4BDAFADE3746}`): IInterpolate
- **Joint** (`{51AE9789-73AE-4D75-85E7-328734699211}`): IJoint
- **Layup** (`{EDB333C5-3711-47A5-A628-33B4B8768F88}`): ILayup
- **LoadBolt** (`{0DC9D657-721A-4AE7-B468-0C4B0FDC97AA}`): ILoadBolt
- **LoadDefinition** (`{A9BF3A21-E8F6-4D5C-BC48-A191C61C57D2}`): ILoadDefinition
- **LoadETemp** (`{1FAF0E16-F6C9-11D4-9456-001083FFF11C}`): ILoadETemp
- **LoadGeom** (`{78456268-F7A9-11D4-9457-001083FFF11C}`): ILoadGeom
- **LoadMesh** (`{FFDF9E7E-F6DD-11D4-9456-001083FFF11C}`): ILoadMesh
- **LoadNTemp** (`{33A4C0D6-F6C5-11D4-9456-001083FFF11C}`): ILoadNTemp
- **LoadSet** (`{39A8F664-F3CF-11D4-9453-001083FFF11C}`): ILoadSet
- **MapData** (`{0023EA25-812A-4253-A431-86B427A49C8C}`): IMapData
- **MapOutput** (`{FB7C8191-2114-43D6-86DE-78138CDF8C0B}`): IMapOutput
- **Matl** (`{0AD6E2EA-EE3E-11D4-944C-001083FFF11C}`): IMatl
- **MatrixInput** (`{2B6ABCD3-ABB6-448D-BC13-FB9C102792B9}`): IMatrixInput
- **MergeTool** (`{8B79ED27-CCB9-4E14-9C0B-49E9EC00B1DC}`): IMergeTool
- **MeshHardPoint** (`{3054CBAC-8117-467C-8987-74764DC3DF3D}`): IMeshHardPoint
- **MeshHardPointDefinition** (`{D6EDD9A7-EFF2-41AC-891A-F9FED8F10CEE}`): IMeshHardPointDefinition
- **Mesher** (`{B0BD5EA5-C79D-4140-83FF-0642F66D2F37}`): IMesher
- **MidFaceCentroidModel** (`{8D7600B6-C1B7-4740-8D63-50E476A84B2D}`): IMidFaceCentroidModel
- **MonitorPoint** (`{80701FE2-7A74-44F7-936B-218FA64D8D91}`): IMonitorPoint
- **MoveTool** (`{23FA0A31-1F8E-4ED3-A527-F3F46B40DC9F}`): IMoveTool
- **Node** (`{43752AF8-E669-11D4-9441-001083FFF11C}`): INode
- **OptMC** (`{56532637-5FE8-417C-B067-B131C22DC038}`): IOptMC
- **OptRel** (`{859D91FA-AFD8-4561-83FB-1F02033297C3}`): IOptRel
- **OptResp** (`{2BF41A8E-BFEF-479D-9C37-146A3AF46FCE}`): IOptResp
- **Optim** (`{D3A5591B-080C-11D5-9468-001083FFF11C}`): IOptim
- **Output** (`{F7E2A8A2-0820-11D5-9468-001083FFF11C}`): IOutput
- **OutputSet** (`{423C4776-0814-11D5-9468-001083FFF11C}`): IOutputSet
- **OutputTable** (`{90B7095F-01BC-4A71-BDFC-A37FF796A824}`): IOutputTable
- **Plane** (`{891A6127-406E-4438-8A3F-AF254F4508DD}`): IPlane
- **PlyMaterial** (`{86B145A2-34EE-4242-BC0D-216007960CA1}`): IPlyMaterial
- **Point** (`{A97FA4FC-09CA-11D5-946C-001083FFF11C}`): IPoint
- **Prop** (`{7110873C-F096-11D4-944F-001083FFF11C}`): IProp
- **PublishTable** (`{BE32C853-7FC3-4486-AD34-DF79ABD7EC56}`): IPublishTable
- **PublishTool** (`{49201AE4-58D3-431E-B227-3128F38A55E2}`): IPublishTool
- **Read** (`{86603852-0DA7-11D5-9470-001083FFF11C}`): IRead
- **Reference** (`{E6F57AB1-E85E-455B-AA4D-4FF48824BB31}`): IReference
- **Report** (`{0D85757E-0374-11D5-9465-001083FFF11C}`): IReport
- **Results** (`{2B88E74B-3213-47AB-9CAD-0AEA2E415F16}`): IResults
- **ResultsIDQuery** (`{08AD5C37-28EC-4DD2-BC7E-EF2B94B624A2}`): IResultsIDQuery
- **RotationalSpeedDefinition** (`{A3C30FA1-9764-4171-8387-D36E2F1B0FD2}`): IRotationalSpeedDefinition
- **SEReference** (`{BCF73008-FAAA-4648-9ABE-A4DF900D45BF}`): ISEReference
- **Scratch** (`{98D6BD3E-3DDD-4457-B6AD-15D6A1F3CE51}`): IScratch
- **Selector** (`{8A3498F9-A383-419E-8117-86A0305175FF}`): ISelector
- **Set** (`{FC77C4FB-EC92-11D4-9449-001083FFF11C}`): ISet
- **Solid** (`{28BCBA86-0D7F-11D5-9470-001083FFF11C}`): ISolid
- **SolidCleanupTool** (`{04B2D4B8-4F23-485B-8151-307D0C14462E}`): ISolidCleanupTool
- **SolidEdit** (`{C9B3B297-F3EE-44EC-9B20-D37CA9D588A3}`): ISolidEdit
- **SortSet** (`{E4A806F2-65DD-4B9A-8CA7-BB2B71BEDFAE}`): ISortSet
- **StressLinear** (`{08B1C6B3-3124-4D88-BE4C-DFE7642E817E}`): IStressLinear
- **Surface** (`{AA0FCDBE-0CB0-11D5-946F-001083FFF11C}`): ISurface
- **TableData** (`{17387167-149C-43E5-A91D-EAC4D1E4EAAD}`): ITableData
- **TmgBC** (`{F809A644-09BC-11D5-946C-001083FFF11C}`): ITmgBC
- **TmgCtl** (`{C1DD56FA-09BD-11D5-946C-001083FFF11C}`): ITmgCtl
- **TmgInt** (`{5A0AEF82-09BE-11D5-946C-001083FFF11C}`): ITmgInt
- **TmgOpt** (`{EC1095A8-09BE-11D5-946C-001083FFF11C}`): ITmgOpt
- **TmgReal** (`{9D6A22B6-09BE-11D5-946C-001083FFF11C}`): ITmgReal
- **TrackData** (`{CF420F81-631E-4597-83A5-B6C971AEAB99}`): ITrackData
- **UserData** (`{CFA77C4E-63E9-11D5-94AA-001083FFF11C}`): IUserData
- **UserDefinedGraphics** (`{9B5131E7-BFB8-4219-8F7D-764DBC32C323}`): IUserDefinedGraphics
- **Var** (`{72473E7F-0369-11D5-9465-001083FFF11C}`): IVar
- **View** (`{037BFA02-F86C-11D4-9458-001083FFF11C}`): IView
- **ViewOrient** (`{3042DDD2-BB63-41CB-85F7-52FDE63B0624}`): IViewOrient
- **XYPlotDefinition** (`{FFE3E8FE-F64A-4FE0-9430-6A60BA5A3B22}`): IXYPlotDefinition
- **globalply** (`{A09ECE68-9245-409B-9321-A2476AE7D4E7}`): IGlobalPly
- **group** (`{FA671D0A-F7A8-11D4-9457-001083FFF11C}`): IGroup
- **layer** (`{E0974274-0376-11D5-9465-001083FFF11C}`): ILayer
- **model** (`{A01DD4C4-A8F0-11D4-9FAC-00105A0A86C2}`): Imodel
- **text** (`{FDEA6C67-77F3-4F6C-BDB9-EA976919B421}`): IText
- **vector** (`{F2E67C74-0E5B-477F-8377-BACD7317A2FF}`): IVector
