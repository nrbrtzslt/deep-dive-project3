import pytest
from app.utils.validators import validate_integer


class TestIntegerValidator:
    def test_validate_integer_ok(self):
        validate_integer('arg', 10, 0, 20, 'min msg', 'max msg')

    def test_validate_float(self):
        with pytest.raises(TypeError):
            validate_integer('arg', 10.5)

    def test_validate_min_value(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 10, 20)
        assert 'arg' in str(ex.value)
        assert '20' in str(ex.value)

    def test_validate_max_value(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 10, max_value=5)
        assert 'arg' in str(ex.value)
        assert '5' in str(ex.value)

    def test_custom_min_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 10, 100, custom_min_message='Custom min msg.')
        assert 'Custom min msg.' == str(ex.value)

    def test_custom_max_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 10, max_value=5, custom_max_message='Custom max msg.')
        assert 'Custom max msg.' == str(ex.value)
