

with open('id_data.txt', 'r') as f:
    data = f.readlines()

my_dict = {}

for line in data:
    line_info = line.strip().replace("\t", " ").split(" ")
    print("len=",len(line_info))
    id = line_info[0]
    
    data_length = len(line_info)

    if 4 < data_length < 8 :
        name = line_info[1] + " " + line_info[2]
    elif data_length == 8:
        name = line_info[1] + " " + line_info[2] + " " + line_info[3]
    else: 
        name = line_info[1]

    print(f"ID: {id}, Name: {name}")

    my_dict[name] = id

print(my_dict)