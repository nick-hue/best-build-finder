
with open("id_data.txt", "r") as f:
    data = f.readlines()

my_dict = {}

for item in data:
    info = item.split(" ")
    # print(info)
    if len(info) > 5:
        _, current_id, _, name, name2, _ = item.split(" ")
        final_name = name.replace('"', "").replace(";","") + " " + name2.replace('"', "").replace(";","")

    else:
        _, current_id, _, name, _ = item.split(" ")
        final_name = name.replace('"', "").replace(";","")

    final_id = current_id.replace(":", "")

    #print(f"ID: {final_id:>4}| Name: {final_name}")

    my_dict[final_name] = final_id

myKeys = list(my_dict.keys())
myKeys.sort()
sorted_dict = {i: my_dict[i] for i in myKeys}

print(sorted_dict)