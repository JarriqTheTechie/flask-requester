import os.path
import uuid
from typing import Any
from urllib import parse

from flask import request, flash


class requester(object):
    @classmethod
    def formDict(cls, url: str) -> dict:
        url: str = 'localhost?' + url
        return dict(parse.parse_qsl(parse.urlsplit(url).query))

    @classmethod
    def all(cls, arrays: dict | None = None) -> dict:
        if arrays is None:
            arrays = []
        if request.method == 'GET':
            return cls.formDict(request.query_string.decode('utf-8'))
        elif request.method == 'POST' or request.method == 'PUT':
            if request.files and request.form:
                files = request.files.to_dict()
                form = request.form.to_dict()
                req = files.copy()
                req.update(form)
                for array in arrays:
                    key = array
                    data = request.form.getlist(f'{array}')
                    req[key] = data
                return req
            if request.files:
                files = request.files.to_dict()
                return files
            if request.form:
                form = request.form.to_dict()
                if len(arrays) > 0:
                    for array in arrays:
                        key = array
                        data = request.form.getlist(f'{array}')
                        form[key] = data
                return form

    @classmethod
    def input(cls, key: str, default: Any = None) -> Any:
        return cls.all().get(key, default)

    @classmethod
    def boolean(cls, key: str) -> bool:
        if cls.input(key) == "on" or cls.input(key) == "1" or cls.input(key) == 1 or cls.input(
                key) == "true" or cls.input(key) == "yes" or cls.input(key) == "True":
            return True
        else:
            return False

    @classmethod
    def only(cls, list_of_keys: list) -> dict:
        if type(list_of_keys) == str:
            list_of_keys: list = [list_of_keys]
        array: dict = {}
        for item in list_of_keys:
            array[item] = cls.input(item)
        return array

    @classmethod
    def ignore(cls, ignore_keys: str | list) -> dict:
        if type(ignore_keys) == str:
            ignore_keys = [ignore_keys]

        all_keys = cls.all()
        for key in ignore_keys:
            all_keys.pop(key, None)
        return all_keys

    @classmethod
    def has(cls, key: str) -> bool:
        keys: list = []
        results: list = []
        if type(key) == str:
            keys = [key]
        elif type(key) == list:
            keys = key
        for key in keys:
            if key in cls.all():
                results.append(True)
            else:
                results.append(False)
        if False in results:
            return False
        else:
            return True

    @classmethod
    def filled(cls, key: str) -> bool:
        if cls.input(key) == "" or cls.input(key) is None:
            return False
        else:
            return True

    @classmethod
    def missing(cls, key: str) -> bool:
        if cls.input(key) is None:
            return True
        else:
            return False

    @classmethod
    def flash(cls) -> None:
        flash(cls.all())

    @classmethod
    def flashOnly(cls, list_of_keys) -> None:
        flash(cls.only(list_of_keys))

    @classmethod
    def flashIgnore(cls, ignore_keys) -> None:
        flash(cls.ignore(ignore_keys))

    @classmethod
    def cookies(cls, key: str) -> Any:
        return request.cookies.get(key)

    # Files
    @classmethod
    def file(cls, key: str):
        file = cls.only(key)
        return file[key]

    @classmethod
    def hasFile(cls, key: str) -> bool:
        keys = cls.only(key)
        for x in keys:
            if keys[x].__dict__['filename'] == "":
                return False
            else:
                return True

    @classmethod
    def store(cls, key: str, prefix: str = "", suffix: str = "", prefix_separator: str = "", suffix_separator: str = "",
              keep_name: bool = False) -> str:
        extension: str = os.path.splitext(cls.file(key).__dict__['filename'])[1][1:].strip()
        if keep_name is True:
            with cls.file(key).__dict__['stream'] as f:
                file_guts: bytes = f.read()
            with open(r'UPLOADS\\' + f'{prefix}{prefix_separator}{cls.file(key).__dict__["filename"]}', 'wb') as output:
                output.write(file_guts)
            return cls.file(key).__dict__['filename']
        cls.file(key).__dict__[
            'filename'] = f"{prefix}{prefix_separator}{str(uuid.uuid4())}{suffix_separator}{suffix}" + "." + extension
        with cls.file(key).__dict__['stream'] as f:
            file_guts: bytes = f.read()
        with open(r'UPLOADS\\' + f'{cls.file(key).__dict__["filename"]}', 'wb') as output:
            output.write(file_guts)
        return cls.file(key).__dict__['filename']

    @classmethod
    def upload_multiple(cls, key: str, keep_name: bool = False):
        saved_file_path_list: list = []
        files: list = request.files.getlist(f'{key}')
        for file in files:
            extension: str = os.path.splitext(file.filename)[1][1:].strip()
            if keep_name is False:
                file.filename = str(uuid.uuid4()) + "." + extension
            with file.stream as f:
                file_guts: bytes = f.read()
            with open(r'UPLOADS\\' + f'{file.filename}', 'wb') as output:
                output.write(file_guts)
            saved_file_path_list.append(file.filename)
        return saved_file_path_list
