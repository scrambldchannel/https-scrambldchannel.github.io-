Title: SQL cheat sheet
Date: 2019-10-16 11:59
Category: docs
Tags: sql, postgres
slug: sql-cheatsheet
Authors: Alexander
Summary: Documenting common SQL queries and variations between flavours

## Queries

A few snippets to refer back to that use the pagila example database - <https://github.com/devrimgunduz/pagila>

### Simple selects and filtering

```SQL
/* trivial select */
SELECT *
FROM actor;

/* output only specific fields */
SELECT first_name, last_name 
FROM actor;

/* rename output columns */ 
SELECT first_name AS name, last_name AS surname 
FROM actor;

/* only unique records */ 
SELECT DISTINCT first_name 
FROM actor;

/* simple where clause */
SELECT first_name AS name, last_name AS surname 
FROM actor
WHERE last_name = 'CHASE';

/* wildcard filtering */
SELECT first_name AS name, last_name AS surname 
FROM actor
WHERE last_name LIKE 'CHA%';

/* numeric operations */
SELECT *
FROM payment_p2017_01
WHERE amount > 10

/* limit rows returned first ten */
SELECT *
FROM payment_p2017_01
LIMIT 10

/* add an offset */
SELECT *
FROM payment_p2017_01
LIMIT 10
OFFSET 5
```

### Aggregations and grouping

```SQL
/* counts of different first names */
SELECT count(*), first_name
FROM actor
GROUP BY first_name

/* order by highest count */
SELECT count(*), first_name
FROM actor
GROUP BY first_name
ORDER BY count DESC

/* filter on aggregations */
SELECT count(*), first_name
FROM actor
GROUP BY first_name
HAVING count(*) > 2
ORDER BY count ASC
```

### Joins

#### Inner joins

```SQL
/* Explicit inner join */
SELECT *
FROM customer
INNER JOIN address ON customer.address_id = address.address_id;

/* implicit version of the above */
SELECT *
FROM customer, address
WHERE customer.address_id = address.address_id;

/* implicit inner join of more than two tables using tagging to cut down on typing */
SELECT f.title, a.first_name, a.last_name
FROM film f, film_actor fa, actor a
WHERE f.film_id = fa.film_id
AND	fa.actor_id = a.actor_id

/* use count to get number of actors in each film */
SELECT count(*), f.title
FROM film f, film_actor fa, actor a
WHERE f.film_id = fa.film_id
AND	fa.actor_id = a.actor_id
GROUP BY f.title
```

#### Outer joins

Only left illustrated here but right essentially is the same thing in reverse.

```SQL
/* left outer join */
SELECT *
FROM payment_p2017_05 p5
LEFT JOIN  payment_p2017_01 p1 ON p5.customer_id = p1.customer_id
WHERE p1.customer_id IS NULL

/* left outer join including only records in left table and not in right table*/
SELECT *
FROM payment_p2017_05 p5
LEFT JOIN  payment_p2017_01 p1 ON p5.customer_id = p1.customer_id
WHERE p1.customer_id IS NULL

/* combining an inner join and and an outer join */
SELECT c.first_name, c.last_name
FROM payment_p2017_05 p5 
INNER JOIN customer c ON p5.customer_id = c.customer_id
LEFT JOIN  payment_p2017_01 p1 ON p5.customer_id = p1.customer_id
WHERE p1.customer_id IS NULL

/* full outer join */
SELECT p5.customer_id AS p5_cust, p1.customer_id AS p1_cust
FROM payment_p2017_05 p5
FULL JOIN payment_p2017_01 p1 ON p5.customer_id = p1.customer_id
```

#### Other joins

```SQL
/* cross or cartesian join */
SELECT *
FROM store s
CROSS JOIN address a

/* cross join implicit */
SELECT *
FROM store s, address a

/* natural join - this will work but not really useful in practice and can have unforseen consequences */ 
SELECT *
FROM payment_p2017_01
NATURAL JOIN rental;	
```

### Union, except and intersect

```SQL
/* union - all films that either Bob and Jennifers are in, excluding duplicates */
SELECT DISTINCT f.title
FROM film f, film_actor fa, actor a
WHERE f.film_id = fa.film_id
AND fa.actor_id = a.actor_id
AND a.first_name = 'BOB'
UNION
SELECT DISTINCT f.title
FROM film f, film_actor fa, actor a
WHERE f.film_id = fa.film_id
AND fa.actor_id = a.actor_id
AND a.first_name = 'JENNIFER'

/* union all - all films that either Bob and Jennifers are in, including duplicates */
SELECT DISTINCT f.title
FROM film f, film_actor fa, actor a
WHERE f.film_id = fa.film_id
AND fa.actor_id = a.actor_id
AND a.first_name = 'BOB'
UNION ALL
SELECT DISTINCT f.title
FROM film f, film_actor fa, actor a
WHERE f.film_id = fa.film_id
AND fa.actor_id = a.actor_id
AND a.first_name = 'JENNIFER'

/* except - all films starring a Bob except those that star a Jennifer too */
SELECT DISTINCT f.title
FROM film f, film_actor fa, actor a
WHERE f.film_id = fa.film_id
AND fa.actor_id = a.actor_id
AND a.first_name = 'BOB'
EXCEPT
SELECT DISTINCT f.title
FROM film f, film_actor fa, actor a
WHERE f.film_id = fa.film_id
AND fa.actor_id = a.actor_id
AND a.first_name = 'JENNIFER'

/* intersection - all films that contain both a Bob and a Jennifer */
SELECT DISTINCT f.title
FROM film f, film_actor fa, actor a
WHERE f.film_id = fa.film_id
AND fa.actor_id = a.actor_id
AND a.first_name = 'BOB'
INTERSECT
SELECT DISTINCT f.title
FROM film f, film_actor fa, actor a
WHERE f.film_id = fa.film_id
AND fa.actor_id = a.actor_id
AND a.first_name = 'JENNIFER'
```
