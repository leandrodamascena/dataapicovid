# CovidAPI serverless

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Esta API para servir dados do COVID 19 (#fiqueemcasa) tem por objetivo demonstrar o uso do conceito serverless para construção de aplicativos em nuvem. As tecnologias abaixo foram utilizadas:

  - AWS - Amazon Web Services
  - DynamoDB - Banco de dados NoSQL da AWS
  - API Gateway - Gateway de API da AWS
  - Lambda - Plataforma de execução de códigos serverless da AWS
  - Python3.8 - Linguagem de programação Python na versão 3.8
  - Flask - Framework do Python para escrever API em padrão Rest
  - Zappa - Framework para deploys de aplicações Serverless

### Custos

- A AWS tem uma sólida política de free-tier para que as pessoas possam iniciar a jornada de computação em nuvem de forma gratuita. Todo esse projeto vai funcionar na nuvem AWS de forma gratuita se for utilizado de forma acadêmia. Se este projeto for usado de forma profissional, então você poderá ter custos. Consulte a política de free-tier aqui https://aws.amazon.com/pt/free/. 

### Configuração inicial da AWS

  - É preciso ter uma conta na AWS para rodar este projeto.
  - Abra a console AWS e crie um usuário com acesso programático. Copie as chaves do mesmo.
  - Crie uma role para este usuário e dê permissão para criar/atualizar/apagar itens no DynamoDB, CloudWatch, Lambda, API Gateway e XRay.
  - Instale o AWS Command Line Interface (AWSCli) na sua máquina e execute o "aws configure". Informe suas chaves na configuração e coloque a região default como "us-east-1"
  
### Instalação local para testes

Esta API requer Python3.8 e PIP para funcionar.

Criar o ambiente virtual.

```sh
$  python -m venv apicovid
```

Ativar o ambiente virutal

```sh
$ apicovid\Scripts\activate.bat (Windows)
$ ./apiconvid/scripts/activate (Linux)
```

Instalar os pacotes necessários com o PIP

```sh
$ pip install -r requirements.txt
```
Realize a carga da tabela utilizando o comando abaixo (deve demorar uns 10 minutos para concluir):

```sh
$ python data/proccessdata.py
```

Rodar o comando abaixo e realizar testes locais com o próprio browser ou postman/soapui nos endereço http://127.0.0.1:5000/countryDailyResults ou http://127.0.0.1:5000/countryDailyResults/Brazil ou http://127.0.0.1:5000/countryDailyResults/Brazil/2020-02-20. PS: Pode substituir Brazil por qualquer outro país/região e a data também.

```sh
$ python run.py
```

### Configuração do Zappa para deploy na AWS

Execute o comando "zappa init". Nas opções não coloque deploy global e deixe as demais opções que vem por padrão (stage, bucket e afins)

```sh
$ zappa init
```
Abra o arquivo zappa_settings.json e adicione as seguintes linhas:

"aws_region": "us-east-1",
"xray_tracing": true

Execute o comando "zappa deploy dev" e aguarde completar o deploy. O próprio zappa vai informar a URL da API que foi exposta na API Gateway e você pode testar alterando o "http://127.0.0.1:5000/" do item anterior para este novo endereço.

```sh
$ zappa deploy dev
```

Caso realize qualquer modificação no projeto, então execute o comando "zappa update dev" para realizar um update do stage

```sh
$ zappa update dev
```

Execute o comando "zappa undeploy dev" para fazer undeploy do projeto.

```sh
$ zappa undeploy dev
```

### Configurações adicionais

- Abra o console da AWS, vá até o Stage da APIGateway criada e habilite a opção "Enable X-Ray Tracing".
- Abra o console da AWS, vá até o XRay e veja o trace da chamada, tempo de resposta e possíveis gargalos. 

### Limpando o ambiente

Após realizar o undeploy do projeto, vá até o DynamoDB e remova a tabela criada.

### No futuro...

 - Criar um DynamoDB Stream para invocar uma função Lambda de atualização de quantidades por país quando o dado for atualizado na tabela dailyResults.


License
----

MIT


**Free Software, Hell Yeah! For a better and free world**
