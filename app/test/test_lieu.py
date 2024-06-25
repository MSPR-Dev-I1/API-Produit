from fastapi.testclient import TestClient
from app.test.utils import memory_engine
from app import models, actions
from app.main import app

client = TestClient(app)

def test_get_lieux(mocker):
    """
        Cas passant (retourne la liste des lieux)
    """
    lieux = [{
        "id_lieu": 1,
        "nom": "test",
        "adresse": "3 rue monnaie",
        "code_postal": "59000",
        "ville": "France"
    }]
    mocker.patch("sqlalchemy.orm.Session.query", return_value=lieux)

    response = client.get("/lieu")

    assert response.status_code == 200
    assert response.json() == lieux

def test_get_lieux_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    response = client.get("/lieu")

    assert response.status_code == 500

def test_get_lieu(mocker):
    """
        Cas passant (retourne un lieu)
    """
    db_lieu = {
        "id_lieu": 1,
        "nom": "test",
        "adresse": "3 rue monnaie",
        "code_postal": "59000",
        "ville": "France"
    }
    mock_query = mocker.MagicMock()
    mock_query.where.return_value.first.return_value = db_lieu
    mocker.patch("sqlalchemy.orm.Session.query", return_value=mock_query)

    response = client.get("/lieu/" + str(db_lieu['id_lieu']))

    assert response.status_code == 200
    assert response.json() == db_lieu

def test_get_lieu_error_404(mocker):
    """
        Cas non passant (le lieu n'a pas été trouvé)
    """
    db_lieu = None
    mock_query = mocker.MagicMock()
    mock_query.where.return_value.first.return_value = db_lieu
    mocker.patch("sqlalchemy.orm.Session.query", return_value=mock_query)

    response = client.get("/lieu/1")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Lieu not found'}

def test_get_lieu_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    response = client.get("/lieu/1")

    assert response.status_code == 500

def test_post_lieu(mocker):
    """
        Cas passant (retourne le lieu avec un id)
    """
    new_lieu = {
        "nom": "test",
        "adresse": "3 rue monnaie",
        "code_postal": "59000",
        "ville": "France"
    }
    db_lieu = models.Lieu(
        id_lieu=1,
        nom=new_lieu['nom'],
        adresse=new_lieu['adresse'],
        code_postal=new_lieu['code_postal'],
        ville=new_lieu['ville'],
    )

    mocker.patch("app.actions.create_lieu", return_value=db_lieu)

    response = client.post("/lieu", json=new_lieu)

    assert response.status_code == 201

def test_action_create_lieu():
    """
        Test unitaire de la function create lieu
    """
    database = memory_engine()
    new_lieu = models.Lieu(
        nom="test",
        adresse="3 rue monnaie",
        code_postal="59000",
        ville="France"
    )

    db_lieu = actions.create_lieu(new_lieu, database)

    assert isinstance(db_lieu, models.Lieu)
    assert db_lieu.id_lieu is not None

def test_post_lieu_error_422():
    """
        Cas non passant (des informations du lieu sont manquants)
    """
    new_lieu = {
        "adresse": "3 rue monnaie",
        "code_postal": "59000",
        "ville": "France"
    }

    response = client.post("/lieu", json=new_lieu)

    assert response.status_code == 422

def test_post_lieu_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    new_lieu = {
        "nom": "test",
        "adresse": "3 rue monnaie",
        "code_postal": "59000",
        "ville": "France"
    }
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    response = client.post("/lieu", json=new_lieu)

    assert response.status_code == 500

def test_delete_lieu(mocker):
    """
        Cas passant (retourne l'id du lieu supprimé)
    """
    db_lieu = models.Lieu(
        id_lieu=1,
        nom="test",
        adresse="3 rue monnaie",
        code_postal="59000",
        ville="France"
    )
    mocker.patch("app.actions.get_lieu", return_value=db_lieu)
    mocker.patch("sqlalchemy.orm.Session.delete", return_value=None)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    response = client.delete("/lieu/" + str(db_lieu.id_lieu))

    assert response.status_code == 200
    assert response.json() == {"deleted": db_lieu.id_lieu}

def test_delete_lieu_error_404(mocker):
    """
        Cas non passant (le lieu n'est pas trouvé)
    """
    mocker.patch("app.actions.get_lieu", return_value=None)

    response = client.delete("/lieu/1")

    assert response.status_code == 404

def test_delete_lieu_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    db_lieu = models.Lieu(
        id_lieu=1,
        nom="test",
        adresse="3 rue monnaie",
        code_postal="59000",
        ville="France"
    )
    mocker.patch("app.actions.get_lieu", return_value=db_lieu)
    mocker.patch("sqlalchemy.orm.Session.delete", side_effect=Exception("Connection error"))

    response = client.delete("/lieu/1")

    assert response.status_code == 500

def test_patch_lieu(mocker):
    """
        Cas passant (retourne le lieu mis à jour)
    """
    db_lieu = models.Lieu(
        id_lieu=1,
        nom="test",
        adresse="3 rue monnaie",
        code_postal="59000",
        ville="France"
    )
    lieu_updated = {
        "adresse": "4 rue monnaie",
    }
    mocker.patch("app.actions.get_lieu", return_value=db_lieu)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    response = client.patch("/lieu/" + str(db_lieu.id_lieu), json=lieu_updated)

    assert response.status_code == 200
    assert response.json()["adresse"] == lieu_updated["adresse"]

def test_patch_lieu_error_404(mocker):
    """
         Cas non passant (le lieu n'est pas trouvé)
    """
    lieu_updated = {
        "adresse": "4 rue monnaie",
    }
    mocker.patch("app.actions.get_lieu", return_value=None)

    response = client.patch("/lieu/1", json=lieu_updated)

    assert response.status_code == 404

def test_patch_lieu_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    db_lieu = models.Lieu(
        id_lieu=1,
        nom="test",
        adresse="3 rue monnaie",
        code_postal="59000",
        ville="France"
    )
    lieu_updated = {
        "adresse": "4 rue monnaie",
    }
    mocker.patch("app.actions.get_lieu", return_value=db_lieu)
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    response = client.patch("/lieu/" + str(db_lieu.id_lieu), json=lieu_updated)

    assert response.status_code == 500
