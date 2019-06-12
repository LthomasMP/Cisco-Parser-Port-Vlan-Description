#!/usr/bin/env python3

###################### WARNING #################################
#   You need at leat a show run command in your file. Without  #
#   the show run, the parsing won't work                        # 
################################################################

from ciscoconfparse import CiscoConfParse
import sys
import csv

class Port:

    name = "interface"
    mode = ""
    vlans = 0
    description = "Default"

    def __init__(self, name, mode, vlan, description):
        self.name = name
        self.mode = mode
        self.vlan = vlan
        self.description = description

    def find_mode(self, parse, conf_file):
        if parse.find_children_w_parents(r'%s' %self.name, r'switchport mode') != []:
            intf = parse.find_children_w_parents(r'%s' %self.name, r'switchport mode')[0]
            self.mode = intf.replace('switchport mode ','').replace(' ','')
        else:
            self.mode = "mode not found"

    def find_vlans(self, parse, conf_file):
        if self.mode == 'access':
            if parse.find_children_w_parents(r'%s' %self.name, r'authentication event server dead action authorize vlan') != []:
                intf = parse.find_children_w_parents(r'%s' %self.name, r'authentication event server dead action authorize vlan')[0]
                self.vlan = intf.replace('authentication event server dead action authorize vlan ', '').replace(' ', '')
            else:
                if parse.find_children_w_parents(r'%s' %self.name, r'switchport access vlan') != []:
                    intf = parse.find_children_w_parents(r'%s' %self.name, r'switchport access vlan')[0]
                    self.vlan = intf.replace('switchport access vlan ', '').replace(' ', '')
        else:
            self.vlan = 0

    def find_port_description(self, parse, conf_file):
        if parse.find_children_w_parents(r'%s' %self.name, r'description') != []:
            intf = parse.find_children_w_parents(r'%s' %self.name, r'description')[0]
            self.description = intf.replace('description ','')
        else:
            self.description = "Description not found"

def find_every_gigabit_ports(parse, Port_list, conf_file):
    intf = parse.find_objects(r'^interface GigabitEthernet')
    for i in range (len(intf)):
        Port_list.append(intf[i].text.replace('interface ', ''))

def find_every_ten_gigabit_ports(parse, Port_list, conf_file):
    intf = parse.find_objects(r'^interface TenGigabitEthernet')
    for i in range (len(intf)):
        Port_list.append(intf[i].text)

def find_every_fast_ports(parse, Port_list, conf_file):
    intf = parse.find_objects(r'^interface FastEthernet')
    for i in range (len(intf)):
        Port_list.append(intf[i].text)

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: ./parseur.py <your_file>")

    else :
        conf_file = sys.argv[1]
        parse = CiscoConfParse(conf_file, factory=True)
        Port_list = []
        find_every_gigabit_ports(parse, Port_list, conf_file)
        find_every_ten_gigabit_ports(parse, Port_list, conf_file)
        find_every_fast_ports(parse, Port_list, conf_file)
        
        for i in range(len(Port_list)):
            port = Port(Port_list[i], "", 0, "Default")
            port.find_port_description(parse, conf_file)
            port.find_mode(parse, conf_file)
            port.find_vlans(parse, conf_file)
            Port_list[i] = port

        # Clean the path to isolate just <name>.<extension>
        while conf_file.find('/') != -1:
            conf_file = conf_file[conf_file.find('/')+1:]
        
        print(len(Port_list), " port has been found")
        with open(conf_file[:conf_file.find('.')] + '-parsed.csv', 'w') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(['port','switchport', 'vlan', 'description'])
            for i in range(len(Port_list)):
                writer.writerow([Port_list[i].name, Port_list[i].mode, Port_list[i].vlan, Port_list[i].description])
                print(Port_list[i].name, " mode: ", Port_list[i].mode, " vlan: ", str(Port_list[i].vlan), " and description: ", Port_list[i].description) 
         
if __name__ == '__main__':
    main()

