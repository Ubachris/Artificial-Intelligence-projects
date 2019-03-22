from operator import itemgetter, attrgetter, methodcaller

max_landing_runways= 0
max_num_gates= 0
max_takeoff_runways= 0
list_of_planes= []
num_planes= 0

class Planes:

	def __init__ (self, remaining_fuel, mins_to_gate, service_time, mins_for_takeoff, mins_before_complaint, index):
		self.remaining_fuel= remaining_fuel
		self.mins_to_gate= mins_to_gate
		self.service_time= service_time
		self.mins_for_takeoff= mins_for_takeoff
		self.mins_before_complaint= mins_before_complaint
		self.index= index
		self.plane_landing= 0
		self.plane_takeoff= 0

	# Landing time is set, and is between 0 and the remaining fuel the plane has
	def set_plane_landing(self, land_time):
		self.plane_landing= land_time

	def get_plane_landing_end(self):
		return self.plane_landing + self.mins_to_gate

	# Takeoff time is set and is between the range of service time, to the minutes before the customers complain
	def set_plane_takeoff(self, takeoff_time):
		self.plane_takeoff= takeoff_time

	def get_plane_takeoff_start(self):
		return self.plane_landing+ self.mins_to_gate+ self.service_time+ self.plane_takeoff

	def get_plane_takeoff_end(self):
		return self.plane_takeoff + self.mins_for_takeoff


	def toString(self):
		return " Initial index: " + str(self.index)+ " R: "+ str(self.remaining_fuel)+ " M: "+ str(self.mins_to_gate) + " S: "+ str(self.service_time) \
		 		+ " O: "+ str(self.mins_for_takeoff) +" C: "+ str(self.mins_before_complaint)+ " land time: "+\
		 		 str(self.plane_landing) +" takeoff time: " + str(self.plane_takeoff)


def print_sorted_list_of_planes(list_of_planes):
	count= 1
	if list_of_planes is not None:
		for plane in list_of_planes:
			print "Plane "+ str(count) + " => " +plane.toString() 
			count+=1

def print_unsorted_list_of_planes(list_of_planes):
	count= 1
	if list_of_planes is not None:
		list_of_planes.sort(key=lambda plane: plane.index, reverse= False)
		for plane in list_of_planes:
			print "Plane "+ str(count) + " => " +plane.toString() 
			count+=1

def print_land_and_takeoff_times(list_of_planes):
	if list_of_planes is not None:
		list_of_planes.sort(key=lambda plane: plane.index, reverse= False)
		for plane in list_of_planes:
			print str(plane.plane_landing)+ " " + str(plane.plane_takeoff)


	'''print "Initial List of planes in sorted order:"
	print_list_of_planes(list_of_planes)'''  
	#print "\n" 

def find_earliest_land_time(current_list, current_failed_land_time):
	ending_land_time= []

	if current_list:
		for element in current_list:
			end_land_time= element.plane_landing + element.mins_to_gate
			if end_land_time > current_failed_land_time:
				ending_land_time.append(end_land_time)

		#print "list of the end of the plane landing times: " + str(ending_land_time)
		time= min(ending_land_time)
		return time 

def find_earliest_gate_time(current_list, current_failed_gate_time, landing):
	print "Cureent plane landing: "+ str(landing)
	start_gate_time= []

	if current_list:
		for element in current_list:
			gate_end= element.plane_takeoff
			print "This is the gate end time: " + str(gate_end)
			print "This is our current gate time: "+ str(current_failed_gate_time)
			if gate_end > current_failed_gate_time:
				start_gate_time.append(gate_end)

		print "list of the end of the plane gate times: " + str(start_gate_time)
		time= min(start_gate_time)
		return time 
 
def isSafe(land, M, takeoff, O, plane_list):
	L=0
	G=0
	T=0	
	list_of_landing_ranges= []
	list_of_gate_ranges= []
	list_of_takeoff_ranges= []
	list_of_landing_ranges.extend([[land, 1], [land+M, 0]])
	list_of_gate_ranges.extend([[land+M, 1], [takeoff, 0]])
	list_of_takeoff_ranges.extend([[takeoff,1], [takeoff+O, 0]])

	#print "checking new land time: " + str(land) +" for plane number: " + str(len(plane_list)+1)
	#print "checking new takeoff time: " + str(takeoff) +" for plane number: " + str(len(plane_list)+1) + "\n" 

	for plane in plane_list:
		land_time_start= [plane.plane_landing, 1]
		land_time_end= [plane.get_plane_landing_end(), 0]
		gate_time_start= [plane.get_plane_landing_end(), 1] 
		gate_time_end= [plane.plane_takeoff, 0]
		takeoff_start= [plane.plane_takeoff, 1]
		takeoff_end= [plane.get_plane_takeoff_end(), 0]

		list_of_landing_ranges.extend([land_time_start, land_time_end])
		list_of_gate_ranges.extend([gate_time_start, gate_time_end])
		list_of_takeoff_ranges.extend([takeoff_start, takeoff_end])

	#list_of_planes.sort(key=lambda plane: plane.index, reverse= False)

	list_of_landing_ranges.sort(key= lambda value: (value[0], value[1]))
	list_of_gate_ranges.sort(key= lambda value: (value[0], value[1]))
	list_of_takeoff_ranges.sort(key= lambda value: (value[0], value[1]))


	for index in range(len(list_of_landing_ranges)):

		if(list_of_landing_ranges[index][1] == 1 ):
			L+=1
			if(L> max_landing_runways):
				return (False,1)
		else:
			L-=1

		if(list_of_gate_ranges[index][1] == 1 ):
			G+=1
			if(G> max_num_gates):
				return (False,2)
		else:
			G-=1

		if(list_of_takeoff_ranges[index][1] == 1 ):
			T+=1
			if(T> max_takeoff_runways):
				return (False,3)
		else:
			T-=1


	return (True,-1)


