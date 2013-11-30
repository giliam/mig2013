################################################################################
#                                                                              #
#                               DB System                                      #
#                           MIG SE Team 2013                                   # 
#                                                                              #
################################################################################

=== DESCRIPTION ===

DB System is our manager of database. It handles the way our files are stored in
the directories and the different possibilities to access to them or to show what
is currently stored.

=== HOW TO USE IT ===

1. First you need to initialize the system by giving :
    -> the path prefix which gives the path to the storage directory (e.g. "../../db" from current directory)
    -> the option verbose to show messages in the console
    -> the name of the file that contains the list of stored files
2. You can know use it to add, create, delete and access to files !

=== METHODS ===

Use the documentation of the code (i.e. help(Db) in a python shell)
 _                                                                      _
/!\  The parameters fileName is used to store the file in the system,  /!\
¯|¯ it's a kind of ID for the file. Do NOT confuse with dirFile        ¯|¯
