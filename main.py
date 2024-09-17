from fastapi import FastAPI, Request, Form, Body, HTTPException

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from typing import Annotated
from pydantic import BaseModel, Field

import time

app = FastAPI()

# Paramétrage de l'application FastAPI
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

# !! > Consulter la documentation automatique de l'API sur http://localhost:8000/docs 
# (après démarrage du serveur évidemment...)

# --------------
# # Initialisation des variables

intervalle = 60  # minutes
repas_distribues = 0  # repas

# --------------
# Pages Web

@app.get("/", response_class=HTMLResponse, tags=["Pages Web"])
async def page_accueil(request: Request):
    """
    Page d'accueil retournée lorsque l'utilisateur interroge le serveur sur la racine du site.
    """
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "intervalle": intervalle, 
        "repas_distribues": repas_distribues
        })


@app.get("/repas/init", response_class=HTMLResponse, tags=["Pages Web"])
async def page_intialisation(request: Request):
    """
    Page d'initalisation d'une nouvelle génération de *petits poussins kromignons*, retournée lorsque l'utilisateur accède à l'url /init.
    """
    return templates.TemplateResponse("heure.html", {
        "request": request,
        "intervalle": intervalle, 
        "repas_distribues": repas_distribues
        })  # TODO: il faut corriger ici le nom de la page retournée

# --------------
# Services API

# Réception de l'heure système
@app.get("/heuresysteme", tags=["Services API"])
async def recv_heure_systeme(request: Request) -> str:
    """
    Service API qui permet de récupérer l'heure système du serveur'.
    """
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("L'heure est demandé.")

    return current_time


# Reception de l'intervalle de distribution
@app.get("/intervalle/reception", tags=["Services API"])
async def recv_intervalle(request: Request) -> int:
    """
    Service API qui permet de récupérer la valeur d'intervalle **en minute** à appliquer pour la distribution de la nourriture.
    """
    global intervalle
    print("L'intervalle est demandé.")

    return intervalle


# Modification de l'intervalle de distribution
@app.post("/intervalle/modification", response_class=HTMLResponse, tags=["Services API"])
async def modif_intervalle(request: Request, nouvel_intervalle: Annotated[int, Form()]):
    """
    Service API qui permet de modifier la valeur d'intervalle **en minutes**.
    """
    global intervalle

    intervalle = nouvel_intervalle
    print("Nouvel valeur d'intervalle :", intervalle)
    
    # Suite à réception de la valeur le serveur redirige vers la page d'accueil.
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "intervalle": intervalle, 
        "repas_distribues": repas_distribues
        })



# Ajout du nombre de repas à incrémenter
@app.post("/repas/ajout", tags=["Services API"])
async def recv_repas_distribues(repas: Annotated[int, Form()]) -> bool:
    """
    Service API qui permet d'ajouter un nombre de repas au total de repas donné actuellement enregistré par le serveur'.
    """
    global repas_distribues

    if repas <= 0:
        raise HTTPException(status_code=406, detail="Le nombre de repas doit être supérieur à 0.")

    repas_distribues += repas
    print("Nouveau comptage de repas :", repas_distribues)

    return True


# Initialisation du nombre de repas distribué
@app.post("/repas/init", response_class=HTMLResponse, tags=["Services API"])
async def recv_repas_initiaux(request: Request, repas_init: Annotated[int, Form()]) -> bool:
    """
    Service API qui permet d'intialiser une nouvelle valeur de nombre de repas distribués.'.
    """
    global repas_distribues

    repas_distribues = repas.repas_distribues

    # Suite à réception de la valeur le serveur redirige vers la page d'accueil.
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "intervalle": intervalle, 
        "repas_distribues": repas_distribues
        })