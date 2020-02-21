import pytest

from typing import Optional, Union, Dict, Hashable
from unittest.mock import Mock

from . import exceptions
from .container import Container, injectable


@pytest.mark.parametrize('context', [
    None,
    {},
])
def test_should_create_Container(context):
    container = Container(context)
    assert container


def test_should_create_simple_service_instance_0():
    injectable = Container()

    @injectable()
    class ServiceA:
        def __init__(self):
            pass

    assert isinstance(injectable.get(ServiceA), ServiceA)
    assert injectable.get(ServiceA) is injectable.get(ServiceA)


def test_should_create_simple_service_instance_1():
    injectable = Container()

    @injectable()
    class ServiceA:
        def foo():
            ...

    assert isinstance(injectable.get(ServiceA), ServiceA)
    assert injectable.get(ServiceA) is injectable.get(ServiceA)


def test_should_create_simple_service_instance_2():
    injectable = Container()

    @injectable()
    class ServiceA:
        def __init__(self, *args, **kwargs):
            pass

    assert isinstance(injectable.get(ServiceA), ServiceA)
    assert injectable.get(ServiceA) is injectable.get(ServiceA)


@pytest.mark.parametrize('key', (
    'name',
    1,
    tuple([1]),
    tuple(['abc']),
    tuple([object()]),
    tuple(['namespace', 'name']),
))
def test_should_create_simple_service_using_custom_key_0(
    key: Hashable
):
    injectable = Container()

    @injectable(key=key)
    class ServiceA:
        def __init__(self):
            pass

    assert isinstance(injectable.get(key), ServiceA)
    assert isinstance(injectable.get(ServiceA), ServiceA)
    assert injectable.get(ServiceA) is injectable.get(ServiceA)


def test_should_create_simple_non_singleton_service():
    injectable = Container()

    @injectable(key='service', singleton=False)
    class ServiceA:
        def __init__(self):
            ...

    assert isinstance(injectable.get('service'), ServiceA)
    assert isinstance(injectable.get(ServiceA), ServiceA)
    assert injectable.get(ServiceA) is not injectable.get(ServiceA)


def test_should_create_simple_service_using_factory():
    @injectable(singleton=False)
    class ServiceA:
        def __init__(self):
            pass

    instance_1 = injectable.get(ServiceA)
    instance_2 = injectable.get(ServiceA)

    assert isinstance(instance_1, ServiceA)
    assert isinstance(instance_2, ServiceA)
    assert instance_1 != instance_2


def test_should_create_singleton_service_using_factory_1():
    class ServiceA:
        def __init__(self, value: int):
            self.value = value

    injectable = Container({
        ServiceA: lambda inj: ServiceA(1)
    })
    injectable.register(ServiceA, ServiceA, True)

    instance_1 = injectable.get(ServiceA)
    instance_2 = injectable.get(ServiceA)

    assert isinstance(instance_1, ServiceA)
    assert isinstance(instance_2, ServiceA)
    assert instance_1 is instance_2


def test_should_create_non_singleton_service_using_factory_1():
    class ServiceA:
        def __init__(self, value: int):
            self.value = value

    injectable = Container({
        ServiceA: lambda inj: ServiceA(1)
    })
    injectable.register(ServiceA, ServiceA, False)

    instance_1 = injectable.get(ServiceA)
    instance_2 = injectable.get(ServiceA)

    assert isinstance(instance_1, ServiceA)
    assert isinstance(instance_2, ServiceA)
    assert instance_1 is not instance_2


@pytest.mark.parametrize('singleton', [
    True, False
])
def test_should_provide_value_instead_of_service_0(singleton: bool):
    class ServiceA:
        def __init__(self):
            pass

    injectable = Container({ServiceA: Mock()})
    injectable.register(ServiceA, ServiceA, singleton)
    instance_1 = injectable.get(ServiceA)
    instance_2 = injectable.get(ServiceA)

    assert isinstance(instance_1, Mock)
    assert isinstance(instance_2, Mock)
    assert instance_1 is instance_2


@pytest.mark.parametrize('singleton', [
    True, False
])
def test_should_provide_value_instead_of_service_1(singleton: bool):
    class ServiceA:
        def __init__(self):
            pass

    injectable = Container({ServiceA: lambda inj: Mock()})
    injectable.register(ServiceA, ServiceA, False)
    instance_1 = injectable.get(ServiceA)
    instance_2 = injectable.get(ServiceA)

    assert isinstance(instance_1, Mock)
    assert isinstance(instance_2, Mock)
    assert instance_1 is not instance_2


def test_should_create_transitive_non_singleton_service():
    injectable = Container()

    @injectable(singleton=False)
    class A:
        def __init__(self):
            pass

    @injectable()
    class B:
        def __init__(self, a: A):
            self.a = a

    @injectable()
    class C:
        def __init__(self, a: A):
            self.a = a

    instances = [injectable.get(B), injectable.get(C)]

    assert isinstance(instances[0], B)
    assert instances[0] is injectable.get(B)

    assert isinstance(instances[1], C)
    assert instances[1] is injectable.get(C)

    assert instances[0].a != instances[1].a
    assert instances[0].a != injectable.get(A)


