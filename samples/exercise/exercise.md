en mi cluster de k8s levantar 2 elementos:

- un servicio que exponga un servidor web simple (nginx, apache, etc) con nombre "mi-servicio" en el namespace "default"
- un job que haga una peticion al servicio anterior y escriba la respuesta en logs y en un volumen
- un volumen persistente (hostPath o emptyDir) para que el job pueda escribir la respuesta
- otro job que lea el volumen y muestre la respuesta en logs