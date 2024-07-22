import logging
import telebot
from telebot import apihelper
import json
import argparse
import os

script_dir = os.path.dirname(__file__)

parameters = json.loads(open(f"{script_dir}\config.json").read())

# Telegram Init
TELE_USE_PROXY=parameters["preferences"]["use_proxy"]
PROXY= parameters["preferences"]["proxy"]
BOT_TOKEN = parameters["preferences"]["bot_token"]
PROTOCOL = parameters["preferences"]["protocol"]
CHATID = parameters["preferences"]["chat_id"]


state_dictionary = {
    1: "Ошибка",
    2: "Проверено",
    3: "Приостановлено",
    4: "Супер - раздача",
    5: "Раздаётся",
    6: "Загружается",
    7: "Супер - сид[F]",
    8: "Раздаётся[F]",
    9: "Загружается[F]",
    10: "Сид в очереди",
    11: "Завершено",
    12: "В очереди",
    13: "Остановлено",
    17: "Распределение",
    18: "Pfuhe; f.ncz метаданные",
    19: "Соединение с пирами",
    20: "Перемещение",
    21: "Очистка",
    22: "Требуется DHT",
    23: "Поиск пиров",
    24: "Сопоставление",
    25: "Запись"
}


def send_telegram_msg(headertext, msgtext):
    logger = telebot.logger
    telebot.logger.setLevel(logging.DEBUG)
    if TELE_USE_PROXY:
        apihelper.proxy = {PROTOCOL}
    else:
        bot = telebot.TeleBot(BOT_TOKEN)

    bot.send_message(CHATID, f"{headertext}\n{msgtext}", parse_mode="HTML")


def proceed_state():
    """
    % F - имя загруженного файла(для торрентов с одним файлом)
    % D - папка сохранения файлов
    % N - название торрента
    % P - предыдущее состояние торрента
    % L - метка
    % T - трекер
    % M - строка статуса(как в колонке статуса)
    % I - hex - кодированный инфо - хеш
    % S - состояние торрента
    % K - вид торрента(одиночный | мульти)
    где состояние - одно из:
    Ошибка - 1
    Проверено - 2
    Приостановлено - 3
    Супер - раздача - 4
    Раздаётся - 5
    Загружается - 6
    Супер - сид[F] - 7
    Раздаётся[F] - 8
    ЗАгружается[F] - 9
    Сид в очереди - 10
    Завершено - 11
    В очереди - 12
    Остановлено - 13
    В очереди - 12
    Распределение - 17
    Pfuhe; f.ncz метаданные - 18
    Соединение с пирами - 19
    Перемещение - 20
    Очистка - 21
    Требуется DHT - 22
    Поиск пиров - 23
    Сопоставление - 24
    Запись - 25
    """

    file_name = ""
    file_folder = ""
    torrent_name = ""
    previouse_state = 0
    torrent_label = ""
    torrent_tracker = ""
    status = ""
    hex_val = ""
    torrent_state = 0
    torrent_type = ""
    strLogName = f"{script_dir}\\app_logs.log"

    # Init parameters
    parser = argparse.ArgumentParser(description="UTorrent job alert")
    parser.add_argument("--f", default="", type=str, help="имя загруженного файла")
    parser.add_argument("--d", default="", type=str, help="папка сохранения файлов")
    parser.add_argument("--n", default="", type=str, help="имя торрента")
    parser.add_argument(
        "--p", default=0, type=int, help="предыдущее состояние торрента"
    )
    parser.add_argument("--l", default="", type=str, help="метка")
    parser.add_argument("--t", default="", type=str, help="tracker")
    parser.add_argument("--m", default="", type=str, help="строка статуса")
    parser.add_argument("--i", default="", type=str, help="инфо хэш")
    parser.add_argument("--s", default=0, type=int, help="состояние торрента")
    parser.add_argument("--k", default="", type=str, help="вид торрента")

    args = parser.parse_args()

    print(args)

    file_name = args.f if args.f != "" else file_name
    file_folder = args.d if args.d != "" else file_folder
    torrent_name = args.n if args.n != "" else torrent_name
    previouse_state = int(args.p) if int(args.p) > 0 else previouse_state
    torrent_label = args.l if args.l != "" else torrent_label
    torrent_tracker = args.t if args.t != "" else torrent_tracker
    status = args.m if args.m != "" else status
    hex_val = args.i if args.i != "" else hex_val
    torrent_state = int(args.s) if int(args.s) > 0 else torrent_state
    torrent_type = args.k if args.k != "" else torrent_type

    # Init logging
    logging.basicConfig(
        filename=strLogName,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s : %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S %p",
    )
    logging.info("=== Application started ===")

    logging.info(f"Proceed torrent info: {file_name}")

    if torrent_state == 11:
        send_telegram_msg("<b>Загрузка завершена</b>", f"{file_name}")
    else:
        send_telegram_msg(
            "<b>Изменение состояния</b>",
            f"{file_name}\n{state_dictionary[previouse_state]} --> {state_dictionary[torrent_state]}",
        )

    logging.info("=== Complete ===")


if __name__ == "__main__":
    proceed_state()
