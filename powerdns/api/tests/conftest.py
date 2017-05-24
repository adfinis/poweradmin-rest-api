import pytest


@pytest.fixture(autouse=True, scope="session")
def managed_models():
    """
    For unit tests we need create an empty powerdns database
    scheme but this only works for models which are managed.
    Hence with this auto fixture we temporarly change models to be managed.
    """
    from django.apps import apps
    app = apps.get_app_config('api')
    unmanaged_models = list(app.get_models())
    for model in unmanaged_models:
        model._meta.managed = True

    yield

    unmanaged_models = list(app.get_models())
    for model in unmanaged_models:
        model._meta.managed = False
