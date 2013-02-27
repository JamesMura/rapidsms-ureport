def create_group(driver, name):
    driver.open('/admin/auth/group/')
    driver.browser.click_link_by_partial_text('Add group')
    driver.browser.fill("name", name)
    driver.browser.find_by_name('_save').first.click()


def create_backend(driver, name):
    driver.open('/admin/rapidsms/backend/')
    driver.browser.click_link_by_partial_text('Add backend')
    driver.browser.fill("name", name)
    driver.browser.find_by_name('_save').click()


def create_contact(driver, name, phone, username, group_name, backend_name):
    driver.open('/admin/rapidsms/contact/')
    driver.browser.click_link_by_partial_text('Add contact')
    driver.browser.fill("name", name)
    driver.select_by_text('user', username)
    driver.select_by_text('groups', group_name)
    driver.browser.fill('birthdate_0', '2013-02-22')
    driver.browser.fill('birthdate_1', '12:55:40')
    driver.select_by_text('gender', 'Male')
    driver.select_by_text('connection_set-0-backend', backend_name)
    driver.browser.fill("connection_set-0-identity", phone)
    driver.browser.find_by_name('_save').click()


def create_poll(driver, poll_name, question, group_name):
    driver.open('/mypolls/')
    driver.browser.click_link_by_partial_href('/createpoll/')
    driver.browser.fill("name", "%s" % poll_name)
    driver.browser.fill("question_en", question)
    driver.select_by_text('groups', group_name)
    driver.browser.click_link_by_partial_href('javascript:void(0);')


def admin_can_create_poll(driver, ):
    group_name = 'group1'
    backend_name = 'dmark'
    user = driver.create_and_sign_in_admin("pass", "jamo")
    create_backend(driver, backend_name)
    create_group(driver, group_name)
    create_contact(driver, "jamo", "999", user.username, group_name, backend_name)
    poll_name = "our poll"
    question = "question 12"
    create_poll(driver, poll_name, question, group_name)
    driver.open('/polls/')
    assert driver.browser.is_text_present(question)