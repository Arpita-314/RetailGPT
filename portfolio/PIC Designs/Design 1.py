import gdsfactory as gf

# Create a new device
pic = gf.Component("Photonic_Integrated_Circuit")

# Add a straight waveguide
waveguide = gf.components.straight(length=10, width=0.5)
wg1 = pic << waveguide
wg1.move((0, 0))

# Add a bend waveguide
bend = gf.components.bend_euler(radius=5, width=0.5, angle=90)
bend1 = pic << bend
bend1.connect("o1", wg1.ports["o2"])

# Add a Y-branch splitter
y_splitter = gf.components.y_splitter(width=0.5, length=5, port_spacing=2)
splitter = pic << y_splitter
splitter.connect("o1", bend1.ports["o2"])

# Add output waveguides
wg2 = pic << waveguide
wg2.connect("o1", splitter.ports["o2"])

wg3 = pic << waveguide
wg3.connect("o1", splitter.ports["o3"])

# Save the layout to a GDS file
pic.write_gds("photonic_integrated_circuit.gds")

# Display the layout
pic.show()
pic.plot()