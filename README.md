# TopographicStructureDEM
Extracting topographic structures from digital elevation model for GIS analysis

### Steps involved:
1. Fill single-cell depressions by raising each cell’s elevation to the elevation of its lowest elevation neighbor if 
that neighbor is higher in elevation than the cell

2. Compute flow directions

  2 a. For all cells adjacent to the data set edge or the study area mask,assign the flowdirection to flow to the edge or the mask.  
  Assuming thatthe study area is interior to the data set
  
  2 b. For each cell not assigned a flow direction in step 2a., compute thedistance-weighted drop in elevation to each of the cell’s eightneighbors.
  
  2 c. Examine the drop value to determine the neighbor(s) with thelargest drop and perform one of the following:
      If the largest drop is less than zero, assign a negative flowdirection to indicate undefined.
      If the largest drop is greater than or equal to zero and occurs atonly one neighbor, assign the flow direction to that neighbor.
      If the largest drop is greater than zero and occurs at more than oneneighbor, assign the flow direction logically according to a look-up table.
      If the largest drop is equal to zero and occurs at more than one neighbor, encode the locations of those neighbors by summing their neighbor location codes.
        The center cell is a part of a Flat area
        
  2 d. For each cell not already encoded as negative, 1, 2, 4, 8, 16, 32,64, or 128, examine the neighbor cells with the largest drop. 
  If the largest drop neighbor is encountered which has a flow direction of 1, 2, 4, 8, 16,32, 64, or 128, 
  and the neighbor does not flow to the center cell,assign the center cell a flow direction which flows to this neighbor.
  
  2 e. Make the flow direction value negative for cells that are not equal to 1, 2, 4, 8, 16, 32, 64, or 128.
    This situation will not occur for a depressionless DEM
    
3. For every spatially connected group of cells that has undefined flow direction, find the group’s uniquely labeled watershed from the flow directions

4. Build a table of pour point elevations between all pairs of watershed labels
    
    4 a. Compare each cell in a watershed data set to its eightneighbors. When a cell and its neighbor have differentwatershed labels, proceed to steps 4b-c.
    
    4 b. Compare the elevation values of the cell and its neighbor. The larger of the two elevation values is the elevation of the possible pour point they represent, 
    and the line and sample of the cell with the larger elevation is the pour point location.
    
    4 c.  If this pair of watershed labels is already in the pour pointtable, compare the elevation in the table to the elevation forthe possible pour point being examined. 
    If the newelevation is lower, replace the old pour point location,and elevation with the new ones.
    
5. For each watershed, mark the pour point that is lowest in elevation as that watershed’s “lowest pour point.” 
If there are duplicate lowest pour points, select one arbitrarily.

6. For each watershed, follow the path of lowest pour points until either the data set edge is reached (go to step 7) 
or the path loops back on itself (go to step 6a).

  6 a. Fix paths that loop back on themselves by aggregating the watersheds which comprised the loop, re-computing “lowest pour point” for the new aggregated watershed, 
  and resume following the path of lowest pour points
  
7. In each watershed’s path of lowest pour points, find the one that is highest in elevation. This is the threshold value for the watershed. 
Raise all cells in the watershed that are less than the threshold value to the threshold value.

