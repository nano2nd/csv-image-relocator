import csv
from shutil import copyfile
import os

from csv_image_relocator.relocator_tools.image_data_row import ImageDataRow
from csv_image_relocator.relocator_tools import tools


class CsvParser:

    def __init__(self, input_file, status_text, export_directory):
        self.status_text = status_text
        self.input_file = input_file

        self.image_data = CsvParser._read_csv(input_file)
        if self.image_data is None or len(self.image_data) == 0:
            raise ValueError("Error reading file '{}'".format(input_file))

        self.file_count = self.count_files()
        self.current_file_count = 0

        self.destination = export_directory

    def copy_all_images(self):
        for data in self.image_data:
            self._copy_images(data)

    @staticmethod
    def _read_csv(filename):
        try:
            with open(filename, 'rt') as csvfile:
                csvfile.seek(0)
                csvfile.readline()  # skip first line
                reader = csv.reader(csvfile)

                image_data = []
                count = 0
                for row_data in reader:
                    image_data.append(ImageDataRow(row_data, count))
                    count += 1

                return image_data

        except ValueError:
            raise

    def count_files(self):
        return sum(data.image_file_count() for data in self.image_data)

    def _update_status_text_for_file_count(self):
        self.status_text.set('Moving {} of {} files'.format(self.current_file_count,
                                                            self.file_count))

    def _copy_images(self, data_row):
        dest_image_name = str.join('', [data_row.subject,
                                        '-', data_row.week_condition,
                                        '-', data_row.trip_num])

        if tools.is_valid_str(data_row.first_image_name):
            self._copy_image(data_row.media_directory,
                             data_row.first_image_name,
                             dest_image_name)

        if tools.is_valid_str(data_row.second_image_name):
            self._copy_image(data_row.media_directory,
                             data_row.second_image_name,
                             dest_image_name)

        if tools.is_valid_str(data_row.third_image_name):
            self._copy_image(data_row.media_directory,
                             data_row.third_image_name,
                             dest_image_name)

    def _copy_image(self, search_dir, search_term, dest_folder):
        if not bool(search_term):
            return

        self.current_file_count += 1
        self._update_status_text_for_file_count()

        try:
            found_file_name = tools.search_file(search_term, search_dir)
        except FileNotFoundError:
            raise ValueError("File containing {} could not be found in {}"
                             .format(search_term, search_dir))

        # Create destination if it does not exist
        os.makedirs(self.destination, exist_ok=True)

        dest_folder_path = self.destination + '/' + dest_folder
        os.makedirs(dest_folder_path, exist_ok=True)

        src_path = search_dir + '/' + found_file_name
        dest_path = dest_folder_path + '/' + found_file_name

        try:
            copyfile(src_path, dest_path)
        except:
            raise ValueError('Unable to copy image "{}"'.format(src_path))
