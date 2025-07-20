## Laboratorio 2  
Irving Acosta - 22781  

El archivo program_test_pass.txt pasa sin errores porque está construido conforme la grámatica escritra en el .g4 y respuesta las reglas semánticas, las cuales van acompañadas de una lógica de tipos. Por ejemplo, no solo se cumple que en medio de un operador "+" vayan dos números, sino que esos dos números sean del mismo tipo (INT o FLOAT)
El caso contrario de esto es el program_test_no_pass.txt, ya que en este archivo se encuentran operaciones que no están definidas en las reglas grámaticales, por ejemplo podemos encontrar una división de un INT sobre una STRING, lo cual no hace sentido en ningún lenguaje. De igual manera cadenas como `"hello" + 3` aunque en lenguajes como python podrían ser una concatenación simple, acá no están definidas, por lo que produce un error. Se puede decir que el principal causante de los errores en este archivo es la incompatibilidad de tipos.  

Las operaciones agregadas por mi parte fueron de comparación, mayor y menor que (>, <), comparaciones de igualdad (==, !=) y de último las expresiones lógicas de ('&&' | '||). Para ello se agregaron las reglas en el archivo .g4 y se el manejo de errores se trabajó desde los type_checker.py correspondientes. Tanto en Visitor como en Listener.  

Al momento de expandir el sistema de tipos para validar otros tipos de conflictos se escogieron los siguientes:
1. Mezclar String y Int con +.     
2. Hacer < entre Bool y Int.   
3. Usar && entre Float y Bool.   

### Enlace al vídeo
[Lab_2:Video](https://www.youtube.com/watch?v=h_xR2HdEbgI)