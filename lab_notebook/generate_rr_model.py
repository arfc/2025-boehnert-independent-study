import openmc

model = openmc.Model.from_xml()
model.convert_to_multigroup()
model.convert_to_random_ray()

n=100
mesh=openmc.RegularMesh()
mesh.dimension = (n,n)
mesh.lower_left = model.geometry.bounding_box.lower_left
mesh.upper_right = model.geometry.bounding_box.upper_right
model.settings.random_ray['source_region_meshes'] = [(mesh, [model.geometry.root_universe])]
model.settings.random_ray['volume_normalized_flux_tallies'] = False
model.settings.entropy_mesh = mesh
model.export_to_xml()

