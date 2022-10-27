import pytest

from src import robots


def test_weapons_get_energy() -> None:
    """Test weapons, get energy method with various inputs."""
    assert robots.Weapons.get_energy('laser') == 6
    assert robots.Weapons.get_energy('spike') == 2
    assert robots.Weapons.get_energy('plasma_gun') == 12

    with pytest.raises(KeyError):
        assert robots.Weapons.get_energy('')
        assert robots.Weapons.get_energy('nonsense')

    with pytest.raises(AttributeError):
        assert robots.Weapons.get_energy(5)
        assert robots.Weapons.get_energy([0,1])
