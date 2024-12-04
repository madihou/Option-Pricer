import pickle


class DataManager:

    @staticmethod
    def dump_data(obj):
        with open("data.pickle", "wb") as f:
            pickle.dump(obj, f)

    @staticmethod
    def load_data():
        with open("data.pickle", 'rb') as f:
            data = pickle.load(f)
        return data
