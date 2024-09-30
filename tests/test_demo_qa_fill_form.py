import os.path

from selene import be, have, browser, by

# elements
first_name_input = browser.element("#firstName")
last_name_input = browser.element("#lastName")
email_input = browser.element("#userEmail")
phone_number = browser.element("#userNumber")
birth_date_input = browser.element("#dateOfBirthInput")
subject_input = browser.element("#subjectsInput")
upload_file_button = browser.element("#uploadPicture")
current_address_input = browser.element("#currentAddress")
state_list = browser.element("#state")
city_list = browser.element("#city")
submit_button = browser.element("#submit")

# test_data
name = "Lev"
surname = "Savinkov"
test_email = "www@test.ru"
male_gender = "Male"
test_number = "9997776633"
test_day, test_month, test_year = 10, "August", 1993
test_subject = "Hindi"
sport_hobby = "Sports"
music_hobby = "Music"
test_file = os.path.abspath("../test_image.jpg")
test_address = "Thailand, Prachuap Khiri Khan, HuaHin, 18/19"
test_state = "Rajasthan"
test_city = "Jaipur"


def open_browser():
    browser.open("/automation-practice-form")


def delete_banners():
    browser.driver.execute_script("$('#fixedban').remove()")
    browser.driver.execute_script("$('footer').remove()")


def get_gender_input(gender):
    return browser.element(by.xpath(f"//input[@value='{gender}']/ancestor::div[contains(@class, 'custom-control')]"))


def get_hobbies_input(hobby):
    return browser.element(by.xpath(
        f"//label[@class='custom-control-label' and text()='{hobby}']"
        "/ancestor::div[contains(@class, 'custom-checkbox')]"))


def fill_name(first_name):
    first_name_input.should(be.blank).type(first_name)


def fill_surname(second_name):
    last_name_input.should(be.blank).type(second_name)


def fill_email(email):
    email_input.should(be.blank).type(email)


def choose_gender(gender):
    """
    :param gender: 'Male', 'Female' or 'Other'
    """
    get_gender_input(gender).click()


def fill_phone_number(number):
    phone_number.type(number)


def fill_date_as_text(date):
    birth_date_input.click()
    browser.execute_script("document.getElementById('dateOfBirthInput').value = '';")
    birth_date_input.set(value=date).press_enter()


def fill_date_from_calendar(day, month, year):
    birth_date_input.click()
    browser.element(by.xpath("//select[@class = 'react-datepicker__year-select']")).click().element(
        by.xpath(f"//option[text() = '{year}']")
    ).click()
    browser.element(by.xpath("//select[@class = 'react-datepicker__month-select']")).click().element(
        by.xpath(f"//option[text() = '{month}']")).click()
    browser.element(
        by.xpath(f"//div[contains(@class, 'react-datepicker__day') and text() = '{day}']")).click()


def fill_subject(subject):
    subject_input.type(subject).press_enter()


def fill_hobbies(*hobbies):
    """
    
    :param hobbies: Sports, Reading or Music
    
    """
    for i in hobbies:
        get_hobbies_input(i).should(be.clickable).click()


def upload_file(path):
    upload_file_button.type(path)


def fill_current_address(address):
    current_address_input.type(address)


def choose_state(option):
    state_list.click()
    browser.element(f"//div[contains(@id, 'react-select-3-option') and contains(text(), '{option}')]").click()


def choose_city(option):
    city_list.click()
    browser.element(f"//div[contains(@id, 'react-select-4-option') and contains(text(), '{option}')]").click()


def assert_table_value(param, expected_value):
    (browser.element(by.xpath(f"//table/tbody//td[text() = '{param}']/following-sibling::td"))
     .should(have.text(expected_value)))


def test_fill_form():
    open_browser()
    delete_banners()
    fill_name(name)
    fill_surname(surname)
    fill_email(test_email)
    choose_gender(male_gender)
    fill_phone_number(test_number)
    fill_date_from_calendar(test_day, test_month, test_year)
    fill_subject(test_subject)
    fill_hobbies(sport_hobby, music_hobby)
    upload_file(test_file)
    fill_current_address(test_address)
    choose_state(test_state)
    choose_city(test_city)
    submit_button.click()
    assert_table_value("Student Name", f"{name} {surname}")
    assert_table_value("Student Email", test_email)
    assert_table_value("Gender", male_gender)
    assert_table_value("Mobile", test_number)
    assert_table_value("Date of Birth", f"{test_day} {test_month},{test_year}")
    assert_table_value("Subjects", test_subject)
    assert_table_value("Hobbies", f"{sport_hobby}, {music_hobby}")
    assert_table_value("Picture", test_file.split("\\")[-1])
    assert_table_value("Address", test_address)
    assert_table_value("State and City", f"{test_state} {test_city}")
