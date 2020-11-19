#!/usr/bin/python3
# coding : utf-8

import os
import pytest

from pur_beurre.settings import BASE_DIR

from results.management.commands.loadlanguages import Command
from results.models import Translation


###############################################################################
# results.management.commands.loadlanguages.Command
###############################################################################
class TestLoadlanguages():
    path = os.path.join(BASE_DIR, "results/test/samples/lang")

    @pytest.mark.django_db
    def test_load_tag(self, django_db_blocker):
        with django_db_blocker.unblock():
            load_l = Command()
            load_l.path = self.path
            load_l.handle()
        prods = Translation.objects.all()
        assert len(prods) == 2
