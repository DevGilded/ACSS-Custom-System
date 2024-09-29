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
        self._found = {}

        if isinstance(self._filter, str):
            self._found.update(self.__filter(self._filter))
        elif isinstance(self._filter, list):
            filtered_list = []
            for f in self._filter:
                filtered_list.append(self.__filter(f))

            for filtered in filtered_list:
                for table, field in filtered.items():
                    # print()
                    if table not in self._found:
                        self._found[table] = field
                    else:
                        self._found[table].update(field)


    def __filter_key(self, filter_: str, data):
        result = {}
        # find the ID of the filter
        for ky, it in data.items():
            if isinstance(it, dict):
                found = self.__filter_key(filter_, it)
                if found:
                    result.update({ky: found})
            elif str(ky) == filter_:
                try:
                    return {filter_: data['PI_ID']}
                except:
                    return {filter_: data['ID']}

        if result:
            return result

    def __filter_item(self, filter_: str, data):
        result = {}
        # find the ID of the filter
        for ky, it in data.items():
            if isinstance(it, dict):
                found = self.__filter_item(filter_, it)
                if found:
                    result.update({ky: found})
                continue

            if filter_ in str(it).split(', '):
                try:
                    return {filter_: data['PI_ID']}
                except:
                    return {filter_: data['ID']}

        if result:
            return result

    def __find_filtered_id(self, filtered_id: dict):
        filtered_id = [[id_ for id_, _ in column.items()] for _, column in filtered_id.items()][0]

        result = {}
        for table, field in self._data.items():
            result[table] = {}
            for i, v in field.items():
                if i in filtered_id:
                    result[table].update({i: v})

        if result:
            return result


    def __filter(self, filter_: str):
        if self.__is_key(filter_, self._data): # if the filter is a field
            return self.__find_filtered_id(self.__filter_key(filter_, self._data))
        elif self.__is_item(filter_, self._data): # if the filter is a value
            return self.__find_filtered_id(self.__filter_item(filter_, self._data))
        else:
            pass

    def __is_key(self, filter_: str | int, data) -> bool:
        for ky, it in data.items():
            if isinstance(it, dict):
                if self.__is_key(filter_, it):
                    return True

            if str(ky) == filter_:
                return True

        return False

    def __is_item(self, filter_: str | int, data) -> bool:
        for ky, it in data.items():
            if isinstance(it, dict):
                if self.__is_item(filter_, it):
                    return True

            if filter_ in str(it).split(', '):
                return True

        return False


    def found(self):
        return self._found
