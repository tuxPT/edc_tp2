from django import forms
from bootstrap_datepicker_plus import DatePickerInput


STATE = [('Em Resolução','Em Resolução'),
         ('Conclusão','Conclusão'),
         ('Encerrada','Encerrada'),
         ('Em curso','Em curso'),
         ('Despacho de 1º Alerta','Despacho de 1º Alerta')
         ]


DISTRITOS = [('Aveiro','Aveiro'),
             ('Beja', 'Beja'),
             ('Braga', 'Braga'),
             ('Bragança','Bragança'),
             ('Castelo Branco','Castelo Branco'),
             ('Coimbra','Coimbra'),
             ('Évora','Évora'),
             ('Faro','Faro'),
             ('Guarda','Guarda'),
             ('Leiria','Leiria'),
             ('Lisboa','Lisboa'),
             ('Portalegre','Portalegre'),
             ('Porto','Porto'),
             ('Santarém','Santarém'),
             ('Setúbal','Setúbal'),
             ('Viana do Castelo','Viana do Castelo'),
             ('Vila Real','Vila Real'),
             ('Viseu','Viseu')
             ]

NATUREZA=[
    ('Protecção e Assistência a Pessoas e Bens', 'Protecção e Assistência a Pessoas e Bens'),
    ('Riscos Tecnológicos', 'Riscos Tecnológicos'),
    ('Riscos Mistos', 'Riscos Mistos'),
    ('Riscos Tecnológicos', 'Riscos Tecnológicos'),
    ('Riscos Naturais','Riscos Naturais'),
    ('Operações e Estados de Alerta', 'Operações e Estados de Alerta'),
]

class RelatarForm(forms.Form):
    data_ocorrencia = forms.DateField(label='Data da ocorrência', input_formats=['%d-%m-%Y'], widget=DatePickerInput(format='%d-%m-%Y', attrs={'class': 'form-control'}))
    natureza = forms.CharField(label='Natureza', widget=forms.Select(choices=NATUREZA, attrs={'class': 'form-control'}))
    estado = forms.CharField(label='Estado', widget=forms.Select(choices=STATE, attrs={'class': 'form-control'}))
    distrito = forms.CharField(label='Distrito', widget=forms.Select(choices=DISTRITOS, attrs={'class': 'form-control'}))
    concelho = forms.CharField(label='Concelho', widget=forms.TextInput(attrs={'class': 'form-control'}))
    freguesia = forms.CharField(label='Freguesia', widget=forms.TextInput(attrs={'class': 'form-control'}))
    latitude = forms.FloatField(label='Latitude', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    longitude = forms.FloatField(label='Longitude', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    meiosTerrestres = forms.IntegerField(label='Meios Terrestres', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    opTerrestres = forms.IntegerField(label = 'Operacionais Terrestres', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    meiosAereos = forms.IntegerField(label = 'Meios Aéreos', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    opAereos = forms.IntegerField(label = 'Operacionais Aéreos', widget=forms.NumberInput(attrs={'class': 'form-control'}))
