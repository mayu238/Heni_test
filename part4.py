'''
Inner Join: Selects all records that have matching values in two or more tables
e.g. 
SELECT name
FROM table1
INNER JOIN table2
ON table1.name = table2.name

Left Join: Selects all the records from the left table and the matching records from the right table. If there are no matches NULL is returned
e.g.
SELECT name
FROM table1
LEFT JOIN table2
ON table1.name = table2.name

Right Join: Selects all the records from the right table and the matching records from the left table. If there are no matches NULL is returned
e.g.
SELECT name
FROM table1
RIGHT JOIN table2
ON table1.name = table2.name

Full Join: Combines the results of both left and right outer joins. THis table contains all records from both tables.
e.g.
SELECT table1.name, table2.name
FROM table1
FULL JOIN table2
ON table1.field1 = table2.field1
'''

a)
SELECT flights.arr_time,flights.origin,
flights.dest, airlines.name
FROM flights
INNER JOIN airlines
ON flights.carrier = airlines.carrier

b)
SELECT flights.arr_time,flights.origin,
flights.dest, airlines.name
FROM flights
INNER JOIN airlines
ON flights.carrier = airlines.carrier
and name LIKE '%JetBlue%' 

c)
SELECT origin,count(origin) FROM
(SELECT flights.arr_time,flights.origin,
flights.dest, airlines.name
FROM flights
INNER JOIN airlines
ON flights.carrier = airlines.carrier
and name LIKE '%JetBlue%') 
group by origin
order by count(origin) ASC

d)
SELECT origin,count(origin) as numFlights FROM
(SELECT flights.arr_time,flights.origin,
flights.dest, airlines.name
FROM flights
INNER JOIN airlines
ON flights.carrier = airlines.carrier
and name LIKE '%JetBlue%')
WHERE count(origin)>100 
group by origin
order by count(origin) ASC
