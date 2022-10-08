from api.books import router as book_router
from api.files import router as file_router
from api.heroes import router as hero_router
from api.teams import router as team_router
from api.tutorials import router as tutorial_router

__all__ = [hero_router, team_router, tutorial_router, file_router, book_router]
