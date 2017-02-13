from csv_image_relocator.relocator_tools import tools


class ImageDataRow:

    def __init__(self, row_data, index):
        self.index = index

        self._parse_row(row_data)
        self._check_valid()

    def _check_valid(self):
        if not tools.is_valid_str(self.subject):
            raise ValueError(self._error_message('subject'))
        if not tools.is_valid_str(self.week_condition):
            raise ValueError(self._error_message('weekconditionvec'))
        if not tools.is_valid_str(self.trip_num):
            raise ValueError(self._error_message('tripnumlabel'))
        if not tools.is_valid_str(self.media_directory):
            raise ValueError(self._error_message('mediadirectory'))

        return True

    def _parse_row(self, row_data):
        self.subject = row_data[1]
        self.week_condition = row_data[2]
        self.trip_num = row_data[4]
        self.media_directory = row_data[6]

        self.first_image_name = ''
        self.second_image_name = ''
        self.third_image_name = ''

        if not tools.is_na(row_data[8]) and tools.is_valid_str(row_data[8]):
            self.first_image_name = row_data[8]
        if not tools.is_na(row_data[9]) and tools.is_valid_str(row_data[9]):
            self.second_image_name = row_data[9]
        if not tools.is_na(row_data[10]) and tools.is_valid_str(row_data[10]):
            self.third_image_name = row_data[10]

    def image_file_count(self):
        count = 0
        if tools.is_valid_str(self.first_image_name) and not tools.is_na(self.first_image_name):
            count += 1
        if tools.is_valid_str(self.second_image_name) and not tools.is_na(self.first_image_name):
            count += 1
        if tools.is_valid_str(self.third_image_name) and not tools.is_na(self.first_image_name):
            count += 1

        return count

    def _error_message(self, invalid_col_name):
        return 'Row {} has invalid data for {}'.format(self.index, invalid_col_name)
