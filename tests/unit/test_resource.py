import pytest
from app.models.inventory import Resource


@pytest.fixture
def resource_values():
    return {
        'name': 'Parrot',
        'manufacturer': 'Pirates A-Hoy',
        'total': 100,
        'allocated': 50
    }


@pytest.fixture
def resource(resource_values):
    return Resource(**resource_values)


def test_create_resource(resource_values, resource):
    for attr_name in resource_values:
        assert getattr(resource, attr_name) == resource_values.get(attr_name)


def test_invalid_total_type():
    with pytest.raises(TypeError):
        Resource('name', 'manufacturer', 10.5, 5)


def test_invalid_allocated_type():
    with pytest.raises(TypeError):
        Resource('name', 'manufacturer', 10, 5.5)


def test_invalid_total_value():
    with pytest.raises(ValueError):
        Resource('name', 'manufacturer', -10, 5)


def test_invalid_allocated_value():
    with pytest.raises(ValueError):
        Resource('name', 'manufacturer', 10, -5)


@pytest.mark.parametrize('total,allocated', [(10, -5), (10, 20)])
def test_create_invalid_allocate_value(total, allocated):
    with pytest.raises(ValueError):
        Resource('name', 'manufacturer', total, allocated)


def test_total(resource):
    assert resource.total == resource._total


def test_allocated(resource):
    assert resource.allocated == resource._allocated


def test_category(resource):
    assert resource.category == 'resource'


def test_available(resource):
    assert resource.available == resource._total - resource._allocated


def test_str_repr(resource):
    assert str(resource) == resource.name


def test_repr_repr(resource):
    assert repr(resource) == '{} ({} - {}) : total={}, allocated={}'.format(
        resource.name, resource.category, resource.manufacturer, resource.total,
        resource.allocated
    )


def test_claim(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.claim(n)
    assert resource.total == original_total
    assert resource.allocated == original_allocated + n


@pytest.mark.parametrize('value', [-1, 0, 1_000])
def test_claim_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.claim(value)


def test_free_up(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.free_up(n)
    assert resource.total == original_total
    assert resource.allocated == original_allocated - n


@pytest.mark.parametrize('value', [-1, 0, 51])
def test_free_up_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.free_up(value)


def test_died(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.died(n)
    assert resource.total == original_total - n
    assert resource.allocated == original_allocated - n


@pytest.mark.parametrize('value', [-1, 0, 51])
def test_died_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.died(value)


def test_purchased(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.purchased(n)
    assert resource.total == original_total + n
    assert resource.allocated == original_allocated


@pytest.mark.parametrize('value', [-1, 0])
def test_died_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.purchased(value)