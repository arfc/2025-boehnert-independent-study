import numpy as np
import openmc

###############################################################################
# Create materials for the problem

# Instantiate Uranium Fuel and Water moderator
uo2 = openmc.Material(name='UO2 fuel')
uo2.add_element('U', 1.0, enrichment=2.4)
uo2.add_element('O', 2.0)
uo2.set_density('g/cm3', 10.29769)

water = openmc.Material(name='Water')
water.set_density('g/cm3', 1.0)
water.add_element('H', 2.0)
water.add_element('O', 1.0)

# Instantiate a Materials collection and export to XML
materials_file = openmc.Materials([uo2, water])
materials_file.export_to_xml()

###############################################################################
# Define problem geometry

# The geometry we will define a simplified pincell with fuel radius 0.54 cm
# surrounded by moderator

fuel_or = openmc.ZCylinder(r=0.54)

fuel_cell = openmc.Cell(region=-fuel_or, fill=uo2)
water_cell = openmc.Cell(region=+fuel_or, fill=water)
p = openmc.Universe(cells=[fuel_cell, water_cell])
w = openmc.Universe(cells=[openmc.Cell(fill=water)])

# Create a region represented as the inside of a rectangular prism
pitch = 1.26
lattice = openmc.RectLattice()
lattice.lower_left = (-pitch, -pitch)
lattice.pitch = (pitch, pitch)
lattice.universes = [[p,w],
                     [p,p]]
box = openmc.model.RectangularPrism(pitch*2, pitch*2, boundary_type='reflective')
pincell_bounded = openmc.Cell(fill=lattice, region=-box, name='pincell')

# Create a geometry (specifying merge surfaces option to remove
# all the redundant surfaces) and export to XML
geometry = openmc.Geometry([pincell_bounded], merge_surfaces=True)
geometry.export_to_xml()

###############################################################################
# Create tallies for the model

# Distribcell filter for checking out the pincells. We use a DistribcellFilter
# to tally duplicated cells that are in a lattice.
distribcell_filter_fuel = openmc.DistribcellFilter(fuel_cell)

# Tally to count the fission rate in the fuel

tally_fuel = openmc.Tally(name='flux_fuel')
tally_fuel.filters = [distribcell_filter_fuel]
tally_fuel.scores = ['flux', 'nu-fission']

# TODO: Create tallys for the flux in the water cells

distribcell_filter_water = openmc.DistribcellFilter(water_cell)
tally_water = openmc.Tally(name='flux_water')
tally_water.filters = [distribcell_filter_water]
tally_water.scores = ['flux']

watercell_filter = openmc.UniverseFilter(w)
tally_empty = openmc.Tally(name='tally_empty')
tally_empty.filters = [watercell_filter]
tally_empty.scores = ['flux']

tallies = openmc.Tallies([tally_fuel,tally_water,tally_empty])
tallies.export_to_xml()


###############################################################################
# Create a plot to visualize the geometry

plot = openmc.Plot()
plot.basis='xy'
plot.origin = (0.0, 0.0, 0.0)
plot.width = (2*pitch, 2*pitch)
plot.pixels = (400,400)
plot.color_by = 'material'
plot.colors = {
    water: 'blue',
    uo2: 'red'
}

plots = openmc.Plots()
plots.append(plot)
plots.export_to_xml()

###############################################################################
# Create settings for the problem and Shannon Entropy Mesh to evaluate the number of inactive batches needed

# TODO: Change the settings file to run an eigenvalue simulation

entropy_mesh = openmc.RegularMesh()
entropy_mesh.lower_left = (-pitch,-pitch)
entropy_mesh.upper_right = (pitch,pitch)
entropy_mesh.dimension = (8, 8)

settings = openmc.Settings()
settings.batches = 300 
settings.inactive = 200
settings.particles = 10000
settings.run_mode = 'eigenvalue'
settings.entropy_mesh = entropy_mesh
settings.export_to_xml()
