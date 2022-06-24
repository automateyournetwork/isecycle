import sys
import os
import json
import requests
import rich_click as click
import yaml
import xmltodict
import urllib3
import cairosvg
import networkx as nx
import pandas as pd
from pathlib import Path
from rich import print_json
from jinja2 import Environment, FileSystemLoader
from gtts import gTTS
from rich.console import Console
from rich.table import Table
from pyvis.network import Network

urllib3.disable_warnings()

##
# Main Class - Isecycle
# Takes URL, Username, Password, API
##

class Isecycle():
    def __init__(self,
                url,
                username,
                password,
                api,
                filetype):
        self.url = url
        self.username = username
        self.password = password
        self.api = api
        self.filetype = filetype

    def isecycle(self):
        parsed_json = json.dumps(self.capture_state(), indent=4, sort_keys=True)
        if self.filetype != "none":
            self.pick_filetype(parsed_json)
            if self.filetype != "svg":
                print_json(parsed_json)
        else:
            print_json(parsed_json)

    def capture_state(self):
        if self.api == "version":
            url = f"{ self.url }/admin/API/mnt/Version"
            version = requests.request("GET", url, auth=(self.username, self.password), verify=False)
            xmlParse = xmltodict.parse(version.text)
            parsed_json = json.loads(json.dumps(xmlParse))
            return(parsed_json)
        else: 
            click.secho(f"{ self.api } is not a supported API. Please check the READ ME")

    def pick_filetype(self, parsed_json):
        if self.filetype == "none":
            pass
        elif self.filetype == "json":
            self.json_file(parsed_json)
        elif self.filetype == "yaml":
            self.yaml_file(parsed_json)
        elif self.filetype == "csv":
            self.csv_file(parsed_json)
        elif self.filetype == "markdown":
            self.markdown_file(parsed_json)
        elif self.filetype == "html":
            self.html_file(parsed_json)
        elif self.filetype == "mindmap":
            self.mindmap_file(parsed_json)
        elif self.filetype == "mp3":
            self.mp3_file(parsed_json)
        elif self.filetype == "svg":
            self.svg_file(parsed_json)
        elif self.filetype == "png":
            self.png_file(parsed_json)
        elif self.filetype == "flowchart":
            self.flowchart_file(parsed_json)
        elif self.filetype == "class":
            self.class_file(parsed_json)
        elif self.filetype == "relationship":
            self.relationship_file(parsed_json)
        elif self.filetype == "state":
            self.state_file(parsed_json)
        elif self.filetype == "graph":
            self.graph_file(parsed_json)

    def json_file(self, parsed_json):
        with open(f'{ self.api }.json', 'w' ) as f:
            f.write(parsed_json)
        click.secho(f'JSON file created at { sys.path[0] }/{ self.api }.json',
        fg='green')

    def yaml_file(self, parsed_json):
        clean_yaml = yaml.dump(json.loads(parsed_json), default_flow_style=False)
        with open(f'{ self.api }.yaml', 'w' ) as f:
            f.write(clean_yaml)
        click.secho(f'YAML file created at { sys.path[0] }/{ self.api }.yaml',
        fg='green')

    def csv_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        csv_template = env.get_template('ISE_csv.j2')
        csv_output = csv_template.render(api = self.api,
                                         data_to_template = json.loads(parsed_json))
        with open(f'{ self.api }.csv', 'w' ) as f:
            f.write(csv_output)
        click.secho(f'CSV file created at { sys.path[0] }/{ self.api }.csv',
        fg='green')

    def markdown_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        markdown_template = env.get_template('ISE_md.j2')
        markdown_output = markdown_template.render(api = self.api,
                                         data_to_template = json.loads(parsed_json))
        with open(f'{ self.api }.md', 'w' ) as f:
            f.write(markdown_output)
        click.secho(f'Markdown file created at { sys.path[0] }/{ self.api }.md',
        fg='green')

    def html_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        html_template = env.get_template('ISE_html.j2')
        html_output = html_template.render(api = self.api,
                                         data_to_template = json.loads(parsed_json))
        with open(f'{ self.api }.html', 'w' ) as f:
            f.write(html_output)
        click.secho(f'HTML Datatable file created at { sys.path[0] }/{ self.api }.html',
        fg='green')

    def mindmap_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        mindmap_template = env.get_template('ISE_mindmap.j2')
        mindmap_output = mindmap_template.render(api = self.api,
                                         data_to_template = json.loads(parsed_json))
        with open(f'{ self.api } Mindmap.md', 'w' ) as f:
            f.write(mindmap_output)
        click.secho(f'Mindmap file created at { sys.path[0] }/{ self.api } Mindmap.md',
        fg='green')

    def mp3_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        mp3_template = env.get_template('ISE_mp3.j2')
        mp3_output = mp3_template.render(api = self.api,
                                         data_to_template = json.loads(parsed_json))
        language = "en-US"
        mp3 = gTTS(text = mp3_output, lang=language)
        mp3.save(f'{ self.api }.mp3')
        click.secho(f'MP3 file created at { sys.path[0] }/{ self.api }.mp3',
        fg='green')

    def svg_file(self, parsed_json):
        console = Console(record=True)
        if self.api == "version":
            dict_json = json.loads(parsed_json)
            print(dict_json)
            table = Table(title=f"ISE MnT {self.api} API")
            table.add_column("Product Name", style="bold blue", justify="center")
            table.add_column("Type of Node", style="bold green", justify="center")
            table.add_column("Version", style="bold green", justify="center")
            table.add_row(f"{ dict_json['product']['@name'] }",f"{ dict_json['product']['type_of_node'] }",f"{ dict_json['product']['version'] }")
            console.print(table, justify="center")
            console.save_svg(f"{self.api}.svg",
                             title=f"ISE MnT {self.api} API")
            click.secho(f'SVG file created at { sys.path[0] }/{ self.api }.svg',
                fg='green')

    def png_file(self, parsed_json):
        self.svg_file(parsed_json)
        cairosvg.svg2png(
            url=f"{self.api}.svg", write_to=f"{self.api}.png")
        click.secho(f'PNG file created at { sys.path[0] }/{ self.api }.png',
        fg='green')

    def flowchart_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        flowchart_template = env.get_template('ISE_mermaid_flowchart.j2')
        flowchart_output = flowchart_template.render(api = self.api,
                                         data_to_template = json.loads(parsed_json))
        with open(f'{ self.api } Flowchart.md', 'w' ) as f:
            f.write(flowchart_output)
        click.secho(f'Mermaid Flowchart file created at { sys.path[0] }/{ self.api } Flowchart.md',
        fg='green')

    def class_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        class_template = env.get_template('ISE_mermaid_class.j2')
        class_output = class_template.render(api = self.api,
                                         data_to_template = json.loads(parsed_json))
        with open(f'{ self.api } Class.md', 'w' ) as f:
            f.write(class_output)
        click.secho(f'Mermaid Class file created at { sys.path[0] }/{ self.api } Class.md',
        fg='green')

    def relationship_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        relationship_template = env.get_template('ISE_mermaid_relationship.j2')
        relationship_output = relationship_template.render(api = self.api,
                                         data_to_template = json.loads(parsed_json))
        with open(f'{ self.api } Relationship.md', 'w' ) as f:
            f.write(relationship_output)
        click.secho(f'Mermaid Relationship file created at { sys.path[0] }/{ self.api } Relationship.md',
        fg='green')

    def state_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        state_template = env.get_template('ISE_mermaid_state.j2')
        state_output = state_template.render(api = self.api,
                                         data_to_template = json.loads(parsed_json))
        with open(f'{ self.api } State.md', 'w' ) as f:
            f.write(state_output)
        click.secho(f'Mermaid State file created at { sys.path[0] }/{ self.api } State.md',
        fg='green')

    def graph_file(self, parsed_json):
        self.graph_csv_file(parsed_json)
        df = pd.read_csv(f'{self.api}_graph.csv')
        G = nx.from_pandas_edgelist(df,source='Source',target="Target",edge_attr=True)
        net = Network(notebook=True, width=1500, height=1000)
        net.show_buttons(True)
        net.from_nx(G)
        net.show(f'{self.api} graph.html')
        os.remove(f'{self.api}_graph.csv')
        click.secho(
            f"Network Graph file created at { sys.path[0] }/{self.api} graph.html",
            fg='green')

    def graph_csv_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        graph_csv_template = env.get_template('ISE_graph_csv.j2')
        graph_csv_output = graph_csv_template.render(api = self.api,
            data_to_template=json.loads(parsed_json),)
        with open(f'{self.api}_graph.csv', 'w') as f:
            f.write(graph_csv_output)         
        return
        
@click.command()
@click.option('--url',
    prompt="ISE URL",
    help="Cisco Identity Services Engine URL",
    required=True,envvar="URL")
@click.option('--username',
    prompt="ISE Username",
    help="Cisco Identity Services Engine Username",
    required=True,envvar="USERNAME")
@click.option('--password',
    prompt="ISE Password",
    help="Cisco Identity Services Engine Password",
    required=True,envvar="PASSWORD",hide_input=True)
@click.option('--api',
    prompt="ISE API",
    help="For a list of API shortcodes check the README",
    required=True)
@click.option('--filetype',
    prompt="Filetype",
    help="For a list of filetypes check the README",
    required=True,default='none',
    type=click.Choice(['none',
                        'json',
                        'yaml',
                        'csv',
                        'html',
                        'markdown',
                        'mindmap',
                        'mp3',
                        'svg',
                        'png',
                        'flowchart',
                        'class',
                        'relationship',
                        'state',
                        'graph',
                        'all']))

def cli(url,
        username,
        password,
        api,
        filetype
    ):
    invoke_class = Isecycle(url,
                            username,
                            password,
                            api,
                            filetype
                            )
    invoke_class.isecycle()

if __name__ == "__main__":
    cli()
