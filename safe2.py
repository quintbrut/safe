import random
import threading
import time
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
# Создаем сессию пользователя
user = requests.Session()
# Браузер пользователя
userAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'

user.headers = {
    'user-agent': userAgent
}
PUT = 'put'
TAKE = 'take'
# Ссылки
url = 'https://pacan.mobi'


def login(userLogin, password, session):
    """
    Функция авторизации
    """
    loginData = {
        'login': userLogin,
        'password': password
    }

    # Жмем кнопку авторизоваться с данными введенными ранее
    session.post(url + '/index.php?r=site/auth/', data=loginData)
    print('Авторизованы под ником ', userLogin)


def getSafeData(session):
    safe_url = 'https://pacan.mobi/index.php?r=property/safe'
    safe_page = session.get(safe_url)
    soup = bs(safe_page.content, "lxml")
    in_safe = int(
        soup.find('div', class_="center font14 bold").find('img', alt='доценты').findParent().getText().strip())
    token = soup.find('input', attrs={'type': 'hidden', 'name': 'token'})['value']
    in_pocket = int(soup.find('span', id='res-docents').getText().strip())
    print('В сейфе: ', in_safe)
    print('В кармане: ', in_pocket)
    print('Токен: ', token)
    return {
        'in_safe': in_safe,
        'in_pocket': in_pocket,
        'token': token,
    }


def safeControl(action, token, amount,session):
    urlControl = 'https://pacan.mobi/index.php?r=property/safe'
    # if amount > 1:
    #     amount = amount // 2
    form = {
        'token': token,
        'currency': 'money_r',
        'amount': amount,
    }

    if action == 'put':
        form.update({'put': ''})
        print('Положим {0} доц'.format(amount))
    if action == 'take':
        form.update({'take': ''})
        print('Заберем {0} доц'.format(amount))
    
    session.post(urlControl, data=form)


def oneIteration(session):
    try:
        data = getSafeData(session)
        if data['in_pocket'] > 0:
            safeControl(PUT, data['token'], data['in_pocket'], session)
        elif data['in_safe'] > 0:
            safeControl(TAKE, data['token'], data['in_safe'], session)
    except Exception as e:
        print('Ошибка:', e)


def unlimitedSafer():
    print('Add new session')
    session = requests.Session()
    ua = UserAgent()
    ua_fake = ua.chrome
    session.headers = {
        'user-agent': ua_fake
    }
    login('weakjoker5', '7shokpar7', session)
    print('Add auth on ', ua_fake)
    while True:
        print('Working ...')
        oneIteration(session)


def main():
    print('Starting ...')
    for _ in range(25):
        threading.Thread(target=unlimitedSafer).start()


def test():
    login('weakjoker5', '7shokpar7')
    for _ in range(4):
        oneIteration()


if __name__ == '__main__':
    main()
    # test()
