#!/usr/bin/python3
# coding : utf-8

import os
import json
import pytest

from results.models import Product
from results.management.commands.populatedb import Command

from pur_beurre.settings import off_api


def j(json_file):
    """This function opens and returns a json file
    in test/samples/
    :param json_file: str, 'valid_off.json'
    :return: dict, the file
    """
    path = os.path.join("results/test/samples/", json_file)
    with open(path, "r") as file_a:
        json_file = file_a.read()
    return json.loads(json_file)


###############################################################################
# results.management.commands.populatedb.Command
###############################################################################
class TestPopulateDB():
    off_api_test = off_api.copy()
    off_api_test["categories"] = ["desserts-au-chocolat"]

    @pytest.mark.django_db
    def test_popu_valid(self, django_db_blocker, patch_get_and_load):
        with django_db_blocker.unblock():
            popdb = Command(self.off_api_test)
            patch_get_and_load.values = j("populatedb_valid.json")
            popdb.handle()
        prods = Product.objects.all()
        assert len(prods) == 2

    @pytest.mark.django_db
    def test_popu_invalid(self, django_db_blocker, patch_get_and_load):
        with django_db_blocker.unblock():
            popdb = Command(self.off_api_test)
            patch_get_and_load.values = j("populatedb_invalid.json")
            popdb.handle()
        prods = Product.objects.all()
        assert len(prods) == 1

    @pytest.mark.django_db
    def test_popu_update(self, django_db_blocker, patch_get_and_load):
        # 2 products
        with django_db_blocker.unblock():
            popdb = Command(self.off_api_test)
            patch_get_and_load.values = j("populatedb_valid.json")
            popdb.handle()
        # update 1st prod
        with django_db_blocker.unblock():
            popdb = Command(self.off_api_test)
            patch_get_and_load.values = j('populatedb_update.json')
            popdb.handle(**{"update": True})
        prods = Product.objects.all()
        prod = prods[1]
        assert prod.nutrition_grades == "b"
        assert isinstance(prod.updated_timestamp, int)