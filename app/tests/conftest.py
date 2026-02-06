import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def mock_database():
    with patch("app.config.database.db_config") as mock_db:
        mock_db.init_database.return_value = None
        mock_db.get_session.return_value = MagicMock()
        yield

@pytest.fixture
def app(mock_database): 
    from app import create_app
    app = create_app()
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()