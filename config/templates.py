TMP_BOT_INFO = (
    "👋 <b>Привет, сосед!</b>\n"
    "Я — проект, разработанный вашим соседом. Работаю сугубо в рамках нашего "
    "ЖК «Армейский». Помогу вам узнать больше о выключениях электричества. "
    "Здесь можно получить информацию обо мне и узнать, что я умею.\n\n"
    "❓<b>Что ты умеешь?</b>\n"
    "❕<i>1. Сообщать о наличии электроэнергии в любое время суток, "
    "а также время, когда было отключение/включение;\n"
    "     2. Рассылать уведомления о включении/отключении "
    "электричества в реальном времени тем, "
    "кто подписан на рассылку;\n"
    "     3. Выдавать статистику за последнее время "
    "о наличии электроэнергии.\n\n"
    "💡 если моя помощь будет полезна, "
    "то я обязательно научусь делать что-то новое.</i>\n\n"
    "❓<b>Знаешь, когда включат свет?</b>\n"
    "❕<i> Увы, на текущий момент нет надежного источника такой информации. "
    "Могу предложить ориентироваться на данные из вкладки «Статистика», "
    "где есть средние показатели за прошлые дни.</i>\n\n"
    "❓<b>Почему ты не всегда отвечаешь?</b>\n"
    "❕<i> Я, как и обычный собеседник, получаю и отправляю сообщения. "
    "Для меня очень важно, чтобы вашего соединения "
    "хватало для таких операций. "
    "Если вы сталкиваетесь с ситуацией, что я вам не отвечаю, "
    "или отвечаю по несколько раз,"
    " то скорее всего, причина в вашем слабом интернете. "
    "Если же ситуация повторяется при "
    "стабильном подключении к сети, напишите в «Обратную связь».</i>\n\n"
    "❓<b>Почему уведомления приходят не сразу?</b>\n"
    "❕<i>Это обусловлено внутренними процессами, которые происходят"
    '"под капотом". Задержка во время отключения ~1мин., а во время '
    "включения ~3мин.</i>\n\n"
    "❓<b>Зачем тебе информация обо мне?</b>\n"
    "❕<i> Информация при регистрации служит для формирования "
    "более качественной статистики о "
    "выключениях электричества для пользователей. "
    "Если хотите сохранить анонимность, "
    "можно пропустить вопрос о номере дома и квартиры.</i>\n\n"
    "❓<b>На какие ЖК распространяется твоя работа?</b>\n"
    "❕<i>Я показываю актуальную информацию в пределах ЖК «Армейский».  "
    "Вы можете рекомендовать меня жителям других комплексов, "
    "графики отключений которых совпадают с нашим, "
    "но гарантировать 100% точность, увы, будет невозможно.</i>\n\n"
    "Спасибо за внимание ✌\n\n"
    "<i>*чтобы вернуться в главное меню, "
    "воспользуйтесь кнопкой <b>«Меню»</b></i>"
)
TMP_REGISTER_STEP_ONE = (
    "Выберите свой дом и введите номер квартиры\n\n"
    "<i>Это необходимо для формирования лучшей статистики, "
    "<u>можно пропустить</u></i>"
    "\n\nВаш адрес Армейская 8*?\n<i><b>(выбрать ниже из предложенных)</b></i>"
)
TMP_SUPPORT_INFO = (
    "<b>📢 Обратная связь</b> 📢\n\n"
    "‼ Перед отправкой сообщения, ознакомьтесь с часто "
    "задаваемыми вопросами во вкладке «О Боте».\n\n"
    "Чтобы я зарегистрировал ваше обращение, напишите свой текст ниже.\n"
    "Вы можете отправить:\n"
    "<b>— проблемные моменты;\n"
    "— свои отзывы;\n"
    "— предложения по улучшению.</b>\n"
    "Старайтесь писать понятно и компактно 😉\n\n"
    "<i>*чтобы вернуться в главное меню, нажмите <b>«Назад»</b></i>"
)
TMP_RECEIVED_RESPONSE = "📨 <b>Ответ на обратную связь</b>\n\n"
TMP_NO_REPLY_POSTFIX = "\n\n<i>*отвечать на это сообщение <u>не нужно</u></i>"
TMP_ADMIN_MSG_PREFIX = "🎙 <b>Сообщение от администратора</b>"
TMP_NO_REPLY_ALL_POSTFIX = (
    "<i>*разослано всем пользователям, отвечать <u>не нужно</u></i>"
)
TMP_MENU = "<b>📱 Главное меню</b>"
TMP_LIGHT_INFO = "На текущий момент"
TMP_DTEK_INFO = (
    "Актуальный график 🎲\n\n"
    '<i>Источник: <a href="https://www.dtek-oem.com.ua/ua/shutdowns">'
    "<b>Сайт ДТЭК</b></a></i>"
)
TMP_LIGHT_ON = (
    "💡 На текущий момент 💡\n\n"
    "📃 Статус: <b>Электричество есть</b> 🟢\n"
    "📆 Время включения: {time_of_event}\n"
    "⏱️ Времени прошло: {time_passed}"
)
TMP_LIGHT_OFF = (
    "🕯 На текущий момент 🕯\n\n"
    "📃 Статус: <b>Электричества нет</b> 🔴\n"
    "📆 Время отключения: {time_of_event}\n"
    "⏱️ Времени прошло: {time_passed}"
)