def test_should_create_transitive_singleton_service():
    injectable = Container()

    @injectable(singleton=True)
    class A:
        def __init__(self):
            pass

    @injectable()
    class B:
        def __init__(self, a: A):
            self.a = a

    @injectable()
    class C:
        def __init__(self, a: A):
            self.a = a

    instances = [injectable.get(B), injectable.get(C)]

    assert isinstance(instances[0], B)
    assert instances[0] is injectable.get(B)

    assert isinstance(instances[1], C)
    assert instances[1] is injectable.get(C)

    assert instances[0].a is instances[1].a
    assert instances[0].a is injectable.get(A)


def test_instantiate_service_from_parent_container():
    root = Container()
    children = [
        Container(parent=root),
        Container(parent=root),
    ]

    class A:
        pass

    root.register(A, A, True)

    class B:
        def __init__(self, a: A):
            self.a = a

    children[0].register(B, B, True)

    class C:
        def __init__(self, a: A):
            self.a = a

    children[1].register(C, C, True)

    b, c = (children[0].get(B), children[1].get(C))

    assert isinstance(b, B)
    assert isinstance(b.a, A)
    assert isinstance(c, C)
    assert isinstance(c.a, A)

    assert b.a is c.a


def test_instantiate_service_from_parent_container_using_context():
    root = Container({
        'service_a': object()
    })
    children = [
        Container(parent=root),
        Container(parent=root),
    ]

    class A:
        pass

    root.register('service_a', A, True)

    class B:
        def __init__(self, a: A):
            self.a = a

    children[0].register(B, B, True)

    class C:
        def __init__(self, a: A):
            self.a = a

    children[1].register(C, C, True)

    b, c = (children[0].get(B), children[1].get(C))

    assert isinstance(b, B)
    assert isinstance(b.a, A)
    assert isinstance(c, C)
    assert isinstance(c.a, A)

    assert b.a is c.a


def test_should_create_service_using_factory():
    container = Container()

    class A:
        pass

    class B:
        def __init__(self, a: A):
            self.a = a

    class C:
        def __init__(self, b: B, value: int):
            self.b = b
            self.value = value

    container.register(A, A, True)
    container.register(B, B, True)
    container.register(C, C, True)
    container.context = {
        C: lambda injector: C(injector.get(B), 999)
    }

    instance = container.get(C)

    assert isinstance(instance, C)
    assert isinstance(instance.b, B)
    assert instance.b is container.get(B)

    assert isinstance(instance.b.a, A)
    assert instance.b.a is container.get(A)

    assert instance.value == 999
    assert instance is container.get(C)


def test_should_raise_exception_with_non_injectable_argument_0():
    injectable = Container()

    @injectable()
    class A:
        pass

    @injectable()
    class B:
        def __init__(self, a: A):
            self.a = a

    @injectable()
    class C:
        def __init__(self, b: B, value: int):
            self.service_b = b
            self.value = value

    with pytest.raises(exceptions.NonInjectableArgument) as handler:
        injectable.get(C)

    assert handler.value.client is C
    assert handler.value.argument_name == 'value'
    assert handler.value.argument_type is int


def test_should_raise_exception_with_non_injectable_argument_1():
    container = Container()

    class A:
        pass

    class B:
        def __init__(self, a: A):
            self.a = a

    container.register(B, B, True)

    with pytest.raises(exceptions.NonInjectableArgument) as handler:
        container.get(B)

    assert handler.value.client is B
    assert handler.value.argument_name == 'a'
    assert handler.value.argument_type is A


def test_raise_error_when_getting_non_registered_service():
    class A:
        pass

    container = Container({})

    with pytest.raises(exceptions.NonInjectableClass) as handler:
        container.get(A)

    assert handler.value.klass is A


def test_should_provide_services_using_union_typing_0():
    injectable = Container()

    @injectable()
    class JsonLogger:
        pass

    @injectable()
    class PlainFileLogger:
        pass

    @injectable()
    class ServiceC:
        def __init__(
            self, service: Union[JsonLogger, PlainFileLogger]
        ):
            self.service = service

    c = injectable.get(ServiceC)
    assert isinstance(c.service, JsonLogger)


def test_should_provide_services_using_union_typing_1():
    injectable = Container()

    class JsonLogger:
        pass

    @injectable()
    class PlainFileLogger:
        pass

    @injectable()
    class ServiceC:
        def __init__(
            self, service: Union[JsonLogger, PlainFileLogger]
        ):
            self.service = service

    c = injectable.get(ServiceC)
    assert isinstance(c.service, PlainFileLogger)


def test_should_provide_optional_service_0():
    injectable = Container()

    @injectable()
    class ServiceA:
        def __init__(self):
            pass

    @injectable()
    class ServiceB:
        def __init__(
            self, service: Optional[ServiceA]
        ):
            self.service = service

    b = injectable.get(ServiceB)
    assert isinstance(b.service, ServiceA)
