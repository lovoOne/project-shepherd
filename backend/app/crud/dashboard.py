from sqlalchemy.orm import Session

from app.models.member import Member
from app.models.user import User


def get_dashboard_stats(db: Session, current_user: User):

    if current_user.role == "super_admin":
        members_query = db.query(Member)
        users_query = db.query(User)

    else:
        members_query = db.query(Member).filter(
            Member.church_id == current_user.church_id
        )

        users_query = db.query(User).filter(
            User.church_id == current_user.church_id
        )

    total_members = members_query.count()

    active_members = members_query.filter(
        Member.is_active == True
    ).count()

    inactive_members = members_query.filter(
        Member.is_active == False
    ).count()

    male_members = members_query.filter(
        Member.gender == "masculino"
    ).count()

    female_members = members_query.filter(
        Member.gender == "femenino"
    ).count()

    baptized_members = members_query.filter(
        Member.baptized == True
    ).count()

    not_baptized_members = members_query.filter(
        Member.baptized == False
    ).count()

    total_users = users_query.count()

    return {
        "total_members": total_members,
        "active_members": active_members,
        "inactive_members": inactive_members,
        "male_members": male_members,
        "female_members": female_members,
        "baptized_members": baptized_members,
        "not_baptized_members": not_baptized_members,
        "total_users": total_users,
    }