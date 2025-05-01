import openmc

sp = openmc.StatePoint('statepoint.300.h5')

fuel_tally = sp.get_tally(id=1, scores=['flux', 'nu-fission'])
fuel_flux = fuel_tally.get_slice(scores=['flux'])
fuel_nu_fission = fuel_tally.get_slice(scores=['nu-fission'])

for i in fuel_tally.get_filter_indices():
    print(f'Flux in fuel pin {i}: ', fuel_flux.mean[i].flatten()[0])
