[ссылка на тестовое задание](https://drive.google.com/file/d/1lxGI4WkTMiTkONj679DjNdzEh97qt05t/view?usp=sharing)

## Телеграм бот

 [Бот телеграм](https://t.me/komandor_test2_bot)

 База данных: SQLite

 Данные: файл для когортного анализа

## Дашборд SuperSet с когортным анализом

Развернуть на linux не получилось. Docer и SuperSet  установил все запустилось судя по логам но подключатся через браузер не хотел. 
Воспользовался onlain сервисом [preset.io](preset.io)

[Дашборд SuperSet](https://7898282f.us1a.app.preset.io/superset/dashboard/8/?native_filters_key=aFJjV_4NUui1urdRlkVWRhfeIZ7-9N5cF89M_lm0IdV_h2opgQ5bBOrsqW2F_aiu)

Так как приписку к тестовому о подключении базы данных заметил не сразу сделал двумя способами.

### Первый способ

Chart: komandor_csv_file

В csv файл добавил дополнителный столбец с датой первой покупки клиента. Загрузил новый файл в Superset через GoogleSheets. И создал Chart перетаскивая столбцы без sql кода. 
sql код работал, но очень медленно 4 минуты.

### Второй способ

Chart: komandor_post

с помощью вашей базы даннных PostgresSQL.
(После очень неудобной работы с csv файлом, работа с бд одно удовольствие.)

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

На основе этого запроса получил данные и cформировал chart.

## Дашборд Datalens

На всякий случай сделал в Datalens

Принцип тот же что и первым chart дополнительное поля с первой покупкой клиента.

[Datalens](https://datalens.yandex.ru/0dfrxnaqroa4q-komandor)

 
