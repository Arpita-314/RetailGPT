import ScriptEnv
import math

# Initialize the HFSS environment
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")

# Define parameters
substrate_size = 0.4  # mm (400 micrometers)
substrate_thickness = 0.05  # mm (50 micrometers, adjust as needed)
microcoil_width = 0.01  # mm (10 micrometers, adjust as needed)
microcoil_thickness = 0.0002  # mm (200 nm)
center_gap_radius = 0.02  # mm (20 micrometers, adjust as needed)

# Create diamond substrate
oEditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", "-0.2mm",
        "YPosition:=", "-0.2mm",
        "ZPosition:=", "0mm",
        "XSize:=", f"{substrate_size}mm",
        "YSize:=", f"{substrate_size}mm",
        "ZSize:=", f"{substrate_thickness}mm"
    ],
    [
        "NAME:Attributes",
        "Name:=", "DiamondSubstrate",
        "Flags:=", "",
        "Color:=", "(143 175 143)",
        "Transparency:=", 0.1,
        "PartCoordinateSystem:=", "Global",
        "MaterialName:=", "diamond",
        "SolveInside:=", True
    ])

# Function to create a single microcoil arm
def create_microcoil_arm(angle):
    start_x = center_gap_radius * math.cos(angle)
    start_y = center_gap_radius * math.sin(angle)
    end_x = (substrate_size / 2) * math.cos(angle)
    end_y = (substrate_size / 2) * math.sin(angle)
    
    oEditor.CreatePolyline(
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:=", True,
            "IsPolylineClosed:=", False,
            ["NAME:PolylinePoints",
             ["NAME:PLPoint", "X:=", f"{start_x}mm", "Y:=", f"{start_y}mm", "Z:=", f"{substrate_thickness}mm"],
             ["NAME:PLPoint", "X:=", f"{end_x}mm", "Y:=", f"{end_y}mm", "Z:=", f"{substrate_thickness}mm"]],
            ["NAME:PolylineSegments", ["NAME:PLSegment", "SegmentType:=", "Line", "StartIndex:=", 0, "NoOfPoints:=", 2]],
        ],
        [
            "NAME:Attributes",
            "Name:=", f"MicrocoilArm_{angle}",
            "Flags:=", "",
            "Color:=", "(255 215 0)",
            "Transparency:=", 0,
            "PartCoordinateSystem:=", "Global",
            "MaterialName:=", "gold",
            "SolveInside:=", False
        ])

    # Thicken the arm
    oEditor.SweepAlongVector(
        [
            "NAME:Selections",
            "Selections:=", f"MicrocoilArm_{angle}",
            "NewPartsModelFlag:=", "Model"
        ],
        [
            "NAME:VectorSweepParameters",
            "DraftAngle:=", "0deg",
            "DraftType:=", "Round",
            "CheckFaceFaceIntersection:=", False,
            "SweepVectorX:=", "0mm",
            "SweepVectorY:=", "0mm",
            "SweepVectorZ:=", f"{microcoil_thickness}mm"
        ])

    # Cover the arm
    oEditor.CoverLines(
        [
            "NAME:Selections",
            "Selections:=", f"MicrocoilArm_{angle}",
            "NewPartsModelFlag:=", "Model"
        ])

# Create 8 microcoil arms
for i in range(8):
    angle = i * math.pi / 4
    create_microcoil_arm(angle)

# Unite all microcoil arms
oEditor.Unite(
    [
        "NAME:Selections",
        "Selections:=", ",".join([f"MicrocoilArm_{i*math.pi/4}" for i in range(8)])
    ],
    [
        "NAME:UniteParameters",
        "KeepOriginals:=", False
    ])

# Rename the united object
oEditor.ChangeProperty(
    [
        "NAME:AllTabs",
        [
            "NAME:Geometry3DAttributeTab",
            ["NAME:PropServers", "MicrocoilArm_0.0"],
            ["NAME:ChangedProps", ["NAME:Name", "Value:=", "Microcoil"]]
        ]
    ])

# Create wave ports
port_width = microcoil_width
port_positions = [
    (0.2, 0), (0.2/math.sqrt(2), 0.2/math.sqrt(2)), (0, 0.2), 
    (-0.2/math.sqrt(2), 0.2/math.sqrt(2)), (-0.2, 0),
    (-0.2/math.sqrt(2), -0.2/math.sqrt(2)), (0, -0.2),
    (0.2/math.sqrt(2), -0.2/math.sqrt(2))
]

