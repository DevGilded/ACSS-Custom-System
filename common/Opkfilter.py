def have_tail(text: str) -> bool:
    tails_characters = {
    'g', 'j', 'p', 'q', 'y',  # Lowercase letters with tails
    '₲', '₭', '₿',  # Currency symbols with tails (example)
    'ƒ', '₣', '₰',  # Other symbols with tails (example)
    '↙', '↧', '↲',  # Arrows and other symbols (example)
    }
    for letter in text:
        if letter in tails_characters:
            return True
    return False

# Filtering Step
# class <- ? -> function
# class

# get the data that need to be find e.i value
# check all dictionary
# if find goodz only store the keys else return Null
# check again all dictionary with all match primary key and foreign key

class DataBaseDictFilter:
    def __init__(self, data: dict, filter_: list | tuple | str):
        self._data = data
        self._filter = filter_
        self._filtered_id = {}

        if isinstance(self._filter, str):
            self.__filter(self._filter)

    def __filter_key(self):
        raise NotImplemented

    def __filter_item(self):
        raise NotImplemented

    def __filter(self, filter_: str):
        if self.__is_key(filter_, self._data):
            self.__filter_key()
        else:
            pass

    def __is_key(self, filter_: str | int, data) -> bool:
        for ky, it in data.items():
            if str(ky) == filter_:
                return True

            if isinstance(it, dict):
                return self.__is_key(filter_, it)

        return False


    def __repr__(self):
        raise NotImplemented
        pass