

def handle_slice(wsd):
	"""
	Handles the creation of a new slice
	"""

	services_end_points = []
	pop_end_points = []

	# Create the network graph
	for nap in wsd['wsd']['services-segment']:
		services_end_points.append(nap['service_id'])
	print(services_end_points)

	for new_pop in wsd['wsd']['pop']:
		pop_end_points.append(new_pop['vim_id'])
	print(pop_end_points)