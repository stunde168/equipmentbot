import requests

def get_equipment(id: int):
    url='http://roach/maint/frio/frio_equipment.php'
    params = dict(
        history=id
    )
    r = requests.get(url, params=params )
    r.encoding = 'utf-8-sig'
    data = r.json() # Check the JSON Response Content documentation below
    eq = data[0]
    # id = eq["id"]
    # equipment = eq["equipment"]
    # parametr = eq["parametr"]
    # note = eq["note"]
    return eq

def main():
    eq = get_equipment(0)
    print(eq)

if __name__ == "__main__":
    main()