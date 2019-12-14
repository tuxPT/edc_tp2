import json
import xml.etree.ElementTree as ET
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

from .forms import RelatarForm
from lxml import etree
from datetime import datetime


def index(request):
    return render(request, 'index.html')

def sobre(request):
    return render(request, 'sobre.html')


def relatar(request):
    form = RelatarForm()
    return render(request, 'relatar.html', {'form': form})
    #return render(request, 'relatar.html')


def estatisticas(request):
    tparams = {
        'month': get_occmonth(),
        'categories': get_occcategory()
    }
    return render(request, 'estatisticas.html', tparams)


def avisos(request):
    return render(request, 'avisos.html')


def confirm(request):
    return render(request, 'confirm.html')

def notconfirm(request):
    return render(request, 'notconfirm.html')

def listar(request):
    dic = incidentes_recentes_lista()
    context = {
        'info': dic,
    }
    return render(request, 'incidentes_recentes.html', context)


def get_occmonth():
    query = """
        select (COUNT(?month) as ?months) where { 
            ?s anpc:DataOcorrencia ?o .
            bind(month(?o) as ?month)
        }
        group by ?month
    """
    res = queryDB(query)
    print(res)
    return list()

    '''
    tree = ET.parse('app/xml/db.xml')
    root = tree.getroot()
    months = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for c in root.findall('incidente'):
        months[int(c.find('DataOcorrencia').text[5:7])-1] += 1
    return months
    '''


def get_occcategory():
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    file = open('app/xml/occu_p_category.xqm', 'r')
    try:
        query = session.query(file.read())
        occuCategory = json.loads(query.execute())
        query.close()
    finally:
        # close session
        if session:
            session.close()
    return occuCategory


#lista de fogos que estao a ocorrer --> usar xpath (so para usar sem ser com a bd) e assim mostra uma lista de fogos sem ser no mapa
def incidentes_recentes_lista():
    dic = {}
    tree = ET.parse('db.xml')
    root = tree.getroot()
    for c in root.findall('incidente'):
        if c.find('Estado').text == 'Em Curso' and c.find('DataOcorrencia').text[5:7] == '12':
            dic.update({c.attrib['Numero']: [c.find('DataOcorrencia').text[0:10], c.find('Natureza').text, c.find('Estado').text, c.find('Distrito').text, c.find('Concelho').text, c.find('Freguesia').text, c.find('OperacionaisTerrestres').text]})
    return dic


#mostrar detalhes dos incendios descritos na função incidentes_recentes_lista (para um especifico selecionado)
#ToDo...
def get_fogo(xml_file: str, value: str):
    dic = {}
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for c in root.findall('fogo'):
        if c.find("Freguesia").text == value:
            dic = {
                'DataOcorrencia': c.find('DataOcorrencia').text,
                'Natureza': c.find('Natureza').text,
                'Estado': c.find('Estado').text,
                'Distrito': c.find('Distrito').text,
                'Concelho': c.find('Concelho').text,
                'Freguesia': c.find('Freguesia').text,
                'Latitude': c.find('Latitude').text,
                'Longitude': c.find('Longitude').text,
                'MeiosTerrestres': c.find('MeiosTerrestres').text,
                'OperacionaisTerrestres': c.find('OperacionaisTerrestres').text,
                'MeiosAereos': c.find('MeiosAereos').text,
                'OperacionaisAereos': c.find('OperacionaisAereos').text,
            }
            break
    return dic


#mostrar detalhes dos incendios descritos na função incidentes_recentes_lista (para um especifico selecionado)
def mostrar_detalhes(request):

    template = loader.get_template('detalhes.html')
    value = request.GET.get('Freguesia')
    context = get_fogo("db.xml", value)
    return HttpResponse(template.render(context, request))


