from cls.cls_Person import Person

my_list = [0, 1, 2, 3, 4, 5, 6, 7]


class PersonListIteration:

    def __init__(self, person_list):
        self.person_list = person_list

    def get_id(self) -> str:
        for person in self.person_list:
            yield person
        yield 'It was a last one'


# pers_list = PersonListIteration(my_list)
# for item in pers_list.get_id():
#     print(item)


class PersonListStack:
    def __init__(self, person_list):
        self.stack_list = person_list

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


# print('pers_st = PersonListStack(my_list)')
#
# pers_st = PersonListStack(my_list)
#
# while not pers_st.is_empty():
#     print(pers_st.get_next())
#
# print('It was a last one')
