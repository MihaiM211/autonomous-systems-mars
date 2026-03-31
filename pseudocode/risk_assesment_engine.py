STORM_ETA = 12 * 60
SAFETY_BUFFER = 2 * 60
SHIELD_DEPLOY_TIME = 15 

def evaluate(storm_data, aircraft_state, terrain_data):
	
	#Calculate Evasion Viability
	evasion_route = calculate_shortest_path(storm_data, aircraft_state.position)
	time_to_evade = evasion_route.distance / aircraft_state.max_speed
	evade = False
	if(time_to_evade < (STORM_ETA – SAFETY_BUFFER)) and (aircraft_state.battery > evasion_route.energy_req):
		evade = True

	#Calculate Landing Viability
	landing_zone = scan_terrain(terrain_data, max_search_radius=500)
	time_to_land = calculate_descent_time(aircraft_state.altitude, landing_zone)

	total_land_time = time_to_land + SHIELD_DEPLOY_TIME

	#Decision Tree

	if evade:
		print(“Executing Evasion Route”)
		return execute_flight_path(evasion_route)

	elif total_landing_time < STORM_ETA:
		print(“Executing emergency landing”)
		execute_landing(landing_zone)
		wait_engine_shutdown()
		deploy_EDS()
		return enter_hibernation_mode()

	else:
		print(“Critical Failure: Cannot Evade or land in time.”)
		return execute_brace_protocol()
