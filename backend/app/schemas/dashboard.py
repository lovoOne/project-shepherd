from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_members: int
    active_members: int
    inactive_members: int

    male_members: int
    female_members: int

    baptized_members: int
    not_baptized_members: int

    total_users: int