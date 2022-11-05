from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import re
from time import sleep


class Elyza_Pencil():
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    def close(self) -> None:
        self.driver.quit()
    
    def _query(self, keywords: list) -> str:
        url = "https://www.pencil.elyza.ai/"
        self.driver.get(url)
        forms = self.driver.find_elements(By.XPATH, '//input[@type="text"]')
        for i in range(min(8, len(keywords))):
            forms[i].clear()
            forms[i].send_keys(keywords[i])
        checkbox = self.driver.find_elements(By.XPATH, '//input[@type="checkbox"]')[0]
        checkbox.click()
        button = self.driver.find_elements(By.XPATH, '//button[text()="AI執筆スタート"]')[0]
        button.click()
        sleep(15)
        result_url = self.driver.current_url
        return result_url
    
    def _get_result(self, draft_id: str):
        url = f"https://api.pencil.elyza.ai/web/drafts/{str(draft_id)}"
        response = requests.get(url)
        return response


def generate(keywords: list) -> dict:
    ep = Elyza_Pencil()
    try:
        result_url = ep._query(keywords)
    finally:
        ep.close()
    draft_id = re.search(r'\d+$', result_url).group()
    result = ep._get_result(draft_id)
    return result.json()


if __name__ == "__main__":
    keywords = ["いい感じ", "天気が悪い"]
    res = generate(keywords)
    print(res)
    # {
    #     'draft_id': '1059814913240287847', 
    #     'keywords': ['いい感じ', '天気が悪い'], 
    #     'kind': 'news', 
    #     'status': 'success', 
    #     'title': '天気の悪い日はいい感じに距離が縮まる!?男子が思う「いい感じの彼女」の特徴4つ', 
    #     'content': '天気の悪い日に「いいな」と思う女性の特徴を22〜39歳の社会人男性に聞いた。気遣いができる、雰囲気がいい、笑顔がかわいい。服装がオシャレである、いい感じの関係が続いている。'
    # }