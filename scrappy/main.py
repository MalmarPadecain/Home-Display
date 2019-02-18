import multiprocessing
import functools

from scrappy.scrapers import meteo, calls
import secret

meteo.scrap_and_write(secret.METEO_ZIP)

# methods = [functools.partial(meteo.scrap_and_write, secret.METEO_ZIP), phone_list.scrap_and_write]
#
# p_lst = []
# for method in methods:
#     process = multiprocessing.Process(target=method)
#     process.start()
#     p_lst.append(process)
#
# for process in p_lst:
#     process.join()
