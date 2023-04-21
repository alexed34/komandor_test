## Телеграм бот

 [Бот телеграм](https://t.me/komandor_test2_bot)

 База данных: SQLite

 Данные: файл для когортного анализа

## Дашборд SuperSet с когортным анализом

Развернуть на linux не получилось. Docer и SuperSet  установил все запустилось судя по логам но подключатся через браузер не хотел. 
Воспользовался onlain сервисом [preset.io](preset.io)

Ссылки ведут на один и тот же дашборд. SuperSet создал разные url.

[ссылка 1](https://7898282f.us1a.app.preset.io/superset/dashboard/p/zY1AP5OZBRj/)

[ссылка 2](https://7898282f.us1a.app.preset.io/superset/dashboard/8/?native_filters_key=xV4Qs0XkffKWrYZgREyUeJSoPcz3b8jQ_K0rLoTochfKxkV4_-8n2KWOKEgg1zJH)

Выяснилось что при попытке войти по ссылке требуется ввести email я на всякий случай добавил доступ для *yulenkovayue@sm-komandor.ru*

Код sql для когортного анализа.

```  
WITH cohorts
AS (
	SELECT DISTINCT card_id
		, min(datet) OVER (PARTITION BY card_id) cohort_date
	FROM new_date k
	)
SELECT cohorts.cohort_date
	, datet AS purchase_month
	, COUNT(DISTINCT cohorts.card_id) AS cohort_size
FROM new_date
INNER JOIN cohorts ON new_date.card_id = cohorts.card_id
GROUP BY 1, 2
ORDER BY 1, 2
```
Я не разобрался какой диалект в SuperSet, но что бы код заработал, пришлось немного упростить отказатся от extract. На extract запрос ломался.

Код работает на сервисе, но очень медленно 4 минуты в SQL Lab.
Поступил проще. Создал в файле еще одно поле куда добавил первую покупку клиента и в SuperSet создал график-таблицу простым перетаскиванием полей.


## Дашборд Datalens

На всякий случай сделал в Datalens

Принцип тот же дополнительное поля с первой покупкой клиента.

[Datalens](https://datalens.yandex.ru/0dfrxnaqroa4q-komandor)

 