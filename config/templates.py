TMP_BOT_INFO = (
    "👋 <b>Привет, сосед!</b>\n"
    "Здесь ты сможешь получить больше информации о боте и узнать о его функциях.\n\n"
    "❓Что за бот?\n"
    "❕<i>Это некоммерческий проект, разработанный вашим соседом. Работает сугубо в рамках нашего "
    "ЖК «Армейский». Служит для облегчения жизни жителям ЖК.</i>\n\n"
    "❓Для чего нужен?\n"
    "❕<i>Нужен для того, чтобы дать людям возможность быстро получать актуальную "
    "информацию наличии электроэнергии в ЖК и сопутствующую информацию. Ну и, конечно же, "
    "очистить чат ОСМД от постоянных вопросов: «Света есть? А когда ушла?»</i> 😄\n\n"
    "❓Что умеет?\n"
    "❕<i>1. Сообщать о наличии электроэнергии в любое время суток, а также время, когда было отключение/включение;\n"
    "2. Рассылать уведомления подписанным на рассылку пользователям в момент, когда произошло отключение/включение;\n"
    "3. Выдавать статистику за последнее время о наличии электроэнергии;\n"
    "💡если бот будет востребован, список возможностей будет дополняться.</i>\n\n"
    "❓Когда включат свет?\n"
    "❕<i> Увы, на текущий момент нет надежного источника такой информации. "
    "Но можно ориентироваться на данные из вкладки «Статистика», "
    "где есть средние показатели за прошлые дни.</i>\n\n"
    "❓Зачем боту информация обо мне?\n"
    "❕<i> Информация при регистрации служит для формирования более качественной статистики о "
    "выключениях электричества для пользователей. Если хотите сохранить анонимность, "
    "можно пропустить вопрос о номере дома и квартиры.</i>\n\n"
    "❓На какие ЖК распространяется работа бота?\n"
    "❕<i>Бот показывает актуальную информацию в пределах ЖК «Армейский».  "
    "Им можно делиться с жителями других комплексов, график отключений которых совпадают с нашим, "
    "но гарантировать 100% точность, увы, будет невозможно.</i>\n\n"
    "Спасибо за внимание ✌️\n\n"
    '<i>*чтобы вернуться в главное меню, воспользуйтесь кнопкой <b>"Меню"</b></i>'
)
TMP_REGISTER_STEP_ONE = (
    "Выберите свой дом и введите номер квартиры\n\n"
    "<i>Это необходимо для формирования лучшей статистики, <u>можно пропустить</u></i>"
    "\n\nВаш адрес Армейская 8*?\n<i><b>(выбрать ниже из предложенных)</b></i>"
)
TMP_SUPPORT_INFO = (
    "<b>📢 Обратная связь</b>\n\n"
    "Чтобы зарегистрировать обращение, напишите боту текст.\n"
    "Вы можете отправлять сюда:\n"
    "<b>— проблемные моменты;\n"
    "— свои отзывы;\n"
    "— предложения по улучшению.</b>\n"
    "Старайтесь писать понятно и компактно 😉"
)
TMP_NO_REPLY_POSTFIX = "\n\n<i>*на это сообщение отвечать <u>не нужно</u></i>"
TMP_ADMIN_MSG_PREFIX = "🎙 <b>Сообщение от администратора</b>"
TMP_NO_REPLY_ALL_POSTFIX = (
    "<i>*разослано всем пользователям, отвечать <u>не нужно</u></i>"
)
TMP_MENU = "<b>Главное меню</b>"
TMP_LIGHT_INFO = "На данный момент"
TMP_DTEK_INFO = "Актуальный график 🥴"
TMP_LIGHT_ON = (
    "💡 На данный момент 💡\n\n"
    "📃 Статус: <b>Электричество есть</b> 🟢\n"
    "📆 Время включения: {time_of_event}\n"
    "⏱️ Времени прошло: {time_passed}"
)
TMP_LIGHT_OFF = (
    "🕯 На данный момент 🕯\n\n"
    "📃 Статус: <b>Электричества нет</b> 🔴\n"
    "📆 Время отключения: {time_of_event}\n"
    "⏱️ Времени прошло: {time_passed}"
)
TMP_USER_SUBED = "Вы подписаны на уведомления 👍"
TMP_USER_UNSUBED = "Вы не подписаны на уведомления 👎"
TMP_SUB_SUCCESS = "🔔 Вы успешно подписались на уведомления"
TMP_UNSUB_SUCCESS = "🔕 Вы успешно отписались от уведомлений"
TMP_SUPPORT_MSG_CREATED = "📤 Обращение успешно отправлено"
TMP_REGISTER_FLAT_NUM = "Ваш номер квартиры?\n(ввести цифрами)"
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
    "🔘 Данные за неделю\n"
    "<i>({stat_date_week_ago} - {stat_date_now})</i>\n\n"
    "➖ Электричества не было в сумме: <b>{light_off_time}</b>\n"
    "➕ Электричество было в сумме: <b>{light_on_time}</b>\n"
    "〰 Электричество включалось в среднем на: <b>{light_turn_on_avg_data}</b>"
)

TMP_STAT_INFO_LAST_TWO_WEEKS = (
    "🔘 Данные за прошлую неделю\n"
    "<i>({stat_date_week_ago} - {stat_date_now})</i>\n\n"
    "➖ Электричества не было в сумме: <b>{light_off_time}</b>\n"
    "➕ Электричество было в сумме: <b>{light_on_time}</b>\n"
    "〰 Электричество включалось в среднем на: <b>{light_turn_on_avg_data}</b>"
)

TMP_STAT_INFO_COMPARE = (
    "🔘 Сравнение данных за две недели\n\n"
    "➕ На этой неделе электричества было (по времени): "
    "{emoji} <b>{less_or_more}</b> на <b>{light_on_time}%</b>, чем на прошлой.\n"
    "〰 Электричество включалось в среднем (по времени): "
    "{emoji_avg} <b>{less_or_more_avg}</b> на <b>{light_on_time_avg}%</b>, чем на прошлой."
)
