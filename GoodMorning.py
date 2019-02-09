__author__ = 'Rohit Shende'
import cookielib
import datetime
import urllib2
from random import randint

import requests
from bs4 import BeautifulSoup


# returns a list of quotes by scrapping a website
def get_quotes():
    url = "http://quotespill.com/motivational-morning-messages/"
    req = requests.get(url)
    bs = BeautifulSoup(req.text, features="html.parser")

    quotes = bs.find_all('blockquote')
    actual_quotes = map(lambda x: x.text.strip().encode('utf8'), quotes)
    return actual_quotes


def read_phonebook():
    file = 'phonebook.txt'
    f = open(file)
    contacts = f.readlines()
    contacts = map(lambda x: x.strip().split(' ')[0], contacts)
    return contacts


class Way2SMS:
    username = '7028447369'
    password = '7028447369'

    # logging into the sms site
    url = 'http://site24.way2sms.com/Login1.action?'
    data = 'username=' + username + '&password=' + password + '&Submit=Sign+in'

    # For cookies

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    def __init__(self):
        # Adding header details
        self.opener.addheaders = \
            [('User-Agent',
              'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
        try:
            self.usock = self.opener.open(self.url, self.data)
        except IOError:
            print "error"

    def send_sms(self, number, message):
        message = "+".join(message.split(' '))
        jession_id = str(self.cj).split('~')[1].split(' ')[0]
        send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
        send_sms_data = 'ssaction=ss&Token=' + jession_id + '&mobile=' + number + '&message=' + message + '&msgLen=136'
        self.opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token=' + jession_id)]
        try:
            sms_sent_page = self.opener.open(send_sms_url, send_sms_data)
        except IOError:
            print "Error"
            return False
        print "success"
        return True


if __name__ == '__main__':
    quotes = get_quotes()
    portal = Way2SMS()
    numbers = read_phonebook()
    time_to_sms = datetime.time(9, 0, 0, 0)  # sms at 9 am

    for num in numbers:
        index = randint(0, len(quotes))
        msg = quotes[index] + '\n- Rohit'
        print '\n\n------- Sending SMS -----------'
        print 'number :', num, '\nsms :', msg
        print '-' * 30
        portal.send_sms(num, msg)

    print '********* SMS Sent Successfully ! ****************'
