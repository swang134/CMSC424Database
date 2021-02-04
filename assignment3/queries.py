queries = ["" for i in range(0, 16)]

### 0. Report the votes for the normal (i.e, not special) Senate Election in Maryland in 2018.
### Output column order: candidatename, candidatevotes
### Order by candidatename ascending
queries[0] = """
select 0;
"""

### 1. Write a query to find the maximum, minimum, and average population in 2010 across all states.
### The result will be a single row.
### Truncate the avg population to a whole number using trunc
### Output Columns: max_population, min_population, avg_population
### Order by: none
queries[1] = """
select 0;
"""

### 2. Write a query to print the candidate with the maximum votes in the 2008 MI Senate Election. 
### Output Column: candidatename
### Order by: none
queries[2] = """
select 0;
"""

### 3. Write a query to find the number of candidates who are listed in the sen_state_returns table for each senate election held in 2018. 
### Note that there may be two elections in some states, and there should be two tuples in the output for that state.
### 'NA' or '' (empty) should be treated as candidates. 
### Output columns: statecode, specialelections, numcandidates
### Order by: statecode, specialelections
queries[3] = """
select 0;
"""

### 4. Write a query to find, for the 2008 elections, the number of counties where Barack Obama received strictly more votes 
### than John McCain.
### This will require you to do a self-join, i.e., join pres_county_returns with itself.
### Output columns: num_counties
### Order by: none
queries[4] = """
select 0;
"""


### 5. Write a query to find the names of the states with at least 100 counties in the 'counties' table.
### Use HAVING clause for this purpose.
### Output columns: statename, num_counties
### Order by: statename
queries[5] = """
select 0;
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
select 0;
"""

### 7. Create a listing to show the disparity between the populations listed in 'states' table and those listed in 'counties' table for 1950 and 2010.
### Result should be: 
### So disparity_1950 = state population 1950 - sum of population_1950 for the counties in that state
### Use HAVING to only output those states where there is some disparity (i.e., where at least one of the two is non-zero)
### Output columns: statename, disparity_1950, disparity_2010
### Order by statename
queries[7] = """
select 0;
"""

### 8. Use 'EXISTS' or 'NOT EXISTS' to find the states where no counties have population in 2010 above 500000 (500 thousand).
### Output columns: statename
### Order by statename
queries[8] = """
select 0;
"""

### 9. List the first 10 county names (alphabetically) that are used multiple times. 
### Use a scalar subquery to simplify the query.
### Output columns: name
### Order by name
queries[9] = """
select 0;
"""

### 10. Use Set Intersection to find the counties that Barack Obama lost in 2008, but won in 2012.
###
### Output columns: countyname, statecode
### Order by countyname, statecode
queries[10] = """
select 0;
"""


### 11. Find all presidential candidates listed in pres_county_returns who did NOT run for elections as a senator.
### HINT: Use "except" to simplify the query
###
### Every candidate should be reported only once. You will see incorrect answers in there because "names" don't match -- that's fine.
###
### Output columns: candidatename
### Order by: candidatename
queries[11] = """
select 0;
"""



### 12. Create a table listing the months and the number of states that were admitted to the union (admitted_to_union field) in that month.
### Use 'extract' for operating on dates, and the ability to create a small inline table in SQL. For example, try:
###         select * from (values(1, 'Jan'), (2, 'Feb')) as x;
###
### Output columns: month_no, monthname, num_states_admitted
### month should take values: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
### Order by: month_no
queries[12] = """
select 0;
"""


### 13. Create a view pres_state_votes with schema (year, statecode, candidatename, partyname, candidatevotes) 
### where we maintain aggregated counts by statecode (i.e., candidatevotes in this view would be the total votes
### for each state, including states with statecode 'NA').
### Output columns: none
### Order by: none
queries[13] = """
select 0;
"""

### 14. Use a natural join to list the presidential candidate who got the most votes for each year where votes were cast, sorted by increasing year.
###     You may use any table or view in this query.
### Output columns: year, candidatename
### Order by: year
queries[14] = """
select 0;
"""

### 15. Print a table of states s.t. the party that won that state is the same each presidential election.
###   - There should only be at most one listing for a given state. 
###   - Easiest approach is to do this iteratively, w/ a succession of WITH clauses. Try out each clause before adding the next.
### Output columns: state, party
### Order by: state
queries[15] = """
select 0;
"""


