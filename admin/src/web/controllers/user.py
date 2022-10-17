from flask import Blueprint, redirect, url_for, request, render_template, flash
from src.core.auth import (
    create_user,
    list_users,
    update_user,
    delete_user,
    get_user_by_id,
    disable_user,
    enable_user,
    add_role_to_user,
    get_roles,
    get_role,
    remove_role_to_user,
)
from src.core.auth.user import User
from src.web.forms.user import UserForm, UpdateUserForm
from passlib.hash import sha256_crypt
from src.web.helpers.form_utils import csrf_remover
from src.web.helpers.auth import login_required
from src.web.helpers.pagination import pagination_generator

user_blueprint = Blueprint("user", __name__, url_prefix="/usuarios")


@user_blueprint.get("/")
@login_required
def index():
    """Returns:
        HTML: List of users.
    """    
    # return render_template("user/list.html", users=list_users())

    pairs = [
        ("first_name", "Nombre"),
        ("last_name", "Apellido"),
        ("email", "Email"),
        ("username", "Usuario"),
    ]

    if request.args.get("search"):
        paginated_query_data = pagination_generator(
            list_users(request.args.get("column"), request.args.get("search")),
            request,
            "users",
        )
    else:
        paginated_query_data = pagination_generator(list_users(), request, "users")

    return render_template("user/list.html", pairs=pairs, **paginated_query_data)

@user_blueprint.get("/agregar")
@login_required
def get_add():
    """Returns:
        HTML: Form to create a user.
    """    
    return render_template(
        "user/add.html", form=UserForm(roles=list(map(lambda r: (r, r), get_roles())))
    )

@user_blueprint.post("/agregar")
@login_required
def post_add():
    """Returns:
        HTML: Redirect to user list.
    """    
    form = UserForm(request.form)
    if form.validate():
        form_encp = dict(form.data)
        if form_encp["roles"] != []:
            form_encp["password"] = sha256_crypt.encrypt(form_encp["password"])
            user = create_user(form_encp)
            user = get_user_by_id(user.id)
            for role in form_encp["roles"]:
                add_role_to_user(user, get_role(role))
        else:
            flash(f"Se deben asignar roles al usuario", category="alert alert-warning")
            return render_template(
                "user/add.html",
                form=UserForm(roles=list(map(lambda r: (r, r), get_roles()))),
            )
    return redirect(url_for("user.index"))

@user_blueprint.get("/actualizar/<id>")
@login_required
def get_update(id):
    """Args:
        id (int): User id.
    Returns:
        HTML: Form to update a user.
    """    
    user = get_user_by_id(id)
    form = UpdateUserForm(obj=user, roles=get_roles())
    return render_template("user/update.html", form=form)

@user_blueprint.post("/actualizar/<id>")
@login_required
def post_update(id):
    """Args:
        id (int): User id.
    Returns:
        HTML: Redirect to user list.
    """    
    form = UpdateUserForm(request.form)
    if form.validate():
        form = csrf_remover(form.data)
        roles_form = form.pop("roles")
        update_user(id, form)
        user = get_user_by_id(id)
        roles = get_roles()
        if roles_form != []:
            for role in roles:
                if role.name in roles_form:
                    add_role_to_user(user, role)
                else:
                    remove_role_to_user(user, role)
        else:
            flash(f"Se deben asignar roles al usuario", category="alert alert-warning")
            return render_template(
                "user/update.html",
                form=UpdateUserForm(obj=user, roles=get_roles()),
            )
        return redirect(url_for("user.index"))
    return render_template("user/update.html", form=form)


@user_blueprint.post("/borrar/<id>")
@login_required
def delete(id):
    """Args:
        id (int): Id of the user to delete.
    Returns:
        HTML: Redirect to user list.
    """    
    flash(f"Se elimino al usuario satisfactoriamente", category="alert alert-warning")
    delete_user(id)
    return redirect(url_for("user.index"))


@user_blueprint.post("/desactivar/<id>")
@login_required
def disable(id):
    """Args:
        id (int): Id of the user to disable.
    Returns:
        HTML: Redirect to user list.
    """    
    flash(
        f"Se deshabilito al usuario satisfactoriamente", category="alert alert-warning"
    )
    disable_user(id)
    return redirect(url_for("user.index"))


# disabling associates
@user_blueprint.post("/activar/<id>")
@login_required
def enable(id):
    """Args:
        id (int): Id of the user to enable.
    Returns:
        HTML: Redirect to user list.
    """    
    flash(f"Se habilito al usuario satisfactoriamente", category="alert alert-warning")
    enable_user(id)
    return redirect(url_for("user.index"))
