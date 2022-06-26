"""
Helper functions for parsing html text with BeautifulSoup
"""
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet

def get_soup_page(html_page: str) -> BeautifulSoup:
    """
    Converts html text to a BeautifulSoup object.

    Args:
        html_page: html text

    Return:
        soup_page: BeautifulSoup representation of the html page
    """
    soup_page = BeautifulSoup(html_page, 'html.parser')
    return soup_page

def parse_soup_page_attr(soup_page: BeautifulSoup, attr_name: str,
                         attr_value: str) -> ResultSet:
    """
    Parse the soup page and return all divs containing the specified attribute
    with the specified value.

    Args:
        soup_page: BeautifulSoup representation of a html business page
        attr_name: name of attribute to search for, i.e. 'class'
        attr_value: value of attribute, i.e. 'mainReviews'

    Return:
        BeautifulSoup ResultSet containing all reviews on the given soup page
    """
    return soup_page.find_all("div", {attr_name: attr_value})

def parse_soup_tag_class(soup_tag: Tag, class_name: str) -> str:
    """
    Gets the contents of a specified class on a single given tag
    and converts it to a string.

    Args:
        soup_tag: BeautifulSoup Tag containing metadata
        class_name: class name on the soup_tag

    Return:
        contents of the specified class
    """
    tag_element = soup_tag.find( class_ = class_name)
    return str(tag_element.contents[0].string)
