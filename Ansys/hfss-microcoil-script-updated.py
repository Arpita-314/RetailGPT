# -*- coding: utf-8 -*-

import ScriptEnv
import math

# Initialize the HFSS environment
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()

# Check if there's an active project, if not, create a new one
oProject = oDesktop.GetActiveProject()
if oProject is None:
    oProject = oDesktop.NewProject()

# Check if there's an active design, if not, create a new one
oDesign = oProject.GetActiveDesign()
if oDesign is None:
    oDesign = oProject.InsertDesign("HFSS", "HFSSDesign1", "DrivenModal", "")

# Set the active editor to 3D Modeler
oEditor = oDesign.SetActiveEditor("3D Modeler")

# Define parameters
substrate_size = 4  # mm (400 micrometers)
substrate_thickness = 0.05  # mm (50 micrometers, adjust as needed)
microcoil_width = 0.01  # mm (10 micrometers, adjust as needed)
microcoil_thickness = 0.0002  # mm (200 nm)

# Create diamond substrate
substrate_name = "DiamondSubstrate_1"
oEditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", "-2mm",
        "YPosition:=", "-2mm",
        "ZPosition:=", "0mm",
        "XSize:=", "{0}mm".format(substrate_size),
        "YSize:=", "{0}mm".format(substrate_size),
        "ZSize:=", "{0}mm".format(substrate_thickness)
    ],
    [
        "NAME:Attributes",
        "Name:=", substrate_name,
        "Flags:=", "",
        "Color:=", "(143 175 143)",
        "Transparency:=", 0.1,
        "PartCoordinateSystem:=", "Global",
        "MaterialName:=", "diamond",
        "SolveInside:=", True
    ])

# Import the DXF file
oEditor.ImportDXF(
    ["NAME:options",
     "FileName:=", "C:/Users/go29lap/code/ansys/microcoils_v3.dxf",
     "Scale:=", 0.001,
     "AutoDetectClosed:=", True,
     "SelfStitch:=", True,
     "DefeatureGeometry:=", False,
     "DefeatureDistance:=", 0,
     "RoundCoordinates:=", False,
     "RoundNumDigits:=", 4,
     "WritePolyWithWidthAsFilledPoly:=", False,
     "ImportMethod:=", 1,
     "2DSheetBodies:=", True,
     ["NAME:LayerInfo",
      ["NAME:0",
       "source:=", "0",
       "display_source:=", "0",
       "import:=", True,
       "dest:=", "0",
       "dest_selected:=", False,
       "layer_type:=", "signal"
      ],
      ["NAME:LAYER_1",
       "source:=", "LAYER_1",
       "display_source:=", "LAYER_1",
       "import:=", False,
       "dest:=", "LAYER_1",
       "dest_selected:=", False,
       "layer_type:=", "signal"
      ],
      ["NAME:LAYER_2",
       "source:=", "LAYER_2",
       "display_source:=", "LAYER_2",
       "import:=", False,
       "dest:=", "LAYER_2",
       "dest_selected:=", False,
       "layer_type:=", "signal"
      ]
     ]
    ])

# Thicken the imported sheets
oEditor.ThickenSheet(
    ["NAME:Selections",
     "Selections:=", "0",
     "NewPartsModelFlag:=", "Model"
    ],
    ["NAME:SheetThickenParameters",
     "Thickness:=", "200nm",
     "BothSides:=", False
    ])

# Create wave ports
port_width = microcoil_width
port_positions = [
    (2, -1.170478567), (1.201158763, 2), (0, 2), 
    (-1.019214464, 2), (-2, 1.201158763),
    (-2, -1.019214464), (-1.201158763, -2),
    (1.050351405, -2)
]

for i, (x, y) in enumerate(port_positions):
    port_name = "WavePort_{0}".format(i+1)
    oEditor.CreateRectangle(
        [
            "NAME:RectangleParameters",
            "IsCovered:=", True,
            "XStart:=", "{0}mm".format(x - port_width/2),
            "YStart:=", "{0}mm".format(y - port_width/2),
            "ZStart:=", "{0}mm".format(substrate_thickness),
            "Width:=", "{0}mm".format(port_width),
            "Height:=", "{0}mm".format(port_width),
            "WhichAxis:=", "Z"
        ],
        [
            "NAME:Attributes",
            "Name:=", port_name,
            "Flags:=", "",
            "Color:=", "(0 0 255)",
            "Transparency:=", 0,
            "PartCoordinateSystem:=", "Global",
            "MaterialName:=", "vacuum",
            "SolveInside:=", True
        ])

# Project sheet to connect the waveports with the wires
oEditor.ProjectSheet(
    ['NAME:Selections',
     'Selections:=', '0,WavePort_1,WavePort_2,WavePort_3,WavePort_4,WavePort_5,WavePort_6,WavePort_7,WavePort_8'],
    ['NAME:ProjectSheetParameters',
     'Thickness:=', '0mm']
)

# Create radiation boundary
radiation_boundary_offset = 0.3  # mm (300 micrometers)
oEditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", "{0}mm".format(-substrate_size/2 - radiation_boundary_offset),
        "YPosition:=", "{0}mm".format(-substrate_size/2 - radiation_boundary_offset),
        "ZPosition:=", "{0}mm".format(-radiation_boundary_offset),
        "XSize:=", "{0}mm".format(substrate_size + 2*radiation_boundary_offset),
        "YSize:=", "{0}mm".format(substrate_size + 2*radiation_boundary_offset),
        "ZSize:=", "{0}mm".format(substrate_thickness + 2*radiation_boundary_offset)
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
    port_name = "WavePort_{0}".format(i)
    oModule.AssignWavePort(
        [
            "NAME:" + port_name,
            "Objects:=", [port_name],
            "NumModes:=", 1,
            "RenormalizeAllTerminals:=", True,
            "UseLineModeAlignment:=", False,
            "DoDeembed:=", False,
            [
                "NAME:Modes",
                [
                    "NAME:Mode1",
                    "ModeNum:=", 1,
                    "UseIntLine:=", True
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
        "AdaptMultipleFreqs:=", True,
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
oModule.CreateReport("S_Parameters", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
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

# Z-parameters
oModule.CreateReport("Z_Parameters", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
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
