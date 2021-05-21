queries = ["" for i in range(0, 16)]

### 0. Report the votes for the normal (i.e, not special) Senate Election in Maryland in 2018.
### Output column order: candidatename, candidatevotes
### Order by candidatename ascending
queries[0] = """
select candidatename, candidatevotes
from sen_state_returns
where year = 2018 and statecode = 'MD' and specialelections = False
order by candidatename asc;
"""

### 1. Write a query to find the maximum, minimum, and average population in 2010 across all states.
### The result will be a single row.
### Truncate the avg population to a whole number using trunc
### Output Columns: max_population, min_population, avg_population
### Order by: none
queries[1] = """
select max(population_2010), min(population_2010), TRUNC(avg(population_2010),0) from states;
"""

### 2. Write a query to print the candidate with the maximum votes in the 2008 MI Senate Election. 
### Output Column: candidatename
### Order by: none
queries[2] = """
select candidatename
from sen_state_returns
where candidatevotes= (select max(candidatevotes) from sen_state_returns where year = 2008 and statecode = 'MI');

"""

### 3. Write a query to find the number of candidates who are listed in the sen_state_returns table for each senate election held in 2018. 
### Note that there may be two elections in some states, and there should be two tuples in the output for that state.
### 'NA' or '' (empty) should be treated as candidates. 
### Output columns: statecode, specialelections, numcandidates
### Order by: statecode, specialelections
queries[3] = """
select statecode, specialelections, count(*)
from sen_state_returns
where year = 2018
group by statecode, specialelections
Order by statecode, specialelections asc;
"""

### 4. Write a query to find, for the 2008 elections, the number of counties where Barack Obama received strictly more votes 
### than John McCain.
### This will require you to do a self-join, i.e., join pres_county_returns with itself.
### Output columns: num_counties
### Order by: none
queries[4] = """
SELECT count(*)
FROM pres_county_returns a, pres_county_returns b
WHERE a.countyname = b. countyname and a.statecode = b.statecode and a.year = b.year and a.candidatename = 'Barack Obama' 
and b.candidatename = 'John McCain' and a.candidatevotes > b.candidatevotes and a.year = 2008;
"""


### 5. Write a query to find the names of the states with at least 100 counties in the 'counties' table.
### Use HAVING clause for this purpose.
### Output columns: statename, num_counties
### Order by: statename
queries[5] = """
SELECT states.name as statename, COUNT(counties.*)
FROM counties
join states on counties.statecode = states.statecode
GROUP BY counties.statecode, statename
HAVING COUNT(counties.*) >= 100
ORDER BY statename ASC;
"""

### 6. Print for all states:
###     (statecode, total_votes_2008, total_votes_2012)
### to count the total number of votes by state for Barack Obama in the two elections.
###
### Use the ability to "sum" an expression (e.g., the following query returns the number of counties in 'AR')
### select sum(case when statecode = 'AR' then 1 else 0 end) from counties;
###
### Output columns: statecode, total_votes_2008, total_votes_2012
### Order by: statecode
queries[6] = """
SELECT statecode, sum(case when candidatename = 'Barack Obama'and year = 2008 then candidatevotes else 0 end),
 sum(case when candidatename = 'Barack Obama'and year = 2012 then candidatevotes else 0 end) 
FROM pres_county_returns
GROUP BY statecode
ORDER by statecode;

"""

### 7. Create a listing to show the disparity between the populations listed in 'states' table and those listed in 'counties' table for 1950 and 2010.
### Result should be: 
### So disparity_1950 = state population 1950 - sum of population_1950 for the counties in that state
### Use HAVING to only output those states where there is some disparity (i.e., where at least one of the two is non-zero)
### Output columns: statename, disparity_1950, disparity_2010
### Order by statename
queries[7] = """
SELECT states.name, states.population_1950 - sum(counties.population_1950) ,
states.population_2010 - sum(counties.population_2010) 
FROM states 
JOIN counties on counties.statecode = states.statecode
GROUP BY
    states.statecode
HAVING 
   states.population_1950 - sum(counties.population_1950) != 0 or states.population_2010 - sum(counties.population_2010) != 0 
ORDER BY states.name;
"""

### 8. Use 'EXISTS' or 'NOT EXISTS' to find the states where no counties have population in 2010 above 500000 (500 thousand).
### Output columns: statename
### Order by statename
queries[8] = """
SELECT name
FROM states
WHERE NOT EXISTS (SELECT statecode FROM counties WHERE states.statecode = counties.statecode AND population_2010 > 500000)
order by name;
"""

### 9. List the first 10 county names (alphabetically) that are used multiple times. 
### Use a scalar subquery to simplify the query.
### Output columns: name
### Order by name
queries[9] = """
SELECT name  
    FROM 
    (SELECT name, count(name) as Counter 
     FROM counties
     GROUP BY name) AS tbl WHERE Counter >= 2
     Order by name asc
     FETCH FIRST 10 ROWS ONLY;
"""

