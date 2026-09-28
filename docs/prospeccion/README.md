# Prospección desde Instagram · Kodo 360

Cada día a las 20:30 (hora de Canarias) Claude pide una cuenta de Instagram. Después analiza sus seguidores con Mailerfind y devuelve una lista de leads cualificados, cada uno con su correo personalizado listo para revisar.

## 1. Quién es un lead cualificado

Solo **cuentas de empresa o de profesionales** que cumplan todo esto:

| Criterio | Cómo se mira |
|---|---|
| Está en Canarias | Ubicación, bio, dirección o prefijo +34 928 / 922 |
| Es un negocio | Cuenta de empresa o de creador con categoría, o una bio con servicio y contacto |
| Tiene contacto público | Correo o teléfono en el perfil o en su web |
| Es pyme | Entre 300 y 50.000 seguidores; no es una marca nacional ni una cadena |

Se descartan:
- particulares;
- competidores (agencias, desarrolladores, marketing digital);
- administraciones públicas;
- cuentas inactivas: más de 90 días sin publicar.

### Puntuación (0–100)
- **Sector con mucho trabajo repetitivo (+30):** alojamiento, restauración, clínicas, academias, inmobiliarias, talleres, asesorías, comercio con tienda online.
- **Señal de dolor visible (+25):** «reservas por DM», «pide cita por WhatsApp», formularios o PDF, varios idiomas.
- **Tamaño (+20):** tiene equipo, más de un local o ventas online.
- **Actividad (+15):** ha publicado en los últimos 30 días.
- **Correo de empresa (+10):** del dominio propio, no un @gmail.

**Cualificado: 60 puntos o más.** Se entregan como máximo 20 leads por día, ordenados por puntuación.

## 2. Formato de la lista

Se entrega como `leads/AAAA-MM-DD-<cuenta>.csv`, junto con un resumen en el chat:

```
puntuacion,usuario_ig,negocio,nombre_contacto,sector,isla,email,telefono,web,seguidores,señal,idea,asunto
```

- **`señal`:** qué hemos visto. Da pie al `{{gancho}}` del correo.
- **`idea`:** la automatización concreta que le propondríamos (`{{idea}}`).

## 3. Correo

La plantilla está en dos versiones: `plantilla-correo.html` y `plantilla-correo.txt`.

| Variable | Contenido |
|---|---|
| `{{nombre}}` | Nombre de pila, o «equipo de {{negocio}}» si no se conoce |
| `{{negocio}}` | Nombre comercial |
| `{{gancho}}` | Una frase **verdadera y concreta** sobre lo que se ha visto en su perfil |
| `{{idea}}` | Una sola propuesta, en una o dos frases |
| `{{asunto}}` | «{{negocio}}: una idea para …», en menos de 60 caracteres, sin mayúsculas ni emojis |
| `{{email}}` | El correo del destinatario, para el enlace de baja |

**Envío:**
- Los correos se preparan como **borradores en Gmail**; Christian los revisa y los envía él.
- Máximo 20 al día, uno a uno y nunca en copia.
- Seguimiento, un solo recordatorio a los 5 días si no responde.

## 4. Legal: leer antes de enviar

- **LSSI, art. 21.** En España, mandar publicidad por correo a quien no la ha pedido está prohibido, **también a empresas**. La AEPD multa por ello, normalmente entre 1.000 y 30.000 €.
  - El riesgo es menor si el correo es uno a uno, se dirige a la dirección de contacto que el negocio publica y ofrece la baja con un clic.
  - Aun así, **no es una base legal**. La vía más segura es que el primer contacto sea por DM de Instagram, teléfono o en persona, y enviar el correo cuando el negocio lo acepte.
- **LSSI, art. 20.** El mensaje debe identificarse como «Publicidad» e identificar a la empresa. La plantilla ya lo hace en el pie.
- **RGPD.**
  - La lista de leads la guarda solo Kodo y no se comparte.
  - Cada baja se añade a `leads/bajas.csv` y se excluye de todas las listas futuras.
  - Los leads sin respuesta se borran a los 6 meses.
- **Instagram y Mailerfind.** Usar Mailerfind es responsabilidad de la cuenta que lo contrata. Revisa sus condiciones y las de Meta.
