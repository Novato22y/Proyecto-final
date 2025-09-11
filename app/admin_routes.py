from flask import Blueprint, render_template, abort, redirect, url_for, flash
from flask_login import current_user, login_required
from app.database import get_db_connection

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def check_admin():
    """Protege todas las rutas de este blueprint para que solo sean accesibles por administradores."""
    if not current_user.is_admin:
        abort(403)

@admin_bp.route('/users')
def list_users():
    """Muestra una lista de todos los usuarios registrados."""
    conn = get_db_connection()
    users = []
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, name, email, is_admin FROM users ORDER BY id")
            users_data = cur.fetchall()
            for row in users_data:
                users.append({'id': row[0], 'name': row[1], 'email': row[2], 'is_admin': row[3]})
        except Exception as e:
            flash(f"Error al consultar usuarios: {e}", "error")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    return render_template('admin_dashboard.html', users=users)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Elimina un usuario de la base de datos."""
    if user_id == current_user.id:
        flash("No puedes eliminar tu propia cuenta.", "error")
        return redirect(url_for('admin.list_users'))

    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            flash("Usuario eliminado correctamente.", "success")
        except Exception as e:
            flash(f"Error al eliminar el usuario: {e}", "error")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    return redirect(url_for('admin.list_users'))

@admin_bp.route('/update_role/<int:user_id>', methods=['POST'])
def update_role(user_id):
    """Actualiza el rol de un usuario a administrador o usuario normal."""
    # Evitar que el admin cambie su propio rol
    if user_id == current_user.id:
        flash("No puedes cambiar tu propio rol de administrador.", "error")
        return redirect(url_for('admin.list_users'))

    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            # Obtener el estado actual de is_admin
            cur.execute("SELECT is_admin FROM users WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            if user_data is not None:
                current_is_admin = user_data[0]
                # Alternar el estado de is_admin
                new_is_admin = not current_is_admin
                cur.execute("UPDATE users SET is_admin = %s WHERE id = %s", (new_is_admin, user_id))
                conn.commit()
                rol_txt = "Administrador" if new_is_admin else "Usuario"
                flash(f"Rol del usuario actualizado a {rol_txt}.", "success")
            else:
                flash("Usuario no encontrado.", "error")
        except Exception as e:
            flash(f"Error al actualizar el rol: {e}", "error")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    return redirect(url_for('admin.list_users'))
