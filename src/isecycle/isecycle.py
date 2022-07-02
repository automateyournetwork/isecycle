import sys
import os
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
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
                filetype,
                room,
                token,):
        self.url = url
        self.username = username
        self.password = password
        self.api = api
        self.filetype = filetype
        self.room = room
        self.token = token

    def isecycle(self):
        parsed_json = json.dumps(self.capture_state(), indent=4, sort_keys=True)
        if self.filetype != "none":
            self.pick_filetype(parsed_json)
            if self.filetype != "svg":
                print_json(parsed_json)
        else:
            print_json(parsed_json)
        if self.room != "none":
            self.chatbot(parsed_json)

    def set_urlPath(self):
        if self.api == "version":
            api_path = f"{ self.url }/admin/API/mnt/Version"
        elif self.api == "node":
            api_path = f"{ self.url }/ers/config/node"
        elif self.api == "policy-set":
            api_path = f"{ self.url }/api/v1/policy/network-access/policy-set"            
        else:
            click.secho(f"{ self.api } is not a supported API. Please check the READ ME",
            fg='red')
        return(api_path)

    def capture_state(self):
            self.api_path = self.set_urlPath()
            click.secho(f"The following URL was used for this request { self.api_path }",
            fg='green')
            if "mnt" in self.api_path:
                api_data = requests.request("GET", self.api_path, auth=(self.username, self.password), verify=False)                
                xmlParse = xmltodict.parse(api_data.text)
                parsed_json = json.loads(json.dumps(xmlParse))
            elif "ers" in self.api_path:
                headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                }                
                api_data = requests.request("GET", self.api_path, headers=headers, auth=(self.username, self.password), verify=False)                
                all_json = api_data.json()
                parsed_json = all_json['SearchResult']['resources']
            else:
                headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                }                
                api_data = requests.request("GET", self.api_path, headers=headers, auth=(self.username, self.password), verify=False)                
                all_json = api_data.json()
                parsed_json = all_json['response']
            return(parsed_json)

    def pick_filetype(self, parsed_json):
        if self.filetype == "none":
            pass
        elif self.filetype == "json":
            self.json_file(parsed_json)
        elif self.filetype == "yaml":
            self.yaml_file(parsed_json)
        elif self.filetype == "text":
            self.text_file(parsed_json)            
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
        elif self.filetype == "all":
            self.all_files(parsed_json)

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

    def text_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        text_template = env.get_template('ISE_text.j2')
        text_output = text_template.render(api = self.api,
                                         data_to_template = json.loads(parsed_json))
        with open(f'{ self.api }.txt', 'w' ) as f:
            f.write(text_output)
        click.secho(f'Text file created at { sys.path[0] }/{ self.api }.txt',
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
        language = "en-US"
        if "mnt" in self.api_path:
            mp3_output = mp3_template.render(api = self.api,
                                             data_to_template = json.loads(parsed_json))
            mp3 = gTTS(text = mp3_output, lang=language)
            mp3.save(f'{ self.api }.mp3')
            click.secho(f'MP3 file created at { sys.path[0] }/{ self.api }.mp3',
                fg='green')
        else:
            dict_json = json.loads(parsed_json)
            for result in dict_json:
                print(result)
                mp3_output = mp3_template.render(api = self.api,
                        data_to_template=result
                        )
                mp3 = gTTS(text = mp3_output, lang=language)
                # Save MP3
                mp3.save(f'{self.api} {result["name"]} MP3.mp3')
                click.secho(f'MP3 file created at { sys.path[0] }/{ self.api } {result["id"]}.mp3',
                    fg='green')

    def svg_file(self, parsed_json):
        console = Console(record=True)
        if self.api == "node":
            dict_json = json.loads(parsed_json)
            print(dict_json)
            table = Table(title=f"ISE ERS {self.api} API")
            table.add_column("Node Name", style="bold blue", justify="center")
            table.add_column("Node ID", style="bold green", justify="center")
            table.add_column("URL", style="bold green", justify="center")
            for node in dict_json:
                table.add_row(f"{ node['name'] }",f"{ node['id'] }",f"{ node['link']['href'] }")
            console.print(table, justify="center")
            console.save_svg(f"{self.api}.svg",
                             title=f"ISE ERS {self.api} API")
            click.secho(f'SVG file created at { sys.path[0] }/{ self.api }.svg',
                fg='green')

        if self.api == "policy-set":
            dict_json = json.loads(parsed_json)
            print(dict_json)
            table = Table(title=f"ISE OpenAPI {self.api} API")
            table.add_column("Name", style="bold blue", justify="center")
            table.add_column("Serice Name", style="bold green", justify="center")
            table.add_column("Description", style="bold green", justify="center")
            table.add_column("ID", style="bold green", justify="center")
            table.add_column("State", style="bold green", justify="center")
            table.add_column("Condition", style="bold green", justify="center")
            table.add_column("Default", style="bold green", justify="center")
            table.add_column("Hits", style="bold green", justify="center")
            table.add_column("Rank", style="bold green", justify="center")
            table.add_column("Is Proxy", style="bold green", justify="center")
            table.add_column("URL", style="bold green", justify="center")
            for policy in dict_json:
                table.add_row(f"{ policy['name'] }",f"{ policy['serviceName'] }",f"{ policy['description'] }",f"{ policy['id'] }",f"{ policy['state'] }",f"{ policy['condition'] }",f"{ policy['default'] }",f"{ policy['hitCounts'] }",f"{ policy['rank'] }",f"{ policy['isProxy'] }",f"{ policy['link']['href'] }")
            console.print(table, justify="center")
            console.save_svg(f"{self.api}.svg",
                             title=f"ISE OpenAPI {self.api} API")
            click.secho(f'SVG file created at { sys.path[0] }/{ self.api }.svg',
                fg='green')

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

    def all_files(self, parsed_json):
        self.json_file(parsed_json)
        self.yaml_file(parsed_json)
        self.csv_file(parsed_json)
        self.markdown_file(parsed_json)
        self.html_file(parsed_json)
        self.mindmap_file(parsed_json)
        self.mp3_file(parsed_json)
        self.svg_file(parsed_json)
        self.png_file(parsed_json)
        self.flowchart_file(parsed_json)
        self.class_file(parsed_json)
        self.relationship_file(parsed_json)
        self.state_file(parsed_json)
        self.graph_file(parsed_json)

    def chatbot(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        adaptive_card_template = env.get_template('ISE_adaptive_card.j2')
        dict_json = json.loads(parsed_json)
        for result in dict_json:
            adatpive_card_output = adaptive_card_template.render(api = self.api,
                data_to_template=result,
                roomid = self.room)        
            webex_adaptive_card_response = requests.post('https://webexapis.com/v1/messages', data=adatpive_card_output, headers={"Content-Type": "application/json", "Authorization": f"Bearer { self.token }" })
            print('The POST to WebEx had a response code of ' + str(webex_adaptive_card_response.status_code) + 'due to' + webex_adaptive_card_response.reason)
        if self.filetype == "text":
            m = MultipartEncoder({'roomId': self.room,
            'text': f'ISE { self.api } Text File',
            'files': (f'{ self.api }.txt', open(f'{ self.api }.txt', "rb"),
                      'text/text' )})
            webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m, headers={"Content-Type": m.content_type, "Authorization": f"Bearer { self.token }" })
            print('The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)
        elif self.filetype == "csv":
            m = MultipartEncoder({'roomId': self.room,
            'text': f'ISE { self.api } CSV File',
            'files': (f'{ self.api }.csv', open(f'{ self.api }.csv', "rb"),
                      'text/text' )})
            webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m, headers={"Content-Type": m.content_type, "Authorization": f"Bearer { self.token }" })
            print('The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)

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
                        'text',
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
@click.option('--room',
    prompt="Webex Room",
    help="The Webex Room ID",
    required=False,
    default="none",envvar="ROOM")
@click.option('--token',
    prompt="Webex Token",
    help="The Webex Token",
    required=False,
    default="none",envvar="TOKEN")
def cli(url,
        username,
        password,
        api,
        filetype,
        room,
        token
    ):
    invoke_class = Isecycle(url,
                            username,
                            password,
                            api,
                            filetype,
                            room,
                            token
                            )
    invoke_class.isecycle()

if __name__ == "__main__":
    cli()
