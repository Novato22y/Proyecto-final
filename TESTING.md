# Guía de Pruebas (Testing Guide)

Este documento describe los pasos para probar las funcionalidades clave implementadas en la aplicación, incluyendo el panel de administración, la integración con Google Calendar y la página de perfil.

## Prerrequisitos

- La aplicación debe estar ejecutándose localmente (`python run.py`).
- Se recomienda tener al menos dos usuarios registrados para las pruebas: un administrador (`admin@planeador.com`) y un usuario de prueba (ej. `test@user.com`).

---

## 1. Prueba del Panel de Administración

**Objetivo:** Verificar que el panel de administración funciona correctamente y que solo los administradores pueden acceder a él.

**Pasos a seguir:**

1.  **Acceso Denegado para Usuario Normal:**
    *   Inicia sesión con una cuenta de usuario normal (ej. `test@user.com`).
    *   Intenta navegar directamente a la URL `/admin/users`.
    *   **Resultado esperado:** Deberías ver una página de error "403 Forbidden" o ser redirigido, indicando que no tienes permiso.

2.  **Acceso Permitido para Administrador:**
    *   Cierra sesión y vuelve a iniciarla con la cuenta de administrador: `admin@planeador.com` / `contraseña`.
    *   Navega a `/admin/users` (si no hay un enlace directo, puedes escribir la URL).
    *   **Resultado esperado:** Deberías ver la página "Gestión de Usuarios" con una tabla que lista todos los usuarios registrados.

3.  **Prueba de Eliminación de Usuario:**
    *   En la tabla de usuarios, localiza la fila del usuario de prueba (`test@user.com`).
    *   Haz clic en el botón **"Eliminar"**. Acepta la confirmación.
    *   **Resultado esperado:** La página se recargará y el usuario de prueba ya no aparecerá en la lista.

4.  **Prueba de Actualización de Rol:**
    *   Crea un nuevo usuario de prueba si eliminaste el anterior.
    *   En el panel de administración, localiza al nuevo usuario (que tendrá el rol `usuario`).
    *   Haz clic en el botón **"Cambiar Rol"**.
    *   **Resultado esperado:** La página se recargará y el rol del usuario debería haber cambiado a `administrador`.

---

## 2. Prueba de la Integración con Google Calendar

**Objetivo:** Asegurarse de que un usuario puede conectar y desconectar su cuenta de Google para ver sus eventos.

**Pasos a seguir:**

1.  **Conectar la Cuenta:**
    *   Inicia sesión con una cuenta de usuario normal.
    *   En la página principal, busca la sección "GOOGLE CALENDAR" en la barra lateral.
    *   Haz clic en el enlace **"Conectar con Google Calendar"**.
    *   Serás redirigido a la página de consentimiento de Google. Inicia sesión y concede los permisos.
    *   **Resultado esperado:** Serás redirigido de vuelta a la página principal. Debería aparecer un mensaje flash de éxito y, en la barra lateral, ahora verás una lista de tus próximos 10 eventos del calendario y un enlace para "Desconectar".

2.  **Desconectar la Cuenta:**
    *   Con la cuenta ya conectada, haz clic en el enlace **"Desconectar cuenta de Google"**.
    *   **Resultado esperado:** La página se recargará. La lista de eventos desaparecerá y volverás a ver el enlace original para "Conectar con Google Calendar".

---

## 3. Prueba de la Página de Perfil

**Objetivo:** Verificar que la página de perfil es accesible y muestra la información correcta.

**Pasos a seguir:**

1.  **Acceso al Perfil:**
    *   Inicia sesión con cualquier cuenta (administrador o normal).
    *   En la barra de navegación superior, haz clic en tu nombre de usuario (ej. "Hola, [Tu Nombre]").
    *   **Resultado esperado:** Serás redirigido a la página `/profile`.

2.  **Verificación de Datos:**
    *   En la página de perfil, comprueba que la información mostrada (Nombre, Correo Electrónico y Rol) coincide con la del usuario con el que has iniciado sesión.
    *   **Resultado esperado:** Todos los datos deben ser correctos.
