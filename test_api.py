import pytest
from api import get_taller_superhero, get_superheroes, Superhero


@pytest.fixture(scope="module")
def superheroes() -> dict[int, Superhero]:
    return {hero.id: hero for hero in get_superheroes()}


@pytest.mark.parametrize('gender, has_work, expected_id',
                         [('male', False, 728),
                          ('Male', True, 681),
                          ('FEMALE', False, 42),
                          ('FeMalE', True, 284),])
@pytest.mark.xfail(raises=ConnectionError)
def test_get_taller_superhero(gender: str, has_work: bool, expected_id: int, superheroes):
    assert get_taller_superhero(gender, has_work) == superheroes[expected_id]

@pytest.mark.parametrize('gender, has_work',
                         [('no_gender', False),
                          ('', True),])
@pytest.mark.xfail(raises=ConnectionError)
def test_get_taller_superhero_wrong_gender(gender: str, has_work: bool):
    assert get_taller_superhero(gender, has_work) is None

@pytest.mark.parametrize('gender, has_work',
                         [(42, True),
                          ('', None),
                          (None, None)])
def test_get_taller_superhero_wrong_attrs(gender, has_work):
    with pytest.raises(TypeError):
        get_taller_superhero(gender, has_work)