def create_incident(data):
    incidentes = etree.Element('incidentes')

    num = datetime.now().strftime('%Y%m%d%H%M%S')

    incidente = etree.SubElement(incidentes, 'incidente', {'Numero': str(num)})

    data_ocorrencia = etree.SubElement(incidente, 'DataOcorrencia')
    data_ocorrencia.text = data['data_ocorrencia'].strftime('%Y-%m-%dT%H:%M:%S')

    natureza = etree.SubElement(incidente, 'Natureza')
    natureza.text = data['natureza']

    estado = etree.SubElement(incidente, 'Estado')
    estado.text = data['estado']

    distrito = etree.SubElement(incidente, 'Distrito')
    distrito.text = data['distrito'].upper()

    concelho = etree.SubElement(incidente, 'Concelho')
    concelho.text = data['concelho']

    freguesia = etree.SubElement(incidente, 'Freguesia')
    freguesia.text = data['freguesia']

    latitude = etree.SubElement(incidente, 'Latitude')
    latitude.text = str(data['latitude'])

    longitude = etree.SubElement(incidente, 'Longitude')
    longitude.text = str(data['longitude'])

    meios_terrestres = etree.SubElement(incidente, 'MeiosTerrestres')
    meios_terrestres.text = str(data['meiosTerrestres'])

    operacionais_terrestres = etree.SubElement(incidente, 'OperacionaisTerrestres')
    operacionais_terrestres.text = str(data['opTerrestres'])

    meios_aereos = etree.SubElement(incidente, 'MeiosAereos')
    meios_aereos.text = str(data['meiosAereos'])

    operacionais_aereos = etree.SubElement(incidente, 'OperacionaisAereos')
    operacionais_aereos.text = str(data['opAereos'])

    return incidentes


# abre o ficheiro XML e adiciona o incidente no final
def store_incident(doc, file_xml):
    tree = etree.parse(file_xml)
    root = tree.getroot()
    root.append(doc)
    tree.write(file_xml, xml_declaration=True, encoding='UTF-8')


# recebe dados do formulário e coloca no ficheiro xml se os dados forem válidos
def store_data(request):
    if request.method == 'POST':
        form = RelatarForm(request.POST)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            for k in data:
                print('{} : {}'.format(k, data[k]))
            doc = create_incident(data)
            print(etree.tostring(doc.find('incidente'), pretty_print=True))
            if validate(doc, 'app/xml/schema.xsd'):
                print('ok')
                store_incident(doc.find('incidente'), 'db.xml')
                return HttpResponseRedirect('confirm')
            else:
                print('not ok')
                return HttpResponseRedirect('notconfirm')
        else:
            print('not valid')
            return HttpResponseRedirect('notconfirm')


#validate a xml file with xml schema
def validate(doc: str, file_schema: str):
    # parsing xsd
    with open(file_schema, 'r') as schema_file:
        xmlschema_doc = etree.parse(schema_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)

        # validate against schema
        try:
            xmlschema.assertValid(doc)
            print('XML valid, schema validation ok.')
            return True

        except etree.DocumentInvalid as err:
            print('Schema validation error: '+str(err))
            return False

        except Exception as e:
            print('Unknown error: ' + str(e))
            return False


def list_recent_distance(request):
    lat = request.GET.get('lat')
    long = request.GET.get('lng')
    radius = request.GET.get('radius')

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    file = open('app/xml/recent_incident.xqm', 'r')
    rv = None
    try:
        query = session.query(file.read() + 'return (local:list_in_range({}, {}, {}))'.format(lat, long, radius))
        rv = json.loads(query.execute())
        query.close()

    finally:
        # close session
        if session:
            session.close()
    print(json.dumps(rv))
    return HttpResponse(json.dumps(rv), content_type="application/json")

def queryDB(query):
    query = """
        PREFIX anpc: <http://centraldedados.pt/anpc-2018.csv#>
        PREFIX spif: <http://spinrdf.org/spif#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    """
    endpoint = "http://localhost:7200"
    repo = "anpc"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    if ("INSERT" or "UPDATE") in query:
        payload = {"update": query}
        result = accessor.sparql_update(body=payload, repo_name=repo)
    else:
        payload = {"query": query}
        result = accessor.sparql_select(body=payload, repo_name=repo)
    return result
