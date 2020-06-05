import os

import pytest
from sqlalchemy import event

from app import create_app, db as _db


CONFIG_ENVVAR = "FLASK_ENV"


class EnvVar:
    def __init__(self, **kw):
        self.envvars = kw

    def __enter__(self):
        self._environ = os.environ.copy()
        os.environ.update(self.envvars)
        return None

    def __exit__(self, type, value, traceback):
        os.environ.clear()
        os.environ.update(self._environ)


def an_app(config="testing"):
    with EnvVar(**{CONFIG_ENVVAR: config}):
        app = create_app()
        return app


@pytest.fixture
def client(app):
    with app.test_request_context():
        with app.test_client() as client:
            with app.app_context():
                yield client
                _db.session.rollback()


@pytest.fixture(scope="session")
def app():
    return an_app()


@pytest.fixture(scope="session")
def db(app):
    _db.app = app
    yield _db


@pytest.fixture(scope="function", autouse=True)
def session(app, db):
    with app.app_context():
        conn = _db.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = _db.create_scoped_session(options=options)

        # establish  a SAVEPOINT just before beginning the test
        # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
        sess.begin_nested()

        @event.listens_for(sess(), "after_transaction_end")
        def restart_savepoint(sess2, trans):
            # Detecting whether this is indeed the nested transaction of the test
            if trans.nested and not trans._parent.nested:
                # The test should have normally called session.commit(),
                # but to be safe we explicitly expire the session
                sess2.expire_all()
                sess2.begin_nested()

        _db.session = sess
        yield sess

        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()
        conn.close()
