from dataclasses import dataclass
from requests import get, JSONDecodeError


BASE_URL = "https://akabab.github.io/superhero-api/api"

@dataclass
class Powerstats:
    intelligence: int
    strength: int
    speed: int
    durability:int
    power: int
    combat: int

@dataclass
class Appearance:
    gender: str
    race: str
    height: list[str]
    weight: list[str]
    eyeColor: str
    hairColor: str

@dataclass
class Biography:
    fullName: str
    alterEgos: str
    aliases: list[str]
    placeOfBirth: str
    firstAppearance: str
    publisher: str
    alignment: str

@dataclass
class Work:
    occupation: str
    base: str

@dataclass
class Connections:
    groupAffiliation: str
    relatives: str

@dataclass
class Images:
    xs: str = ""
    sm: str = ""
    md: str = ""
    lg: str = ""

@dataclass
class Superhero:
    id: int
    name: str
    slug: str
    powerstats: Powerstats | dict[str, str | list[str]]
    appearance: Appearance | dict[str, str | list[str]]
    biography: Biography | dict[str, str | list[str]]
    work: Work | dict[str, str]
    connections: Connections | dict[str, str]
    images: Images | dict[str, str]

    def __post_init__(self):
        if isinstance(self.powerstats, dict):
            self.powerstats = Powerstats(**self.powerstats)
        if isinstance(self.appearance, dict):
            self.appearance = Appearance(**self.appearance)
        if isinstance(self.biography, dict):
            self.biography = Biography(**self.biography)
        if isinstance(self.work, dict):
            self.work = Work(**self.work)
        if isinstance(self.connections, dict):
            self.connections = Connections(**self.connections)
        if isinstance(self.images, dict):
            self.images = Images(**self.images)

    def get_height_in_cm(self) -> int:
        value, unit = self.appearance.height[1].split()
        match unit:
            case 'cm':
                return int(value)
            case 'meters':
                return int(float(value) * 100)
            case _:
                return 0

    def has_work(self) -> bool:
        return self.work.occupation != '-'

def get_superheroes() -> list[Superhero]:
    try:
        response = get(BASE_URL + "/all.json")
        if response.status_code != 200:
            return []
        return [Superhero(**hero) for hero in response.json()]
    except JSONDecodeError:
        return []
    except Exception:
        raise ConnectionError()


def get_taller_superhero(gender: str, has_work: bool) -> Superhero | None:
    if not isinstance(has_work, bool) or not isinstance(gender, str):
        raise TypeError("has_work and gender must be bool or str")
    superheroes = get_superheroes()
    if not superheroes:
        return None

    filtered_superheroes = list(filter(
        lambda hero: hero.appearance.gender.lower() == gender.lower() and hero.has_work() == has_work,
        superheroes
    ))
    if len(filtered_superheroes) == 0:
        return None
    return max(filtered_superheroes, key=lambda hero: hero.get_height_in_cm())
