===================
Blue Medical - API
===================


Descripción
==========

Módulo que expone un endpoint REST para la creación de órdenes de venta en Odoo.

* Creación de órdenes vía API

* Validación de autenticación mediante API Key (Bearer Token)

* Validación de existencia de cliente

* Validación de existencia de productos

* Creación de orden en estado "pending"

* Retorno de respuesta JSON estructurada

* Este módulo depende de blue_sale_extension y sale.


Instalación
=============

Requisitos:

* Odoo 16.0

* Módulo sale instalado

* Módulo blue_sale_extension instalado

* Modo desarrollador activado

Pasos:

* Clonar el repositorio:

* git clone https://github.com/eddPerez/Technical_test_BM.git

* Copiar el módulo 'blue_sale_api' dentro de:

    * odoo/addons/ o agregar path de submódulo a archivo de configuración

* Actualizar lista de aplicaciones desde Apps e instalar


Estructura
==========

Controller REST:
~~~~~~~~~~~~

Se implementa el endpoint:

* POST /api/v1/sale-order

Se utiliza:

* @http.route
* type='json'
* auth='none'

Autenticación:
~~~~~~~~~~~~

La autenticación se realiza mediante header:

* Authorization: Bearer <API_KEY>

* Se valida contra el API Key configurado en el usuario
* Para pruebas se utilizó el API Key del usuario Administrador
* Permite autenticación stateless sin sesión web


Validaciones:
~~~~~~~~~~~~

El endpoint valida:

* Existencia del header Authorization
* Formato correcto del Bearer Token
* Validez del API Key
* Existencia del cliente (partner_id)
* Existencia de los productos enviados

Si alguna validación falla, se retorna error controlado.


Respuesta:
~~~~~~~~~~~~

Respuesta exitosa:

* {
    "order_id": 45,
    "status": "pending"
  }

La orden se crea en estado:

* authorization_status = pending


Decisiones Técnicas
===========

Autenticación mediante API Key
~~~~~~~~~~~~

Se implementó validación manual del token en lugar de usar auth='user'.

Motivo:

* Se requiere integración externa sin sesión web
* Permite autenticación stateless
* Da mayor control sobre manejo de errores
* Es el mecanismo recomendado para integraciones en Odoo


Creación en estado Pending
~~~~~~~~~~~~

Las órdenes se crean inicialmente como:

* authorization_status = pending

Motivo:

* Permite flujo de aprobación interno
* Se integra con la lógica del módulo blue_sale_extension
* Evita confirmaciones automáticas sin autorización


Funcionamiento
=============

1. El sistema externo envía petición POST con Bearer Token.
2. Se valida autenticación.
3. Se valida cliente y productos.
4. Se crea la orden en estado pending.
5. Se retorna JSON con order_id y status.


Autor
=======

* Edwin Pérez <edwinpj038@gmail.com>
