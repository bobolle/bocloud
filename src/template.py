import os
import re

class BoTemplate:
    def __init__(self, name):
        self.name = name
        self.template = None
        self.components = []
    
    def get(self):
        path = os.path.join('template', self.name)

        try:
            with open(path, 'r') as file:
                self.template = file.read()
        except FileNotFoundError:
            print('Template not found')
            return

        self.parse_config('tabledata')
        self.disassemble_component('tabledata')

        return self.template.encode('utf-8')

    def parse_config(self, component):
        component_matches = re.findall(f'<{component}(.*?)>', self.template)
        if component_matches:
            for config in component_matches:
                component_id = re.search(r'ID="(.*?)"', config.strip())
                if component_id:
                    self.components.append([component, component_id.group(1)])

    def disassemble_component(self, component):
        if component == 'tabledata':
            re.sub(r'<tabledata(.*?)>', '<tr><td>test</td></tr>', self.template)
