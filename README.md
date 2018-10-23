# Vending Machine Problem

Please add 2 arguments for the program to work, both should be paths to json files with extensions and in the expected format

Assumptions and Decisions I made for this program
* -h tag can be used with the file name to see how the arguments are used
* I chose both the arguments for path variables as positional arguments

* If the files are not at the given path then a message saying the same will be printed

* I have not made any checks to see if the content of json files is in the order expected

* In the output file for product delivered key I have added one more field which explains a little more about 
why the result is the way it is. There are 3 possibilities why a transaction can fail
1. Insufficient funds
2. Item is out of stock
3. Item is not in the inventory

I have accounted for all the possibilities