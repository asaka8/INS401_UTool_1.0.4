import csv
class CsvCreator:

    def __init__(self, file_name):
        self._file_name = file_name
        self._field_names = []

    def create(self, field_names):
        self._field_names = field_names
        with open(self._file_name, 'a+', newline='') as out_file:
            writer = csv.DictWriter(out_file, fieldnames = field_names)
            writer.writeheader()

    def write_log(self, info_dicts):
        with open(self._file_name, 'a+', newline='') as out_file:
            writer = csv.DictWriter(out_file, fieldnames = self._field_names)
            writer.writerow(info_dicts)

    
