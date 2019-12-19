## Instalar dependências python
- No diretório base instalar as dependências descritas no ficheiro com o seguinte comando, sem aspas:
- "pip3 install --user -r requirements.txt" ou "pip3 install pipenv; pipenv sync"

# Setup(Windows)
- Abrir o projeto neste diretório no pycharm
- Abrir o ficheiro requirements.txt no pycharm e instalar o plugin requirements.txt
- Correr, pelo menu iniciar, o programa "GraphDB Free"
- correr no pycharm, clicando no botão "manage" em alternative pode-se executar pelo terminal do pycharm o comando "python3 manage.py runserver"
- abrir o browser no endereço "http://127.0.0.1:8000/"

#Setup(Linux)
## Execução do Basex server
- executar o GraphDB, se instalado

## Execução do projecto
- executar o comando "python3 manage.py runserver" no diretório base do projeto

# Nota dataset
- O dataset original "anpc-2018.csv" foi reduzido para 1/256 por questões de performance com recurso ao awk que deu origem ao "dataset.csv"
