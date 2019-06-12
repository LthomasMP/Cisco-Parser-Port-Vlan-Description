#!/usr/bin/env python3

###################### WARNING #################################
#   You need at leat a show run command in your file. Without  #
#   the show run, the parsing won't work                        # 
################################################################

from ciscoconfparse import CiscoConfParse

conf_file = ''

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
        try:
            intf = parse.find_children_w_parents(r'%s' %self.name, r'switchport mode')[0]
            self.mode = intf.replace('switchport mode ','').replace(' ','')
        except:
            self.mode = "mode not found"

    def find_vlans(self, parse, conf_file):
        if self.mode == 'access':
            try:
                intf = parse.find_children_w_parents(r'%s' %self.name, r'authentication event server dead action authorize vlan')[0]
                self.vlan = intf.replace('authentication event server dead action authorize vlan ', '').replace(' ', '')
            except:
                self.vlan = 0
        else:
            self.vlan = 0

    def find_port_description(self, parse, conf_file):
        try:
            intf = parse.find_children_w_parents(r'%s' %self.name, r'description')[0]
            self.description = intf.replace('description ','')
        except:
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
    
    print(len(Port_list), " port has been found")
    for i in range(len(Port_list)):
        print(Port_list[i].name, " mode: ", Port_list[i].mode, " vlan: ", str(Port_list[i].vlan), " and description: ", Port_list[i].description) 

         
if __name__ == '__main__':
    main()

