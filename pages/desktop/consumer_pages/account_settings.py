# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

from pages.page import PageRegion
from pages.desktop.consumer_pages.base import Base


class AccountSettings(Base):
    """
    Account settings base page
    Contains the common objects in the account setting area
    """
    _payment_locator = (By.CSS_SELECTOR, '.sub-nav > li:nth-child(2) > a')
    _payment_page_locator = (By.ID, 'purchases')
    _settings_sign_in_locator = (By.CSS_SELECTOR, '.account-settings-save a:not(.register)')

    def go_to_settings_page(self):
        self.set_window_size()
        self.selenium.get(self.base_url + '/settings')
        self.wait_for_page_to_load()

    def click_sign_in(self):
        self.find_element(*self._settings_sign_in_locator).click()


class BasicInfo(AccountSettings):
    """
    User Account Settings page
    https://marketplace-dev.allizom.org/en-US/settings/
    """

    _page_title = 'Settings | Firefox Marketplace'

    _email_locator = (By.CSS_SELECTOR, '.settings-email.account-field > p')
    _display_name_input_locator = (By.ID, 'display_name')
    _save_button_locator = (By.CSS_SELECTOR, '.button[type="submit"]')
    _multiple_language_select_locator = (By.ID, 'language')
    _account_settings_header_locator = (By.CSS_SELECTOR, '#account-settings > h2')
    _display_field_name_text_locator = (By.CSS_SELECTOR, '.form-label>label[for="id_display_name"]')
    _language_field_text_locator = (By.CSS_SELECTOR, '.form-label>label[for="language"]')
    _region_field_locator = (By.CSS_SELECTOR, '.region span')
    _region_locator = (By.CSS_SELECTOR, '#account-settings .region')
    _recommendations_checkbox_locator = (By.CSS_SELECTOR, '#enable_recommendations')
    _recommended_tab_locator = (By.CSS_SELECTOR, '#navigation li a.recommended')

    @property
    def email(self):
        return self.selenium.find_element(*self._email_locator).text

    @property
    def is_email_visible(self):
        return self.is_element_visible(*self._email_locator)

    @property
    def display_name(self):
        return self.selenium.find_element(*self._display_name_input_locator).get_attribute('value')

    @property
    def is_display_name_visible(self):
        return self.is_element_visible(*self._display_name_input_locator)

    def save_changes(self):
        self.selenium.find_element(*self._save_button_locator).click()
        notification = self.selenium.find_element(*self._notification_locator)
        WebDriverWait(self.selenium, self.timeout).until(
            EC.visibility_of(notification))

    def edit_display_name(self, text):
        self.type_in_element(self._display_name_input_locator, text)

    @property
    def is_save_button_visible(self):
        return self.is_element_visible(*self._save_button_locator)

    @property
    def account_settings_header_text(self):
        return self.selenium.find_element(*self._account_settings_header_locator).text

    @property
    def display_name_field_text(self):
        return self.selenium.find_element(*self._display_field_name_text_locator).text

    @property
    def language_field_text(self):
        return self.selenium.find_element(*self._language_field_text_locator).text

    @property
    def is_region_field_visible(self):
        return self.is_element_visible(*self._region_field_locator)

    def edit_language(self, option_value):
        element = self.selenium.find_element(*self._multiple_language_select_locator)
        select = Select(element)
        select.select_by_value(option_value)

    def disable_recommendations(self):
        checkbox = self.selenium.find_element(*self._recommendations_checkbox_locator)
        assert checkbox.is_selected(), 'Recommendations checkbox is expected to be checked, but it is unchecked'
        checkbox.click()

    def wait_for_recommended_tab_not_visible(self):
        WebDriverWait(self.selenium, self.timeout).until(
            EC.invisibility_of_element_located(self._recommended_tab_locator))

    @property
    def is_recommended_tab_visible(self):
        return self.is_element_visible(*self._recommended_tab_locator)

    @property
    def is_recommendations_enabled(self):
        return self.selenium.find_element(*self._recommendations_checkbox_locator).is_selected()


class My_Apps(AccountSettings):

    _page_title = 'My Apps | Firefox Marketplace'

    _my_apps_list_locator = (By.CSS_SELECTOR, '.item')
    _expand_button_locator = (By.CSS_SELECTOR, '.app-list-filters-content .app-list-filters-expand-toggle')

    def go_to_my_apps_page(self):
        self.set_window_size()
        self.selenium.get(self.base_url + '/purchases')

    def click_expand_button(self):
        self.find_element(*self._expand_button_locator).click()

    @property
    def apps(self):
        return [self.Apps(self.base_url, self.selenium, web_element)
                for web_element in self.selenium.find_elements(*self._my_apps_list_locator)]

    class Apps(PageRegion):

        _screenshots_locator = (By.CSS_SELECTOR, '.screenshot')

        @property
        def are_screenshots_visible(self):
            return self.find_element(*self._screenshots_locator).is_displayed()
