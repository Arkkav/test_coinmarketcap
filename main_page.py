import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from base_page import BasePage


class MainPage(BasePage):
	def __init__(self, browser, url):
		super().__init__(browser, url)
		self.page_titles_order = {
			'DE': (1, "Kryptowährung Marktkapitalisierungen | CoinMarketCap"),
			'EN': (2, "Cryptocurrency Market Capitalizations | CoinMarketCap"),
			'ES': (3, "Capitalización de Mercado de Criptomoneda | CoinMarketCap"),
			'FIL': (4, "Kapitalisasyon sa Market ng Cryptocurrency | CoinMarketCap"),
			'FR': (5, "Capitalisations Marché Crypto-Monnaie | CoinMarketCap"),
			'HI': (6, "क्रिप्टोकरेंसी मार्केट पूंजीकरण | CoinMarketCap"),
			'IT': (7, "Capitalizzazioni di mercato di criptovaluta | CoinMarketCap"),
			'JA': (8, "仮想通貨の時価総額 | CoinMarketCap"),
			'KO': (9, "암호화폐 시가총액 | CoinMarketCap"),
			'PT-BR': (10, "Capitalizações do Mercado de Criptomoeda | CoinMarketCap"),
			'RU': (11, "Рыночные капитализации криптовалют | CoinMarketCap"),
			'TR': (12, "Kripto Para Piyasa Değeri | CoinMarketCap"),
			'VI': (13, "Tổng Vốn Hóa Thị Trường Tiền Điện Tử | CoinMarketCap"),
			'ZH': (14, "数字货币行情_最新加密货币价格走势_虚拟货币价格排行榜_加密货币市值 | CoinMarketCap"),
			'ZH-TW': (15, "加密貨幣市值 | CoinMarketCap"),
		}
		self.desktop_panel_button = ".frscwy-0.eNPZip > .frscwy-2.XiBjH:nth-child(2) .sc-14gaqg0-0.jGQJR"
		self.desktop_choose_language_button = \
			".cmc-popover__dropdown > .frscwy-3.frscwy-4.iUHqnq:nth-child({}) .cmc-language-picker__option"

		self.mobile_side_bar_button = ".svg-inline--fa.fa-bars.fa-w-14.cmc-icon"
		self.mobile_panel_button = ".jacumr-1.idJTBb > .jacumr-2.iYVkEr:nth-child(1) .jacumr-0.fCcmrJ"
		self.mobile_choose_language_button = ".jacumr-3.jacumr-4.kVVJu:nth-child({})"

	def go_to_mobile_side_bar(self):
		assert self.is_element_present(By.CSS_SELECTOR, self.mobile_side_bar_button), "Language panel doesn't exist"
		login_link = self.browser.find_element(By.CSS_SELECTOR, self.mobile_side_bar_button)
		login_link.click()

	def go_to_mobile_language_panel(self):
		assert self.is_element_present(By.CSS_SELECTOR, self.mobile_panel_button), "Language panel doesn't exist"
		login_link = self.browser.find_element(By.CSS_SELECTOR, self.mobile_panel_button)
		login_link.click()

	def choose_mobile_language(self, language):
		assert self.is_element_present(By.CSS_SELECTOR,
					self.mobile_choose_language_button.format(str(self.page_titles_order.get(language)[0]))), \
					"Language {} button doesn't exist".format(language)
		login_link = self.browser.find_element(By.CSS_SELECTOR,
					self.mobile_choose_language_button.format(str(self.page_titles_order.get(language)[0])))
		login_link.click()

	def is_element_present(self, how, what):
		try:
			self.browser.find_element(how, what)
		except NoSuchElementException:
			return False
		return True

	def go_to_desktop_language_panel(self):
		assert self.is_element_present(By.CSS_SELECTOR, self.desktop_panel_button), "Language panel doesn't exist"
		login_link = self.browser.find_element(By.CSS_SELECTOR, self.desktop_panel_button)
		login_link.click()

	def choose_desktop_language(self, language):
		assert self.is_element_present(By.CSS_SELECTOR,
					self.desktop_choose_language_button.format(str(self.page_titles_order.get(language)[0]))), \
					"Language {} button doesn't exist".format(language)
		login_link = self.browser.find_element(By.CSS_SELECTOR,
					self.desktop_choose_language_button.format(str(self.page_titles_order.get(language)[0])))
		login_link.click()

	def title_has_right_language(self, language):
		time.sleep(5)
		current_title = self.browser.title
		right_title = self.page_titles_order.get(language)[1]
		assert current_title == right_title, "Title is not right for language {}".format(language)

	def change_size(self, w=1920, h=1080):
		self.browser.set_window_size(w, h)

	def quit_browser(self):
		self.browser.quit()



