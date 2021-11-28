import csv
import matplotlib.pyplot as plt
from utils import haversine_distance


class Glacier:
    def __init__(self, political_unity, glacier_id, name, unit, lat, lon, code):
        self.political_unity = political_unity
        self.glacier_id = glacier_id
        self.name = name
        self.unit = unit
        self.lat = lat
        self.lon = lon
        self.code = code

        if len(political_unity) != 2:
            raise ValueError(
                "Political unity should have 2 digits")

        if len(str(glacier_id)) != 5:
            raise ValueError(
                "Glacier ID should have 5 digits")

        if lat > 90 or lat < -90:
            raise ValueError(
                "The latitude should be between -90 and 90")

        if lon > 180 or lon < -180:
            raise ValueError(
                "The longitude should be between -180 and 180")

    def add_mass_balance_measurement(self, year, glacier_name, data_list):
        """Due to my own coding logic for the whole file, this function only works for the sub-region measurements"""
        """The code in the sort_by_latest_mass_balance function can directly tell if it is processing a sub-region"""
        """or a whole region measurement"""

        if year > 2021:
            raise ValueError(
                "The year number should make sense (e.g. not in the future)")

        if type(year) != int:
            raise TypeError(
                "The year number should be an integer"
            )

        mass_measurement = 0
        for i in data_list:
            if i[2] != 9999:
                if i[0] == glacier_name:
                    if i[1] == year:
                        mass_measurement = mass_measurement + i[3]

        if type(mass_measurement) != int:
            raise TypeError(
                "The mass measurement should be an integer"
            )

        return mass_measurement

    def plot_mass_balance(self, input_path, output_path):
        """Get the file data by read_mass_balance_data method"""
        data_dict = GlacierCollection.read_mass_balance_data(self, input_path)

        year_list = []
        mass_balance_list =[]
        for k in data_dict:
            if k[0] == self.name:
                year_list.append(k[1])
                mass_balance_list.append(data_dict[k])

        plt.plot(year_list, mass_balance_list, color='b', label="Mass balance curve")
        plt.ylabel('Mass Balance')
        plt.xlabel('Year')
        plt.legend()
        plt.savefig(output_path)
        plt.show()

        
