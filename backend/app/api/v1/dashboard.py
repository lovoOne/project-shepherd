from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_role
from app.crud.dashboard import get_dashboard_stats
from app.db.session import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardStats


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/",
    response_model=DashboardStats,
)
def read_dashboard(
    current_user: User = Depends(
        require_role(
            "admin",
            "super_admin",
            "secretary",
        )
    ),
    db: Session = Depends(get_db),
):
    return get_dashboard_stats(
        db,
        current_user,
    )