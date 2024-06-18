from csv import reader

from django.core.management.base import BaseCommand

from api.models import AttributeType, Attribute


class Command(BaseCommand):
    """Загрузка типов атрибутов и самих атрибутов."""
    help = "Загрузка CSV-файлов в базу данных."

    def handle(self, *args, **kwargs):
        count = 0
        with open('data/attributes_types.csv', 'r',
                  encoding='UTF-8') as attr_types:
            for type_name in reader(attr_types):
                try:
                    AttributeType.objects.get_or_create(type_name=type_name[0])
                    count += 1
                    print(type_name[0])
                except Exception as error:
                    print(error)
        print('Импорт типов атрибутов закончен, итого {} типов записано в БД'.format(count))

        with open('data/attributes.csv', 'r', encoding='UTF-8') as attrs:
            for field_name, attr_type, label, help_text, is_uniq in reader(attrs):
                try:
                    attr_type = AttributeType.objects.get(type_name=attr_type)
                    Attribute.objects.get_or_create(
                        field_name=field_name, attr_type=attr_type,
                        label=label, help_text=help_text, is_uniq=is_uniq
                    )
                except Exception as error:
                    print(error)
        print('Импорт атрибутов закончен')
