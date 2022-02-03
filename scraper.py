import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.bbc.com/mundo'

XPATH_LINK_TO_ARTICLE = '//h3[@class="bbc-t81ytv e1tfxkuo2"]/a/@href'
XPATH_TITLE = '//h1[@class="bbc-1lsgtu3 e1yj3cbb0"]/text()'
XPATH_BODY = '//div[@class="bbc-19j92fr e57qer20"]/p//text()'

def delete_invalid_caracters(title):   
    title = title.replace("?","")
    title = title.replace("¿","")
    title = title.replace("\'","")
    title = title.replace("/","")
    title = title.replace(":","")
    title = title.replace("*","")
    title = title.replace("<","")
    title = title.replace(">","")        
    title = title.replace("|","")        

    return title    

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                print("Title: " + title)
                title_txt = delete_invalid_caracters(title)              
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return
                        
            with open(f'{today}/{title_txt}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
            
        else:
            raise ValueError(print("Error: "+{response.status_code}))
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices:
                parse_notice("https://www.bbc.com" + link, today)
            
        else:
            raise ValueError(print("Error: "+{response.status_code}))
    except ValueError as ve:
        print(ve)
        
def main():
    parse_home()
    
if __name__ == '__main__':
    main()