from models.hero import HeroCreate, HeroUpdate
from models.joined import Hero, HeroRead, HeroReadWithTeam, Team, TeamRead, TeamReadWithHeroes
from models.student import StudentModel, UpdateStudentModel
from models.team import TeamCreate, TeamUpdate

__all__ = [
    # postgres
    Hero,
    HeroRead,
    Team,
    TeamRead,
    HeroCreate,
    HeroUpdate,
    TeamCreate,
    TeamUpdate,
    HeroReadWithTeam,
    TeamReadWithHeroes,
    # mongodb
    StudentModel,
    UpdateStudentModel,
]