class GlacierCollection:
    def __init__(self, file_path):
        self.file_path = file_path
        self.mass_balance_data_dict = {}

    def read_mass_balance_data(self, file_path):
        """Open a file and keep the data for further processing"""
        file = open(file_path, encoding='utf-8')
        csv_f = csv.reader(file)
        next(csv_f)

        result_dict = {}
        result_list = []
        for row in csv_f:
            if row[11] != "":
                result_dict[row[1], int(row[3])] = int(row[11])
                result_list.append([row[1], int(row[3]), int(row[4]), int(row[11])])

        for i1 in result_list:
            if i1[2] != 9999:
                result_dict[i1[0], i1[1]] = Glacier.add_mass_balance_measurement(self, i1[1], i1[0], result_list)

        self.mass_balance_data_dict = result_dict

        return result_dict

    def find_nearest(self, lat, lon, n):
        """Get the n glaciers closest to the given coordinates."""

        """Get the file from the argument in '__init__'"""
        file = open(self.file_path, encoding='utf-8')
        csv_f = csv.reader(file)
        next(csv_f)

        result_list = []
        distance_list = []
        for row in csv_f:
            d = haversine_distance(lat, lon, float(row[5]), float(row[6]))
            name = row[1]
            result_list.append({d: name})
            distance_list.append(d)

        distance_list.sort()

        sorted_result_list = []
        checklist = []
        for i in range(len(distance_list)):
            for k in range(len(result_list)):
                if distance_list[i] == list(result_list[k].keys())[0]:
                    if result_list[k] not in checklist:
                        if len(sorted_result_list) < n:
                            sorted_result_list.append(list(result_list[k].values())[0])
                            checklist.append(result_list[k])

        return sorted_result_list
    
    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""

        """Get the file from the argument in '__init__'"""
        file = open(self.file_path, encoding='utf-8')
        csv_f = csv.reader(file)
        next(csv_f)

        """Search the pattern code in each row and compare it with the given code_pattern"""
        filter_result = []
        for row in csv_f:
            """i2 is the index of the first list in the row that we need to check"""
            i2 = 7
            for i1 in range(len(code_pattern)):
                match_or_not = True
                if code_pattern[i1] == "?":
                    i2 = i2 + 1
                    continue
                else:
                    if row[i2] == code_pattern[i1]:
                        i2 = i2 + 1
                        continue
                    else:
                        match_or_not = False
                        break

            if match_or_not:
                filter_result.append(row[1])

        """Return the result list"""
        return filter_result

    def sort_by_latest_mass_balance(self, n, reverse):
        """Return the N glaciers with the highest area accumulated in the last measurement."""

        """Get the file data from the mass_balance_data_dict"""
        data_dict = self.mass_balance_data_dict
        latest_data_dict = {}

        for k in data_dict:
            if k[0] in list(latest_data_dict.keys()):
                if k[1] >= latest_data_dict[k[0]][0]:
                    latest_data_dict[k[0]] = [k[1], data_dict[k]]
            else:
                latest_data_dict[k[0]] = [k[1], data_dict[k]]

        total_glaciers_list = []
        for k in latest_data_dict:
            total_glaciers_list.append({k: [latest_data_dict[k][0], latest_data_dict[k][1]]})

        for i in range(len(total_glaciers_list)):
            for j in range(i + 1, len(total_glaciers_list)):
                if list(total_glaciers_list[i].values())[0][1] < list(total_glaciers_list[j].values())[0][1]:
                    total_glaciers_list[i], total_glaciers_list[j] = total_glaciers_list[j], total_glaciers_list[i]

        sorted_glaciers_list = total_glaciers_list

        final_largest_latest_list = []
        for i in range(len(sorted_glaciers_list)):
            final_largest_latest_list.append(list(sorted_glaciers_list[i].keys())[0])

        if reverse:
            final_largest_latest_list.reverse()
            n_latest_glaciers_list = final_largest_latest_list[0:n]
        else:
            n_latest_glaciers_list = final_largest_latest_list[0:n]

        return n_latest_glaciers_list

    def summary(self):
        """Get the file data from the mass_balance_data_dict"""
        data_dict = self.mass_balance_data_dict

        glaciers_set = set()
        year_list = []
        latest_data_dict = {}

        for k in data_dict:
            if k[0] not in glaciers_set:
                glaciers_set.add(k[0])

            year_list.append(k[1])

            for k in data_dict:
                if k[0] in list(latest_data_dict.keys()):
                    if k[1] >= latest_data_dict[k[0]][0]:
                        latest_data_dict[k[0]] = [k[1], data_dict[k]]
                else:
                    latest_data_dict[k[0]] = [k[1], data_dict[k]]

        number_of_glaciers = len(glaciers_set)
        print("This collection has {} glaciers.".format(number_of_glaciers))

        year_list.sort()
        print("The earliest measurement was in {}.".format(str(year_list[0])))

        number_of_shrunk_glaciers = 0
        for k in latest_data_dict:
            if latest_data_dict[k][1] < 0:
                number_of_shrunk_glaciers = number_of_shrunk_glaciers + 1
        shrunk_percentage = round(100*(number_of_shrunk_glaciers/number_of_glaciers))
        print("{}% of glaciers shrunk in their last measurement.".format(shrunk_percentage))

    def plot_extremes(self, output_path):
        largest_glacier = self.sort_by_latest_mass_balance(1, True)[0]
        smallest_glacier = self.sort_by_latest_mass_balance(1, False)[0]

        largest_glacier_x = []
        largest_glacier_y = []
        smallest_glacier_x = []
        smallest_glacier_y = []

        """Get the file data from the mass_balance_data_dict"""
        data_dict = self.mass_balance_data_dict

        """Get the values for the plot"""
        for k in data_dict:
            if k[0] == largest_glacier:
                largest_glacier_x.append(k[1])
                largest_glacier_y.append(data_dict[k])
            if k[0] == smallest_glacier:
                smallest_glacier_x.append(k[1])
                smallest_glacier_y.append(data_dict[k])

        """Plot the data and show & save the plot"""
        plt.plot(largest_glacier_x, largest_glacier_y, color='b', label="The glacier that grew the most")
        plt.plot(smallest_glacier_x, smallest_glacier_y, color='r', label="The glacier that shrunk the most")
        plt.ylabel('Mass Balance')
        plt.xlabel('Year')
        plt.legend()
        plt.savefig(output_path)
        plt.show()