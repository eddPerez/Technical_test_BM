===================
Blue Medical - Ventas
===================


Descripción
==========

Módulo que extiende la funcionalidad estándar de ventas en Odoo agregando:

* Gestión de autorización de seguros

* Control de margen por orden de venta

* Validaciones de negocio para confirmación

* Grupo de seguridad especializado

* Control de visibilidad del margen

* Este módulo extiende los modelos sale.order y sale.order.line.


Instalación
=============

Requisitos:

* Odoo 16.0

* Módulo sale instalado

* Modo desarrollador activado

Pasos:

* Clonar el repositorio:

* git clone https://github.com/eddPerez/Technical_test_BM.git

Copiar el módulo 'blue_sale_extension' dentro de:

odoo/addons/ o agregar path de submódulo a archivo de configuración

Actualizar lista de aplicaciones desde Apps e instalar

Estructura
==========

Extensión de sale.order:
~~~~~~~~~~~~

Se agregaron los siguientes campos:

* insurance_number (Char)

* authorization_status (Selection)

    * draft

    * pending

    * approved

    * rejected

* total_margin (Float, store=True)
* El pedido de venta no podrá ser confirmado si el campo authorization_status no está "Aprobado"

Extensión de sale.order.line:
~~~~~~~~~~~~

El costo del producto se gestiona a nivel de línea, ya que:

* Es donde se calcula el margen real

* Permite ver margen por producto

* Sigue el estándar arquitectónico de Odoo

Cálculo de Margen:
~~~~~~~~~~~~

El margen se calcula como:

* precio_unitario - costo_producto
* El campo total_margin es store=True para:

    * Mejor rendimiento
    * Permitir búsquedas, importación y exportación
    * Permitir visibilidad controlada por seguridad


Decisiones Técnicas
===========

Margen negativo
~~~~~~~~~~~~
No se utilizó @api.constrains.

Motivo:

* El campo total_margin es store=True, por lo tanto:
    * Se recalcula automáticamente durante la instalación del módulo.
    * Si existiera un constraint, este se ejecutaría en la instalación.
    * Bloquea el despliegue si encuentra valores inconsistentes, es decir, si se cumple la condición.



Funcionamiento
=============




Autor
=======

* Edwin Pérez <edwinpj038@gmail.com>