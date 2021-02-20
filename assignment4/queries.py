# Explanation: The given left-join query fails because ...
#
#
queryWilliam = """
select 0;
"""



# NOTE:  This trigger is both INCORRECT and INCOMPLETE. You need to find and fix the bugs, and ensure
# that it will correctly update NumberOfFlightsTaken on both insertions and deletions from "flewon".
queryTrigger = """
select 0;      
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
