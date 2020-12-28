from urllib import parse
from flask import Flask, request, flash
import uuid
import os.path



class requester(object):
    @classmethod
    def formDict(cls, url):
        url = 'localhost?' + url
        return dict(parse.parse_qsl(parse.urlsplit(url).query))

    @classmethod
    def all(cls):
        if request.method == 'GET':
            return cls.formDict(request.query_string.decode('utf-8'))
        elif request.method == 'POST':
            if request.files and request.form:
                files = request.files.to_dict()
                form = request.form.to_dict()
                req = files.copy()
                req.update(form)
                return req
            if request.files:
                files = request.files.to_dict()
                return files
            if request.form:
                form = request.form.to_dict()
                return form

    @classmethod
    def input(cls, key):
        return cls.all().get(key)

    @classmethod
    def boolean(cls, key):
        if cls.input(key) == "on" or cls.input(key) == "1" or cls.input(key) == 1 or cls.input(key) == "true" or cls.input(key) == "yes" or cls.input(key) == "True":
            return True
        else:
            return False

    @classmethod
    def only(cls, list_of_keys):
        if type(list_of_keys) == str:
            list_of_keys = [list_of_keys]
        array = {}
        for item in list_of_keys:
            array[item] = cls.input(item)
        return array

    @classmethod
    def ignore(cls, ignore_keys):
        if type(ignore_keys) == str:
            ignore_keys = [ignore_keys]
        array = {}
        all_keys = cls.all()
        for key in ignore_keys:
            all_keys.pop(key, None)
        return all_keys

    @classmethod
    def has(cls, key):
        keys = []
        results = []
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
    def filled(cls, key):
        if cls.input(key) == "" or cls.input(key) is None:
            return False
        else:
            return True

    @classmethod
    def missing(cls, key):
        if cls.input(key) is None:
            return True
        else:
            return False

    @classmethod
    def flash(cls):
        flash(cls.all())

    @classmethod
    def flashOnly(cls, list_of_keys):
        flash(cls.only(list_of_keys))

    @classmethod
    def flashIgnore(cls, ignore_keys):
        flash(cls.ignore(ignore_keys))

    @classmethod
    def cookies(cls, key):
        return request.cookies.get(key)


    # Files
    @classmethod
    def file(cls, key):
        file = cls.only(key)
        return file[key]

    @classmethod
    def hasFile(cls, key):
        keys = cls.only(key)
        for x in keys:
            if keys[x].__dict__['filename'] == "":
                return False
            else:
                return True

    @classmethod
    def store(cls, key, location):
        extension = os.path.splitext(cls.file(key).__dict__['filename'])[1][1:].strip()
        cls.file(key).__dict__['filename'] = str(uuid.uuid4()) + "." + extension
        with cls.file(key).__dict__['stream'] as f:
            file_guts = f.read()
        with open(f'{location}\\{cls.file(key).__dict__["filename"]}', 'wb') as output:
            output.write(file_guts)
        return cls.file(key)