for i, (x, y) in enumerate(port_positions):
    oEditor.CreateRectangle(
        [
            "NAME:RectangleParameters",
            "IsCovered:=", True,
            "XStart:=", f"{x}mm",
            "YStart:=", f"{y-port_width/2}mm",
            "ZStart:=", f"{substrate_thickness}mm",
            "Width:=", f"{port_width}mm",
            "Height:=", f"{microcoil_thickness}mm",
            "WhichAxis:=", "Z"
        ],
        [
            "NAME:Attributes",
            "Name:=", f"WavePort{i+1}",
            "Flags:=", "",
            "Color:=", "(0 0 255)",
            "Transparency:=", 0,
            "PartCoordinateSystem:=", "Global",
            "MaterialName:=", "vacuum",
            "SolveInside:=", True
        ])

# Create radiation boundary
radiation_boundary_offset = 0.1  # mm (100 micrometers)
oEditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", f"{-substrate_size/2 - radiation_boundary_offset}mm",
        "YPosition:=", f"{-substrate_size/2 - radiation_boundary_offset}mm",
        "ZPosition:=", f"{-radiation_boundary_offset}mm",
        "XSize:=", f"{substrate_size + 2*radiation_boundary_offset}mm",
        "YSize:=", f"{substrate_size + 2*radiation_boundary_offset}mm",
        "ZSize:=", f"{substrate_thickness + 2*radiation_boundary_offset}mm"
    ],
    [
        "NAME:Attributes",
        "Name:=", "RadiationBoundary",
        "Flags:=", "",
        "Color:=", "(0 0 255)",
        "Transparency:=", 0.8,
        "PartCoordinateSystem:=", "Global",
        "MaterialName:=", "vacuum",
        "SolveInside:=", False
    ])

# Assign radiation boundary condition
oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignRadiation(
    [
        "NAME:Rad1",
        "Objects:=", ["RadiationBoundary"],
        "IsFssReference:=", False,
        "IsForPML:=", False
    ])

# Assign wave ports
for i in range(1, 9):  # 8 ports
    oModule.AssignWavePort(
        [
            f"NAME:WavePort{i}",
            "Objects:=", [f"WavePort{i}"],
            "NumModes:=", 1,
            "RenormalizeAllTerminals:=", True,
            "UseLineModeAlignment:=", False,
            "DoDeembed:=", False,
            [
                "NAME:Modes",
                [
                    "NAME:Mode1",
                    "ModeNum:=", 1,
                    "UseIntLine:=", False
                ]
            ],
            "ShowReporterFilter:=", False,
            "ReporterFilter:=", [True],
            "UseAnalyticAlignment:=", False
        ])

# Set up analysis
oModule = oDesign.GetModule("AnalysisSetup")
oModule.InsertSetup("HfssDriven", 
    [
        "NAME:Setup1",
        "AdaptMultipleFreqs:=", False,
        "Frequency:=", "25MHz",
        "MaxDeltaS:=", 0.02,
        "PortsOnly:=", False,
        "UseMatrixConv:=", False,
        "MaximumPasses:=", 6,
        "MinimumPasses:=", 1,
        "MinimumConvergedPasses:=", 1,
        "PercentRefinement:=", 30,
        "IsEnabled:=", True,
        "BasisOrder:=", 1,
        "DoLambdaRefine:=", True,
        "DoMaterialLambda:=", True,
        "SetLambdaTarget:=", False,
        "Target:=", 0.3333,
        "UseMaxTetIncrease:=", False,
        "PortAccuracy:=", 2,
        "UseABCOnPort:=", False,
        "SetPortMinMaxTri:=", False,
        "UseDomains:=", False,
        "UseIterativeSolver:=", False,
        "SaveRadFieldsOnly:=", False,
        "SaveAnyFields:=", True,
        "IESolverType:=", "Auto",
        "LambdaTargetForIESolver:=", 0.15,
        "UseDefaultLambdaTgtForIESolver:=", True
    ])

# Set up frequency sweep
oModule.InsertFrequencySweep("Setup1", 
    [
        "NAME:Sweep",
        "IsEnabled:=", True,
        "RangeType:=", "LinearStep",
        "RangeStart:=", "1MHz",
        "RangeEnd:=", "50MHz",
        "RangeStep:=", "1MHz",
        "Type:=", "Discrete",
        "SaveFields:=", False,
        "SaveRadFields:=", False,
        "ExtrapToDC:=", False
    ])

# Create reports (S-parameters and Z-parameters)
oModule = oDesign.GetModule("ReportSetup")
oModule.CreateReport("S Parameters", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    [
        "Domain:=", "Sweep"
    ], 
    [
        "Freq:=", ["All"]
    ], 
    [
        "X Component:=", "Freq",
        "Y Component:=", ["dB(S(1,1))", "dB(S(2,1))"]
    ], [])

oModule.CreateReport("Z Parameters", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    [
        "Domain:=", "Sweep"
    ], 
    [
        "Freq:=", ["All"]
    ], 
    [
        "X Component:=", "Freq",
        "Y Component:=", ["re(Z(1,1))", "im(Z(1,1))"]
    ], [])

# Save the project
oProject.Save()

# Analyze
oDesign.Analyze("Setup1")
