import argparse
import json
import pathlib


def vending(inventory_file, transactions_file):
    """Takes Paths for 2 JSON files and generates the output file

    Args:
        inventory_file: Path to the inventory file
        transactions_file: Path to the transactions file

    Returns:
        List of dictionaries with the result of each transaction
    """
    # getting the two json files as python objects
    inventory, transactions = json_load(inventory_file, transactions_file)
    output_list = []
    for transaction in transactions:
        name = transaction['name']
        funds = transaction['funds']
        if name in inventory:
            #if the item is in inventory
            outcome, inventory = inInventory(name, funds, inventory)
            output_list.append(outcome)
        else:
            #if the item is not in the inventory
            output_list.append(notInInventory(funds))
    return output_list

def inInventory(name, funds, inventory):
    """Returns the outcome of one transaction event

    Args:
        name: Name of the item
        funds: Funds in the transaction
        inventory: Dictionary containing the list of items
    Returns:
        Outcome for one transaction
    """
    price = inventory[name]['price']
    outcome = {}
    if inventory[name]['quantity'] > 0:
        if sum(funds)/100 >= price:
            inventory[name]['quantity'] -= 1
            outcome['product_delivered'] = [True, 'Transaction Successful']
            outcome['change'] = calculateFunds(funds, price)
        else:
            outcome['product_delivered'] = [False, 'Insufficient Funds']
            outcome['change'] = funds
    else:
        outcome['product_delivered'] = [False, 'Item is out of Stock']
        outcome['change'] = funds
    return [outcome, inventory]


def notInInventory(funds):
    # If the item is not in the inventory
    outcome = {'product_delivered': [False, 'Item is not in the Inventory'], 'change': funds}
    return outcome

def calculateFunds(funds, price):
    """Returns the change in coins

    Args:
        funds: Funds given for the transaction
        price: Price of the item

    Returns:
        Change in terms of coins, available options for the coins are (10, 25, 50 ,100)
    """
    remaining = int(sum(funds) - price*100)
    hundred = remaining//100
    fifty = (remaining%100)//50
    twentyFive = (remaining%50)//25
    tens = (remaining%25)//10
    change = []
    if tens: change.extend([10 for i in range(tens)])
    if twentyFive: change.extend([25 for i in range(twentyFive)])
    if fifty: change.extend([50 for i in range(fifty)])
    if hundred: change.extend([100 for i in range(hundred)])
    return change



def json_load(path1, path2):
    # loads json files into python objects
    with open(path1) as f1:
        with open(path2) as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
    return [data1, data2]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('json1', help='specify the path to the inventory json file')
    parser.add_argument('json2', help='Specify the path to the transactions json file')
    args = parser.parse_args()

    inventory_file = pathlib.Path(args.json1)
    transactions_file = pathlib.Path(args.json2)

    if inventory_file.is_file() and transactions_file.is_file():
        result = vending(inventory_file, transactions_file)
    else:
        result = 'Please check if the file path for both json files is correct'
    output_path = inventory_file.parent / 'output.json'
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    with open(output_path) as f:
        f_contents = f.read(1024)
        while f_contents:
            print(f_contents, end='')
            f_contents = f.read(1024)