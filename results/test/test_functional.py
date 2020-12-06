#!/usr/bin/python3
# coding : utf-8

import pytest


from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException


@pytest.mark.django_db()
def test_webdriver(live_server, firefox, django_db_set):
    firefox.get(live_server.url)
    assert firefox.title == "Pur Beurre(fr) -"


@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_set')
class TestFunctionalBase:
    """Base for functional testing with pytest & selenium"""

    def find_id(self, firefox, elem_id):
        elem = firefox.find_element(By.ID, elem_id)
        return elem

    def move_and_click(self, firefox, elem):
        height = elem.location['y']+elem.size['height']
        last_height = firefox.get_window_size()['height']
        if height >= last_height:
            firefox.execute_script(
                f"window.scrollTo(0, {elem.location['y']});")
        actions = webdriver.ActionChains(firefox)
        actions.move_to_element(elem).click().perform()

    def fill_form(self, firefox, form):
        for input_id, value in form.items():
            input_elem = self.find_id(firefox, input_id)
            input_elem.send_keys(value)

    def submit_form(self, firefox, submit_button_id):
        submit_button = self.find_id(firefox, submit_button_id)
        self.move_and_click(firefox, submit_button)

    def wait(self, firefox, elem, duration=5):
        wait = WebDriverWait(firefox, duration)
        try:
            wait.until(
                e_c.presence_of_element_located(elem))
        except TimeoutException:
            pytest.fail(
                f"TimeoutException, {elem} not in {firefox.current_url}")


@pytest.mark.django_db()
@pytest.mark.usefixtures('django_db_set')
class TestAuthentification(TestFunctionalBase):
    reg_form = {
        'input-username': 'usertest',
        'input-password1': 'g8e$rHadm254',
        'input-password2': 'g8e$rHadm254',
        'input-email': 'usertest@gmail.com',
        'input-first-name': 'user',
        'input-last-name': 'test',
    }
    auth_form = {
        'input-username': 'usertest@gmail.com',
        'input-password': 'g8e$rHadm254'
    }

    def test_sign_up(self, firefox, live_server):
        firefox.get(live_server.url)
        sign_up_link = self.find_id(firefox, "sign-up-link")
        self.move_and_click(firefox, sign_up_link)
        self.wait(firefox, (By.ID, 'register-zone'))
        self.fill_form(firefox, self.reg_form)
        self.submit_form(firefox, 'sign_up')
        self.wait(firefox, (By.ID, "about"))
        assert firefox.title == 'Pur Beurre(fr) -'
        assert firefox.current_url == live_server.url + "/"

    def test_sign_in(self, firefox, live_server):
        self.test_sign_up(firefox, live_server)
        firefox.get(live_server.url)
        sign_in_link = self.find_id(firefox, 'sign-in-link')
        self.move_and_click(firefox, sign_in_link)
        self.wait(firefox, (By.ID, 'login-zone'))
        self.fill_form(firefox, self.auth_form)
        self.submit_form(firefox, 'sign_in')
        self.wait(firefox, (By.ID, 'auth_success'))
        firefox.get(live_server.url)
        assert firefox.title == "Pur Beurre(fr) -"


@pytest.mark.django_db()
@pytest.mark.usefixtures('django_db_set')
class TestFeatures(TestFunctionalBase):
    search_form = {
        "navbar-input": "Petit Nesquik"
    }

    def test_search(self, firefox, live_server):
        firefox.get(live_server.url)
        search = self.find_id(firefox, 'navbar-input')
        self.move_and_click(firefox, search)
        self.fill_form(firefox, self.search_form)
        search.send_keys(Keys.RETURN)
        self.wait(firefox, (By.ID, 'masthead-title'))
        masthead = self.find_id(firefox, 'masthead-title')
        masthead_text = masthead.get_attribute('textContent')
        assert masthead_text == 'Petit nesquik'

    def test_change_language(self, firefox, live_server):
        firefox.get(live_server.url)
        assert firefox.title == "Pur Beurre(fr) -"
        lang_selector = self.find_id(firefox, "lang-selector")
        actions = webdriver.ActionChains(firefox)
        actions.move_to_element(lang_selector).move_to_element(
            firefox.find_element(By.ID, "en_GB")).click().perform()
        firefox.get(live_server.url)
        assert firefox.title == "Pur Beurre(en) -"
        assert firefox.get_cookie('lang')['value'] == "en_GB"
