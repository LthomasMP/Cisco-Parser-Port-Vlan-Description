# Cisco Parser Port-Vlan-Description
Tiny script that finds VLAN and description for each port with a Cisco equipment's show run

## Requirements ##
This script uses the CiscoConfParse lib, be carrefull of installing it before running the script.

## Use ##
Just run the script with your files in argument of the command. The script will create a csv file with name, switchport mode, vlan and description. 

``` console
$ ./parser.py <your_file_1.log> ... <your_file_n.log>
```

I tried the program with .log files, but it will work for every text file, I think (I hope).

## Lacks ##
When a port is in trunk mode, my client didn't want to know allowed vlan, that's why vlan ID is set to 0 when it is a trunk port. I will improve it later if I need it.
