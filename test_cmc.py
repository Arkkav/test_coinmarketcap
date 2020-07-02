from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import timedelta, datetime
import pytest
import asyncio
import aiohttp
import time
import numpy as np
from main_page import MainPage
from selenium import webdriver


URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
PARAMETERS = {
	'start': '1',
	'limit': '10',
	'convert': 'USD',
	'sort': 'volume_24h',
}
HEADERS = {
	'Accepts': 'application/json',
	'X-CMC_PRO_API_KEY': '99e22be7-c182-4c20-ac4f-e48ceec32563',
}
REQUESTS_COUNT = 8
TEST_TIME_DELTA = timedelta(milliseconds=500)
LENGTH = 10
TEST_PERCENTILE = 450
TEST_RPS = 5


def request_func():
	session = Session()
	session.headers.update(HEADERS)
	try:
		response = session.get(URL, params=PARAMETERS)
		data = json.loads(response.text)
	except (ConnectionError, Timeout, TooManyRedirects) as e:
		print(e)
	td_elapsed = response.elapsed  # время запроса
	datetime_object = data.get('status').get('timestamp')[0:10]  # текущий день в формате yyyy-mm-ddThh:mm:ss.mmmZ
	length = len(response.content)/1000  # размер данных
	return td_elapsed, datetime_object, length


def test_1():
	currtime = datetime.utcnow().strftime('%Y-%m-%d')
	td_elapsed, datetime_object, length = request_func()
	assert length < LENGTH, "Response object is too big - " + str(length) + "kb"
	assert currtime == datetime_object[0:10], "Incorrect date of a data received from server"
	assert td_elapsed < TEST_TIME_DELTA, "Long response time"


# Asynchronous test run using py-test-xdist, but without calculating total rps and percentile
@pytest.mark.parametrize('id', [1, 2, 3, 4, 5, 6, 7, 8, ])
def test_3(id):
	currtime = datetime.utcnow().strftime('%Y-%m-%d')
	td_elapsed, datetime_object, length = request_func()
	assert length < LENGTH, "Response object is too big - " + str(length) + "kb"
	assert currtime == datetime_object[0:10], "Incorrect date of a data received from server"
	assert td_elapsed < TEST_TIME_DELTA, "Long response time"


async def async_request_func(session):
	start = datetime.now()
	async with session.get(URL, params=PARAMETERS) as response:
		result = await response.text()
		end = datetime.now()
		data = json.loads(result)
		td_elapsed = end- start  # время запроса
		datetime_object = data.get('status').get('timestamp')[0:10]  # текущий день в формате yyyy-mm-ddThh:mm:ss.mmmZ
		length = len(result) / 1000  # размер данных
	return td_elapsed, datetime_object, length


async def asynchronous():
	async with aiohttp.ClientSession(headers=HEADERS) as session:
		tasks = [asyncio.ensure_future(
			async_request_func(session)) for i in range(REQUESTS_COUNT)]
		results = await asyncio.gather(*tasks)
		return results


def test_2():
	currtime = datetime.utcnow().strftime('%Y-%m-%d')
	io_loop = asyncio.get_event_loop()
	try:
		results = io_loop.run_until_complete(asynchronous())
	except Exception as e:
		print(e)
	finally:
		io_loop.close()
	response_time = []
	rps = timedelta(milliseconds=0)
	for i in range(REQUESTS_COUNT):
		assert results[i][2] < LENGTH, "Response object is too big - " + str(results[i][2]) + "kb"
		assert results[i][1][0:10] == currtime, "Incorrect date of a data received from server"
		assert results[i][0] < TEST_TIME_DELTA, "Long response time " + str(results[i][0]) + "s"
		response_time.append(results[i][0])
		rps += results[i][0]
	rps = REQUESTS_COUNT / rps.total_seconds()
	percentile = np.percentile(response_time, 80).total_seconds() * 1000
	print('80% latency: ' + str(percentile) + 'ms')
	print('Speed: ' + str(rps) + 'rps')
	assert rps > TEST_RPS, "RPS " + str(rps) + " is less than " + str(TEST_RPS)
	assert percentile < TEST_PERCENTILE, "80% " + str(percentile) + " latency is less than " + str(TEST_PERCENTILE)


def test_change_language():
	browser = webdriver.Chrome()
	link = "https://coinmarketcap.com/"
	page = MainPage(browser, link)
	page.open()
	page.change_size(1920, 1080)
	for key in page.page_titles_order:
		time.sleep(3)
		page.go_to_desktop_language_panel()
		page.choose_desktop_language(key)
		page.title_has_right_language(key)
	page.change_size(800, 1024)
	for key in page.page_titles_order:
		time.sleep(3)
		page.go_to_mobile_side_bar()
		page.go_to_mobile_language_panel()
		page.choose_mobile_language(key)
		page.title_has_right_language(key)
	page.quit_browser()


if __name__ == '__main__':
	pass

