from selenium import webdriver
from time import sleep, perf_counter
import random
from datetime import datetime
from bs4 import BeautifulSoup

from selenium.webdriver.firefox.options import Options
from selenium.common import exceptions as sel_exception

from custom_exceptions import *

default_options = Options()
default_options.headless = True


class BasicSpider:
    def __init__(self, url, sleep_time=3, options=default_options):
        """ 
        Args:
        
            url (str): page to load when browser is first launched
            sleep_time (int): a wait-time (in seconds) to allow things like page loads to finish.
            options (selenium.webdriver.firefox.options.Options): custom options for browser
        """

        self.sleep_time = sleep_time
        self._browser = webdriver.Firefox(options=options)

        self.page_soup = None


    def _load_page_soup(self):
        return BeautifulSoup(self.page_source, features="lxml")


    def _confirm_positive_integer(self, value, include_zero=False):
        """
        Check given value to be a positive integer
        """
        try:
            # Positive
            if include_zero:
                assert value >= 0

            else:
                assert value > 0

            # Integer
            assert type(value) == type(1)   # Integer
        
        except AssertionError:
            raise ValueError("value must be a positive integer")


    def get_page_y_offset(self):
        y_offset = self._browser.execute_script("return window.pageYOffset")

        return y_offset


    def get_element_inner_html(self, element_id=None, element_class=None):
        """
        return the innerHTML of given element.
        if element is to be found by class name, then the innerHTML of the first element
        that matches the given class name will be returned.
        """
        if element_id is not None:
            return self._browser.execute_script(f'return document.getElementById("{element_id}").innerHTML')

        elif element_class is not None:
            return self._browser.execute_script(f'return document.getElementsByClassName("{element_class}")[0].innerHTML')

        else:
            msg = "Pass either element_id or element_class, but not both"
            raise ParameterConflictError(msg)


    def wait(self, time=None):
        
        if time is None:
            time = self.sleep_time    

        sleep(self.sleep_time)


    def goto(self, url, wait=False, wait_for=None):
        """
        Navigate to given URL. Note that some pages will not load all elements
        even if driver thinks the page has been loaded. hence why there's a wait param
        """
        self._browser.get(url)

        if wait:
            self.wait(wait_for)


    def refresh_page(self, wait=False, wait_for=None):
        """
        Refresh the page and reset local variables to get new page source.
        """
        self._browser.refresh()

        if wait:
            self.wait(wait_for)

        # refresh page source to get new changes
        self.page_soup = self._load_page_soup()


    def get_timestamp(self, for_filename=False):
        """
        returns a formatted timestamp string (e.g "2020-09-25 Weekday 16:45:37" )
        """
        if for_filename:
            formatted_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        else:
            formatted_time = datetime.now().strftime("%Y-%m-%d %A %H:%M:%S")

        return formatted_time


    def smooth_vscroll_down_to(self, scroll_to, speed=1):
        """
        Smoothly scroll down to given position
        :Paramaters

        scroll_to: (int) y position to scroll to.

        speed: (int) pixels scrolled per loop (effective speed)
        """
        
        self._confirm_positive_integer(scroll_to)
        self._confirm_positive_integer(speed)

        current_y = self.get_page_y_offset()

        if current_y >= scroll_to:
            msg = "'scroll_to' >= current y offset. consider using smooth_vscroll_up_to instead."
            raise BadScrollPositionException(msg)

        while current_y < scroll_to:
            
            current_y += speed
            self.instant_vscroll_to(current_y)
            
        # Jump to target when few enough pixels remain
        self.instant_vscroll_to(scroll_to)
    
    def smooth_vscroll_down_by(self, scroll_by, speed=1):
        """
        Scroll down by the given amount of pixels at the given speed

        :Parameters:

        scroll_by: (int) amount of pixels to scroll

        speed: (int) amount of pixels scrolled per loop
        """
        
        self._confirm_positive_integer(scroll_by)
        self._confirm_positive_integer(speed)

        current_y = self.get_page_y_offset()
        final_y = current_y + scroll_by

        while current_y < final_y:
            current_y += speed
            self.instant_vscroll_to(current_y)

        # To avoid inaccuracies from numbers that don't factor into eachother
        self.instant_vscroll_to(final_y)


    def smooth_vscroll_up_to(self, scroll_to, speed=1):
        """
        Slowly scroll to a given y coordinate. if y is not given,
        then scroll down infinitely, but stop when the bottom is reached.

        :Paramaters

        scroll_to: (int) y position to scroll to.

        speed: (int) pixels scrolled per loop (effective speed)
        """
            
        self._confirm_positive_integer(scroll_to, include_zero=True)
        self._confirm_positive_integer(speed)

        current_y = self.get_page_y_offset()

        if current_y < scroll_to:
            msg = "'scroll_to' < current y offset. consider using smooth_vscroll_down_to instead?"
            raise BadScrollPositionException(msg)


        while current_y > scroll_to:            
            current_y -= speed
            self.instant_vscroll_to(current_y)

        # When fewer than 'speed' pixels remain, jump to target
        self.instant_vscroll_to(scroll_to)

    def smooth_vscroll_up_by(self, scroll_by, speed=1):
        """
        Scroll up by the given amount of pixels at the given speed

        :Parameters:

        scroll_by: (int) amount of pixels to scroll

        speed: (int) amount of pixels scrolled per loop
        """
        
        self._confirm_positive_integer(scroll_by)
        self._confirm_positive_integer(speed)

        current_y = self.get_page_y_offset()
        final_y = current_y - scroll_by if current_y > scroll_by else 0

        while current_y > final_y:
            current_y -= speed
            self.instant_vscroll_to(current_y)

        # To avoid inaccuracies from numbers that don't factor into eachother
        self.instant_vscroll_to(final_y)


    def instant_vscroll_to(self, scroll_to):
        """
        Instantly scroll to a given y coordinate
        """
        try:
            assert scroll_to >= 0
        
        except AssertionError:
            raise ValueError("scroll_to must be >= 0")

        self._browser.execute_script(f"window.scrollTo(0, {scroll_to})")

    def instant_vscroll_by(self, scroll_by):
        """
        Instantly vertically scroll by given amount
        """
        self._browser.execute_script(f"window.scrollBy(0, {scroll_by})")


    def mousewheel_vscroll_to(self, scroll_to):
        """
        Scroll to given position while imitating a human using a mousewheel
        """
        pass

    def mousewheel_vscroll_by(self, scroll_to):
        """
        Scroll to given position while imitating a human using a mousewheel
        """
        pass


    def smooth_hscroll(self, scroll_to):
        pass

    def instant_hscroll(self, scroll_to):
        pass

    
    def _get_rand_float(self, range_=(0, 1)):
        """
        returns a random float number within given range
        """
        return random.uniform(*range_)


    def slow_type(self, sentence, speed=0, field_id=None, field=None, speed_range=(0.05, 0.25)):
        """
        Slowly send text to a given input field.

        :Params:

        sentence: (str) text to send to field

        speed: (int) how quick to send text

        field_id: (str) id of input field.

        field: (selenium.WebElement) pass instead of field_id.
        """

        range_ = speed_range

        if field is not None:
            for letter in sentence:
                field.send_keys(letter)
                sleep(self._get_rand_float(range_))

        elif field_id is not None:
            # Raises NoSuchElementException
            field = self._browser.find_element_by_id(field_id)
            
            for letter in sentence:
                field.send_keys(letter)
                sleep(self._get_rand_float(range_))

        else:
            raise ParameterConflictError("Must pass either 'field' OR 'field_id', but not both.")


    def click_button(self, button_id=None, button=None):
        if button_id is not None:
            button = self._browser.execute_script(f'return document.getElementById("{button_id}")')
            button.click()

        elif button is not None:
            button.click()

        else:
            raise ParameterConflictError("Must pass either 'button_id' OR 'button', but not both")


    def select_from_combobox(self, combobox, selection):
        """
        Select an item from a combobox
        """
        pass


    def toggle_checkbox(self, checkbox):
        pass
        
    def tick_checkbox(self, checkbox):
        """
        Raises _undefined_ exception if given checkbox is already ticked
        """
        pass

    def untick_checkbox(self, checkbox):
        """
        Raises _undefined_ exception if given checkbox is already unticked
        """
        pass

    
