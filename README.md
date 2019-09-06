# Eventex

Sistema de Eventos

## Como desenvolver?

1. Clone o repositório.
2. Crie o virtualenv com python 3.5
3. Ative o virtualenv.
4. Instale as dependências.
5. Configure a instência com o .env
6. Execute os testes.

```console

git clone git@github.com:lucasdev/eventex.git wttd
cd wttd
python -m venv .wttd
source .wttd/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```

## Como fazer deploy

1. Crie uma instância no heroku.
2. Envie as configurações para p heroku.
3. Defina uma SECRET_KEY segura para instância.
4. Defina DEBUG=False
5. Configure o serviço de email.
6. Envie o código pro heroku.

```console

heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False
# configuro o email
git push heroku --force
```
