from pytest import raises
from glaciers import Glacier
from glaciers import GlacierCollection


def test_mass_balance():
    glacier = Glacier("AR", 12345, "AB", 0, 0, 0, 456)
    data_list = [["AB", 1998, 5555, 1], ["AB", 1998, 5555, 5], ["AB", 1998, 9999, 3]]
    mass_balance = glacier.add_mass_balance_measurement(1998, "AB", data_list)

    assert mass_balance == 6


def test_filter_by_code():
    file = GlacierCollection("sheet-A.csv")
    file.read_mass_balance_data("sheet-EE.csv")
    filtered_list = file.filter_by_code("4?4")

    assert filtered_list == ['AMEGHINO', 'AMALIA', 'ASIA', 'BALMACEDA', 'BERNARDO', 'CALVO', 'CHICO', 'DICKSON', 'EUROPA', 'FIERO', 'GREVE', 'GREY', 'HPS12', 'HPS13', 'HPS15', 'HPS19', 'HPS28', 'HPS29', 'HPS31', 'HPS34', 'HPS38', 'HPS41', 'HPS8', 'HPS9', 'LEONES', 'OCCIDENTAL', 'OFHIDRO', "O'HIGGINS", 'PENGUIN', 'PINGO', 'PIO XI (BRUEGGEN)', 'SAN RAFAEL', 'SNOWY', 'TEMPANO', 'BREIDAMJOKULL E. A.', 'BREIDAMJOKULL E. B.', 'BREIDAMJOKULL W. A.', 'FJALLSJOKULL BY BREIDAMERKURFJALL', 'FJALLSJOKULL BY GAMLASEL', 'FJALLSJOKULL FITJAR', 'GIGJOKULL', 'HEINABERGSJOKULL', 'HEINABERGSJOKULL H']


def test_sort_by_largest_mass_balance():
    file = GlacierCollection("sheet-A.csv")
    file.read_mass_balance_data("sheet-EE.csv")
    largest_list = file.sort_by_latest_mass_balance(2, False)

    assert largest_list == ['STORSTEINSFJELLBREEN', 'CAINHAVARRE']


def test_sort_by_smallest_mass_balance():
    file = GlacierCollection("sheet-A.csv")
    file.read_mass_balance_data("sheet-EE.csv")
    smallest_list = file.sort_by_latest_mass_balance(2, True)

    assert smallest_list == ['ARTESONRAJU', 'TUNSBERGDALSBREEN']


def test_input_of_glacier_class():
    with raises(ValueError) as exception:
        Glacier("ABC", 12345, "ABC", 0, 0, 0, 456)

    with raises(ValueError) as exception:
        Glacier("AB", 123456, "ABC", 0, 0, 0, 456)