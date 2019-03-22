f=open("input3.txt", "r")
input_f = f.readlines()
line_number = 0
lax_params = []
planes_number = None
planes_dict = {} ## key is #plane and value is list of [int(R),int(M),int(S),int(O),int(C)]

for single_line in input_f:
    if line_number == 0:
        line_number += 1
        lax_params.append(int(single_line.split()[0]))
        lax_params.append(int(single_line.split()[1]))
        lax_params.append(int(single_line.split()[2]))
    elif line_number == 1:
        line_number += 1
        planes_number = int(single_line.strip())
    else:
        R = single_line.split()[0]
        M = single_line.split()[1]
        S = single_line.split()[2]
        O = single_line.split()[3]
        C = single_line.split()[4]
        planes_dict[line_number-1] = [int(R),int(M),int(S),int(O),int(C)]
        line_number += 1
        
        
f2=open("output.txt", "r")
output_f = f2.readlines()
ranges = []
plane_number = 1
for single_line in output_f:
    R = planes_dict[plane_number][0]
    M = planes_dict[plane_number][1]
    S = planes_dict[plane_number][2]
    O = planes_dict[plane_number][3]
    C = planes_dict[plane_number][4]
    landing = int(single_line.split()[0])
    takeoff = int(single_line.split()[1])
    landing_range = [(landing,"s"),(landing+M,"e")]
    gate_range = [(landing+M,"s"),(takeoff,"e")]
    takeoff_range = [(takeoff,"s"),(takeoff+O,"e")]
    curr_assignment = [landing_range,gate_range,takeoff_range,plane_number]
    ranges.append(curr_assignment)
    plane_number += 1
    
 

print("Landing:")
res = True
temp_plane_assignments = [] ## list of tuples
for single_assignment in ranges:
    curr_end = single_assignment[0][1]
    curr_start = single_assignment[0][0]
    temp_plane_assignments.append(curr_start)
    temp_plane_assignments.append(curr_end)
sorted_plane_assignments = sorted(temp_plane_assignments, key=lambda x: (x[0], x[1]))
#print(sorted_plane_assignments)
curr_planes_number = 0
for t_index in range(len(sorted_plane_assignments)):
    t = sorted_plane_assignments[t_index]
    if t[1] == "s":
        curr_planes_number += 1
        if curr_planes_number > lax_params[0]:
            res = False
            print("Error at:" + str(t[0]))
            break
    elif t[1] == "e":
        curr_planes_number -= 1
  
print(res)

res = True
temp_plane_assignments = []
print("At the Gate:")    
for single_assignment in ranges:
    curr_end = single_assignment[1][1]
    curr_start = single_assignment[1][0]
    temp_plane_assignments.append(curr_start)
    temp_plane_assignments.append(curr_end)
sorted_plane_assignments = sorted(temp_plane_assignments, key=lambda x: (x[0], x[1]))
    #print(sorted_plane_assignments)
curr_planes_number = 0
for t_index in range(len(sorted_plane_assignments)):
    t = sorted_plane_assignments[t_index]
    if t[1] == "s":
        curr_planes_number += 1
        if curr_planes_number > lax_params[1]:
            res = False
    elif t[1] == "e":
        curr_planes_number -= 1
   
print(res)

res = True
temp_plane_assignments = []
print("Taking Off:")    
for single_assignment in ranges:
    curr_end = single_assignment[2][1]
    curr_start = single_assignment[2][0]
    temp_plane_assignments.append(curr_start)
    temp_plane_assignments.append(curr_end)
sorted_plane_assignments = sorted(temp_plane_assignments, key=lambda x: (x[0], x[1]))
#print(sorted_plane_assignments)
curr_planes_number = 0
for t_index in range(len(sorted_plane_assignments)):
    t = sorted_plane_assignments[t_index]
    if t[1] == "s":
        curr_planes_number += 1
        if curr_planes_number > lax_params[2]:
            res = False
    elif t[1] == "e":
        curr_planes_number -= 1
  
print(res)
    
