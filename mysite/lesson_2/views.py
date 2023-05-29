from datetime import datetime

from django.shortcuts import render


class MyClass:
    # string = ''

    def string(self):
        return "MyClass"

    def __init__(self, s):
        self.string = s
def base_template(request):
    my_num = 0
    my_str = 'some string'
    my_dict = {"some_key": "some_value"}
    my_list = ['list_first_item', 'list_second_item', 'list_third_item']
    my_set = {'set_first_item', 'set_second_item', 'set_third_item'}
    my_tuple = ('tuple_first_item', 'tuple_second_item', 'tuple_third_item')
    my_class = MyClass('class string')
    return render(request, "lesson_2/index.html", {
        'my_num': my_num,
        'my_str': my_str,
        'my_dict': my_dict,
        'my_list': my_list,
        'my_set': my_set,
        'my_tuple': my_tuple,
        'my_class': my_class,
        'display_num': True,
        'now': datetime.now()
    })

def first(request):
    return render(request, 'lesson_2/first.html')