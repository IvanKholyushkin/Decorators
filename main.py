import os
from datetime import datetime
import bs4
import requests


def logger(old_function):
    def new_function(*args, **kwargs):
        time = datetime.utcnow().strftime("%I:%M %a on %B %d, %Y")
        function_name = old_function.__name__
        arguments = args, kwargs
        result = old_function(*args, **kwargs)
        with open("main.log", "a", encoding="utf-8") as doc:
            doc.write(
                f"Function call time in UTC: {time}\n"
                f"Function name: {function_name}\n"
                f"Function arguments: {arguments}\n"
                f"Function result: {result}\n{'/' * 30}\n"
            )

        return result
    return new_function


def test_1():
    path = "main.log"
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return "Hello World"

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert "Hello World" == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), "Должно вернуться целое число"
    assert result == 4, "2 + 2 = 4"
    result = div(6, 2)
    assert result == 3, "6 / 2 = 3"

    assert os.path.exists(path), "файл main.log должен существовать"

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert "summator" in log_file_content, "должно записаться имя функции"
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f"{item} должен быть записан в файл"


if __name__ == "__main__":
    test_1()


def logger2(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            time = datetime.utcnow().strftime("%I:%M %a on %B %d, %Y")
            function_name = old_function.__name__
            arguments = args, kwargs
            result = old_function(*args, **kwargs)
            with open(path, "a", encoding="utf-8") as doc:
                doc.write(
                    f"Function call time in UTC: {time}\n"
                    f"Function name: {function_name}\n"
                    f"Function arguments: {arguments}\n"
                    f"Function result: {result}\n{'/' * 30}\n"
                )
            return result
        return new_function
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger2(path)
        def hello_world():
            return 'Hello World'

        @logger2(path)
        def summator(a, b=0):
            return a + b

        @logger2(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()

@logger
def get_url(key_words):
    URL = f"https://spb.hh.ru/search/vacancy?text={key_words}&area=1&area=2&"
    return URL

def get_count_pages(URL, headers_dict):
    response = requests.get(URL, headers=headers_dict)
    soup = bs4.BeautifulSoup(response.content, "lxml")
    count_pages = int(
        soup.find("div", class_="pager")
        .find_all("span", recursive=False)[-1]
        .find("a")
        .find("span")
        .text
    )
    return count_pages


if __name__ == "__main__":
    key_words = "python+django+flask"
    get_url(key_words)

