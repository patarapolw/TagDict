import pyexcel
import pyexcel_export
import re
from collections import OrderedDict
from IPython.display import IFrame

from TagDict.tags import tag_reader, to_raw_tags


class TagDict:
    def __init__(self, filename: str):
        """

        :param str filename:
        >>> len(TagDict('../user/PathoDict.xlsx').keywords)
        35
        >>> len(TagDict('../user/PathoDict.xlsx').tags)
        1
        """
        self.filename = filename

        # Don't forget to update 3 entries at a time!!!
        self.entries = OrderedDict()
        self.keywords = dict()
        self.tags = dict()

        try:
            for raw_entry in pyexcel.iget_records(file_name=self.filename, sheet_name='TagDict'):
                front = raw_entry['Front'].lower()

                if front == '':
                    break
                self.entries[front] = raw_entry

                self.keywords.setdefault(front, set()).add(front)
                for keyword in tag_reader(raw_entry['Additional keywords']):
                    self.keywords.setdefault(keyword.lower(), set()).add(front)

                for tag in tag_reader(raw_entry['Tags']):
                    self.tags.setdefault(tag.lower(), set()).add(front)
        except FileNotFoundError:
            pass

    def save(self):
        data = OrderedDict()
        data['TagDict'] = []

        data['TagDict'].append(list(list(self.entries.values())[0].keys()))

        assert data['TagDict'][0] == ['Front', 'Back', 'Additional keywords', 'Tags']

        for entry in self.entries.values():
            data['TagDict'].append(list(entry.values()))

        for matrix in data['TagDict']:
            for row in matrix:
                for cell in row:
                    assert isinstance(cell, (int, str, bool))

        pyexcel_export.save_data(self.filename, data)

    def add(self, front: str, data='', additional_keywords: iter=None, tags: iter=None):
        if additional_keywords is None:
            additional_keywords = list()
        if tags is None:
            tags = list()

        front = front.lower()

        if front in self.entries.keys():
            back = self.entries[front]['Back']
            if len(back) > 0 and back[-1] != '\n':
                back += '\n'
            back += data

            self.update(front, data=back, additional_keywords=additional_keywords, tags=tags)

            return self._view_entries(self.entries[front])
        else:
            self.entries[front] = OrderedDict({
                'Front': front,
                'Back': data,
                'Additional keywords': to_raw_tags(additional_keywords),
                'Tags': to_raw_tags(tags)
            })
            self.save()

            keywords = set()
            keywords.add(front)
            keywords.update(additional_keywords)

            for keyword in keywords:
                self.keywords.setdefault(keyword.lower(), set()).add(front)

            for tag in self.tags:
                self.tags.setdefault(tag.lower(), set()).add(front)

            return self._view_entries(self.entries[front])

    def update(self, front: str, data: str=None, additional_keywords: iter=None, tags: iter=None):
        if additional_keywords is None:
            additional_keywords = list()
        if tags is None:
            tags = list()

        front = front.lower()
        if data is not None:
            self.entries[front]['Back'] = data

        additional_keywords.extend(tag_reader(self.entries[front]['Additional keywords']))
        self.entries[front]['Additional keywords'] = to_raw_tags(additional_keywords)

        tags.extend(tag_reader(self.entries[front]['Tags']))
        self.entries[front]['Tags'] = to_raw_tags(tags)

        self.save()

        for keyword in additional_keywords:
            self.keywords.setdefault(keyword.lower(), set()).add(front)

        for tag in tags:
            self.tags.setdefault(tag.lower(), set()).add(front)

        return self._view_entries(self.entries[front])

    def remove(self, front: str):
        self.entries.pop(front)
        self.save()

        to_pop = []
        for k, v in self.keywords.items():
            if front in v:
                self.keywords[k].remove(front)
            if len(self.keywords[k]) == 0:
                to_pop.append(k)
        for k in to_pop:
            self.keywords.pop(k)

        to_pop = []
        for k, v in self.tags.items():
            if front in v:
                self.tags[k].remove(front)
            if len(self.tags[k]) == 0:
                to_pop.append(k)
        for k in to_pop:
            self.tags.pop(k)

        return 'Removed'

    def find(self, keyword_regex: str='', tags: list=None):
        if tags is None:
            tags = list()

        matched_entries = set()
        for word, fronts in self.keywords.items():
            for front in fronts:
                if re.search(keyword_regex, word, flags=re.IGNORECASE):
                    matched_entries.add(front)

        for entry in matched_entries:
            if len(tags) == 0:
                yield self.entries[entry]
            elif all([tag in tag_reader(self.entries[entry]['Tags']) for tag in tags]):
                yield self.entries[entry]

    def view(self, keyword_regex: str='', tags: list=None,
             file_format='handsontable', filename='me', width=800, height=300):
        pyexcel.save_as(
            records=list(self.find(keyword_regex, tags)),
            dest_file_name='{}.{}.html'.format(filename, file_format),
            dest_sheet_name='TagDict'
        )
        return IFrame('{}.{}.html'.format(filename, file_format), width=width, height=height)

    @staticmethod
    def _view_entries(entries,
                      file_format='handsontable', filename='me', width=800, height=150):
        """

        :param dict|OrderedDict|iter entries:
        :param file_format:
        :param filename:
        :param width:
        :param height:
        :return:
        """
        if isinstance(entries, (dict, OrderedDict)):
            entries = [entries]

        pyexcel.save_as(
            records=list(entries),
            dest_file_name='{}.{}.html'.format(filename, file_format),
            dest_sheet_name='TagDict'
        )
        return IFrame('{}.{}.html'.format(filename, file_format), width=width, height=height)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
