Prueba de conocimiento con Django Rest Framework  
[Objetivo] 
Analizar el nivel de conocimiento de los postulantes a desarrollador de backend Clicoh. 
[Prueba lógica] 
Crear una API REST utilizando DJANGO REST FRAMEWORK, que brinde la siguiente funcionalidad básica y acotada de un  Ecommerce. 
El sistema debe tener los modelos Product, Order, OrderDetail con los siguientes atributos: 

Product: 
- id PK [string]
- name [string]
- price [float]
- stock[int]

Order:
- id PK 
- date_time  [datetime] 

OrderDetail:
- order [Order]
- cuantity [int]
- product [Product]

La misma debe proporcionar los siguientes end points: 
* Registrar/Editar un producto 
* Eliminar un producto 
* Consultar un producto 
* Listar todos los productos 
*Modificar stock de un producto 
* Registrar/Editar una orden (inclusive sus detalles). Debe actualizar el stock del producto 
* Eliminar una orden. Restaura stock del producto 
* Consultar una orden y sus detalles 
* Listar todas las ordenes 
La clase Order debe exponer un método get_total el cual calcula el total de la factura y retornar ese valor en el serializer correspondiente. También debe exponer el método get_total_usd, utilizando el API de  
https://www.dolarsi.com/api/api.php?type=valoresprincipales, con “dólar blue” para que te tire el precio en dolares. 
Al crear o editar una orden validar q haya suficiente stock del producto, en caso no contar con stock se debe retornar un  error de validación. 
Para la implementación de la API se debe utilizar ModelViewSet, ModelSerializer. 
El código fuente de la api debe ser subido a un repositorio público, el cual debe ser proporcionado para su correcta  examinación. 
A la hora de crear una orden se debe validar: 
* que la cantidad de cada producto sea mayor a 0 
* que no se repitan productos en el mismo pedido 
* Implementar autenticación basada en tokens (JWT) 
* Deployar la api en producción, por ejemplo en heroku o https://www.pythonanywhere.com/,
* Implementar test unitario para validar los endpoints.

