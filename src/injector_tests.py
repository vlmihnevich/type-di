import pytest

from typing import Hashable

from .injector import Injector


injectable = Injector()


@pytest.fixture()
def f_clean_up_injector():
    yield
    injectable.reset()


def test_injector_register_new_class(f_clean_up_injector):
    @injectable()
    class Service:
        pass

    assert injectable.is_injectable(Service) is True
    assert injectable.get_injectable(Service) is Service


@pytest.mark.parametrize('key', [
    'service_name', 
    tuple(['namespace', 'service_name']),
    666,
])
def test_injector_register_singlethon_class_by_default(
    f_clean_up_injector, key: Hashable
):
    @injectable(key=key)
    class Service:
        ...
    
    assert injectable.get_injectable(Service) is Service
    assert injectable.is_singleton(Service) is True


@pytest.mark.parametrize('is_singleton', [
    True,
    False,
])
@pytest.mark.parametrize('key', [
    'service_name', 
    tuple(['namespace', 'service_name']),
    666,
])
def test_injector_register_new_class_with_custom_key(
    f_clean_up_injector, is_singleton: bool, key: Hashable
):
    @injectable(key=key, singleton=is_singleton)
    class Service:
        ...

    assert injectable.is_injectable(key) is True
    assert injectable.get_injectable(key) is Service
    assert injectable.is_singleton(key) is is_singleton

    assert injectable.is_injectable(Service) is True
    assert injectable.get_injectable(Service) is Service
    assert injectable.is_singleton(Service) is is_singleton



@pytest.mark.parametrize('is_singleton', [
    True,
    False,
])
@pytest.mark.parametrize('key', [
    'service_name', 
    tuple(['namespace', 'service_name']),
    666,
])
def test_injector_register_new_class_with_custom_key(
    f_clean_up_injector, is_singleton: bool, key: Hashable
):
    class Service:
        ...

    injectable.register(key, Service, is_singleton)

    assert injectable.is_injectable(key) is True
    assert injectable.get_injectable(key) is Service
    assert injectable.is_singleton(key) is is_singleton

    assert injectable.is_injectable(Service) is True
    assert injectable.get_injectable(Service) is Service
    assert injectable.is_singleton(Service) is is_singleton
