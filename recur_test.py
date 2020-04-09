array = []

def recur(arr: dict, key_orignal):
    
    arr = []
    for key, value in arr.items():
        if key == 'args' or key == 'result':
            arr.append([key_orignal][key])
        else:
            recur(value, key)
