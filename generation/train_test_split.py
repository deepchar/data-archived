def split_data(source_full, target_full, dest1, dest2, dest3, dest4):

    with open(source_full, "r") as f:
        data = f.readlines()

    with open(target_full, "r") as f:
        data1 = f.readlines()

    leng = len(data)
    leng1 = len(data1)

    print(leng)
    print(leng1)

    train_data = data[0:(leng * 80 // 100)]
    test_data = data[(leng * 80 // 100):leng]

    train_data1 = data1[0:(leng1 * 80 // 100)]
    test_data1 = data1[(leng1 * 80 // 100):leng1]


    ## saving train and test sets
    with open("../raw/" + dest1, "w") as f:
        f.writelines(train_data)
    with open("../raw/" + dest2, "w") as f:
        f.writelines(test_data)
    with open("../raw/" + dest3, "w") as f:
        f.writelines(train_data1)
    with open("../raw/" + dest4, "w") as f:
        f.writelines(test_data1)


path_source_full = "../raw/test/source.txt"
path_target_full = '../raw/test/target.txt'

source_train_path = "test/source_train.txt"
source_test_path = "test/source_test.txt"
target_train_path = "test/target_train.txt"
target_test_path = "test/target_test.txt"

## calling the splitting function
split_data(path_source_full, path_target_full, source_train_path, source_test_path, target_train_path, target_test_path)