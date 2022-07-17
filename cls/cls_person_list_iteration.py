class PersonListIteration:

    def __init__(self, person_list):
        self.person_list = person_list

    def get_id(self) -> str:
        for person in self.person_list:
            yield person
        yield 'It was a last one'


class PersonListStack:
    def __init__(self, person_list):
        self.stack_list = person_list

    def add_list(self, data_list):
        self.stack_list.extend(data_list)

    def clean(self):
        self.stack_list.clear()

    def is_empty(self):
        return self.stack_list == []

    def push(self, item):
        self.stack_list.append(item)

    def pop(self):
        self.stack_list.pop()
        return self.peek()

    def peek(self):
        if not self.is_empty():
            return self.stack_list[len(self.stack_list) - 1]
        else:
            return None

    def get_next(self):
        item = self.peek()
        self.pop()
        return item
