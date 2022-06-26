/*********************************************
 * OPL 12.10.0.0 Model
 * Author: Pablo
 * Creation Date: 3 jun. 2022 at 12:31:42
*********************************************/

int n = ...;
range cities = 1 .. n;

tuple location {
  float x;
  float y;
}

tuple edge {
  float i;
  float j;
}

setof ( edge ) edges = {< i, j > | i, j in cities : i != j};
float c[edges];
location cityLocation[cities] = ...;

//Solucion inicial
int ordenInicial[cities] = [64, 44, 71, 45, 4, 68, 91, 13, 74, 31, 27, 49, 72, 80, 14, 77, 15, 78, 59, 16, 79, 88, 94, 10, 63, 48, 73, 76, 87, 1, 98, 34, 30, 84, 7, 8, 89, 96, 35, 93, 52, 33, 92, 54, 46, 90, 56, 26, 75, 18, 85, 65, 55, 58, 50, 70, 86, 29, 81, 25, 20, 51, 43, 67, 32, 23, 38, 41, 57, 39, 60, 66, 17, 11, 61, 36, 69, 24, 12, 53, 40, 42, 9, 28, 6, 37, 2, 19, 99, 47, 83, 97, 100, 5, 95, 82, 3, 62, 22, 21];

int values[edges];

//int values[e in edges] = ((e.j==e.i+1) || (e.j==1 && e.i==n)) ? 1 : 0;

execute {
  function getDistance(city1, city2) {
    return Opl.sqrt(Opl.pow(city1.x - city2.x, 2)
        + Opl.pow(city1.y - city2.y, 2));
  }

  for ( var e in edges) {
    c[e] = getDistance(cityLocation[e.i], cityLocation[e.j]);
    values[e] = 0;
  }
  
  var ciudadAnterior = ordenInicial[n];

  for ( var i in cities) {

    var ciudad = ordenInicial[i];

    values[edges.find(ciudadAnterior, ciudad)] = 1;

    ciudadAnterior = ciudad;

  }
  
}

dvar boolean x[edges];
dvar float+ u[2 .. n];

dexpr float TotalDistance = sum ( e in edges ) c[e] * x[e];

minimize
  TotalDistance;

subject to {
  forall ( j in cities )
    flow_in:
      sum ( i in cities : i != j ) x[< i, j >] == 1;

  forall ( i in cities )
    flow_out:
      sum ( j in cities : i != j ) x[< i, j >] == 1;

  forall ( i in cities : i > 1, j in cities : j > 1 && j != i )
    subtour:
      u[i] - u[j] + ( n - 1 ) * x[< i, j >] <= n - 2;

}

main {
  var mod = thisOplModel.modelDefinition;
  var dat = thisOplModel.dataElements;
  var cplex1 = new IloCplex();
  var opl = new IloOplModel(mod, cplex1);
  opl.addDataSource(dat);
  opl.generate();
  cplex1.addMIPStart(opl.x,opl.values);

  if (cplex1.solve()) {
    writeln("solution: ", cplex1.getObjValue(), " /size: ", dat.n, " /time: ",
        cplex1.getCplexTime());

    for (i in opl.cities) {
      if (i == 1)
        writeln("Ciudad ", i, ": ", -1);
      else
        writeln("Ciudad ", i, ": ", opl.u[i]);
    }
    opl.end()
    cplex1.end()
  }
}