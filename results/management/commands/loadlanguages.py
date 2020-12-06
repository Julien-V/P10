#!/usr/bin/python3
# coding : utf-8

from django.core.management.base import BaseCommand

import os
import json
import logging

from pur_beurre.settings import BASE_DIR
from results.models import Translation

###############################################################################
# Logs
###############################################################################
logger = logging.getLogger(__name__)
logger.setLevel(20)


class Command(BaseCommand):
    help = "Add languages from results/lang in DB"

    def __init__(self):
        self.path = os.path.join(BASE_DIR, "results/lang")
        self.lang_dict = dict()
        self.formatted_lang = {"tag": ""}
        self.translation_list = list()

    def load_file(self, filename):
        """Loads a json file which should be constructed like this :
            {
                "tag1": "str1",
                "tag2": "str2"
            }
        :return lang: dict (json.loads)
        """
        path = os.path.join(self.path, filename)
        with open(path, "rb") as file_lang:
            text = file_lang.read()
        lang = json.loads(text)
        return lang  # dict

    def make_insertion_dict(self):
        tag_dict = dict()
        for lang in self.lang_dict.keys():
            temp = self.lang_dict[lang].copy()
            for tag in temp.keys():
                if tag in tag_dict.keys():
                    if lang not in tag_dict[tag].keys():
                        tag_dict[tag][lang] = temp[tag]
                else:
                    tag_dict[tag] = {lang: temp[tag]}
        return tag_dict

    def insert_db(self, data):
        success_list = list()
        for tag in data:
            tag_data = data[tag]
            t = len(tag_data.keys())
            try:
                obj, created = Translation.objects.update_or_create(
                    tag=tag,
                    defaults=tag_data)
                obj.save()
                success_list.append((tag, t))
            except Exception as e:
                logger.warn(
                    "[E] loadlanguage insert error",
                    extra=e)
        return success_list

    def handle(self, *args, **options):
        # list json files in self.path
        files = os.listdir(self.path)
        files = [file_lang for file_lang in files if '.json' in file_lang]
        # loads files
        for filename in files:
            language_name = filename.replace(".json", "")
            self.lang_dict[language_name] = self.load_file(filename)
        # format
        insert_dict = self.make_insertion_dict()
        s_list = self.insert_db(insert_dict)
        total = len(list(insert_dict))
        print(f"[*] {len(s_list)}/{total} tag updated")
