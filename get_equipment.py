import requests

from config import SERVER_ROACH

def get_server():
    return SERVER_ROACH

def get_equipment(id: int):
    url = f'http://{get_server()}/maint/frio/frio_equipment.php'
    params = dict(
        id=id
    )
    r = requests.get(url, params=params )
    #    if r.status_code == 404
    r.encoding = 'utf-8-sig'
    data = r.json() # Check the JSON Response Content documentation below
    eq = data[0]
    # id = eq["id"]
    # equipment = eq["equipment"]
    # parametr = eq["parametr"]
    # note = eq["note"]
    return eq

def get_room(id_room: int):
    url = f'http://{get_server()}/maint/frio/frio_equipment.php'
    params = dict(
        room=id_room
    )
    r = requests.get(url, params=params )
    #    if r.status_code == 404
    r.encoding = 'utf-8-sig'
    data = r.json() # Check the JSON Response Content documentation below
    # id = eq["id"]
    # equipment = eq["equipment"]
    return data

def get_listfiles(id: int):
    url = f'http://{get_server()}/maint/frio/frio_equipment_files.php'
    params = dict(
        id=id
    )
    r = requests.get(url, params=params)
    r.encoding = 'utf-8-sig'
    data = r.json() # Check the JSON Response Content documentation below
    if data != None : 
        return data
    return dict()

def get_file(id: int, number: int): #(filename, file)
    # todo: добавить сюда выкачку файла
    # with open(file, 'rb') as tmp:
    # obj = BytesIO(tmp.read())
    # obj.name = '1.txt'
    return (None, None)
    return ('filenamenotfound', '')

def main():
    eq = get_equipment(0)
    print(eq)

if __name__ == "__main__":
    main()