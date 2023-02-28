import pytest


@pytest.mark.django_db(transaction=True)
@pytest.fixture(autouse=True)
def _enable_db(db):
    pass
