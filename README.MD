# Déployez votre application 

La startup Pur Beurre, avec laquelle vous avez déjà travaillé, souhaite développer une plateforme web à destination de ses clients. Ce site permettra à quiconque de trouver un substitut sain à un aliment considéré comme "Trop gras, trop sucré, trop salé".

## Cahier des charges
Le cahier des charges est disponible en cliquant sur ce lien.



## Fonctionnalités
* Affichage du champ de recherche dès la page d’accueil
* La recherche ne doit pas s’effectuer en AJAX
* Interface responsive
* Authentification de l’utilisateur : création de compte en entrant un mail et un mot de passe, sans possibilité de changer son mot de passe pour le moment.

## Installation

Ce projet utilise PostgreSQL.

```
virtualenv Project8
cd Project8
source bin/activate
pip install -r requirements.txt
```

```
$ python3 --version
Python 3.8.5
```
Read [requirements.txt](https://github.com/Julien-V/P8/blob/master/requirements.txt)


## Lancement


### Serveur de développement
```
./manage.py runserver
```
### Tests
```
pytest
```
