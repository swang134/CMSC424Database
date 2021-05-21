# Explanation: The given left-join query fails because ...
# 
# First, the Count(*) will count the exactly numbers of the rows with the same name
# However, the left join will also added the customer's name who didn't fly at all into
# the table, with one rows, it means even they never fly at all, the Count(*) function will
# return 1 since there is one row their with the coustomerid that was not on the flewon table.
# To solve that, we can use count(f.customerid) instead count(*), since for the people who did 
# not flay at all, there will not be a f.customerid for them. 
#
# Second, The origin code left joined both id and names between the two table, which means it
# will returns all records from the left table (table1), and the matched records from the right table
# if any c.customerid = f.customerid or c.name like 'william'. Which the resule will be much bigger 
# than it expected.

queryWilliam = """

select c.customerid, c.name, count(f.customerid)
from customers c left outer join flewon f on c.customerid = f.customerid
where c.name like 'William%'
group by c.customerid, c.name
order by c.customerid;
"""




# NOTE:  This trigger is both INCORRECT and INCOMPLETE. You need to find and fix the bugs, and ensure
# that it will correctly update NumberOfFlightsTaken on both insertions and deletions from "flewon".
queryTrigger = """
 CREATE OR REPLACE FUNCTION updateStatusCount() RETURNS trigger AS $updateStatus$
 		DECLARE
 			old_status_count integer;
 		BEGIN
            IF (TG_OP = 'INSERT') THEN
            SELECT numflights into old_status_count
            From NumberOfFlightsTaken
            WHERE customerid = NEW.customerid;
                IF EXISTS (SELECT customername from NumberOfFlightsTaken WHERE customerid = NEW.customerid) 
                    THEN UPDATE NumberOfFlightsTaken 
                    SET numflights =numflights + 1
                    WHERE customerid = NEW.customerid;
                ELSE 
                    INSERT INTO NumberOfFlightsTaken (customerid, customername, numflights) 
                    values (NEW.customerid, (SELECT name as na from customers where customerid = New.customerid), 1);
                END IF; 

            ELSEIF (TG_OP = 'DELETE') THEN
            SELECT numflights into old_status_count
            From NumberOfFlightsTaken
            WHERE customerid = OLD.customerid;
                    IF (old_status_count = 1) THEN
                        DELETE FROM NumberOfFlightsTaken
                        WHERE customerid = OLD.customerid;
                    ELSE
                        UPDATE NumberOfFlightsTaken
                        SET numflights =numflights - 1
                        WHERE customerid = OLD.customerid;
                    END IF;
            END IF;
        RETURN NULL;
 		END;
 $updateStatus$ LANGUAGE plpgsql; 


 CREATE TRIGGER update_num_status AFTER 
 INSERT OR DELETE ON flewon
 FOR EACH ROW EXECUTE PROCEDURE updateStatusCount();
 END;      
"""

# queryTrigger = """
# CREATE OR REPLACE FUNCTION updateStatusCount() RETURNS trigger AS $updateStatus$
# 		DECLARE
# 			old_status_count integer;
# 		BEGIN
#
# 		END;
# $updateStatus$ LANGUAGE plpgsql;
# 
# CREATE TRIGGER update_num_status AFTER 
# INSERT OR DELETE ON Status 
# FOR EACH ROW EXECUTE PROCEDURE updateStatusCount();
# END;
# 
# """
