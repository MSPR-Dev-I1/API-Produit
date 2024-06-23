from fastapi.testclient import TestClient
from app.test.utils import memory_engine
from app import models, actions
from app.main import app

client = TestClient(app)

def test_get_produits(mocker):
    """
        Cas passant (retourne la liste des produits)
    """
    produits = [{
       "id_produit": 1,
        "nom": "café 1",
        "description": "café de test",
        "prix": 10.50,
        "provenance": "France"
    }]
    mocker.patch("sqlalchemy.orm.Session.query", return_value=produits)

    response = client.get("/produit")

    assert response.status_code == 200
    assert response.json() == produits

def test_get_produits_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    response = client.get("/produit")

    assert response.status_code == 500

def test_get_produit(mocker):
    """
        Cas passant (retourne un produit)
    """
    db_produit = {
       "id_produit": 1,
        "nom": "café 1",
        "description": "café de test",
        "prix": 10.50,
        "provenance": "France"
    }
    mock_query = mocker.MagicMock()
    mock_query.where.return_value.first.return_value = db_produit
    mocker.patch("sqlalchemy.orm.Session.query", return_value=mock_query)

    response = client.get("/produit/" + str(db_produit['id_produit']))

    assert response.status_code == 200
    assert response.json() == db_produit

def test_get_produit_error_404(mocker):
    """
        Cas non passant (le produit n'a pas été trouvé)
    """
    db_produit = None
    mock_query = mocker.MagicMock()
    mock_query.where.return_value.first.return_value = db_produit
    mocker.patch("sqlalchemy.orm.Session.query", return_value=mock_query)

    response = client.get("/produit/1")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Produit not found'}

def test_get_produit_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    response = client.get("/produit/1")

    assert response.status_code == 500

def test_post_produit(mocker):
    """
        Cas passant (retourne le produit avec un id)
    """
    new_produit = {
        "nom": "café 1",
        "description": "café de test",
        "prix": 10.50,
        "provenance": "France"
    }
    db_produit = models.Produit(
        id_produit=1,
        nom=new_produit['nom'],
        description=new_produit['description'],
        prix=new_produit['prix'],
        provenance=new_produit['provenance'],
    )

    mocker.patch("app.actions.create_produit", return_value=db_produit)

    response = client.post("/produit", json=new_produit)

    assert response.status_code == 201

def test_action_create_produit():
    """
        Test unitaire de la function create produit
    """
    database = memory_engine()
    new_produit = models.Produit(
        nom="café 1",
        description="café de test",
        prix=10.50,
        provenance="France"
    )

    db_produit = actions.create_produit(new_produit, database)

    assert isinstance(db_produit, models.Produit)
    assert db_produit.id_produit is not None

def test_post_produit_error_422():
    """
        Cas non passant (des informations du produit sont manquants)
    """
    new_produit = {
        "description": "café de test",
        "prix": 10.50,
        "provenance": "France",
    }

    response = client.post("/produit", json=new_produit)

    assert response.status_code == 422

def test_post_produit_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    new_produit = {
        "nom": "café 1",
        "description": "café de test",
        "prix": 10.50,
        "provenance": "France"
    }
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    response = client.post("/produit", json=new_produit)

    assert response.status_code == 500

def test_delete_produit(mocker):
    """
        Cas passant (retourne l'id du produit supprimé)
    """
    db_produit = models.Produit(
        id_produit=1,
        nom="café 1",
        description="café de test",
        prix=10.50,
        provenance="France"
    )
    mocker.patch("app.actions.get_produit", return_value=db_produit)
    mocker.patch("sqlalchemy.orm.Session.delete", return_value=None)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    response = client.delete("/produit/" + str(db_produit.id_produit))

    assert response.status_code == 200
    assert response.json() == {"deleted": db_produit.id_produit}

def test_delete_produit_error_404(mocker):
    """
        Cas non passant (le produit n'est pas trouvé)
    """
    mocker.patch("app.actions.get_produit", return_value=None)

    response = client.delete("/produit/1")

    assert response.status_code == 404

def test_delete_produit_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    db_produit = models.Produit(
        id_produit=1,
        nom="café 1",
        description="café de test",
        prix=10.50,
        provenance="France"
    )
    mocker.patch("app.actions.get_produit", return_value=db_produit)
    mocker.patch("sqlalchemy.orm.Session.delete", side_effect=Exception("Connection error"))

    response = client.delete("/produit/1")

    assert response.status_code == 500

def test_patch_produit(mocker):
    """
        Cas passant (retourne le produit mis à jour)
    """
    db_produit = models.Produit(
        id_produit=1,
        nom="café 1",
        description="café de test",
        prix=10.50,
        provenance="France"
    )
    produit_updated = {
        "description": "café de test mis à jour",
    }
    mocker.patch("app.actions.get_produit", return_value=db_produit)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    response = client.patch("/produit/" + str(db_produit.id_produit), json=produit_updated)

    assert response.status_code == 200
    assert response.json()["description"] == produit_updated["description"]

def test_patch_produit_error_404(mocker):
    """
         Cas non passant (le produit n'est pas trouvé)
    """
    produit_updated = {
        "description": "produit de test mis à jour",
    }
    mocker.patch("app.actions.get_produit", return_value=None)

    response = client.patch("/produit/1", json=produit_updated)

    assert response.status_code == 404

def test_patch_produit_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    db_produit = models.Produit(
        id_produit=1,
        nom="café 1",
        description="café de test",
        prix=10.50,
        provenance="France"
    )
    produit_updated = {
        "description": "produit de test mis à jour",
    }
    mocker.patch("app.actions.get_produit", return_value=db_produit)
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    response = client.patch("/produit/" + str(db_produit.id_produit), json=produit_updated)

    assert response.status_code == 500
