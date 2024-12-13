from special_dict import SpecialDict

def main():
    special_map = SpecialDict()
    special_map["value1"] = 1
    special_map["value2"] = 2
    special_map["value3"] = 3
    special_map["1"] = 10
    special_map["2"] = 20
    special_map["3"] = 30
    special_map["1, 5"] = 100
    special_map["5, 5"] = 200
    special_map["10, 5"] = 300
    special_map["1, 5, 3"] = 400

    print(special_map.iloc[0])  # >>> 10
    print(special_map.iloc[2])  # >>> 300
    print(special_map.iloc[5])  # >>> 200
    print(special_map.iloc[8])  # >>> 3

    print(special_map.ploc[">=1"])  # >>> {'1': 10, '2': 20, '3': 30}
    print(special_map.ploc["<3"])   # >>> {'1': 10, '2': 20}
    print(special_map.ploc[">0, >0"])  # >>> {'1, 5': 100, '5, 5': 200, '10, 5': 300}
    print(special_map.ploc[">=10, >0"])  # >>> {'10, 5': 300}
    print(special_map.ploc["<5, >=5, >=3"])  # >>> {'1, 5, 3': 400}

if __name__ == "__main__":
    main()
