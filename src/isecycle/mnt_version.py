import requests

url = "https://10.10.20.77/admin/API/mnt/Version"

payload={}
headers = {
  'Accept': 'application/xml',
  'Authorization': 'Basic YWRtaW46QzFzY28xMjM0NQ==',
  'Cookie': 'APPSESSIONID=9CA71B4EB38E2F12DBEEC96BB8D2ABF8; JSESSIONIDSSO=5B4436A43CF06E58CC32A7879674B031'
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

print(response.text)