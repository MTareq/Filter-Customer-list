 Usage: 
 * filter_customers.py [-h] [-v] [-o] input_file

    ```
    This Script filters out customers from a customers info file,
    Based on being within 100 KM from Intercom.io Dublin office (53.339428, -6.257664).
    Input:
        plain text file with line seperated json objects represinting customers info,
        each json object should correspond to this schema:
           {"latitude": String or Float, "user_id": Integer, "name": String, "longitude": String or Float}
    Output:
        JSON file represinting the curated list of customers based on the filtering criteria,
        Sorted by 'user_id' in asscending order.```


 Positional arguments:
  * input_file      input file name

 Optional arguments:
  * -h, --help      show this help message and exit
  * -v              verbose output to console
  * -o              output file Name      
