# gestion/management/commands/seed_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gestion.models import Rol, Empleado, Permiso

class Command(BaseCommand):
    help = 'Ejecuta el seeder para crear roles por defecto y usuarios de prueba'

    def handle(self, *args, **kwargs):
        roles_necesarios = ['Administrador', 'Mesero', 'Cajero']
        
        self.stdout.write("Iniciando el seeding de la base de datos...")

        for nombre_rol in roles_necesarios:
            # 1. Crear o recuperar el Rol
            rol, created_rol = Rol.objects.get_or_create(
                nombre=nombre_rol,
                defaults={'descripcion': f'Acceso total/parcial para el rol de {nombre_rol}'}
            )
            
            if created_rol:
                self.stdout.write(self.style.SUCCESS(f'Rol creado: {nombre_rol}'))

            # 2. Crear un Usuario de prueba para ese rol
            username = f"{nombre_rol.lower()}_test"
            email = f"{nombre_rol.lower()}@pastalavista.com"
            password = "password123"

            user, created_user = User.objects.get_or_create(username=username, email=email)
            
            if created_user:
                user.set_password(password) # Encripta la contraseña
                # Si es administrador, darle acceso al panel admin de Django por si acaso
                if nombre_rol == 'Administrador':
                    user.is_staff = True
                    user.is_superuser = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Usuario creado: {username} (Clave: {password})'))

            # 3. Vincular el Usuario con el modelo Empleado y asignarle el Rol
            # Nota: Ajusta 'rol=rol' si Jules le puso otro nombre a la llave foránea en el modelo Empleado
            empleado, created_emp = Empleado.objects.get_or_create(
                user=user,
                defaults={
                    'nombre': f'Empleado {nombre_rol}',
                    'telefono': '0000000000',
                    'rol': rol  
                }
            )

            if created_emp:
                self.stdout.write(self.style.SUCCESS(f'Empleado vinculado: {empleado.nombre} -> Rol: {nombre_rol}'))

        self.stdout.write(self.style.SUCCESS("Seeding completado con éxito."))