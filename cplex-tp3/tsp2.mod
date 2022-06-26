/*********************************************
 * OPL 12.10.0.0 Data
 * Author: Pablo
 * Creation Date: 3 jun. 2022 at 12:31:42
*********************************************/

/*****************************************************************************
 *
 * DATA
 * 
*****************************************************************************/

// Cities
int n = 100;
range Cities = 1 .. n;

// Edges -- sparse set
tuple edge {
  float i;
  float j;
}
setof ( edge ) Edges = {< i, j > | ordered i, j in Cities};
float dist[Edges];

// Decision variables
dvar boolean x[Edges];

tuple Subtour {
  int size;
  int subtour[Cities];
}
{Subtour} subtours = ...;

tuple location {
  float x;
  float y;
}
location cityLocation[Cities] = ...;

//Solucion inicial
int ordenInicial[Cities] = [64, 44, 71, 45, 4, 68, 91, 13, 74, 31, 27, 49, 72, 80, 14, 77, 15, 78, 59, 16, 79, 88, 94, 10, 63, 48, 73, 76, 87, 1, 98, 34, 30, 84, 7, 8, 89, 96, 35, 93, 52, 33, 92, 54, 46, 90, 56, 26, 75, 18, 85, 65, 55, 58, 50, 70, 86, 29, 81, 25, 20, 51, 43, 67, 32, 23, 38, 41, 57, 39, 60, 66, 17, 11, 61, 36, 69, 24, 12, 53, 40, 42, 9, 28, 6, 37, 2, 19, 99, 47, 83, 97, 100, 5, 95, 82, 3, 62, 22, 21];

int values[Edges];


//int values[e in Edges] = ((e.j==e.i+1) || (e.i==1 && e.j==n)) ? 1 : 0;

execute {
  function getDistance(city1, city2) {
    return Opl.sqrt(Opl.pow(city1.x - city2.x, 2)
        + Opl.pow(city1.y - city2.y, 2));
  }

  for ( var e in Edges) {
    dist[e] = getDistance(cityLocation[e.i], cityLocation[e.j]);
    values[e] = 0;
  }


  var ciudadAnterior = ordenInicial[n];

  for ( var i in Cities) {

    var ciudad = ordenInicial[i];

    if (ciudadAnterior < ciudad) {

      values[Edges.find(ciudadAnterior, ciudad)] = 1;

    } else {

      values[Edges.find(ciudad, ciudadAnterior)] = 1;

    }

    ciudadAnterior = ciudad;

  }
  
}


/*****************************************************************************
 *
 * MODEL
 * 
*****************************************************************************/

// Objective
minimize
  sum ( < i, j > in Edges ) dist[< i, j >] * x[< i, j >];
subject to {
  // Each city is linked with two other cities
  forall ( j in Cities )
    sum ( < i, j > in Edges ) x[< i, j >] + sum ( < j, k > in Edges ) x[< j,
       k >] == 2;

  // Subtour elimination constraints.
  forall ( s in subtours )
    sum ( i in Cities : s.subtour[i] != 0 ) x[< minl ( i, s.subtour[i] ), maxl 
      ( i, s.subtour[i] ) >] <= s.size - 1;

}
;

// POST-PROCESSING to find the subtours

// Solution information
int thisSubtour[Cities];
int newSubtourSize;
int newSubtour[Cities];

// Auxiliary information
int visited[i in Cities] = 0;
setof ( float ) adj[j in Cities] = {i | < i, j > in Edges : x[< i,
   j >] == 1} union {k | < j, k > in Edges : x[< j, k >] == 1};
execute {


  newSubtourSize = n;
  for ( var i in Cities) { // Find an unexplored node
    if (visited[i] == 1)
      continue;
    var start = i;
    var node = i;
    var thisSubtourSize = 0;
    for ( var j in Cities)
      thisSubtour[j] = 0;
    while (node != start || thisSubtourSize == 0) {
      visited[node] = 1;
      var succ = start;
      for (i in adj[node])
        if (visited[i] == 0) {
          succ = i;
          break;
        }

      thisSubtour[node] = succ;
      node = succ;
      ++thisSubtourSize;
    }

    writeln("Found subtour of size : ", thisSubtourSize);
    if (thisSubtourSize < newSubtourSize) {
      for (i in Cities)
        newSubtour[i] = thisSubtour[i];
      newSubtourSize = thisSubtourSize;
    }
  }
  if (newSubtourSize != n)
    writeln("Best subtour of size ", newSubtourSize);
}



/*****************************************************************************
 *
 * SCRIPT
 * 
*****************************************************************************/

main {
  var opl = thisOplModel
  var mod = opl.modelDefinition;
  var dat = opl.dataElements;

  var status = 0;
  var it = 0;
  while (1) {
    var cplex1 = new IloCplex();
    opl = new IloOplModel(mod, cplex1);
    opl.addDataSource(dat);
    opl.generate();
    it++;

    cplex1.addMIPStart(opl.x,opl.values);
    writeln("Iteration ", it, " with ", opl.subtours.size, " subtours.");
    if (!cplex1.solve()) {
      writeln("ERROR: could not solve");
      status = 1;
      opl.end();
      break;
    }
    opl.postProcess();
    writeln("Current solution : ", cplex1.getObjValue());

    if (opl.newSubtourSize == opl.n) {
      opl.end();
      cplex1.end();
      break; // not found
    }

    dat.subtours.add(opl.newSubtourSize, opl.newSubtour);

    opl.end();
    cplex1.end();
  }

  status;
}