### 10. Use Set Intersection to find the counties that Barack Obama lost in 2008, but won in 2012.
###
### Output columns: countyname, statecode
### Order by countyname, statecode
queries[10] = """
with temp1 as (select countyname, statecode, max(candidatevotes) as maxvotes
        from pres_county_returns
        where year = 2008
        group by countyname, statecode
        HAVING max(candidatevotes) > 0),
temp2 as (select countyname, statecode, max(candidatevotes) as maxvotes
        from pres_county_returns
        where year = 2012
        group by countyname, statecode
        HAVING max(candidatevotes) > 0)

(SELECT temp1.countyname, temp1.statecode
FROM temp1
JOIN pres_county_returns ON pres_county_returns.candidatevotes = temp1.maxvotes 
AND pres_county_returns.countyname = temp1.countyname AND pres_county_returns.statecode = temp1.statecode
WHERE  pres_county_returns.candidatename != 'Barack Obama' and pres_county_returns.year = 2008
GROUP BY temp1.countyname, temp1.statecode)

INTERSECT

(SELECT temp2.countyname, temp2.statecode
FROM temp2
JOIN pres_county_returns ON pres_county_returns.candidatevotes = temp2.maxvotes 
AND pres_county_returns.countyname = temp2.countyname AND pres_county_returns.statecode = temp2.statecode
WHERE  pres_county_returns.candidatename = 'Barack Obama' and pres_county_returns.year = 2012
GROUP BY temp2.countyname, temp2.statecode)

ORDER BY countyname, statecode; 


"""


### 11. Find all presidential candidates listed in pres_county_returns who did NOT run for elections as a senator.
### HINT: Use "except" to simplify the query
###
### Every candidate should be reported only once. You will see incorrect answers in there because "names" don't match -- that's fine.
###
### Output columns: candidatename
### Order by: candidatename
queries[11] = """
SELECT candidatename
FROM pres_county_returns

EXCEPT

SELECT candidatename
FROM sen_state_returns

Order by candidatename;

"""



### 12. Create a table listing the months and the number of states that were admitted to the union (admitted_to_union field) in that month.
### Use 'extract' for operating on dates, and the ability to create a small inline table in SQL. For example, try:
###         select * from (values(1, 'Jan'), (2, 'Feb')) as x;
###
### Output columns: month_no, monthname, num_states_admitted
### month should take values: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
### Order by: month_no
queries[12] = """
with temp1 as (select * from (values(1, 'Jan'), (2, 'Feb'),(3,'Mar'), (4, 'Apr'), (5,'May'), (6,'Jun'), (7,'Jul'), (8,'Aug'), (9,'Sep'),
         (10,'Oct'), (11,'Nov'), (12,'Dec')) as x (month_no, monthname)),
     temp2 as (select Extract(month from admitted_to_union) as month from states)

select temp2.month, temp1.monthname, count(temp2.month)
from temp2
join temp1 on temp1.month_no= temp2.month
group by temp2.month, temp1.monthname
order by temp2.month
;
"""


### 13. Create a view pres_state_votes with schema (year, statecode, candidatename, partyname, candidatevotes) 
### where we maintain aggregated counts by statecode (i.e., candidatevotes in this view would be the total votes
### for each state, including states with statecode 'NA').
### Output columns: none
### Order by: none
queries[13] = """


CREATE VIEW pres_state_votes AS
SELECT year, pres_county_returns.statecode, candidatename, partyname, sum(candidatevotes) as candidatevotes
FROM pres_county_returns
Group by year, pres_county_returns.statecode, candidatename, partyname;
"""

### 14. Use a natural join to list the presidential candidate who got the most votes for each year where votes were cast, sorted by increasing year.
###     You may use any table or view in this query.
### Output columns: year, candidatename
### Order by: year
queries[14] = """
with temp1 as (select year, candidatename, sum(candidatevotes) as sumvotes
        from pres_county_returns
        group by year, candidatename), 
     temp2 as (select year, max(sumvotes) as maxvotes
        from temp1
        group by year )

SELECT year, candidatename
FROM temp1
natural join temp2
Where temp1.year = temp2.year and sumvotes = maxvotes 
Order by year;

"""

### 15. Print a table of states s.t. the party that won that state is the same each presidential election.
###   - There should only be at most one listing for a given state. 
###   - Easiest approach is to do this iteratively, w/ a succession of WITH clauses. Try out each clause before adding the next.
### Output columns: state, party
### Order by: state
queries[15] = """

with temp1 as (select year, statecode, max(candidatevotes)as maxvote from pres_state_votes 
                group by year, statecode),
temp2 as (select partyname, count(partyname) as partycount, temp1.statecode, (select count(*) from (select count(*) from pres_state_votes group by year) as count) as co  
        from pres_state_votes 
        join temp1 on pres_state_votes.year = temp1.year and 
        pres_state_votes.candidatevotes = maxvote and pres_state_votes.statecode = temp1.statecode
        group by temp1.statecode, partyname)
select name, partyname 
from temp2 
join states on states.statecode = temp2.statecode
where temp2.partycount = co
order by name;



"""