def schedulePlanes(planes_to_schedule):
	final_result= []
	total_num_planes= num_planes
	
	has_solution= schedulePlanesUtil(0, final_result, num_planes)

	if(has_solution):
		return final_result


def schedulePlanesUtil(n, result, number_of_planes):
	if n== num_planes:
		#print "Have successfully found a schedule for all the planes "
		return True

	'''print "One Level deeper in the recursion"
	print "current plane index: "+ str(n)'''
	#print "current plane number: "+ str(n+1) +"\n"
	plane= list_of_planes[n]
	remaining_fuel= plane.remaining_fuel
	service_time= plane.service_time
	complain_time= plane.mins_before_complaint
	mins_to_gate= plane.mins_to_gate
	takeooff_duration= plane.mins_for_takeoff
	landing_time= 0
	takeoff_range= 0 
	 

	while takeoff_range < complain_time - service_time +1:
		'''print "landing time: " + str(landing_time)
		print "mins to gate: " + str(mins_to_gate)
		print "number of mins for service: " + str(plane.service_time)
		print "number of mins before complaint: " + str(plane.mins_before_complaint)
		print "end of service time: " + str(end_of_service_time)'''
		#print "start of complaint time: " + str(start_of_complaint_time) + "\n"

		landing_time= 0
		while  landing_time < remaining_fuel+1:
			takeoff_time= landing_time+ mins_to_gate + service_time + takeoff_range

			#print "entered the for loop"  #DEBUG- Checking to see if recursion is working
			
			is_safe_res = isSafe(landing_time, mins_to_gate, takeoff_time, takeooff_duration ,result)
			if(is_safe_res[0]):
				plane.set_plane_landing(landing_time)
				plane.set_plane_takeoff(takeoff_time)

				'''print "Setting values for plane number: " + str(n)
				print "plane landing set:" + str(plane.plane_landing)    #DEBUG- Checking to see if the land time is set correctly
				print "plane takeoff set:" + str(plane.plane_takeoff)	 #DEBUG- Checking to see if the tekeoff time is set'''
				result.append(plane)
				#print_sorted_list_of_planes(result)
				#print "\n"

				#print "Before going a level deeper, current number of planes n: " + str(n+1)
				#print "Total number of planes: " +str(num_planes) +""

				if(schedulePlanesUtil(n+1, result, num_planes)):
					return True 
				else:
					del result[-1]



					#print "<-------------------------------------Back from recursion----------------------------------------->\n "
		
			else:
				if is_safe_res[1] == 1:
					new_time_iteration= find_earliest_land_time(result, landing_time)

					if new_time_iteration <= plane.remaining_fuel:
						landing_time= new_time_iteration
						continue
				
					#print "setting new land time to: " +str(landing_time)+ "\n"

					else:	
						return False 

				elif is_safe_res[1] == 2:
					new_time_iteration= find_earliest_gate_time(result, plane.get_plane_landing_end(), plane.plane_landing)
					print "current landing time: " + str(landing_time)
					value= new_time_iteration- plane.mins_to_gate

					if value <= plane.remaining_fuel and value > 0 :
						landing_time= new_time_iteration - plane.mins_to_gate
						print "setting new land time to: " +str(landing_time)+ "\n"
						continue
					

					else:
						return False 

			landing_time += 1
		takeoff_range+= 1
			
	return False


with open("input3.txt", 'r') as file:
	constraints= file.readline()
	list_of_constraints= constraints.split()
	list_of_constraints= map(int, list_of_constraints)
	max_landing_runways= list_of_constraints[0]
	max_num_gates= list_of_constraints[1]
	max_takeoff_runways= list_of_constraints[2]

	num_planes= int(file.readline())
	i=0

	for plane in range(int(num_planes)):
		plane_info= file.readline().split()
		plane_info= map(int, plane_info)
		plane = Planes(plane_info[0], plane_info[1], plane_info[2], plane_info[3], plane_info[4], i)
		list_of_planes.append(plane)
		i+=1

	list_of_planes.sort(key=lambda plane: plane.remaining_fuel)

land_and_takeoff_times= schedulePlanes(list_of_planes)
#print_unsorted_list_of_planes(land_and_takeoff_times) 


with open("output.txt", "w") as output_file:
	land_and_takeoff_times.sort(key=lambda plane: plane.index, reverse= False)
	for plane in land_and_takeoff_times:
		output_file.write(str(plane.plane_landing)+ " " + str(plane.plane_takeoff) + "\n")


			











