import sys
import json
import requests
import rich_click as click
import yaml
import xmltodict
import urllib3
from pathlib import Path
from rich import print_json
from jinja2 import Environment, FileSystemLoader
from gtts import gTTS

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
