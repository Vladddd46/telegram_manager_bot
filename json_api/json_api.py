import json



def json_open(file_name):
    data = None
    with open(file_name, "r") as f:
        data = json.load(f)

    if type(data) != dict:
        print("Some error occured, while opening json file.")
    return data



def json_write(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=2)

        

