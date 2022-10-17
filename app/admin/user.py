from sqladmin import ModelView

from app.model import User


class UserAdmin(ModelView, model=User):
    """Class for setting up the Admin panel for the User model"""

    # Permission
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    # Metadata
    name = "User Model"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    column_list = [User.id, User.email, User.username]
    column_searchable_list = [User.email]
    column_sortable_list = [User.id, User.email, User.username]

    # Details
    column_details_list = [User.id, User.username]

    # Pagination
    page_size = 50
    page_size_options = [25, 50, 100, 200]
