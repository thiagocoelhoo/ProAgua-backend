import os
import shutil
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Reset migrations and delete the SQLite database file.'

    def handle(self, *args, **options):
        migrations_path = os.path.join('src', 'apps', 'proagua_api', 'migrations')
        db_file = 'src/db.sqlite3'

        confirmation = input("Are you sure you want to reset the migrations and delete the database? [y/N]: ")

        if confirmation.lower() != "y":
            self.stdout.write(self.style.SUCCESS("Operação cancelada. Nada foi alterado."))
            return

        # Deletar arquivos de migração
        if os.path.exists(migrations_path):
            shutil.rmtree(migrations_path)
            self.stdout.write(self.style.SUCCESS("Pasta migrations excluída com sucesso."))

        else:
            self.stdout.write(self.style.ERROR("Pasta migrations não encontrada."))

        # Deletar o arquivo do banco de dados SQLite3
        if os.path.exists(db_file):
            os.remove(db_file)
            self.stdout.write(self.style.SUCCESS("Banco de dados deletado com sucesso."))
            
        else:
            self.stdout.write(self.style.ERROR("Banco de dados não encontrado."))


if __name__ == '__main__':
    command = Command()
    command.handle()