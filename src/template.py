import os
import re
import json

class BoTemplate:
    def __init__(self, name):
        self.name = name
        self.template = None
        self.components = []
        self.path = os.path.join('template', self.name)
    
    # return the template in utf-8
    def get(self):
        return self.template.encode('utf-8')

    # fetch the template
    def parse(self):
        try:
            with open(self.path, 'r') as file:
                self.template = file.read()
        except FileNotFoundError:
            print('Template not found')
            return

        self.parse_config('tabledata')

    # store components and their id
    def parse_config(self, component):
        component_matches = re.findall(f'<{component}(.*?)>', self.template)
        if component_matches:
            for config in component_matches:
                component_id = re.search(r'ID="(.*?)"', config.strip())
                if component_id:
                    self.components.append([component_id.group(1), component, 0])

    # convert the <tags> to real html elements
    def disassemble_component(self, component_id, component, data):
        if component == 'tabledata':
            temp_table_data = ''
            for i in data:
                temp_table_data += '<tr>'
                for key, value in i.items():
                    temp_table_data += f'<td>{value}</td>'
                temp_table_data += '</tr>'
            self.template = re.sub(f'<tabledata ID="{component_id}">', temp_table_data, self.template, flags=re.DOTALL)

    # add json data to the corresponding component
    # this could be managed better if I created a structure for the componentdata
    # data = [['ID', [{}]]]
    def add_data(self, data):
        for target in data:
            target_id = target[0]
            target_data = target[1]

            for component in self.components:
                if target_id in component[0]:
                    self.disassemble_component(target_id, component[1], target_data)
