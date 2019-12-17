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
import json


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
    r = []
    for month in res['results']['bindings']:
        r.append(int(month['months']['value']))
    print(r)
    return r

def get_occcategory():
    query="""
        select ?natur (COUNT(?natur) as ?numero) where { 
	        ?s anpc:Natureza ?natureza .
	        bind(strbefore(?natureza,"/") as ?natur)
        }
        group by ?natur
    """
    res = queryDB(query)
    r = dict()
    for natureza in res['results']['bindings']:
        r[natureza['natur']['value']] = natureza['numero']['value']
    print(r)
    return r

#lista de fogos que estao a ocorrer --> usar xpath (so para usar sem ser com a bd) e assim mostra uma lista de fogos sem ser no mapa
def incidentes_recentes_lista():
    query = """
    select ?numero ?data ?natureza ?estado ?distrito ?concelho ?freguesia ?operacionais
    where {
        ?s  anpc:Numero ?numero;
            anpc:EstadoOcorrencia ?estado;
            anpc:DataOcorrencia ?data;
            anpc:Distrito ?distrito;
            anpc:Concelho ?concelho;
            anpc:Freguesia ?freguesia;
            anpc:NumeroOperacionaisTerrestresEnvolvidos ?operacionais;
            anpc:Natureza ?natur .
       	bind(strbefore(?natur,"/") as ?natureza)
        filter(month(?data) = 12) 
    }
    """
    res = queryDB(query)
    r = dict()
    for row in res['results']['bindings']:
        r[row['numero']['value']] = [row['data']['value'],
                                     row['natureza']['value'],
                                     row['estado']['value'],
                                     row['distrito']['value'],
                                     row['concelho']['value'],
                                     row['freguesia']['value'],
                                     row['operacionais']['value']
                                     ]
    return r

"""
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
"""

"""
#mostrar detalhes dos incendios descritos na função incidentes_recentes_lista (para um especifico selecionado)
def mostrar_detalhes(request):

    template = loader.get_template('detalhes.html')
    value = request.GET.get('Freguesia')
    context = get_fogo("db.xml", value)
    return HttpResponse(template.render(context, request))
"""

def create_incident(data):
    """
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
    """
    num = datetime.now().strftime('%Y%m%d%H%M%S')
    data_ocorrencia = data['data_ocorrencia'].strftime('%Y-%m-%dT%H:%M:%S')
    natureza = data['natureza']
    estado = data['estado']
    distrito = data['distrito']
    concelho = data['concelho']
    freguesia = data['freguesia']
    latitude = str(data['latitude'])
    longitude = str(data['longitude'])
    meios_terrestres = str(data['meiosTerrestres'])
    operacionais_terrestres = str(data['opTerrestres'])
    meios_aereos = str(data['meiosAereos'])
    operacionais_aereos = str(data['opAereos'])
    incidentes = """
        insert {{
            ?numero2IRI 	a xsd:anyURI;
                            anpc:Numero ?numero;
                            anpc:DataOcorrencia ?dataOcorrencia ;
                            anpc:Natureza "{}" ;
                            anpc:EstadoOcorrencia "{}" ;
                            anpc:Distrito "{}" ;
                            anpc:Concelho "{}" ;
                            anpc:Freguesia "{}" ;
                            anpc:Latitude ?lat ;
                            anpc:Longitude ?lng ;
                            anpc:NumeroMeiosTerrestresEnvolvidos ?nmt ;
                            anpc:NumeroOperacionaisTerrestresEnvolvidos ?not ;
                            anpc:NumeroMeiosAereosEnvolvidos ?nma ;
                            anpc:NumeroOperacionaisAereosEnvolvidos ?noa .       
        }}
        where{{
            bind(strdt("{}", xsd:integer) as ?numero)
            bind(strdt("{}", xsd:dateTime) as ?dataOcorrencia)
            bind(strdt("{}", xsd:decimal) as ?lat)
            bind(strdt("{}", xsd:decimal) as ?lng)
            bind(strdt("{}", xsd:integer) as ?nmt)
            bind(strdt("{}", xsd:integer) as ?not)
            bind(strdt("{}", xsd:integer) as ?nma)
            bind(strdt("{}", xsd:integer) as ?noa)
            bind(IRI(concat(str("http://centraldedados.pt/anpc-2018.csv#"), str(?numero))) as ?numero2IRI)
        }}
    """.format(natureza, estado, distrito, concelho, freguesia, num, data_ocorrencia, latitude, longitude, meios_terrestres, operacionais_terrestres, meios_aereos, operacionais_aereos)
    return incidentes

# recebe dados do formulário e coloca no ficheiro xml se os dados forem válidos
def store_data(request):
    if request.method == 'POST':
        form = RelatarForm(request.POST)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            for k in data:
                print('{} : {}'.format(k, data[k]))
            query = create_incident(data)
            queryDB(query)
            return HttpResponseRedirect('confirm')
        else:
            print('not valid')
            return HttpResponseRedirect('notconfirm')

def listar_incidentes_map(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    radius = request.GET.get('radius')
    query = """
        PREFIX ofn: <http://www.ontotext.com/sparql/functions/>
        select ?Latitude ?Longitude ?Natureza
        where{{
            ?s  anpc:Latitude ?Latitude;
                anpc:Longitude ?Longitude;
                anpc:Natureza ?Natureza;
                anpc:DataOcorrencia ?data.
            bind(strdt("{0}", xsd:integer) as ?radiusParsed)
            bind(strdt("{1}", xsd:decimal) as ?latParsed)
            bind(strdt("{2}", xsd:decimal) as ?lngParsed)
            filter(?distance <= ?radiusParsed && ((month(?data) = 12 && year(?data) = 2018) || year(?data) > 2018))        
            bind(
                ofn:sqrt(
                    ofn:pow(
                        (?Latitude*111.03-?latParsed*111.03), 2)
                    +
                    ofn:pow(
                        (?Longitude*85.39-?lngParsed*85.39), 2)
                ) as ?distance
            )
        }}
        """.format(radius, lat, lng)

    print(query)

    res = queryDB(query)
    r = []
    for row in res['results']['bindings']:
        r.append({'Natureza': row['Natureza']['value'],
                  'Latitude': float(row['Latitude']['value']),
                  'Longitude': float(row['Longitude']['value'])})

    return HttpResponse(json.dumps(r), content_type="application/json")

def queryDB(query):
    query = """
        PREFIX anpc: <http://centraldedados.pt/anpc-2018.csv#>
        PREFIX spif: <http://spinrdf.org/spif#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    """ + query
    endpoint = "http://localhost:7200"
    repo = "anpc"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    if query.find('update') != -1 or query.find('insert') != -1:
        payload = {"update": query}
        accessor.sparql_update(body=payload, repo_name=repo)
    else:
        payload = {"query": query}
        result = accessor.sparql_select(body=payload, repo_name=repo)
        return json.loads(result)
