## scripts
This scripts module is a collection of 'finalized' python scripts that are meant to run outside of jupyter notebook for performance reasons or otherwise

### Contents
1. Missing_Persons.py
    - pulled from the missing persons jupyter notebook project. This script was taking 3 hours to execute and was timing out during execution in the jupyter notebook environment. Added a loop that would attempt to reconnect after waiting for a little while and the attempt to pull the data again.