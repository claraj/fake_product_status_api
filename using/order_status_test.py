import requests 
import os 

base_url = 'https://mock-plant-store.uc.r.appspot.com/'
def order_lookup(order_number):
    print()
    print('********** Test order lookup **********')

    # URLs are strings
    url = f'{base_url}/orders/status/{order_number}'

    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
    elif response.status_code == 400:
        error_response = response.json()
        print(error_response)
    else:
        print('error', response)
        return

    error = response.get('error')
    status = response.get('status')

    if error:
        print(error)
    elif status:
        print(f'Order status = {status} ')
        for item in response['items']:
            print(item)
    else: 
        print('Unknown response')

    print()


# Example search by name 

def name_search(name):
    print()
    print('********** Test name search **********')
    url = f'{base_url}/search/name?name={name}'
    response = requests.get(url)

    if response.status_code == 200:
        # print(response)
        plants = response.json()
        for p in plants:
            print(p.get('name'))


    elif response.status_code == 400:
        print('Error, bad response')
        print(response.json())

    else:
        print('Error', response)

    print()


def general_search(min_price, max_price, care_level):
    print()
    print('************* Test general search *************')
    
    url = f'{base_url}/search/search'
    params = {'min_price': min_price, 'max_price': max_price, 'care_level': care_level}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        plants = response.json()
        for p in plants:
            print(p.get('name'))


    elif response.status_code == 400:
        print('Error, bad response')
        print(response.json())

    else:
        print('Error', response)

    print()



# order_number = input('Enter your order number: ')
order_number = '1234567890'
order_lookup(order_number)

name = 'palm'
name_search(name)

min_price = 9.99
max_price = 20.00
care = 'easy'
general_search(min_price, max_price, care)