TMP_USER_SUBED = (
    "🚨 <b>Уведомления</b> 🚨\n\n" "<b>Вы подписаны на уведомления</b> 👍"
)
TMP_USER_UNSUBED = (
    "🚨 <b>Уведомления</b> 🚨\n\n<i>Если вы подпишитесь на уведомления, "
    "то я буду вам отправлять сообщения в моменты, "
    "когда электричество включают или отключают</i>\n\n"
    "<b>Вы не подписаны на уведомления</b> 👎"
)
TMP_SUB_SUCCESS = "🔔 Вы успешно подписались на уведомления"
TMP_UNSUB_SUCCESS = "🔕 Вы успешно отписались от уведомлений"
TMP_SUPPORT_MSG_CREATED = "📤 Обращение успешно отправлено"
TMP_REGISTER_FLAT_NUM = "Ваш номер квартиры?\n<b><i>(ввести цифрами)</i></b>"
TMP_REGISTER_SUCCESS = "📒 Регистрация прошла успешно!"
TMP_LIGHT_NOTIFICATION_ON = "🔋 <b>Включили электричество</b> 🔋"
TMP_LIGHT_TIME_NOTIFICATION_ON = "⌛ Электричества не было"
TMP_LIGHT_NOTIFICATION_OFF = "🪫 <b>Электричество выключили</b> 🪫"
TMP_LIGHT_TIME_NOTIFICATION_OFF = "⌛ Электричество было"
TMP_NOTIFICATION_REASON = (
    "\n\n<i>*вы получили это сообщение, потому что подписаны на рассылку</i>"
)
TMP_STAT_INFO_MAIN = "🔬 <b>Статистика</b> 🔬"
TMP_STAT_INFO_LAST_WEEK = (
    "🔎 Данные за неделю\n"
    "<i>({stat_date_week_ago} - {stat_date_now})</i>\n\n"
    "➖ Электричества не было в сумме: <b>{light_off_time}</b>\n"
    "➕ Электричество было в сумме: <b>{light_on_time}</b>\n"
    "〰 Электричество включалось в среднем на: <b>{light_turn_on_avg_data}</b>"
)

TMP_STAT_INFO_LAST_TWO_WEEKS = (
    "🔎 Данные за прошлую неделю\n"
    "<i>({stat_date_week_ago} - {stat_date_now})</i>\n\n"
    "➖ Электричества не было в сумме: <b>{light_off_time}</b>\n"
    "➕ Электричество было в сумме: <b>{light_on_time}</b>\n"
    "〰 Электричество включалось в среднем на: <b>{light_turn_on_avg_data}</b>"
)
TMP_STAT_INFO_NO_DATA = (
    "🔎 Данные за прошлую неделю\n"
    "<i>({stat_date_week_ago} - {stat_date_now})</i>\n\n"
    "❗ <b>Недостаточно данных, ожидайте</b> ❗"
)
TMP_STAT_INFO_COMPARE = (
    "🔎 Сравнение данных за две недели\n\n"
    "➕ На этой неделе электричества было: "
    "{emoji} <b>{less_or_more}</b>"
    "<b>{light_on_time}%</b>, чем на прошлой неделе.\n"
    "〰 На этой неделе электричество включалось в среднем: "
    "{emoji_avg} <b>{less_or_more_avg}</b>"
    "<b>{light_on_time_avg}%</b>, чем на прошлой неделе."
)
TMP_USER_INFO = (
    "🌃 <b>О пользователях</b> 🌃\n\n"
    "🔝 Всего зарегистрировано: <b>{total_reg}</b> 👤\n\n"
    "Из них:\n"
)
TMP_USER_INFO_HOME_PERCENT = "{home} — <b>{percent}%</b>"
