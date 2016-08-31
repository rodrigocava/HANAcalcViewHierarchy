# HANA Calculation View Hierarchy Graph
Creates a graph visualization to show the hierarchy dependencies of a SAP HANA Calculation View.

This simple development generates a graph with all the dependencies of SAP HANA's Calculation View. It can be usefull to check dependencies privileges, or simply to check how many views makeup a full structure of information.

## Utilization
  1. Edit the calcViewHierarchy.py file and add your HANA DB information (the varibles at the top, after the imports): 
    - host 
    - port
    - user
    - password
  2. Run calcViewHierarchy.py local server with the comand: ``` python3 calcViewHierarchy.py ```
  3. Open in your browser the following link: [http://localhost:5000/viewHierarchy](http://localhost:5000/viewHierarchy)
  4. Enter the full name of a Calculation View (< package >.< subpackage >/< viewName >) at the textInput
  5. Hit "Enter" or press the "Generate Hierarchy" button. The hierarchy graph should appear bellow the button

[![View Hierarchy](https://s15.postimg.org/ggfflzhjv/View_Hierarchy.png)](https://postimg.org/image/lf2y0ilcn/)

The graph makes red dots and lines representing Calculation Views and green dots and lines representing Tables. 
*(Don't mind the ugliness of it, the main objective was the graph)*

## Architecture
I used a Python script that have a function to connect to the HANA DB (many thanks for this [post]( https://github.com/SAP/PyHDB)) and also generates a simples HTTP server to run the UI in HTML + JS. The function generates a external file (called resultCalcViewHierarchy.json) that is read by the HTML using D3.js ([this one](http://bl.ocks.org/d3noob/08ecb6ea9bb68ba0d9a7e89f344acec8)). I made it this way because you can also use the .JSON file generated in other documentations as well.

The function check the dependencies at the PUBLIC Schema table called **OBJECT_DEPENDENCIES**. It's important to notice that a query from this table will only show the records that your user have permisson, so make sure to check your user's permission. If you ran in any weird situations.

Also make sure to check the information about of yours HANA System **ports** when your using a Multitenant DB. Check this [link](https://help.sap.com/saphelp_hanaplatform/helpdata/en/44/0f6efe693d4b82ade2d8b182eb1efb/frameset.htm) in case you run in some sort of trouble.

## TO DOs

* Make it prettier :stuck_out_tongue_winking_eye:

