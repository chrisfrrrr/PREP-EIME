# PREP-EIME v1.11.0 — Registro institucional y aprobación

## Instalación
1. Respaldar GitHub y Supabase antes de cambios.
2. Ejecutar `migration_1110_registro_aprobacion.sql` **una vez** en SQL Editor de Supabase.
3. En Supabase Authentication > Providers > Email, habilitar confirmación de correo electrónico. Revisar el SMTP y los límites de envío de correo.
4. Actualizar el código en GitHub, incluyendo `modules/student_access.py`.
5. Si cuenta con un logo autorizado, agregar `assets/logo_institucional.png`. No se incorpora ningún emblema oficial sin un archivo suministrado.
6. Desplegar en Streamlit Cloud.

## Flujo
- El estudiante solicita acceso con correo @ingenieria.usac.edu.gt, carné, nombre y carrera.
- Supabase registra su usuario y el trigger crea un perfil `pendiente` con rol fijo `estudiante`.
- La confirmación del correo se realiza por el proveedor de Supabase, si está habilitada.
- El administrador abre `Usuarios y cohortes`, aprueba o rechaza la solicitud.
- Solo perfiles con `status=activo` pueden entrar a PREP-EIME.

## Seguridad
- La restricción de dominio se aplica en la base de datos (no solo en el formulario).
- El rol no se recibe del usuario, siempre se crea `estudiante`.
- Las funciones de gestión comprueban rol `administrador` activo en servidor.
- El disparador de dominio afecta **nuevas cuentas** de Supabase, incluidas las creadas manualmente desde Authentication. Para crear cuentas institucionales administrativas nuevas, deberán usar el dominio permitido o ajustar la política conscientemente.
- Los perfiles existentes no se alteran. El registro no activa acceso hasta la aprobación.
- No usar la service_role key en Streamlit Secrets.

## Pruebas obligatorias
1. Registro con Gmail: rechazado por interfaz y por servidor.
2. Registro con correo institucional: perfil pendiente.
3. Intento de ingreso pendiente: bloqueado.
4. Administrador aprueba; ingreso confirmado permitido.
5. Estudiante no puede llamar las funciones administrativas RPC.
6. Verificar que la navegación del guardado unificado y las notas publicadas sigan funcionando.
7. Comprobar que Streamlit Cloud mantiene memoria estable.

## Límites
No se ha probado el SQL en la instancia real del usuario. Si ya existen triggers en auth.users que crean perfiles, revisar la compatibilidad antes de ejecutar. No hay logo oficial adjunto.
